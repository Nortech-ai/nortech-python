"""Module containing all schemas related with Devices."""

from __future__ import annotations

from nortech.metadata.values.division import (
    DivisionInput,
    DivisionInputDict,
)

from .common import MetadataOutput, MetadataTimestamps


class DeviceInputDict(DivisionInputDict):
    """Dictionary representation of Device input data.

    Attributes:
        workspace (str): The name of the Workspace.
        asset (str): The name of the Asset.
        division (str): The name of the Division.
        device (str): The name of the Device.

    """

    device: str


class DeviceInput(DivisionInput):
    """Pydantic model for Device input data.

    Attributes:
        workspace (str): The name of the Workspace.
        asset (str): The name of the Asset.
        division (str): The name of the Division.
        device (str): The name of the Device.

    """

    device: str


def parse_device_input(device_input: DeviceInput | DeviceInputDict):  # noqa: D103
    if isinstance(device_input, DeviceInput):
        return device_input
    else:
        return DeviceInput.model_validate(device_input)


class DeviceListOutput(MetadataOutput):
    """Output model for device list entries.

    Attributes:
        id (int): Id of the Device.
        name (str): Name of the Device.
        type (str): The type of the Device.
        onboarded (bool): Whether the Device is onboarded.

    """

    type: str
    onboarded: bool


class DeviceOutput(DeviceListOutput, MetadataTimestamps):
    """Detailed output model for a single device.

    Attributes:
        id (int): Id of the Device.
        name (str): Name of the Device.
        type (str): The type of the Device.
        onboarded (bool): Whether the Device is onboarded.
        created_at (datetime): Timestamp of when the Device was created.
        updated_at (datetime): Timestamp of when the Device was last updated.
        workspace: Metadata about the Workspace containing the Device.
            - id (int): Id of the Workspace.
            - name (str): Name of the Workspace.
        asset: Metadata about the Asset containing the Device.
            - id (int): Id of the Asset.
            - name (str): Name of the Asset.
        division: Metadata about the Division containing the Device.
            - id (int): Id of the Division.
            - name (str): Name of the Division.

    """

    workspace: MetadataOutput
    asset: MetadataOutput
    division: MetadataOutput
