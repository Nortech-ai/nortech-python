"""Module containing all schemas related with Units."""

from __future__ import annotations

from pydantic import BaseModel

from nortech.metadata.values.division import (
    DivisionInput,
    DivisionInputDict,
)

from .common import MetadataOutput, MetadataTimestamps


class UnitInputDict(DivisionInputDict):
    """Dictionary representation of Unit input data.

    Attributes:
        workspace (str): The name of the Workspace.
        asset (str): The name of the Asset.
        division (str): The name of the Division.
        unit (str): The name of the Unit.

    """

    unit: str


class UnitInput(DivisionInput):
    """Pydantic model for Unit input data.

    Attributes:
        workspace (str): The name of the Workspace.
        asset (str): The name of the Asset.
        division (str): The name of the Division.
        unit (str): The name of the Unit.

    """

    unit: str


def parse_unit_input(unit_input: UnitInput | UnitInputDict):  # noqa: D103
    if isinstance(unit_input, UnitInput):
        return unit_input
    else:
        return UnitInput.model_validate(unit_input)


class UnitListOutput(BaseModel):
    """Output model for unit list entries.

    Attributes:
        id (int): Id of the Unit.
        name (str): Name of the Unit.

    """

    id: int
    name: str


class UnitDivision(BaseModel):
    """Output model for unit division entries.

    Attributes:
        id (int): Id of the Division.
        name (str): Name of the Division.

    """

    id: int
    name: str


class UnitOutput(UnitListOutput, MetadataTimestamps):
    """Detailed output model for a single unit.

    Attributes:
        id (int): Id of the Unit.
        name (str): Name of the Unit.
        created_at (datetime): Timestamp of when the Unit was created.
        updated_at (datetime): Timestamp of when the Unit was last updated.
        workspace: Metadata about the Workspace containing the Unit.
            - id (int): Id of the Workspace.
            - name (str): Name of the Workspace.
        asset: Metadata about the Asset containing the Unit.
            - id (int): Id of the Asset.
            - name (str): Name of the Asset.
        division: Metadata about the Division containing the Unit.
            - id (int): Id of the Division.
            - name (str): Name of the Division.

    """

    workspace: MetadataOutput
    asset: MetadataOutput
    division: MetadataOutput
