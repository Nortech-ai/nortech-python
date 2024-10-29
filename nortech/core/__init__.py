from __future__ import annotations

from typing import Literal

import nortech.core.services.asset as asset_service
import nortech.core.services.device as device_service
import nortech.core.services.division as division_service
import nortech.core.services.signal as signal_service
import nortech.core.services.unit as unit_service
import nortech.core.services.workspace as workspace_service
from nortech.core.gateways.nortech_api import NortechAPI, PaginatedResponse, PaginationOptions
from nortech.core.values.asset import AssetInput, AssetInputDict, AssetListOutput, AssetOutput
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

    def list_workspaces(
        self, pagination_options: PaginationOptions[Literal["id", "name", "description"]] | None = None
    ) -> PaginatedResponse[WorkspaceListOutput]:
        return workspace_service.list_workspaces(self.nortech_api, pagination_options)

    def get_workspace(
        self, workspace: WorkspaceInputDict | WorkspaceInput | WorkspaceOutput | int | str
    ) -> WorkspaceOutput | None:
        return workspace_service.get_workspace(self.nortech_api, workspace)


class Asset:
    def __init__(self, nortech_api: NortechAPI):
        self.nortech_api = nortech_api

    def list_workspace_assets(
        self,
        workspace: WorkspaceInputDict | WorkspaceInput | int | str,
        pagination_options: PaginationOptions[Literal["id", "name", "description"]] | None = None,
    ) -> PaginatedResponse[AssetListOutput]:
        return asset_service.list_workspace_assets(self.nortech_api, workspace, pagination_options)

    def get_workspace_asset(self, asset: AssetInputDict | AssetInput | AssetOutput) -> AssetOutput | None:
        return asset_service.get_workspace_asset(self.nortech_api, asset)

    def get_asset(self, asset_id: int) -> AssetOutput | None:
        return asset_service.get_asset(self.nortech_api, asset_id)


class Division:
    def __init__(self, nortech_api: NortechAPI):
        self.nortech_api = nortech_api

    def list_workspace_asset_divisions(
        self,
        asset: AssetInputDict | AssetInput | AssetOutput,
        pagination_options: PaginationOptions[Literal["id", "name", "description"]] | None = None,
    ) -> PaginatedResponse[DivisionListOutput]:
        return division_service.list_workspace_asset_divisions(self.nortech_api, asset, pagination_options)

    def get_workspace_asset_division(
        self, division: DivisionInputDict | DivisionInput | DivisionOutput
    ) -> DivisionOutput | None:
        return division_service.get_workspace_asset_division(self.nortech_api, division)

    def list_workspace_divisions(
        self,
        workspace_id: int,
        pagination_options: PaginationOptions[Literal["id", "name", "description"]] | None = None,
    ) -> PaginatedResponse[DivisionListOutput]:
        return division_service.list_workspace_divisions(self.nortech_api, workspace_id, pagination_options)

    def list_asset_divisions(
        self,
        asset_id: int,
        pagination_options: PaginationOptions[Literal["id", "name", "description"]] | None = None,
    ) -> PaginatedResponse[DivisionListOutput]:
        return division_service.list_asset_divisions(self.nortech_api, asset_id, pagination_options)

    def get_division(self, division_id: int) -> DivisionOutput | None:
        return division_service.get_division(self.nortech_api, division_id)


class Unit:
    def __init__(self, nortech_api: NortechAPI):
        self.nortech_api = nortech_api

    def list_workspace_asset_division_units(
        self,
        division: DivisionInputDict | DivisionInput | DivisionOutput,
        pagination_options: PaginationOptions[Literal["id", "name"]] | None = None,
    ) -> PaginatedResponse[UnitListOutput]:
        return unit_service.list_workspace_asset_division_units(self.nortech_api, division, pagination_options)

    def get_workspace_asset_division_unit(self, unit: UnitInputDict | UnitInput | UnitOutput) -> UnitOutput | None:
        return unit_service.get_workspace_asset_division_unit(self.nortech_api, unit)

    def list_workspace_units(
        self,
        workspace_id: int,
        pagination_options: PaginationOptions[Literal["id", "name"]] | None = None,
    ) -> PaginatedResponse[UnitListOutput]:
        return unit_service.list_workspace_units(self.nortech_api, workspace_id, pagination_options)

    def list_asset_units(
        self,
        asset_id: int,
        pagination_options: PaginationOptions[Literal["id", "name"]] | None = None,
    ) -> PaginatedResponse[UnitListOutput]:
        return unit_service.list_asset_units(self.nortech_api, asset_id, pagination_options)

    def list_division_units(
        self,
        division_id: int,
        pagination_options: PaginationOptions[Literal["id", "name"]] | None = None,
    ) -> PaginatedResponse[UnitListOutput]:
        return unit_service.list_division_units(self.nortech_api, division_id, pagination_options)

    def get_unit(self, unit_id: int) -> UnitOutput | None:
        return unit_service.get_unit(self.nortech_api, unit_id)


