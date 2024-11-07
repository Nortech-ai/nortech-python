from __future__ import annotations

from pydantic import BaseModel
from typing_extensions import TypedDict

from .common import MetadataOutput, MetadataTimestamps


class WorkspaceInputDict(TypedDict):
    workspace: str


class WorkspaceInput(BaseModel):
    workspace: str


def parse_workspace_input(
    workspace_input: WorkspaceInput | WorkspaceInputDict | WorkspaceOutput | WorkspaceListOutput | str | int,
):
    if isinstance(workspace_input, int):
        return workspace_input
    if isinstance(workspace_input, WorkspaceInput):
        return workspace_input.workspace
    elif isinstance(workspace_input, WorkspaceListOutput):
        return workspace_input.id
    if isinstance(workspace_input, str):
        return workspace_input
    return workspace_input["workspace"]


class WorkspaceListOutput(MetadataOutput):
    description: str


class WorkspaceOutput(WorkspaceListOutput, MetadataTimestamps):
    pass
