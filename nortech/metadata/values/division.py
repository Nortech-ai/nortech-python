"""Module containing all schemas related with Divisions."""

from __future__ import annotations

from nortech.metadata.values.asset import AssetInput, AssetInputDict

from .common import MetadataOutput, MetadataTimestamps


class DivisionInputDict(AssetInputDict):
    """Dictionary representation of Division input data.

    Attributes:
        workspace (str): The name of the Workspace.
        asset (str): The name of the Asset.
        division (str): The name of the Division.

    """

    division: str


class DivisionInput(AssetInput):
    """Pydantic model for Division input data.

    Attributes:
        workspace (str): The name of the Workspace.
        asset (str): The name of the Asset.
        division (str): The name of the Division.

    """

    division: str


def parse_division_input(division_input: DivisionInput | DivisionInputDict):  # noqa: D103
    if isinstance(division_input, DivisionInput):
        return division_input
    else:
        return DivisionInput.model_validate(division_input)


class DivisionListOutput(MetadataOutput):
    """Output model for division list entries.

    Attributes:
        id (int): Id of the Division.
        name (str): Name of the Division.
        description (str): A description of the division.

    """

    description: str


class DivisionOutput(DivisionListOutput, MetadataTimestamps):
    """Detailed output model for a single division.

    Attributes:
        id (int): Id of the Division.
        name (str): Name of the Division.
        description (str): A description of the division.
        created_at (datetime): Timestamp of when the Division was created.
        updated_at (datetime): Timestamp of when the Division was last updated.
        workspace: Metadata about the Workspace containing the Division.
            - id (int): Id of the Workspace.
            - name (str): Name of the Workspace.
        asset: Metadata about the Asset containing the Division.
            - id (int): Id of the Asset.
            - name (str): Name of the Asset.

    """

    workspace: MetadataOutput
    asset: MetadataOutput
