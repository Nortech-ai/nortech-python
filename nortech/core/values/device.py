from __future__ import annotations

from nortech.core.values.division import (
    DivisionInput,
    DivisionInputDict,
)

from .common import MetadataOutput, MetadataTimestamps


class DeviceInputDict(DivisionInputDict):
    device: str


class DeviceInput(DivisionInput):
    device: str


def parse_device_input(device_input: DeviceInput | DeviceInputDict):
    if isinstance(device_input, DeviceInput):
        return device_input
    else:
        return DeviceInput.model_validate(device_input)


class DeviceListOutput(MetadataOutput):
    type: str
    onboarded: bool


class DeviceOutput(DeviceListOutput, MetadataTimestamps):
    workspace: MetadataOutput
    asset: MetadataOutput
    division: MetadataOutput
