from __future__ import annotations

from typing import Literal

from nortech.gateways.nortech_api import (
    NortechAPI,
    validate_response,
)
from nortech.metadata.values.asset import (
    AssetInput,
    AssetInputDict,
    AssetListOutput,
    AssetOutput,
    parse_asset_input,
)
from nortech.metadata.values.pagination import PaginatedResponse, PaginationOptions
from nortech.metadata.values.workspace import (
    WorkspaceInput,
    WorkspaceInputDict,
    WorkspaceListOutput,
    WorkspaceOutput,
    parse_workspace_input,
)


def list_workspace_assets(
    nortech_api: NortechAPI,
    workspace: WorkspaceInputDict | WorkspaceInput | WorkspaceOutput | WorkspaceListOutput | int | str,
    pagination_options: PaginationOptions[Literal["id", "name", "description"]] | None = None,
):
    workspace_input = parse_workspace_input(workspace)
    response = nortech_api.get(
        url=f"/api/v1/workspaces/{workspace_input}/assets",
        params=pagination_options.model_dump(exclude_none=True, by_alias=True) if pagination_options else None,
    )
    validate_response(response)

    resp = PaginatedResponse[AssetListOutput].model_validate(
        {**response.json(), "pagination_options": pagination_options}
    )

    if nortech_api.ignore_pagination and resp.next and resp.next.token:
        next_resp = list_workspace_assets(nortech_api, workspace, resp.next_pagination_options())
        return resp.model_copy(
            update={
                "data": resp.data + next_resp.data,
                "size": resp.size + next_resp.size,
                "next": next_resp.next,
            }
        )

    return resp


def get_workspace_asset(
    nortech_api: NortechAPI, asset: int | AssetInputDict | AssetInput | AssetOutput | AssetListOutput
):
    if isinstance(asset, int):
        return get_asset(nortech_api, asset)
    if isinstance(asset, AssetListOutput):
        return get_asset(nortech_api, asset.id)

    asset_input = parse_asset_input(asset)
    response = nortech_api.get(
        url=f"/api/v1/workspaces/{asset_input.workspace}/assets/{asset_input.asset}",
    )
    validate_response(response)
    return AssetOutput.model_validate(response.json())


def get_asset(nortech_api: NortechAPI, asset_id: int):
    response = nortech_api.get(
        url=f"/api/v1/assets/{asset_id}",
    )
    validate_response(response)
    return AssetOutput.model_validate(response.json())
