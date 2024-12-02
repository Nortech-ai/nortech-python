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
from nortech.metadata.values.pagination import PaginatedResponse, PaginationOptions
from nortech.metadata.values.unit import (
    UnitInput,
    UnitInputDict,
    UnitListOutput,
    UnitOutput,
    parse_unit_input,
)


def list_workspace_asset_division_units(
    nortech_api: NortechAPI,
    division: int | DivisionInputDict | DivisionInput | DivisionOutput | DivisionListOutput,
    pagination_options: PaginationOptions[Literal["id", "name"]] | None = None,
):
    if isinstance(division, int):
        return list_division_units(nortech_api, division, pagination_options)
    if isinstance(division, DivisionListOutput):
        return list_division_units(nortech_api, division.id, pagination_options)

    division_input = parse_division_input(division)
    response = nortech_api.get(
        url=f"/api/v1/workspaces/{division_input.workspace}/assets/{division_input.asset}/divisions/{division_input.division}/units",
        params=pagination_options.model_dump(exclude_none=True, by_alias=True) if pagination_options else None,
    )
    validate_response(response)

    resp = PaginatedResponse[UnitListOutput].model_validate(
        {**response.json(), "pagination_options": pagination_options}
    )

    if nortech_api.ignore_pagination and resp.next and resp.next.token:
        next_resp = list_workspace_asset_division_units(nortech_api, division, resp.next_pagination_options())
        return resp.model_copy(
            update={
                "data": resp.data + next_resp.data,
                "size": resp.size + next_resp.size,
                "next": next_resp.next,
            }
        )

    return resp


def get_workspace_asset_division_unit(
    nortech_api: NortechAPI, unit: int | UnitInputDict | UnitInput | UnitOutput | UnitListOutput
):
    if isinstance(unit, int):
        return get_unit(nortech_api, unit)
    if isinstance(unit, UnitListOutput):
        return get_unit(nortech_api, unit.id)

    unit_input = parse_unit_input(unit)
    response = nortech_api.get(
        url=f"/api/v1/workspaces/{unit_input.workspace}/assets/{unit_input.asset}/divisions/{unit_input.division}/units/{unit_input.unit}",
    )
    validate_response(response)
    return UnitOutput.model_validate(response.json())


def list_workspace_units(
    nortech_api: NortechAPI,
    workspace_id: int,
    pagination_options: PaginationOptions[Literal["id", "name"]] | None = None,
):
    response = nortech_api.get(
        url=f"/api/v1/workspaces/{workspace_id}/units",
        params=pagination_options.model_dump(exclude_none=True, by_alias=True) if pagination_options else None,
    )
    validate_response(response)

    resp = PaginatedResponse[UnitListOutput].model_validate(
        {**response.json(), "pagination_options": pagination_options}
    )

    if nortech_api.ignore_pagination and resp.next and resp.next.token:
        next_resp = list_workspace_units(nortech_api, workspace_id, resp.next_pagination_options())
        return resp.model_copy(
            update={
                "data": resp.data + next_resp.data,
                "size": resp.size + next_resp.size,
                "next": next_resp.next,
            }
        )

    return resp


def list_asset_units(
    nortech_api: NortechAPI,
    asset_id: int,
    pagination_options: PaginationOptions[Literal["id", "name"]] | None = None,
):
    response = nortech_api.get(
        url=f"/api/v1/assets/{asset_id}/units",
        params=pagination_options.model_dump(exclude_none=True, by_alias=True) if pagination_options else None,
    )
    validate_response(response)

    resp = PaginatedResponse[UnitListOutput].model_validate(
        {**response.json(), "pagination_options": pagination_options}
    )

    if nortech_api.ignore_pagination and resp.next and resp.next.token:
        next_resp = list_asset_units(nortech_api, asset_id, resp.next_pagination_options())
        return resp.model_copy(
            update={
                "data": resp.data + next_resp.data,
                "size": resp.size + next_resp.size,
                "next": next_resp.next,
            }
        )

    return resp


def list_division_units(
    nortech_api: NortechAPI,
    division_id: int,
    pagination_options: PaginationOptions[Literal["id", "name"]] | None = None,
):
    response = nortech_api.get(
        url=f"/api/v1/divisions/{division_id}/units",
        params=pagination_options.model_dump(exclude_none=True, by_alias=True) if pagination_options else None,
    )
    validate_response(response)

    resp = PaginatedResponse[UnitListOutput].model_validate(
        {**response.json(), "pagination_options": pagination_options}
    )

    if nortech_api.ignore_pagination and resp.next and resp.next.token:
        next_resp = list_division_units(nortech_api, division_id, resp.next_pagination_options())
        return resp.model_copy(
            update={
                "data": resp.data + next_resp.data,
                "size": resp.size + next_resp.size,
                "next": next_resp.next,
            }
        )

    return resp


def get_unit(nortech_api: NortechAPI, unit_id: int):
    response = nortech_api.get(
        url=f"/api/v1/units/{unit_id}",
    )
    validate_response(response)
    return UnitOutput.model_validate(response.json())
