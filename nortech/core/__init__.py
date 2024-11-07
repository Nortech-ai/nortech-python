from __future__ import annotations

from typing import Literal

import nortech.core.services.asset as asset_service
import nortech.core.services.device as device_service
import nortech.core.services.division as division_service
import nortech.core.services.signal as signal_service
import nortech.core.services.unit as unit_service
import nortech.core.services.workspace as workspace_service
from nortech.core.gateways.nortech_api import NextRef, NortechAPI, PaginatedResponse, PaginationOptions
from nortech.core.values.asset import AssetInput, AssetInputDict, AssetListOutput, AssetOutput
from nortech.core.values.common import MetadataOutput
from nortech.core.values.device import DeviceInput, DeviceInputDict, DeviceListOutput, DeviceOutput
from nortech.core.values.division import DivisionInput, DivisionInputDict, DivisionListOutput, DivisionOutput
from nortech.core.values.signal import (
    SignalDeviceInput,
    SignalDeviceInputDict,
    SignalInput,
    SignalInputDict,
    SignalListOutput,
    SignalOutput,
)
from nortech.core.values.unit import UnitInput, UnitInputDict, UnitListOutput, UnitOutput
from nortech.core.values.workspace import WorkspaceInput, WorkspaceInputDict, WorkspaceListOutput, WorkspaceOutput


class Metadata:
    def __init__(self, nortech_api: NortechAPI):
        self.workspace = Workspace(nortech_api)
        self.asset = Asset(nortech_api)
        self.division = Division(nortech_api)
        self.unit = Unit(nortech_api)
        self.device = Device(nortech_api)
        self.signal = Signal(nortech_api)


class Workspace:
    def __init__(self, nortech_api: NortechAPI):
        self.nortech_api = nortech_api

    def get(
        self, workspace: WorkspaceInputDict | WorkspaceInput | WorkspaceOutput | WorkspaceListOutput | int | str
    ) -> WorkspaceOutput:
        return workspace_service.get_workspace(self.nortech_api, workspace)

    def list(
        self, pagination_options: PaginationOptions[Literal["id", "name", "description"]] | None = None
    ) -> PaginatedResponse[WorkspaceListOutput]:
        return workspace_service.list_workspaces(self.nortech_api, pagination_options)


class Asset:
    def __init__(self, nortech_api: NortechAPI):
        self.nortech_api = nortech_api

    def get(self, asset: int | AssetInputDict | AssetInput | AssetOutput | AssetListOutput) -> AssetOutput:
        return asset_service.get_workspace_asset(self.nortech_api, asset)

    def list(
        self,
        workspace: WorkspaceInputDict | WorkspaceInput | WorkspaceOutput | WorkspaceListOutput | int | str,
        pagination_options: PaginationOptions[Literal["id", "name", "description"]] | None = None,
    ) -> PaginatedResponse[AssetListOutput]:
        return asset_service.list_workspace_assets(self.nortech_api, workspace, pagination_options)


class Division:
    def __init__(self, nortech_api: NortechAPI):
        self.nortech_api = nortech_api

    def get(
        self, division: int | DivisionInputDict | DivisionInput | DivisionOutput | DivisionListOutput
    ) -> DivisionOutput:
        return division_service.get_workspace_asset_division(self.nortech_api, division)

    def list(
        self,
        asset: int | AssetInputDict | AssetInput | AssetOutput | AssetListOutput,
        pagination_options: PaginationOptions[Literal["id", "name", "description"]] | None = None,
    ) -> PaginatedResponse[DivisionListOutput]:
        return division_service.list_workspace_asset_divisions(self.nortech_api, asset, pagination_options)

    def list_by_workspace_id(
        self,
        workspace_id: int,
        pagination_options: PaginationOptions[Literal["id", "name", "description"]] | None = None,
    ) -> PaginatedResponse[DivisionListOutput]:
        return division_service.list_workspace_divisions(self.nortech_api, workspace_id, pagination_options)


class Unit:
    def __init__(self, nortech_api: NortechAPI):
        self.nortech_api = nortech_api

    def list(
        self,
        division: int | DivisionInputDict | DivisionInput | DivisionOutput | DivisionListOutput,
        pagination_options: PaginationOptions[Literal["id", "name"]] | None = None,
    ) -> PaginatedResponse[UnitListOutput]:
        return unit_service.list_workspace_asset_division_units(self.nortech_api, division, pagination_options)

    def get(self, unit: int | UnitInputDict | UnitInput | UnitOutput | UnitListOutput) -> UnitOutput:
        return unit_service.get_workspace_asset_division_unit(self.nortech_api, unit)

    def list_by_workspace_id(
        self,
        workspace_id: int,
        pagination_options: PaginationOptions[Literal["id", "name"]] | None = None,
    ) -> PaginatedResponse[UnitListOutput]:
        return unit_service.list_workspace_units(self.nortech_api, workspace_id, pagination_options)

    def list_by_asset_id(
        self,
        asset_id: int,
        pagination_options: PaginationOptions[Literal["id", "name"]] | None = None,
    ) -> PaginatedResponse[UnitListOutput]:
        return unit_service.list_asset_units(self.nortech_api, asset_id, pagination_options)


