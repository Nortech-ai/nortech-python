from __future__ import annotations

from datetime import datetime, timezone
from inspect import getsource
from typing import Literal

from pydantic import BaseModel, Field, field_validator

from nortech.derivers.values.deriver import Deriver, get_deriver_from_script
from nortech.gateways.nortech_api import (
    NortechAPI,
    validate_response,
)
from nortech.metadata.values.pagination import (
    PaginatedResponse,
    PaginationOptions,
)
from nortech.metadata.values.signal import SignalOutputNoDevice


class DeployedDeriverList(BaseModel):
    deriver: type[Deriver] = Field(alias="definition")
    description: str | None = None
    start_at: datetime | None = Field(alias="startAt")
    status: Literal["STARTING", "RUNNING", "STOPPED", "ERROR"]

    @field_validator("deriver", mode="before")
    @classmethod
    def convert_deriver_string(cls, v: str):
        return get_deriver_from_script(v)


class DeployedDeriver(DeployedDeriverList):
    inputs: list[SignalOutputNoDevice]
    outputs: list[SignalOutputNoDevice]


class Log(BaseModel):
    timestamp: datetime
    message: str

    def __str__(self):
        return f"{self.timestamp} {self.message}"


class LogList(BaseModel):
    logs: list[Log]

    def __str__(self) -> str:
        return "\n".join([str(log) for log in self.logs])


def list_derivers(
    nortech_api: NortechAPI,
    pagination_options: PaginationOptions[Literal["id", "name", "description"]] | None = None,
):
    response = nortech_api.get(
        url="/api/v1/derivers",
        params=pagination_options.model_dump(by_alias=True) if pagination_options else None,
    )
    validate_response(response, [200], "Failed to list Derivers.")

    return PaginatedResponse[DeployedDeriverList].model_validate(response.json())


def get_deriver(nortech_api: NortechAPI, deriver: str):
    response = nortech_api.get(url=f"/api/v1/derivers/{deriver}")
    validate_response(response, [200], "Failed to get Deriver.")

    return DeployedDeriver.model_validate(response.json())


def create_deriver(
    nortech_api: NortechAPI,
    deriver: type[Deriver],
    start_at: datetime | None = None,
    description: str | None = None,
    create_parents: bool = False,
):
    response = nortech_api.post(
        url="/api/v1/derivers",
        json={
            "definition": getsource(deriver),
            "startAt": start_at.astimezone(timezone.utc).isoformat().replace("+00:00", "Z") if start_at else None,
            "description": description,
            "createParents": create_parents,
        },
    )
    validate_response(response, [201], "Failed to create Deriver.")

    return DeployedDeriver.model_validate(response.json())


def update_deriver(
    nortech_api: NortechAPI,
    deriver: type[Deriver],
    start_at: datetime | None = None,
    description: str | None = None,
    create_parents: bool = False,
    keep_data: bool = False,
):
    response = nortech_api.post(
        url="/api/v1/derivers",
        json={
            "definition": getsource(deriver),
            "startAt": start_at.astimezone(timezone.utc).isoformat().replace("+00:00", "Z") if start_at else None,
            "description": description,
            "createParents": create_parents,
            "keepData": keep_data,
        },
    )
    validate_response(response, [200], "Failed to create Deriver.")

    return DeployedDeriver.model_validate(response.json())


def get_deriver_logs(
    nortech_api: NortechAPI,
    deriver: type[Deriver],
):
    response = nortech_api.get(
        url=f"/api/v1/derivers/{deriver.__name__}/logs",
    )
    validate_response(response, [200], "Failed to get Deriver logs.")

    return LogList.model_validate(response.json())
