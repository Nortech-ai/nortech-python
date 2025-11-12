from __future__ import annotations

from typing import Literal

import nortech.metadata.services.asset as asset_service
import nortech.metadata.services.division as division_service
import nortech.metadata.services.signal as signal_service
import nortech.metadata.services.unit as unit_service
import nortech.metadata.services.workspace as workspace_service
from nortech.gateways.nortech_api import NortechAPI
from nortech.metadata.values.asset import (
    AssetInput,
    AssetInputDict,
    AssetListOutput,
    AssetOutput,
)
from nortech.metadata.values.common import MetadataOutput
from nortech.metadata.values.division import (
    DivisionInput,
    DivisionInputDict,
    DivisionListOutput,
    DivisionOutput,
)
from nortech.metadata.values.pagination import (
    NextRef,
    PaginatedResponse,
    PaginationOptions,
)
from nortech.metadata.values.signal import (
    SignalInput,
    SignalInputDict,
    SignalListOutput,
    SignalOutput,
)
from nortech.metadata.values.unit import (
    UnitInput,
    UnitInputDict,
    UnitListOutput,
    UnitOutput,
)
from nortech.metadata.values.workspace import (
    WorkspaceInput,
    WorkspaceInputDict,
    WorkspaceListOutput,
    WorkspaceOutput,
)


class Metadata:
    """
    Client for interacting with the Nortech Metadata API.

    Attributes:
        workspace (Workspace): Client for interacting with the Nortech Metadata Workspace API.
        asset (Asset): Client for interacting with the Nortech Metadata Asset API.
        division (Division): Client for interacting with the Nortech Metadata Division API.
        unit (Unit): Client for interacting with the Nortech Metadata Unit API.
        signal (Signal): Client for interacting with the Nortech Metadata Signal API.

    """

    def __init__(self, nortech_api: NortechAPI):
        self.workspace = Workspace(nortech_api)
        self.asset = Asset(nortech_api)
        self.division = Division(nortech_api)
        self.unit = Unit(nortech_api)
        self.signal = Signal(nortech_api)


class Workspace:
    """Workspace."""

    def __init__(self, nortech_api: NortechAPI):
        self.nortech_api = nortech_api

    def get(
        self,
        workspace: int | str | WorkspaceInputDict | WorkspaceInput | WorkspaceOutput | WorkspaceListOutput,
    ) -> WorkspaceOutput:
        """
        Get a workspace by ID or name.

        Args:
            workspace (int | str | WorkspaceInputDict | WorkspaceInput | WorkspaceOutput | WorkspaceListOutput): The workspace identifier, which can be:
                - *int*: The workspace "ID".
                - *str*: The workspace "name".
                - [WorkspaceInputDict](#workspaceinputdict): A dictionary representation of a workspace input.
                - [WorkspaceInput](#workspaceinput): A pydantic model representing a workspace input.
                - [WorkspaceOutput](#workspaceoutput): A pydantic model representing a workspace output. Obtained from requesting a workspace metadata.
                - [WorkspaceListOutput](#workspacelistoutput): A pydantic model representing a listed workspace output. Obtained from requesting workspaces metadata.

        Returns:
            WorkspaceOutput: The workspace details.

        """
        return workspace_service.get_workspace(self.nortech_api, workspace)

    def list(
        self,
        pagination_options: PaginationOptions[Literal["id", "name", "description"]] | None = None,
    ) -> PaginatedResponse[WorkspaceListOutput, Literal["id", "name", "description"]]:
        """
        List all workspaces.

        Args:
            pagination_options (PaginationOptions, optional): Pagination settings.

        Returns:
            PaginatedResponse[WorkspaceListOutput]: A paginated list of workspaces.


        """
        return workspace_service.list_workspaces(self.nortech_api, pagination_options)


