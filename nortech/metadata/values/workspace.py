"""Module containing all schemas related with Workspaces."""

from __future__ import annotations

from pydantic import BaseModel
from typing_extensions import TypedDict

from .common import MetadataOutput, MetadataTimestamps


class WorkspaceInputDict(TypedDict):
    """Dictionary representation of Workspace input data.

    Attributes:
        workspace (str): The name of the Workspace.

    """

    workspace: str


class WorkspaceInput(BaseModel):
    """Pydantic model for Workspace input data.

    Attributes:
        workspace (str): The name of the Workspace.

    """

    workspace: str


def parse_workspace_input(  # noqa: D103
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
    """Output model for workspace list entries.

    Attributes:
        id (int): Id of the Workspace.
        name (str): Name of the Workspace.
        description (str): A description of the Workspace.

    """

    description: str


class WorkspaceOutput(WorkspaceListOutput, MetadataTimestamps):
    """Detailed output model for a single workspace.

    Attributes:
        id (int): Id of the Workspace.
        name (str): Name of the Workspace.
        description (str): A description of the Workspace.
        created_at (datetime): Timestamp of when the Workspace was created.
        updated_at (datetime): Timestamp of when the Workspace was last updated.

    """
