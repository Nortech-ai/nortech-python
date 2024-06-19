from datetime import datetime
from typing import Dict, Generic, List

from dateutil.parser import parse
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from requests import get, post

from nortech.derivers.values.instance import (
    Deriver,
    DeriverInputType,
    DeriverOutputType,
)
from nortech.derivers.values.schema import ConfigurationType, DeriverSchemaDAG


class CustomerAPI(BaseSettings):
    URL: str = Field(default="https://api.apps.nor.tech")
    TOKEN: str = Field(default=...)

    model_config = SettingsConfigDict(env_prefix="CUSTOMER_API_")


class CreateDeriver(
    BaseModel, Generic[DeriverInputType, DeriverOutputType, ConfigurationType]
):
    name: str = Field()
    description: str = Field()

    inputs: Dict[str, DeriverInputType] = Field()
    outputs: Dict[str, DeriverOutputType] = Field()
    configurations: ConfigurationType = Field()

    startAt: str = Field()


class CustomerWorkspace(BaseModel):
    customer_name: str = Field()
    workspace_name: str = Field()


class CustomerWorkspaceExternal(BaseModel):
    customerName: str = Field()
    workspaceName: str = Field()


class CreateDeriverRequest(
    BaseModel, Generic[DeriverInputType, DeriverOutputType, ConfigurationType]
):
    customerWorkspace: CustomerWorkspaceExternal = Field()

    deriver: CreateDeriver[DeriverInputType, DeriverOutputType, ConfigurationType]
    deriverSchemaDAG: DeriverSchemaDAG = Field()

    dryRun: bool = Field()


class Log(BaseModel):
    timestamp: datetime = Field()
    message: str = Field()

    def __str__(self):
        return f"{self.timestamp} {self.message}"


class LogList(BaseModel):
    logs: List[Log] = Field()

    def __str__(self) -> str:
        str_representation = "\n".join([str(log) for log in self.logs])
        return str_representation


class DeriverLogs(BaseModel):
    name: str = Field()
    flow: LogList = Field()
    processor: LogList = Field()

    def __str__(self) -> str:
        str_representation = f"Pod: {self.name}\n"
        str_representation += "\nFlow logs:\n"
        for log in self.flow.logs:
            str_representation += f"{log}\n"

        str_representation += "\nProcessor logs:\n"
        for log in self.processor.logs:
            str_representation += f"{log}\n"

        return str_representation


class LogsPerPod(BaseModel):
    pods: List[DeriverLogs] = Field()

    def __str__(self) -> str:
        str_representation = "Pods:\n"
        for pod in self.pods:
            str_representation += f"{pod}\n"

        return str_representation


def create_deriver(
    customer_API: CustomerAPI,
    customer_workspace: CustomerWorkspace,
    deriver: Deriver,
    deriver_schema_DAG: DeriverSchemaDAG,
    dry_run: bool,
):
    deriver_DAG_endpoint = customer_API.URL + "/api/v1/derivers/createDeriver"

    create_deriver_request = CreateDeriverRequest(
        customerWorkspace=CustomerWorkspaceExternal(
            customerName=customer_workspace.customer_name,
            workspaceName=customer_workspace.workspace_name,
        ),
        deriver=CreateDeriver(
            name=deriver.name,
            description=deriver.description,
            inputs=deriver.inputs,
            outputs=deriver.outputs,
            configurations=deriver.configurations,
            startAt=str(deriver.start_at),
        ),
        deriverSchemaDAG=deriver_schema_DAG,
        dryRun=dry_run,
    )

    response = post(
        url=deriver_DAG_endpoint,
        json=create_deriver_request.model_dump(),
        headers={"Authorization": f"Bearer {customer_API.TOKEN}"},
    )

    try:
        assert response.status_code == 200
    except AssertionError:
        raise AssertionError(
            f"Failed to create DeriverDAG. "
            f"Status code: {response.status_code}. "
            f"Response: {response.json()}"
        )

    return response.json()


def get_logs_from_response_logs(response_logs: str) -> LogList:
    logs = [
        Log(
            timestamp=parse(log.split(" ", 1)[0]),
            message=log.split(" ", 1)[1],
        )
        for log in response_logs.split("\n")
        if log != ""
    ]

    return LogList(logs=logs)


def get_deriver_logs(
    customer_API: CustomerAPI,
    deriverId: int,
):
    get_deriver_logs_endpoint = (
        customer_API.URL + f"/api/v1/derivers/getDeriverLogs/{deriverId}"
    )

    response = get(
        url=get_deriver_logs_endpoint,
        headers={"Authorization": f"Bearer {customer_API.TOKEN}"},
    )

    try:
        assert response.status_code == 200
    except AssertionError:
        raise AssertionError(
            f"Failed to get Deriver logs. "
            f"Status code: {response.status_code}. "
            f"Response: {response.json()}"
        )

    return LogsPerPod(
        pods=[
            DeriverLogs(
                name=pod["podName"],
                flow=get_logs_from_response_logs(pod["flowLogs"]),
                processor=get_logs_from_response_logs(pod["processorLogs"]),
            )
            for pod in response.json()["logsPerPod"]
        ]
    )
