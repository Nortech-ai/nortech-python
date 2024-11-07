from __future__ import annotations

import hashlib
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from nortech.core.values.device import DeviceInput, DeviceInputDict
from nortech.core.values.unit import UnitInput, UnitInputDict

from .common import MetadataOutput, MetadataTimestamps


class SignalInputDict(UnitInputDict):
    signal: str


class SignalInput(UnitInput):
    signal: str

    @property
    def path(self):
        return f"{self.workspace}/{self.asset}/{self.division}/{self.unit}/{self.signal}"

    def hash(self):
        return hashlib.sha256(self.model_dump_json().encode()).hexdigest()

    def model_dump_with_rename(self):
        return {
            "rename": self.hash(),
            **self.model_dump(by_alias=True),
        }


def parse_signal_input(signal_input: SignalInput | SignalInputDict):
    if isinstance(signal_input, SignalInput):
        return signal_input
    else:
        return SignalInput.model_validate(signal_input)


class SignalDeviceInputDict(DeviceInputDict):
    signal: str


class SignalDeviceInput(DeviceInput):
    signal: str


def parse_signal_device_input(
    signal_device_input: SignalDeviceInput | SignalDeviceInputDict | SignalOutput,
):
    if isinstance(signal_device_input, SignalDeviceInput):
        return signal_device_input
    return SignalDeviceInput.model_validate(signal_device_input)


class SignalListOutput(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: int
    name: str
    physical_unit: str = Field(alias="physicalUnit")
    data_type: Literal["float", "boolean", "string", "json"] = Field(alias="dataType")
    description: str
    long_description: str = Field(alias="longDescription")


class SignalOutput(SignalListOutput, MetadataTimestamps):
    workspace: MetadataOutput
    asset: MetadataOutput
    division: MetadataOutput
    unit: MetadataOutput
    device: MetadataOutput

    def to_signal_input(self):
        return SignalInput(
            workspace=self.workspace.name,
            asset=self.asset.name,
            division=self.division.name,
            unit=self.unit.name,
            signal=self.name,
        )
