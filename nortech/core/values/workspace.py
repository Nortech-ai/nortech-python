from __future__ import annotations

from pydantic import BaseModel
from typing_extensions import TypedDict

from .common import MetadataOutput, MetadataTimestamps


class WorkspaceInputDict(TypedDict):
    workspace: str


class WorkspaceInput(BaseModel):
    workspace: str


def parse_workspace_input(
    workspace_input: WorkspaceInput | WorkspaceInputDict | WorkspaceOutput | str | int,
):
    if isinstance(workspace_input, int):
        return workspace_input
    if isinstance(workspace_input, WorkspaceInput):
        return workspace_input.workspace
    elif isinstance(workspace_input, WorkspaceOutput):
        return workspace_input.to_workspace_input()
    if isinstance(workspace_input, str):
        return workspace_input
    return workspace_input["workspace"]


class WorkspaceListOutput(MetadataOutput):
    description: str


class WorkspaceOutput(WorkspaceListOutput, MetadataTimestamps):
    def to_workspace_input(self) -> WorkspaceInput:
        return WorkspaceInput(workspace=self.name)