class Asset:
    def __init__(self, nortech_api: NortechAPI):
        self.nortech_api = nortech_api

    def get(self, asset: int | AssetInputDict | AssetInput | AssetOutput | AssetListOutput) -> AssetOutput:
        """
        Get an asset by ID or input.

        Args:
            asset (int | AssetInputDict | AssetInput | AssetOutput | AssetListOutput): The asset identifier, which can be:
                - *int*: The asset "ID".
                - [AssetInputDict](#assetinputdict): A dictionary representation of an asset input.
                - [AssetInput](#assetinput): A pydantic model representing an asset input.
                - [AssetOutput](#assetoutput): A pydantic model representing an asset output. Obtained from requesting an asset metadata.
                - [AssetListOutput](#assetlistoutput): A pydantic model representing a listed asset output. Obtained from requesting assets metadata.

        Returns:
            AssetOutput: The asset details.


        """
        return asset_service.get_workspace_asset(self.nortech_api, asset)

    def list(
        self,
        workspace: int | str | WorkspaceInputDict | WorkspaceInput | WorkspaceOutput | WorkspaceListOutput,
        pagination_options: PaginationOptions[Literal["id", "name", "description"]] | None = None,
    ) -> PaginatedResponse[AssetListOutput, Literal["id", "name", "description"]]:
        """
        List all assets in a workspace.

        Args:
            workspace (int | str | WorkspaceInputDict | WorkspaceInput | WorkspaceOutput | WorkspaceListOutput): The workspace identifier, which can be:
                - *int*: The workspace "ID".
                - *str*: The workspace "name".
                - [WorkspaceInputDict](#workspaceinputdict): A dictionary representation of a workspace input.
                - [WorkspaceInput](#workspaceinput): A pydantic model representing a workspace input.
                - [WorkspaceOutput](#workspaceoutput): A pydantic model representing a workspace output.
                - [WorkspaceListOutput](#workspacelistoutput): A pydantic model representing a listed workspace output.
            pagination_options (PaginationOptions, optional): Pagination settings.

        Returns:
            PaginatedResponse[AssetListOutput]: A paginated list of assets.

        """
        return asset_service.list_workspace_assets(self.nortech_api, workspace, pagination_options)


class Division:
    def __init__(self, nortech_api: NortechAPI):
        self.nortech_api = nortech_api

    def get(
        self,
        division: int | DivisionInputDict | DivisionInput | DivisionOutput | DivisionListOutput,
    ) -> DivisionOutput:
        """
        Get a division by ID or input.

        Args:
            division (int | DivisionInputDict | DivisionInput | DivisionOutput | DivisionListOutput): The division identifier, which can be:
                - *int*: The division "ID".
                - [DivisionInputDict](#divisioninputdict): A dictionary representation of a division input.
                - [DivisionInput](#divisioninput): A pydantic model representing a division input.
                - [DivisionOutput](#divisionoutput): A pydantic model representing a division output. Obtained from requesting a division metadata.
                - [DivisionListOutput](#divisionlistoutput): A pydantic model representing a listed division output. Obtained from requesting divisions metadata.

        Returns:
            DivisionOutput: The division details.

        """
        return division_service.get_workspace_asset_division(self.nortech_api, division)

    def list(
        self,
        asset: int | AssetInputDict | AssetInput | AssetOutput | AssetListOutput,
        pagination_options: PaginationOptions[Literal["id", "name", "description"]] | None = None,
    ) -> PaginatedResponse[DivisionListOutput, Literal["id", "name", "description"]]:
        """
        List all divisions in an asset.

        Args:
            asset (int | AssetInputDict | AssetInput | AssetOutput | AssetListOutput): The asset identifier, which can be:
                - *int*: The asset "ID".
                - [AssetInputDict](#assetinputdict): A dictionary representation of an asset input.
                - [AssetInput](#assetinput): A pydantic model representing an asset input.
                - [AssetOutput](#assetoutput): A pydantic model representing an asset output.
                - [AssetListOutput](#assetlistoutput): A pydantic model representing a listed asset output.
            pagination_options (PaginationOptions, optional): Pagination settings.

        Returns:
            PaginatedResponse[DivisionListOutput]: A paginated list of divisions.

        """
        return division_service.list_workspace_asset_divisions(self.nortech_api, asset, pagination_options)

    def list_by_workspace_id(
        self,
        workspace_id: int,
        pagination_options: PaginationOptions[Literal["id", "name", "description"]] | None = None,
    ) -> PaginatedResponse[DivisionListOutput, Literal["id", "name", "description"]]:
        """
        List all divisions in a workspace.

        Args:
            workspace_id (int): The workspace ID.
            pagination_options (PaginationOptions, optional): Pagination settings.

        Returns:
            PaginatedResponse[DivisionListOutput]: A paginated list of divisions.

        """
        return division_service.list_workspace_divisions(self.nortech_api, workspace_id, pagination_options)


