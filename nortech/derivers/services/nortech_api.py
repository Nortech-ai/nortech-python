from __future__ import annotations

from datetime import datetime
from typing import Generic, Literal, Mapping

from dateutil.parser import parse
from pydantic import BaseModel, ConfigDict, Field

from nortech.derivers.values.instance import (
    Deriver,
    DeriverInputType,
    DeriverOutputType,
)
from nortech.derivers.values.schema import ConfigurationType, DeriverSchemaDAG
from nortech.gateways.nortech_api import (
    NortechAPI,
    validate_response,
)
from nortech.metadata.values.pagination import PaginatedResponse, PaginationOptions


class CreateDeriver(BaseModel, Generic[DeriverInputType, DeriverOutputType, ConfigurationType]):
    model_config = ConfigDict(populate_by_name=True)

    name: str
    description: str

    inputs: dict[str, DeriverInputType]
    outputs: dict[str, DeriverOutputType]
    configurations: ConfigurationType

    start_at: str = Field(alias="startAt")


class CreateDeriverRequest(BaseModel, Generic[DeriverInputType, DeriverOutputType, ConfigurationType]):
    model_config = ConfigDict(populate_by_name=True)

    workspace: str | None
    deriver: CreateDeriver[DeriverInputType, DeriverOutputType, ConfigurationType]
    deriver_schema_dag: DeriverSchemaDAG = Field(alias="deriverSchemaDAG")
    dry_run: bool = Field(alias="dryRun")


class Log(BaseModel):
    timestamp: datetime
    message: str

    def __str__(self):
        return f"{self.timestamp} {self.message}"


class LogList(BaseModel):
    logs: list[Log]

    def __str__(self) -> str:
        str_representation = "\n".join([str(log) for log in self.logs])
        return str_representation


class DeriverLogs(BaseModel):
    name: str
    flow: LogList
    processor: LogList

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
    pods: list[DeriverLogs]

    def __str__(self) -> str:
        str_representation = "Pods:\n"
        for pod in self.pods:
            str_representation += f"{pod}\n"

        return str_representation


class Schema(BaseModel):
    id: int
    hash: str
    history_id: int = Field(..., alias="historyId")
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt")


class SchemaDiff(BaseModel):
    old: Schema = Field(..., alias="previousSchema")
    new: Schema = Field(..., alias="newSchema")


class DeriverDiffs(BaseModel):
    deriver_schemas: Mapping[str, SchemaDiff] = Field(..., alias="deriverSchemas")
    derivers: Mapping[str, SchemaDiff]

    model_config = ConfigDict(populate_by_name=True)


def list_derivers(
    nortech_api: NortechAPI,
    pagination_options: PaginationOptions[Literal["id", "name", "description"]] | None = None,
):
    response = nortech_api.get(
        url="/api/v1/derivers",
        params=pagination_options.model_dump(by_alias=True) if pagination_options else None,
    )
    validate_response(response, [200], "Failed to list Derivers.")

    return PaginatedResponse[Deriver](**response.json())


def get_deriver(nortech_api: NortechAPI, deriver_id: int):
    response = nortech_api.get(url=f"/api/v1/derivers/{deriver_id}")
    validate_response(response, [200], "Failed to get Deriver.")

    return Deriver(**response.json())


def create_deriver(
    nortech_api: NortechAPI,
    deriver: Deriver,
    deriver_schema_dag: DeriverSchemaDAG,
    workspace: str | None = None,
    dry_run: bool = True,
):
    create_deriver_request = CreateDeriverRequest(
        workspace=workspace,
        deriver=CreateDeriver(
            name=deriver.name,
            description=deriver.description,
            inputs=deriver.inputs,
            outputs=deriver.outputs,
            configurations=deriver.configurations,
            startAt=str(deriver.start_at),
        ),
        deriverSchemaDAG=deriver_schema_dag,
        dryRun=dry_run,
    )

    print(create_deriver_request.model_dump_json(by_alias=True))

    response = nortech_api.post(
        url="/api/v1/derivers",
        json=create_deriver_request.model_dump(by_alias=True),
    )
    validate_response(response, [200], "Failed to create Deriver.")

    return DeriverDiffs.model_validate(response.json())


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
    nortech_api: NortechAPI,
    deriver_id: int,
):
    response = nortech_api.get(
        url=f"/api/v1/derivers/{deriver_id}/logs",
    )
    validate_response(response, [200], "Failed to get Deriver logs.")

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
