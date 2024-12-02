"""Module containing all schemas related with Signals."""

from __future__ import annotations

import hashlib
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from nortech.metadata.values.device import DeviceInput, DeviceInputDict
from nortech.metadata.values.unit import UnitInput, UnitInputDict

from .common import MetadataOutput, MetadataTimestamps


class SignalInputDict(UnitInputDict):
    """Dictionary representation of Signal input data.

    Attributes:
        workspace (str): The name of the Workspace.
        asset (str): The name of the Asset.
        division (str): The name of the Division.
        unit (str): The name of the Unit.
        signal (str): The name of the Signal.

    """

    signal: str


class SignalInput(UnitInput):
    """Pydantic model for Signal input data.

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

    def model_dump_with_rename(self) -> dict:  # noqa: D102
        return {
            "rename": self.hash(),
            **self.model_dump(by_alias=True),
        }


def parse_signal_input(signal_input: SignalInput | SignalInputDict) -> SignalInput:  # noqa: D103
    if isinstance(signal_input, SignalInput):
        return signal_input
    else:
        return SignalInput.model_validate(signal_input)


class SignalDeviceInputDict(DeviceInputDict):
    """Dictionary representation of SignalDevice input data.

    Attributes:
        workspace (str): The name of the Workspace.
        asset (str): The name of the Asset.
        division (str): The name of the Division.
        device (str): The name of the Device.
        signal (str): The name of the Signal.

    """

    signal: str


class SignalDeviceInput(DeviceInput):
    """Pydantic model for SignalDevice input data.

    Attributes:
        workspace (str): The name of the Workspace.
        asset (str): The name of the Asset.
        division (str): The name of the Division.
        device (str): The name of the Device.
        signal (str): The name of the Signal.

    """

    signal: str


def parse_signal_device_input(  # noqa: D103
    signal_device_input: SignalDeviceInput | SignalDeviceInputDict | SignalOutput,
) -> SignalDeviceInput:
    if isinstance(signal_device_input, SignalDeviceInput):
        return signal_device_input
    return SignalDeviceInput.model_validate(signal_device_input)


class SignalListOutput(BaseModel):
    """Output model for signal list entries.

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
    physical_unit: str = Field(alias="physicalUnit")
    data_type: Literal["float", "boolean", "string", "json"] = Field(alias="dataType")
    description: str
    long_description: str = Field(alias="longDescription")


class SignalOutput(SignalListOutput, MetadataTimestamps):
    """Detailed output model for a single signal.

    Attributes:
        id (int): Id of the Signal.
        name (str): Name of the Signal.
        created_at (datetime): Timestamp of when the Signal was created.
        updated_at (datetime): Timestamp of when the Signal was last updated.
        workspace: Metadata about the Workspace containing the Signal.
            - id (int): Id of the Workspace.
            - name (str): Name of the Workspace.
        asset: Metadata about the Asset containing the Signal.
            - id (int): Id of the Asset.
            - name (str): Name of the Asset.
        division: Metadata about the Division containing the Signal.
            - id (int): Id of the Division.
            - name (str): Name of the Division.
        unit: Metadata about the Unit containing the Signal.
            - id (int): Id of the Unit.
            - name (str): Name of the Unit.
        device: Metadata about the Device containing the Signal.
            - id (int): Id of the Device.
            - name (str): Name of the Device.

    """

    workspace: MetadataOutput
    asset: MetadataOutput
    division: MetadataOutput
    unit: MetadataOutput
    device: MetadataOutput

    def to_signal_input(self) -> SignalInput:  # noqa: D102
        return SignalInput(
            workspace=self.workspace.name,
            asset=self.asset.name,
            division=self.division.name,
            unit=self.unit.name,
            signal=self.name,
        )
