from __future__ import annotations

from typing import Literal

from nortech.gateways.nortech_api import (
    NortechAPI,
    validate_response,
)
from nortech.metadata.values.asset import AssetInput, AssetInputDict, AssetListOutput, AssetOutput, parse_asset_input
from nortech.metadata.values.division import (
    DivisionInput,
    DivisionInputDict,
    DivisionListOutput,
    DivisionOutput,
    parse_division_input,
)
from nortech.metadata.values.pagination import PaginatedResponse, PaginationOptions


def list_workspace_asset_divisions(
    nortech_api: NortechAPI,
    asset: int | AssetInputDict | AssetInput | AssetOutput | AssetListOutput,
    pagination_options: PaginationOptions[Literal["id", "name", "description"]] | None = None,
):
    if isinstance(asset, int):
        return list_asset_divisions(nortech_api, asset, pagination_options)
    if isinstance(asset, AssetListOutput):
        return list_asset_divisions(nortech_api, asset.id, pagination_options)

    asset_input = parse_asset_input(asset)
    response = nortech_api.get(
        url=f"/api/v1/workspaces/{asset_input.workspace}/assets/{asset_input.asset}/divisions",
        params=pagination_options.model_dump(exclude_none=True, by_alias=True) if pagination_options else None,
    )
    validate_response(response)

    resp = PaginatedResponse[DivisionListOutput].model_validate(
        {**response.json(), "pagination_options": pagination_options}
    )

    if nortech_api.ignore_pagination and resp.next and resp.next.token:
        next_resp = list_workspace_asset_divisions(nortech_api, asset, resp.next_pagination_options())
        return resp.model_copy(
            update={
                "data": resp.data + next_resp.data,
                "size": resp.size + next_resp.size,
                "next": next_resp.next,
            }
        )

    return resp


def get_workspace_asset_division(
    nortech_api: NortechAPI, division: int | DivisionInputDict | DivisionInput | DivisionOutput | DivisionListOutput
):
    if isinstance(division, int):
        return get_division(nortech_api, division)
    if isinstance(division, DivisionListOutput):
        return get_division(nortech_api, division.id)

    division_input = parse_division_input(division)
    response = nortech_api.get(
        url=f"/api/v1/workspaces/{division_input.workspace}/assets/{division_input.asset}/divisions/{division_input.division}",
    )
    validate_response(response)
    return DivisionOutput.model_validate(response.json())


def list_workspace_divisions(
    nortech_api: NortechAPI,
    workspace_id: int,
    pagination_options: PaginationOptions[Literal["id", "name", "description"]] | None = None,
):
    response = nortech_api.get(
        url=f"/api/v1/workspaces/{workspace_id}/divisions",
        params=pagination_options.model_dump(exclude_none=True, by_alias=True) if pagination_options else None,
    )
    validate_response(response)

    resp = PaginatedResponse[DivisionListOutput].model_validate(
        {**response.json(), "pagination_options": pagination_options}
    )

    if nortech_api.ignore_pagination and resp.next and resp.next.token:
        next_resp = list_workspace_divisions(nortech_api, workspace_id, resp.next_pagination_options())
        return resp.model_copy(
            update={
                "data": resp.data + next_resp.data,
                "size": resp.size + next_resp.size,
                "next": next_resp.next,
            }
        )

    return resp


def list_asset_divisions(
    nortech_api: NortechAPI,
    asset_id: int,
    pagination_options: PaginationOptions[Literal["id", "name", "description"]] | None = None,
):
    response = nortech_api.get(
        url=f"/api/v1/assets/{asset_id}/divisions",
        params=pagination_options.model_dump(exclude_none=True, by_alias=True) if pagination_options else None,
    )
    validate_response(response)

    resp = PaginatedResponse[DivisionListOutput].model_validate(
        {**response.json(), "pagination_options": pagination_options}
    )

    if nortech_api.ignore_pagination and resp.next and resp.next.token:
        next_resp = list_asset_divisions(nortech_api, asset_id, resp.next_pagination_options())
        return resp.model_copy(
            update={
                "data": resp.data + next_resp.data,
                "size": resp.size + next_resp.size,
                "next": next_resp.next,
            }
        )

    return resp


def get_division(nortech_api: NortechAPI, division_id: int):
    response = nortech_api.get(
        url=f"/api/v1/divisions/{division_id}",
    )
    validate_response(response)
    return DivisionOutput.model_validate(response.json())
