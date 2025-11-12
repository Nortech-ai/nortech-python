"""Module containing all schemas related with Signals."""

from __future__ import annotations

import hashlib
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

from nortech.metadata.values.unit import UnitInput, UnitInputDict

from .common import MetadataOutput, MetadataTimestamps


class SignalInputDict(UnitInputDict):
    """
    Dictionary representation of Signal input data.

    Attributes:
        workspace (str): The name of the Workspace.
        asset (str): The name of the Asset.
        division (str): The name of the Division.
        unit (str): The name of the Unit.
        signal (str): The name of the Signal.

    """

    signal: str


class SignalInput(UnitInput):
    """
    Pydantic model for Signal input data.

    Attributes:
        workspace (str): The name of the Workspace.
        asset (str): The name of the Asset.
        division (str): The name of the Division.
        unit (str): The name of the Unit.
        signal (str): The name of the Signal.

    """

    signal: str

    @property
    def path(self) -> str:  # noqa: D102
        return f"{self.workspace}/{self.asset}/{self.division}/{self.unit}/{self.signal}"

    def hash(self) -> str:  # noqa: D102
        return hashlib.sha256(self.model_dump_json().encode()).hexdigest()

    def model_dump_with_rename(self) -> dict[str, str]:  # noqa: D102
        return {
            "rename": self.hash(),
            **self.model_dump(by_alias=True),
        }


def parse_signal_input(signal_input: SignalInput | SignalInputDict) -> SignalInput:  # noqa: D103
    if isinstance(signal_input, SignalInput):
        return signal_input
    else:
        return SignalInput.model_validate(signal_input)


class SignalSpecs(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    physical_unit: Optional[str] = Field(alias="physicalUnit", default=None)
    description: Optional[str] = Field(default=None)
    long_description: Optional[str] = Field(alias="longDescription", default=None)
    data_type: Literal["float", "boolean", "string", "json"] = Field(alias="dataType", default="float")


class SignalListOutput(SignalSpecs):
    """
    Output model for signal list entries.

    Attributes:
        id (int): Id of the Signal.
        name (str): Name of the Signal.
        physical_unit (str): The physical unit of the Signal.
        data_type (Literal["float", "boolean", "string", "json"]): The data type of the Signal.
        description (str): A description of the Signal.
        long_description (str): A long description of the Signal.

    """

    model_config = ConfigDict(populate_by_name=True)

    id: int
    name: str


class SignalOutput(SignalListOutput, MetadataTimestamps):
    workspace: MetadataOutput
    asset: MetadataOutput
    division: MetadataOutput
    unit: MetadataOutput

    def to_signal_input(self) -> SignalInput:
        return SignalInput(
            workspace=self.workspace.name,
            asset=self.asset.name,
            division=self.division.name,
            unit=self.unit.name,
            signal=self.name,
        )


class CreateSignalInput(SignalInput, SignalSpecs):
    group_key: Optional[str] = Field(alias="groupKey", default=None)
