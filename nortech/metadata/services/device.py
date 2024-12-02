from __future__ import annotations

from typing import Literal

from nortech.gateways.nortech_api import (
    NortechAPI,
    validate_response,
)
from nortech.metadata.services.division import (
    DivisionInput,
    DivisionInputDict,
    DivisionListOutput,
    DivisionOutput,
    parse_division_input,
)
from nortech.metadata.values.device import (
    DeviceInput,
    DeviceInputDict,
    DeviceListOutput,
    DeviceOutput,
    parse_device_input,
)
from nortech.metadata.values.pagination import PaginatedResponse, PaginationOptions


def list_workspace_asset_division_devices(
    nortech_api: NortechAPI,
    division: int | DivisionInputDict | DivisionInput | DivisionOutput | DivisionListOutput,
    pagination_options: PaginationOptions[Literal["id", "name", "type", "onboarded"]] | None = None,
):
    if isinstance(division, int):
        return list_division_devices(nortech_api, division, pagination_options)
    if isinstance(division, DivisionListOutput):
        return list_division_devices(nortech_api, division.id, pagination_options)

    division_input = parse_division_input(division)
    response = nortech_api.get(
        url=f"/api/v1/workspaces/{division_input.workspace}/assets/{division_input.asset}/divisions/{division_input.division}/devices",
        params=pagination_options.model_dump(exclude_none=True, by_alias=True) if pagination_options else None,
    )
    validate_response(response)

    resp = PaginatedResponse[DeviceListOutput].model_validate(
        {**response.json(), "pagination_options": pagination_options}
    )

    if nortech_api.ignore_pagination and resp.next and resp.next.token:
        next_resp = list_workspace_asset_division_devices(nortech_api, division, resp.next_pagination_options())
        return resp.model_copy(
            update={
                "data": resp.data + next_resp.data,
                "size": resp.size + next_resp.size,
                "next": next_resp.next,
            }
        )

    return resp


def get_workspace_asset_division_device(
    nortech_api: NortechAPI, device: int | DeviceInputDict | DeviceInput | DeviceOutput | DeviceListOutput
):
    if isinstance(device, int):
        return get_device(nortech_api, device)
    if isinstance(device, DeviceListOutput):
        return get_device(nortech_api, device.id)

    device_input = parse_device_input(device)
    response = nortech_api.get(
        url=f"/api/v1/workspaces/{device_input.workspace}/assets/{device_input.asset}/divisions/{device_input.division}/devices/{device_input.device}",
    )
    validate_response(response)
    return DeviceOutput.model_validate(response.json())


def list_workspace_devices(
    nortech_api: NortechAPI,
    workspace_id: int,
    pagination_options: PaginationOptions[Literal["id", "name", "type", "onboarded"]] | None = None,
):
    response = nortech_api.get(
        url=f"/api/v1/workspaces/{workspace_id}/devices",
        params=pagination_options.model_dump(exclude_none=True, by_alias=True) if pagination_options else None,
    )
    validate_response(response)

    resp = PaginatedResponse[DeviceListOutput].model_validate(
        {**response.json(), "pagination_options": pagination_options}
    )

    if nortech_api.ignore_pagination and resp.next and resp.next.token:
        next_resp = list_workspace_devices(nortech_api, workspace_id, resp.next_pagination_options())
        return resp.model_copy(
            update={
                "data": resp.data + next_resp.data,
                "size": resp.size + next_resp.size,
                "next": next_resp.next,
            }
        )

    return resp


def list_asset_devices(
    nortech_api: NortechAPI,
    asset_id: int,
    pagination_options: PaginationOptions[Literal["id", "name", "type", "onboarded"]] | None = None,
):
    response = nortech_api.get(
        url=f"/api/v1/assets/{asset_id}/devices",
        params=pagination_options.model_dump(exclude_none=True, by_alias=True) if pagination_options else None,
    )
    validate_response(response)

    resp = PaginatedResponse[DeviceListOutput].model_validate(
        {**response.json(), "pagination_options": pagination_options}
    )

    if nortech_api.ignore_pagination and resp.next and resp.next.token:
        next_resp = list_asset_devices(nortech_api, asset_id, resp.next_pagination_options())
        return resp.model_copy(
            update={
                "data": resp.data + next_resp.data,
                "size": resp.size + next_resp.size,
                "next": next_resp.next,
            }
        )

    return resp


def list_division_devices(
    nortech_api: NortechAPI,
    division_id: int,
    pagination_options: PaginationOptions[Literal["id", "name", "type", "onboarded"]] | None = None,
):
    response = nortech_api.get(
        url=f"/api/v1/divisions/{division_id}/devices",
        params=pagination_options.model_dump(exclude_none=True, by_alias=True) if pagination_options else None,
    )
    validate_response(response)

    resp = PaginatedResponse[DeviceListOutput].model_validate(
        {**response.json(), "pagination_options": pagination_options}
    )

    if nortech_api.ignore_pagination and resp.next and resp.next.token:
        next_resp = list_division_devices(nortech_api, division_id, resp.next_pagination_options())
        return resp.model_copy(
            update={
                "data": resp.data + next_resp.data,
                "size": resp.size + next_resp.size,
                "next": next_resp.next,
            }
        )

    return resp


def get_device(nortech_api: NortechAPI, device_id: int):
    response = nortech_api.get(
        url=f"/api/v1/devices/{device_id}",
    )
    validate_response(response)
    return DeviceOutput.model_validate(response.json())