class Device:
    def __init__(self, nortech_api: NortechAPI):
        self.nortech_api = nortech_api

    def get(self, device: int | DeviceInputDict | DeviceInput | DeviceOutput | DeviceListOutput) -> DeviceOutput:
        return device_service.get_workspace_asset_division_device(self.nortech_api, device)

    def list(
        self,
        division: int | DivisionInputDict | DivisionInput | DivisionOutput | DivisionListOutput,
        pagination_options: PaginationOptions[Literal["id", "name", "type", "onboarded"]] | None = None,
    ) -> PaginatedResponse[DeviceListOutput]:
        return device_service.list_workspace_asset_division_devices(self.nortech_api, division, pagination_options)

    def list_by_workspace_id(
        self,
        workspace_id: int,
        pagination_options: PaginationOptions[Literal["id", "name", "type", "onboarded"]] | None = None,
    ) -> PaginatedResponse[DeviceListOutput]:
        return device_service.list_workspace_devices(self.nortech_api, workspace_id, pagination_options)

    def list_by_asset_id(
        self,
        asset_id: int,
        pagination_options: PaginationOptions[Literal["id", "name", "type", "onboarded"]] | None = None,
    ) -> PaginatedResponse[DeviceListOutput]:
        return device_service.list_asset_devices(self.nortech_api, asset_id, pagination_options)


class Signal:
    def __init__(self, nortech_api: NortechAPI):
        self.nortech_api = nortech_api

    def get(
        self,
        signal: int
        | SignalInputDict
        | SignalInput
        | SignalOutput
        | SignalListOutput
        | SignalDeviceInputDict
        | SignalDeviceInput,
    ) -> SignalOutput:
        if isinstance(signal, dict):
            if "device" in signal:
                signal = SignalDeviceInput.model_validate(signal)
            else:
                signal = SignalInput.model_validate(signal)

        if isinstance(signal, SignalDeviceInput):
            return signal_service.get_workspace_asset_division_device_signal(self.nortech_api, signal)

        return signal_service.get_workspace_asset_division_unit_signal(self.nortech_api, signal)

    def list(
        self,
        unit_or_signal: int | UnitInputDict | UnitInput | UnitOutput | DeviceInputDict | DeviceInput | DeviceOutput,
        pagination_options: PaginationOptions[
            Literal["id", "name", "physical_unit", "data_type", "description", "long_description"]
        ]
        | None = None,
    ) -> PaginatedResponse[SignalListOutput]:
        if isinstance(unit_or_signal, dict):
            if "device" in unit_or_signal:
                unit_or_signal = DeviceInput.model_validate(unit_or_signal)
            else:
                unit_or_signal = UnitInput.model_validate(unit_or_signal)

        if isinstance(unit_or_signal, DeviceInput) or isinstance(unit_or_signal, DeviceOutput):
            return signal_service.list_workspace_asset_division_device_signals(
                self.nortech_api, unit_or_signal, pagination_options
            )

        return signal_service.list_workspace_asset_division_unit_signals(
            self.nortech_api, unit_or_signal, pagination_options
        )

    def list_by_workspace_id(
        self,
        workspace_id: int,
        pagination_options: PaginationOptions[
            Literal["id", "name", "physical_unit", "data_type", "description", "long_description"]
        ]
        | None = None,
    ) -> PaginatedResponse[SignalListOutput]:
        return signal_service.list_workspace_signals(self.nortech_api, workspace_id, pagination_options)

    def list_by_asset_id(
        self,
        asset_id: int,
        pagination_options: PaginationOptions[
            Literal["id", "name", "physical_unit", "data_type", "description", "long_description"]
        ]
        | None = None,
    ) -> PaginatedResponse[SignalListOutput]:
        return signal_service.list_asset_signals(self.nortech_api, asset_id, pagination_options)

    def list_by_division_id(
        self,
        division_id: int,
        pagination_options: PaginationOptions[
            Literal["id", "name", "physical_unit", "data_type", "description", "long_description"]
        ]
        | None = None,
    ) -> PaginatedResponse[SignalListOutput]:
        return signal_service.list_division_signals(self.nortech_api, division_id, pagination_options)


__all__ = ["MetadataOutput", "NextRef"]