class Unit:
    def __init__(self, nortech_api: NortechAPI):
        self.nortech_api = nortech_api

    def get(self, unit: int | UnitInputDict | UnitInput | UnitOutput | UnitListOutput) -> UnitOutput:
        """
        Get a unit by ID or input.

        Args:
            unit (int | UnitInputDict | UnitInput | UnitOutput | UnitListOutput): The unit identifier, which can be:
                - *int*: The unit "ID".
                - [UnitInputDict](#unitinputdict): A dictionary representation of a unit input.
                - [UnitInput](#unitinput): A pydantic model representing a unit input.
                - [UnitOutput](#unitoutput): A pydantic model representing a unit output. Obtained from requesting a unit metadata.
                - [UnitListOutput](#unitlistoutput): A pydantic model representing a listed unit output. Obtained from requesting units metadata.

        Returns:
            UnitOutput: The unit details.

        """
        return unit_service.get_workspace_asset_division_unit(self.nortech_api, unit)

    def list(
        self,
        division: int | DivisionInputDict | DivisionInput | DivisionOutput | DivisionListOutput,
        pagination_options: PaginationOptions[Literal["id", "name"]] | None = None,
    ) -> PaginatedResponse[UnitListOutput, Literal["id", "name"]]:
        """
        List all units in a division.

        Args:
            division (int | DivisionInputDict | DivisionInput | DivisionOutput | DivisionListOutput): The division identifier, which can be:
                - *int*: The division "ID".
                - [DivisionInputDict](#divisioninputdict): A dictionary representation of a division input.
                - [DivisionInput](#divisioninput): A pydantic model representing a division input.
                - [DivisionOutput](#divisionoutput): A pydantic model representing a division output.
                - [DivisionListOutput](#divisionlistoutput): A pydantic model representing a listed division output.
            pagination_options (PaginationOptions, optional): Pagination settings.

        Returns:
            PaginatedResponse[UnitListOutput]: A paginated list of units.

        """
        return unit_service.list_workspace_asset_division_units(self.nortech_api, division, pagination_options)

    def list_by_workspace_id(
        self,
        workspace_id: int,
        pagination_options: PaginationOptions[Literal["id", "name"]] | None = None,
    ) -> PaginatedResponse[UnitListOutput, Literal["id", "name"]]:
        """
        List all units in a workspace.

        Args:
            workspace_id (int): The workspace ID.
            pagination_options (PaginationOptions, optional): Pagination settings.

        Returns:
            PaginatedResponse[UnitListOutput]: A paginated list of units.

        """
        return unit_service.list_workspace_units(self.nortech_api, workspace_id, pagination_options)

    def list_by_asset_id(
        self,
        asset_id: int,
        pagination_options: PaginationOptions[Literal["id", "name"]] | None = None,
    ) -> PaginatedResponse[UnitListOutput, Literal["id", "name"]]:
        """
        List all units in an asset.

        Args:
            asset_id (int): The asset ID.
            pagination_options (PaginationOptions, optional): Pagination settings.

        Returns:
            PaginatedResponse[UnitListOutput]: A paginated list of units.

        """
        return unit_service.list_asset_units(self.nortech_api, asset_id, pagination_options)


