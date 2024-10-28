from __future__ import annotations

from typing import Literal

from nortech.common.gateways.nortech_api import (
    NortechAPI,
    PaginatedResponse,
    PaginationOptions,
    validate_response,
)
from nortech.metadata.values.workspace import (
    WorkspaceInput,
    WorkspaceInputDict,
    WorkspaceListOutput,
    WorkspaceOutput,
    parse_workspace_input,
)


def list_workspaces(
    nortech_api: NortechAPI,
    pagination_options: PaginationOptions[Literal["id", "name", "description"]] | None = None,
):
    response = nortech_api.get(
        url="/api/v1/workspaces",
        params=pagination_options.model_dump(exclude_none=True, by_alias=True) if pagination_options else None,
    )
    validate_response(response, [200])

    resp = PaginatedResponse[WorkspaceListOutput].model_validate(
        {**response.json(), "pagination_options": pagination_options}
    )

    if nortech_api.ignore_pagination and resp.next and resp.next.token:
        next_resp = list_workspaces(nortech_api, resp.next_pagination_options())
        return resp.model_copy(
            update={
                "data": resp.data + next_resp.data,
                "size": resp.size + next_resp.size,
                "next": next_resp.next,
            }
        )
    return resp


def get_workspace(
    nortech_api: NortechAPI,
    workspace: WorkspaceInputDict | WorkspaceInput | WorkspaceOutput | int | str,
):
    workspace_input = parse_workspace_input(workspace)
    response = nortech_api.get(url=f"/api/v1/workspaces/{workspace_input}")
    validate_response(response, [200, 404])

    if response.status_code == 404:
        return None
    return WorkspaceOutput.model_validate(response.json())