class Device:
    def __init__(self, nortech_api: NortechAPI):
        self.nortech_api = nortech_api

    def list_workspace_asset_division_devices(
        self,
        division: DivisionInputDict | DivisionInput | DivisionOutput,
        pagination_options: PaginationOptions[Literal["id", "name", "type", "onboarded"]] | None = None,
    ) -> PaginatedResponse[DeviceListOutput]:
        return device_service.list_workspace_asset_division_devices(self.nortech_api, division, pagination_options)

    def get_workspace_asset_division_device(
        self, device: DeviceInputDict | DeviceInput | DeviceOutput
    ) -> DeviceOutput | None:
        return device_service.get_workspace_asset_division_device(self.nortech_api, device)

    def list_workspace_devices(
        self,
        workspace_id: int,
        pagination_options: PaginationOptions[Literal["id", "name", "type", "onboarded"]] | None = None,
    ) -> PaginatedResponse[DeviceListOutput]:
        return device_service.list_workspace_devices(self.nortech_api, workspace_id, pagination_options)

    def list_asset_devices(
        self,
        asset_id: int,
        pagination_options: PaginationOptions[Literal["id", "name", "type", "onboarded"]] | None = None,
    ) -> PaginatedResponse[DeviceListOutput]:
        return device_service.list_asset_devices(self.nortech_api, asset_id, pagination_options)

    def list_division_devices(
        self,
        division_id: int,
        pagination_options: PaginationOptions[Literal["id", "name", "type", "onboarded"]] | None = None,
    ) -> PaginatedResponse[DeviceListOutput]:
        return device_service.list_division_devices(self.nortech_api, division_id, pagination_options)

    def get_device(self, device_id: int) -> DeviceOutput | None:
        return device_service.get_device(self.nortech_api, device_id)


class Signal:
    def __init__(self, nortech_api: NortechAPI):
        self.nortech_api = nortech_api

    def list_workspace_asset_division_unit_signals(
        self,
        unit: UnitInputDict | UnitInput | UnitOutput,
        pagination_options: PaginationOptions[
            Literal["id", "name", "physical_unit", "data_type", "description", "long_description"]
        ]
        | None = None,
    ) -> PaginatedResponse[SignalListOutput]:
        return signal_service.list_workspace_asset_division_unit_signals(self.nortech_api, unit, pagination_options)

    def get_workspace_asset_division_unit_signal(
        self, signal: SignalInputDict | SignalInput | SignalOutput
    ) -> SignalOutput | None:
        return signal_service.get_workspace_asset_division_unit_signal(self.nortech_api, signal)

    def list_workspace_asset_division_device_signals(
        self,
        device: DeviceInputDict | DeviceInput | DeviceOutput,
        pagination_options: PaginationOptions[
            Literal["id", "name", "physical_unit", "data_type", "description", "long_description"]
        ]
        | None = None,
    ) -> PaginatedResponse[SignalListOutput]:
        return signal_service.list_workspace_asset_division_device_signals(self.nortech_api, device, pagination_options)

    def get_workspace_asset_division_device_signal(
        self, signal: SignalDeviceInputDict | SignalDeviceInput | SignalOutput
    ) -> SignalOutput | None:
        return signal_service.get_workspace_asset_division_device_signal(self.nortech_api, signal)

    def list_workspace_signals(
        self,
        workspace_id: int,
        pagination_options: PaginationOptions[
            Literal["id", "name", "physical_unit", "data_type", "description", "long_description"]
        ]
        | None = None,
    ) -> PaginatedResponse[SignalListOutput]:
        return signal_service.list_workspace_signals(self.nortech_api, workspace_id, pagination_options)

    def list_asset_signals(
        self,
        asset_id: int,
        pagination_options: PaginationOptions[
            Literal["id", "name", "physical_unit", "data_type", "description", "long_description"]
        ]
        | None = None,
    ) -> PaginatedResponse[SignalListOutput]:
        return signal_service.list_asset_signals(self.nortech_api, asset_id, pagination_options)

    def list_division_signals(
        self,
        division_id: int,
        pagination_options: PaginationOptions[
            Literal["id", "name", "physical_unit", "data_type", "description", "long_description"]
        ]
        | None = None,
    ) -> PaginatedResponse[SignalListOutput]:
        return signal_service.list_division_signals(self.nortech_api, division_id, pagination_options)

    def list_unit_signals(
        self,
        unit_id: int,
        pagination_options: PaginationOptions[
            Literal["id", "name", "physical_unit", "data_type", "description", "long_description"]
        ]
        | None = None,
    ) -> PaginatedResponse[SignalListOutput]:
        return signal_service.list_unit_signals(self.nortech_api, unit_id, pagination_options)

    def list_device_signals(
        self,
        device_id: int,
        pagination_options: PaginationOptions[
            Literal["id", "name", "physical_unit", "data_type", "description", "long_description"]
        ]
        | None = None,
    ) -> PaginatedResponse[SignalListOutput]:
        return signal_service.list_device_signals(self.nortech_api, device_id, pagination_options)

    def get_signal(self, signal_id: int) -> SignalOutput | None:
        return signal_service.get_signal(self.nortech_api, signal_id)

    def get_signals(self, signals: list[SignalInput | SignalInputDict | SignalOutput | int]) -> list[SignalOutput]:
        return signal_service.get_signals(self.nortech_api, signals)