class Signal:
    def __init__(self, nortech_api: NortechAPI):
        self.nortech_api = nortech_api

    def get(self, signal: int | SignalInputDict | SignalInput | SignalOutput | SignalListOutput) -> SignalOutput:
        """
        Get a signal by ID or input.

        Args:
            signal (int | SignalInputDict | SignalInput | SignalOutput | SignalListOutput): The signal identifier, which can be:
                - *int*: The signal "ID".
                - [SignalInputDict](#signalinputdict): A dictionary representation of a signal input.
                - [SignalInput](#signalinput): A pydantic model representing a signal input.
                - [SignalOutput](#signaloutput): A pydantic model representing a signal output. Obtained from requesting a signal metadata.
                - [SignalListOutput](#signallistoutput): A pydantic model representing a listed signal output. Obtained from requesting signals metadata.

        Returns:
            SignalOutput: The signal details.

        """
        if isinstance(signal, dict):
            signal = SignalInput.model_validate(signal)

        return signal_service.get_workspace_asset_division_unit_signal(self.nortech_api, signal)

    def list(
        self,
        unit: int | UnitInputDict | UnitInput | UnitOutput,
        pagination_options: PaginationOptions[
            Literal[
                "id",
                "name",
                "physical_unit",
                "data_type",
                "description",
                "long_description",
            ]
        ]
        | None = None,
    ) -> PaginatedResponse[
        SignalListOutput, Literal["id", "name", "physical_unit", "data_type", "description", "long_description"]
    ]:
        """
        List all signals in a unit.

        Args:
            unit (int | UnitInputDict | UnitInput | UnitOutput): The unit identifier, which can be:
                - *int*: The unit "ID".
                - [UnitInputDict](#unitinputdict): A dictionary representation of a unit input.
                - [UnitInput](#unitinput): A pydantic model representing a unit input.
                - [UnitOutput](#unitoutput): A pydantic model representing a unit output.
            pagination_options (PaginationOptions, optional): Pagination settings.

        Returns:
            PaginatedResponse[SignalListOutput]: A paginated list of signals.


        """
        if isinstance(unit, dict):
            unit = UnitInput.model_validate(unit)

        return signal_service.list_workspace_asset_division_unit_signals(self.nortech_api, unit, pagination_options)

    def list_by_workspace_id(
        self,
        workspace_id: int,
        pagination_options: PaginationOptions[
            Literal[
                "id",
                "name",
                "physical_unit",
                "data_type",
                "description",
                "long_description",
            ]
        ]
        | None = None,
    ) -> PaginatedResponse[
        SignalListOutput, Literal["id", "name", "physical_unit", "data_type", "description", "long_description"]
    ]:
        """
        List all signals in a workspace.

        Args:
            workspace_id (int): The workspace ID.
            pagination_options (PaginationOptions, optional): Pagination settings.

        Returns:
            PaginatedResponse[SignalListOutput]: A paginated list of signals.


        """
        return signal_service.list_workspace_signals(self.nortech_api, workspace_id, pagination_options)

    def list_by_asset_id(
        self,
        asset_id: int,
        pagination_options: PaginationOptions[
            Literal[
                "id",
                "name",
                "physical_unit",
                "data_type",
                "description",
                "long_description",
            ]
        ]
        | None = None,
    ) -> PaginatedResponse[
        SignalListOutput, Literal["id", "name", "physical_unit", "data_type", "description", "long_description"]
    ]:
        """
        List all signals in an asset.

        Args:
            asset_id (int): The asset ID.
            pagination_options (PaginationOptions, optional): Pagination settings.

        Returns:
            PaginatedResponse[SignalListOutput]: A paginated list of signals.


        """
        return signal_service.list_asset_signals(self.nortech_api, asset_id, pagination_options)

    def list_by_division_id(
        self,
        division_id: int,
        pagination_options: PaginationOptions[
            Literal[
                "id",
                "name",
                "physical_unit",
                "data_type",
                "description",
                "long_description",
            ]
        ]
        | None = None,
    ) -> PaginatedResponse[
        SignalListOutput, Literal["id", "name", "physical_unit", "data_type", "description", "long_description"]
    ]:
        """
        List all signals in a division.

        Args:
            division_id (int): The division ID.
            pagination_options (PaginationOptions, optional): Pagination settings.

        Returns:
            PaginatedResponse[SignalListOutput]: A paginated list of signals.


        """
        return signal_service.list_division_signals(self.nortech_api, division_id, pagination_options)


__all__ = ["MetadataOutput", "NextRef"]
