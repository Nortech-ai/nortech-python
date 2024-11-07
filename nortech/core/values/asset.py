from __future__ import annotations

from .common import MetadataOutput, MetadataTimestamps
from .workspace import WorkspaceInput, WorkspaceInputDict


class AssetInputDict(WorkspaceInputDict):
    asset: str


class AssetInput(WorkspaceInput):
    asset: str


def parse_asset_input(asset_input: AssetInput | AssetInputDict):
    if isinstance(asset_input, AssetInput):
        return asset_input
    else:
        return AssetInput.model_validate(asset_input)


class AssetListOutput(MetadataOutput):
    description: str


class AssetOutput(AssetListOutput, MetadataTimestamps):
    workspace: MetadataOutput
