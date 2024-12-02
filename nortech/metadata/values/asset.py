"""Module containing all schemas related with Assets."""

from __future__ import annotations

from .common import MetadataOutput, MetadataTimestamps
from .workspace import WorkspaceInput, WorkspaceInputDict


class AssetInputDict(WorkspaceInputDict):
    """Dictionary representation of Asset input data.

    Attributes:
        workspace (str): The name of the Workspace.
        asset (str): The name of the Asset.

    """

    asset: str


class AssetInput(WorkspaceInput):
    """Pydantic model for asset input data.

    Attributes:
        workspace (str): The name of the Workspace.
        asset (str): The name of the Asset.

    """

    asset: str


def parse_asset_input(asset_input: AssetInput | AssetInputDict):  # noqa: D103
    if isinstance(asset_input, AssetInput):
        return asset_input
    else:
        return AssetInput.model_validate(asset_input)


class AssetListOutput(MetadataOutput):
    """Output model for asset list entries.

    Attributes:
        id (int): Id of the Asset.
        name (str): Name of the Asset.
        description (str): A description of the Asset.

    """

    description: str


class AssetOutput(AssetListOutput, MetadataTimestamps):
    """Detailed output model for a single asset.

    Attributes:
        id (int): Id of the Asset.
        name (str): Name of the Asset.
        description (str): A description of the Asset.
        created_at (datetime): Timestamp of when the Asset was created.
        updated_at (datetime): Timestamp of when the Asset was last updated.
        workspace: Metadata about the Workspace containing the Asset.
            - id (int): Id of the Workspace.
            - name (str): Name of the Workspace.

    """

    workspace: MetadataOutput
