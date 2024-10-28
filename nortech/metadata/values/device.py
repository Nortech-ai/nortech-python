from __future__ import annotations

from nortech.metadata.values.division import (
    DivisionInput,
    DivisionInputDict,
)

from .common import MetadataOutput, MetadataTimestamps


class DeviceInputDict(DivisionInputDict):
    device: str


class DeviceInput(DivisionInput):
    device: str


def parse_device_input(device_input: DeviceInput | DeviceInputDict | DeviceOutput):
    if isinstance(device_input, DeviceInput):
        return device_input
    elif isinstance(device_input, DeviceOutput):
        return device_input.to_device_input()
    else:
        return DeviceInput.model_validate(device_input)


class DeviceListOutput(MetadataOutput):
    type: str
    onboarded: bool


class DeviceOutput(DeviceListOutput, MetadataTimestamps):
    workspace: MetadataOutput
    asset: MetadataOutput
    division: MetadataOutput

    def to_device_input(self) -> DeviceInput:
        return DeviceInput(
            workspace=self.workspace.name,
            asset=self.asset.name,
            division=self.division.name,
            device=self.name,
        )
