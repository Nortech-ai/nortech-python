from __future__ import annotations

from nortech.core.values.asset import AssetInput, AssetInputDict

from .common import MetadataOutput, MetadataTimestamps


class DivisionInputDict(AssetInputDict):
    division: str


class DivisionInput(AssetInput):
    division: str


def parse_division_input(division_input: DivisionInput | DivisionInputDict | DivisionOutput):
    if isinstance(division_input, DivisionInput):
        return division_input
    elif isinstance(division_input, DivisionOutput):
        return division_input.to_division_input()
    else:
        return DivisionInput.model_validate(division_input)


class DivisionListOutput(MetadataOutput):
    description: str


class DivisionOutput(DivisionListOutput, MetadataTimestamps):
    workspace: MetadataOutput
    asset: MetadataOutput

    def to_division_input(self) -> DivisionInput:
        return DivisionInput(workspace=self.workspace.name, asset=self.asset.name, division=self.name)
