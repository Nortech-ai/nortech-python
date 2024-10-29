from __future__ import annotations

from typing import Literal

from nortech.core.gateways.nortech_api import (
    NortechAPI,
    PaginatedResponse,
    PaginationOptions,
    validate_response,
)
from nortech.core.values.asset import (
    AssetInput,
    AssetInputDict,
    AssetListOutput,
    AssetOutput,
    parse_asset_input,
)
from nortech.core.values.workspace import (
    WorkspaceInput,
    WorkspaceInputDict,
    WorkspaceOutput,
    parse_workspace_input,
)


def list_workspace_assets(
    nortech_api: NortechAPI,
    workspace: WorkspaceInputDict | WorkspaceInput | WorkspaceOutput | int | str,
    pagination_options: PaginationOptions[Literal["id", "name", "description"]] | None = None,
):
    workspace_input = parse_workspace_input(workspace)
    response = nortech_api.get(
        url=f"/api/v1/workspaces/{workspace_input}/assets",
        params=pagination_options.model_dump(exclude_none=True, by_alias=True) if pagination_options else None,
    )
    validate_response(response, [200])

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


def get_workspace_asset(nortech_api: NortechAPI, asset: AssetInputDict | AssetInput | AssetOutput):
    asset_input = parse_asset_input(asset)
    response = nortech_api.get(
        url=f"/api/v1/workspaces/{asset_input.workspace}/assets/{asset_input.asset}",
    )
    validate_response(response, [200, 404])
    if response.status_code == 404:
        return None
    return AssetOutput.model_validate(response.json())


def get_asset(nortech_api: NortechAPI, asset_id: int):
    response = nortech_api.get(
        url=f"/api/v1/assets/{asset_id}",
    )
    validate_response(response, [200, 404])
    if response.status_code == 404:
        return None
    return AssetOutput.model_validate(response.json())
