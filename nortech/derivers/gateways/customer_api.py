from typing import Dict, Generic

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from requests import post

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
