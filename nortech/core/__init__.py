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
        self, workspace: WorkspaceInputDict | WorkspaceInput | WorkspaceOutput | int | str
    ) -> WorkspaceOutput | None:
        return workspace_service.get_workspace(self.nortech_api, workspace)

    def list(
        self, pagination_options: PaginationOptions[Literal["id", "name", "description"]] | None = None
    ) -> PaginatedResponse[WorkspaceListOutput]:
        return workspace_service.list_workspaces(self.nortech_api, pagination_options)


class Asset:
    def __init__(self, nortech_api: NortechAPI):
        self.nortech_api = nortech_api

    def get(self, asset: int | AssetInputDict | AssetInput | AssetOutput) -> AssetOutput | None:
        if isinstance(asset, int):
            return asset_service.get_asset(self.nortech_api, asset)

        return asset_service.get_workspace_asset(self.nortech_api, asset)

    def list(
        self,
        workspace: WorkspaceInputDict | WorkspaceInput | int | str,
        pagination_options: PaginationOptions[Literal["id", "name", "description"]] | None = None,
    ) -> PaginatedResponse[AssetListOutput]:
        return asset_service.list_workspace_assets(self.nortech_api, workspace, pagination_options)


class Division:
    def __init__(self, nortech_api: NortechAPI):
        self.nortech_api = nortech_api

    def get(self, division: int | DivisionInputDict | DivisionInput | DivisionOutput) -> DivisionOutput | None:
        if isinstance(division, int):
            return division_service.get_division(self.nortech_api, division)

        return division_service.get_workspace_asset_division(self.nortech_api, division)

    def list(
        self,
        asset: int | AssetInputDict | AssetInput | AssetOutput,
        pagination_options: PaginationOptions[Literal["id", "name", "description"]] | None = None,
    ) -> PaginatedResponse[DivisionListOutput]:
        if isinstance(asset, int):
            return division_service.list_asset_divisions(self.nortech_api, asset, pagination_options)

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
        division: int | DivisionInputDict | DivisionInput | DivisionOutput,
        pagination_options: PaginationOptions[Literal["id", "name"]] | None = None,
    ) -> PaginatedResponse[UnitListOutput]:
        if isinstance(division, int):
            return unit_service.list_division_units(self.nortech_api, division, pagination_options)

        return unit_service.list_workspace_asset_division_units(self.nortech_api, division, pagination_options)

    def get(self, unit: int | UnitInputDict | UnitInput | UnitOutput) -> UnitOutput | None:
        if isinstance(unit, int):
            return unit_service.get_unit(self.nortech_api, unit)

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

    def get(self, device: int | DeviceInputDict | DeviceInput | DeviceOutput) -> DeviceOutput | None:
        if isinstance(device, int):
            return device_service.get_device(self.nortech_api, device)

        return device_service.get_workspace_asset_division_device(self.nortech_api, device)

    def list(
        self,
        division: int | DivisionInputDict | DivisionInput | DivisionOutput,
        pagination_options: PaginationOptions[Literal["id", "name", "type", "onboarded"]] | None = None,
    ) -> PaginatedResponse[DeviceListOutput]:
        if isinstance(division, int):
            return device_service.list_division_devices(self.nortech_api, division, pagination_options)

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
        self, signal: int | SignalInputDict | SignalInput | SignalOutput | SignalDeviceInputDict | SignalDeviceInput
    ) -> SignalOutput | None:
        if isinstance(signal, int):
            return signal_service.get_signal(self.nortech_api, signal)

        if isinstance(signal, dict):
            if "device" in signal:
                signal = SignalDeviceInput.model_validate(signal)
            else:
                signal = SignalInput.model_validate(signal)

        if isinstance(signal, SignalDeviceInput):
            return signal_service.get_workspace_asset_division_device_signal(self.nortech_api, signal)

        return signal_service.get_workspace_asset_division_unit_signal(self.nortech_api, signal)

    def get_signals(self, signals: list[SignalInput | SignalInputDict | SignalOutput | int]) -> list[SignalOutput]:
        return signal_service.get_signals(self.nortech_api, signals)

    def list(
        self,
        parent: int | UnitInputDict | UnitInput | UnitOutput | DeviceInputDict | DeviceInput | DeviceOutput,
        pagination_options: PaginationOptions[
            Literal["id", "name", "physical_unit", "data_type", "description", "long_description"]
        ]
        | None = None,
    ) -> PaginatedResponse[SignalListOutput]:
        if isinstance(parent, int):
            return signal_service.list_unit_signals(self.nortech_api, parent, pagination_options)

        if isinstance(parent, dict):
            if "device" in parent:
                parent = DeviceInput.model_validate(parent)
            else:
                parent = UnitInput.model_validate(parent)

        if isinstance(parent, DeviceInput) or isinstance(parent, DeviceOutput):
            return signal_service.list_workspace_asset_division_device_signals(
                self.nortech_api, parent, pagination_options
            )

        return signal_service.list_workspace_asset_division_unit_signals(self.nortech_api, parent, pagination_options)

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
