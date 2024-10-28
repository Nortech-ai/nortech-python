from __future__ import annotations

from pydantic import BaseModel

from nortech.metadata.values.division import (
    DivisionInput,
    DivisionInputDict,
)

from .common import MetadataOutput, MetadataTimestamps


class UnitInputDict(DivisionInputDict):
    unit: str


class UnitInput(DivisionInput):
    unit: str


def parse_unit_input(unit_input: UnitInput | UnitInputDict | UnitOutput):
    if isinstance(unit_input, UnitInput):
        return unit_input
    elif isinstance(unit_input, UnitOutput):
        return unit_input.to_unit_input()
    else:
        return UnitInput.model_validate(unit_input)


class UnitListOutput(BaseModel):
    id: int
    name: str


class UnitDivision(BaseModel):
    id: int
    name: str


class UnitOutput(UnitListOutput, MetadataTimestamps):
    workspace: MetadataOutput
    asset: MetadataOutput
    division: MetadataOutput

    def to_unit_input(self) -> UnitInput:
        return UnitInput(
            workspace=self.workspace.name,
            asset=self.asset.name,
            division=self.division.name,
            unit=self.name,
        )
