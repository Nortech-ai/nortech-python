from __future__ import annotations

from typing import Literal

import nortech.metadata.services.asset as asset_service
import nortech.metadata.services.device as device_service
import nortech.metadata.services.division as division_service
import nortech.metadata.services.signal as signal_service
import nortech.metadata.services.unit as unit_service
import nortech.metadata.services.workspace as workspace_service
from nortech.gateways.nortech_api import NortechAPI
from nortech.metadata.values.asset import AssetInput, AssetInputDict, AssetListOutput, AssetOutput
from nortech.metadata.values.common import MetadataOutput
from nortech.metadata.values.device import DeviceInput, DeviceInputDict, DeviceListOutput, DeviceOutput
from nortech.metadata.values.division import DivisionInput, DivisionInputDict, DivisionListOutput, DivisionOutput
from nortech.metadata.values.pagination import NextRef, PaginatedResponse, PaginationOptions
from nortech.metadata.values.signal import (
    SignalDeviceInput,
    SignalDeviceInputDict,
    SignalInput,
    SignalInputDict,
    SignalListOutput,
    SignalOutput,
)
from nortech.metadata.values.unit import UnitInput, UnitInputDict, UnitListOutput, UnitOutput
from nortech.metadata.values.workspace import WorkspaceInput, WorkspaceInputDict, WorkspaceListOutput, WorkspaceOutput


class Metadata:
    """Client for interacting with the Nortech Metadata API.

    Attributes:
        workspace (Workspace): Client for interacting with the Nortech Metadata Workspace API.
        asset (Asset): Client for interacting with the Nortech Metadata Asset API.
        division (Division): Client for interacting with the Nortech Metadata Division API.
        unit (Unit): Client for interacting with the Nortech Metadata Unit API.
        device (Device): Client for interacting with the Nortech Metadata Device API.
        signal (Signal): Client for interacting with the Nortech Metadata Signal API.

    """

    def __init__(self, nortech_api: NortechAPI):
        self.workspace = Workspace(nortech_api)
        self.asset = Asset(nortech_api)
        self.division = Division(nortech_api)
        self.unit = Unit(nortech_api)
        self.device = Device(nortech_api)
        self.signal = Signal(nortech_api)


class Workspace:
    """Workspace."""

    def __init__(self, nortech_api: NortechAPI):
        self.nortech_api = nortech_api

    def get(
        self, workspace: int | str | WorkspaceInputDict | WorkspaceInput | WorkspaceOutput | WorkspaceListOutput
    ) -> WorkspaceOutput:
        """Get a workspace by ID or name.

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

        Example:
        ```python
        from nortech import Nortech
        from nortech.core.values.workspace import WorkspaceInput

        nortech = Nortech()

        # Get by ID
        workspace = nortech.metadata.workspace.get(123)

        # Get by name
        workspace = nortech.metadata.workspace.get("my-workspace")

        # Get by input dict
        workspace = nortech.metadata.workspace.get({"workspace": "my-workspace"})

        # Get by WorkspaceInput pydantic object
        workspace = nortech.metadata.workspace.get(WorkspaceInput(workspace="my-workspace"))

        print(workspace)
        # WorkspaceOutput(
        #     id=123,
        #     name="my-workspace",
        #     description="my-description",
        #     created_at=datetime.datetime(2024, 1, 1, 0, 0, 0, 0),
        #     updated_at=datetime.datetime(2024, 1, 1, 0, 0, 0, 0)
        # )

        ```

        """
        return workspace_service.get_workspace(self.nortech_api, workspace)

    def list(
        self, pagination_options: PaginationOptions[Literal["id", "name", "description"]] | None = None
    ) -> PaginatedResponse[WorkspaceListOutput]:
        """List all workspaces.

        Args:
            pagination_options (PaginationOptions, optional): Pagination settings.

        Returns:
            PaginatedResponse[WorkspaceListOutput]: A paginated list of workspaces.

        Example:
        ```python
        from nortech import Nortech
        from nortech.gateways.nortech_api import PaginationOptions

        nortech = Nortech()

        # List all workspaces
        workspaces = nortech.metadata.workspace.list()

        # List with pagination
        workspaces = nortech.metadata.workspace.list(PaginationOptions(size=10, sortBy="name"))

        print(workspaces)
        # PaginatedResponse(
        #     size=2,
        #     next=None,
        #     data=[
        #         WorkspaceListOutput(
        #             id=1,
        #             name="my-workspace",
        #             description="my-description"
        #         ),
        #         WorkspaceListOutput(
        #             id=2,
        #             name="my-workspace",
        #             description="my-description"
        #         )
        #     ]
        # )

        ```

        """
        return workspace_service.list_workspaces(self.nortech_api, pagination_options)


class Asset:
    def __init__(self, nortech_api: NortechAPI):
        self.nortech_api = nortech_api

    def get(self, asset: int | AssetInputDict | AssetInput | AssetOutput | AssetListOutput) -> AssetOutput:
        """Get an asset by ID or input.

        Args:
            asset (int | AssetInputDict | AssetInput | AssetOutput | AssetListOutput): The asset identifier, which can be:
                - *int*: The asset "ID".
                - [AssetInputDict](#assetinputdict): A dictionary representation of an asset input.
                - [AssetInput](#assetinput): A pydantic model representing an asset input.
                - [AssetOutput](#assetoutput): A pydantic model representing an asset output. Obtained from requesting an asset metadata.
                - [AssetListOutput](#assetlistoutput): A pydantic model representing a listed asset output. Obtained from requesting assets metadata.

        Returns:
            AssetOutput: The asset details.

        Example:
        ```python
        from nortech import Nortech
        from nortech.core.values.asset import AssetInput

        nortech = Nortech()

        # Get by ID
        asset = nortech.metadata.asset.get(123)

        # Get by input dict
        asset = nortech.metadata.asset.get({"workspace": "my-workspace", "asset": "my-asset"})

        # Get by AssetInput pydantic object
        asset = nortech.metadata.asset.get(AssetInput(workspace="my-workspace", asset="my-asset"))

        print(asset)
        # AssetOutput(
        #     id=123,
        #     name="my-asset",
        #     description="my-description",
        #     created_at=datetime.datetime(2024, 1, 1, 0, 0, 0, 0),
        #     updated_at=datetime.datetime(2024, 1, 1, 0, 0, 0, 0),
        #     workspace=MetadataOutput(
        #         id=123,
        #         name="my-workspace",
        #     )
        # )

        ```

        """
        return asset_service.get_workspace_asset(self.nortech_api, asset)

    def list(
        self,
        workspace: int | str | WorkspaceInputDict | WorkspaceInput | WorkspaceOutput | WorkspaceListOutput,
        pagination_options: PaginationOptions[Literal["id", "name", "description"]] | None = None,
    ) -> PaginatedResponse[AssetListOutput]:
        """List all assets in a workspace.

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

        Example:
        ```python
        from nortech import Nortech
        from nortech.gateways.nortech_api import PaginationOptions
        from nortech.core.values.workspace import WorkspaceInput

        nortech = Nortech()

        # List all assets in a workspace
        assets = nortech.metadata.asset.list(123)  # using workspace ID

        # List with pagination
        assets = nortech.metadata.asset.list(
            "my-workspace",  # using workspace name
            PaginationOptions(size=10, sortBy="name"),
        )

        # Using WorkspaceInputDict dictionary
        assets = nortech.metadata.asset.list({"workspace": "my-workspace"})

        # Using WorkspaceInput pydantic object
        assets = nortech.metadata.asset.list(WorkspaceInput(workspace="my-workspace"))

        print(assets)
        # PaginatedResponse(
        #     size=2,
        #     next=None,
        #     data=[
        #         AssetListOutput(
        #             id=1,
        #             name="my-asset",
        #             description="my-description"
        #         ),
        #         AssetListOutput(
        #             id=2,
        #             name="another-asset",
        #             description="another-description"
        #         )
        #     ]
        # )

        ```

        """
        return asset_service.list_workspace_assets(self.nortech_api, workspace, pagination_options)


class Division:
    def __init__(self, nortech_api: NortechAPI):
        self.nortech_api = nortech_api

    def get(
        self, division: int | DivisionInputDict | DivisionInput | DivisionOutput | DivisionListOutput
    ) -> DivisionOutput:
        """Get a division by ID or input.

        Args:
            division (int | DivisionInputDict | DivisionInput | DivisionOutput | DivisionListOutput): The division identifier, which can be:
                - *int*: The division "ID".
                - [DivisionInputDict](#divisioninputdict): A dictionary representation of a division input.
                - [DivisionInput](#divisioninput): A pydantic model representing a division input.
                - [DivisionOutput](#divisionoutput): A pydantic model representing a division output. Obtained from requesting a division metadata.
                - [DivisionListOutput](#divisionlistoutput): A pydantic model representing a listed division output. Obtained from requesting divisions metadata.

        Returns:
            DivisionOutput: The division details.

        Example:
        ```python
        from nortech import Nortech
        from nortech.core.values.division import DivisionInput

        nortech = Nortech()

        # Get by ID
        division = nortech.metadata.division.get(123)

        # Get by input dict
        division = nortech.metadata.division.get({"workspace": "my-workspace", "asset": "my-asset", "division": "my-division"})

        # Get by DivisionInput pydantic object
        division = nortech.metadata.division.get(
            DivisionInput(workspace="my-workspace", asset="my-asset", division="my-division")
        )

        print(division)
        # DivisionOutput(
        #     id=123,
        #     name="my-division",
        #     description="my-description",
        #     created_at=datetime.datetime(2024, 1, 1, 0, 0, 0, 0),
        #     updated_at=datetime.datetime(2024, 1, 1, 0, 0, 0, 0),
        #     workspace=MetadataOutput(
        #         id=123,
        #         name="my-workspace"
        #     ),
        #     asset=MetadataOutput(
        #         id=456,
        #         name="my-asset"
        #     )
        # )

        ```

        """
        return division_service.get_workspace_asset_division(self.nortech_api, division)

    def list(
        self,
        asset: int | AssetInputDict | AssetInput | AssetOutput | AssetListOutput,
        pagination_options: PaginationOptions[Literal["id", "name", "description"]] | None = None,
    ) -> PaginatedResponse[DivisionListOutput]:
        """List all divisions in an asset.

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

        Example:
        ```python
        from nortech import Nortech
        from nortech.gateways.nortech_api import PaginationOptions
        from nortech.core.values.asset import AssetInput

        nortech = Nortech()

        # List all divisions in an asset
        divisions = nortech.metadata.division.list(123)  # using asset ID

        # List with pagination
        divisions = nortech.metadata.division.list(
            {"workspace": "my-workspace", "asset": "my-asset"},  # using AssetInputDict
            PaginationOptions(size=10, sortBy="name"),
        )

        # Using AssetInput pydantic object
        divisions = nortech.metadata.division.list(AssetInput(workspace="my-workspace", asset="my-asset"))

        print(divisions)
        # PaginatedResponse(
        #     size=2,
        #     next=None,
        #     data=[
        #         DivisionListOutput(
        #             id=1,
        #             name="my-division",
        #             description="my-description"
        #         ),
        #         DivisionListOutput(
        #             id=2,
        #             name="another-division",
        #             description="another-description"
        #         )
        #     ]
        # )

        ```

        """
        return division_service.list_workspace_asset_divisions(self.nortech_api, asset, pagination_options)

    def list_by_workspace_id(
        self,
        workspace_id: int,
        pagination_options: PaginationOptions[Literal["id", "name", "description"]] | None = None,
    ) -> PaginatedResponse[DivisionListOutput]:
        """List all divisions in a workspace.

        Args:
            workspace_id (int): The workspace ID.
            pagination_options (PaginationOptions, optional): Pagination settings.

        Returns:
            PaginatedResponse[DivisionListOutput]: A paginated list of divisions.

        Example:
        ```python
        from nortech import Nortech
        from nortech.gateways.nortech_api import PaginationOptions

        nortech = Nortech()

        # List all divisions in a workspace
        divisions = nortech.metadata.division.list_by_workspace_id(123)

        # List with pagination
        divisions = nortech.metadata.division.list_by_workspace_id(123, PaginationOptions(size=10, sortBy="name"))

        print(divisions)
        # PaginatedResponse(
        #     size=2,
        #     next=None,
        #     data=[
        #         DivisionListOutput(
        #             id=1,
        #             name="my-division",
        #             description="my-description"
        #         ),
        #         DivisionListOutput(
        #             id=2,
        #             name="another-division",
        #             description="another-description"
        #         )
        #     ]
        # )

        ```

        """
        return division_service.list_workspace_divisions(self.nortech_api, workspace_id, pagination_options)


class Unit:
    def __init__(self, nortech_api: NortechAPI):
        self.nortech_api = nortech_api

    def get(self, unit: int | UnitInputDict | UnitInput | UnitOutput | UnitListOutput) -> UnitOutput:
        """Get a unit by ID or input.

        Args:
            unit (int | UnitInputDict | UnitInput | UnitOutput | UnitListOutput): The unit identifier, which can be:
                - *int*: The unit "ID".
                - [UnitInputDict](#unitinputdict): A dictionary representation of a unit input.
                - [UnitInput](#unitinput): A pydantic model representing a unit input.
                - [UnitOutput](#unitoutput): A pydantic model representing a unit output. Obtained from requesting a unit metadata.
                - [UnitListOutput](#unitlistoutput): A pydantic model representing a listed unit output. Obtained from requesting units metadata.

        Returns:
            UnitOutput: The unit details.

        Example:
        ```python
        from nortech import Nortech
        from nortech.core.values.unit import UnitInput

        nortech = Nortech()

        # Get by ID
        unit = nortech.metadata.unit.get(123)

        # Get by input dict
        unit = nortech.metadata.unit.get(
            {"workspace": "my-workspace", "asset": "my-asset", "division": "my-division", "unit": "my-unit"}
        )

        # Get by UnitInput pydantic object
        unit = nortech.metadata.unit.get(
            UnitInput(workspace="my-workspace", asset="my-asset", division="my-division", unit="my-unit")
        )

        print(unit)
        # UnitOutput(
        #     id=123,
        #     name="my-unit",
        #     created_at=datetime.datetime(2024, 1, 1, 0, 0, 0, 0),
        #     updated_at=datetime.datetime(2024, 1, 1, 0, 0, 0, 0),
        #     workspace=MetadataOutput(
        #         id=123,
        #         name="my-workspace"
        #     ),
        #     asset=MetadataOutput(
        #         id=456,
        #         name="my-asset"
        #     ),
        #     division=MetadataOutput(
        #         id=789,
        #         name="my-division"
        #     )
        # )

        ```

        """
        return unit_service.get_workspace_asset_division_unit(self.nortech_api, unit)

    def list(
        self,
        division: int | DivisionInputDict | DivisionInput | DivisionOutput | DivisionListOutput,
        pagination_options: PaginationOptions[Literal["id", "name"]] | None = None,
    ) -> PaginatedResponse[UnitListOutput]:
        """List all units in a division.

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

        Example:
        ```python
        from nortech import Nortech
        from nortech.gateways.nortech_api import PaginationOptions
        from nortech.core.values.division import DivisionInput

        nortech = Nortech()

        # List all units in a division
        units = nortech.metadata.unit.list(123)  # using division ID

        # List with pagination
        units = nortech.metadata.unit.list(
            {"workspace": "my-workspace", "asset": "my-asset", "division": "my-division"},  # using DivisionInputDict
            PaginationOptions(size=10, sortBy="name"),
        )

        # Using DivisionInput pydantic object
        units = nortech.metadata.unit.list(DivisionInput(workspace="my-workspace", asset="my-asset", division="my-division"))

        print(units)
        # PaginatedResponse(
        #     size=2,
        #     next=None,
        #     data=[
        #         UnitListOutput(
        #             id=1,
        #             name="my-unit"
        #         ),
        #         UnitListOutput(
        #             id=2,
        #             name="another-unit"
        #         )
        #     ]
        # )

        ```

        """
        return unit_service.list_workspace_asset_division_units(self.nortech_api, division, pagination_options)

    def list_by_workspace_id(
        self,
        workspace_id: int,
        pagination_options: PaginationOptions[Literal["id", "name"]] | None = None,
    ) -> PaginatedResponse[UnitListOutput]:
        """List all units in a workspace.

        Args:
            workspace_id (int): The workspace ID.
            pagination_options (PaginationOptions, optional): Pagination settings.

        Returns:
            PaginatedResponse[UnitListOutput]: A paginated list of units.

        Example:
        ```python
        from nortech import Nortech
        from nortech.gateways.nortech_api import PaginationOptions

        nortech = Nortech()

        # List all units in a workspace
        units = nortech.metadata.unit.list_by_workspace_id(123)

        # List with pagination
        units = nortech.metadata.unit.list_by_workspace_id(123, PaginationOptions(size=10, sortBy="name"))

        print(units)
        # PaginatedResponse(
        #     size=2,
        #     next=None,
        #     data=[
        #         UnitListOutput(
        #             id=1,
        #             name="my-unit"
        #         ),
        #         UnitListOutput(
        #             id=2,
        #             name="another-unit"
        #         )
        #     ]
        # )

        ```

        """
        return unit_service.list_workspace_units(self.nortech_api, workspace_id, pagination_options)

    def list_by_asset_id(
        self,
        asset_id: int,
        pagination_options: PaginationOptions[Literal["id", "name"]] | None = None,
    ) -> PaginatedResponse[UnitListOutput]:
        """List all units in an asset.

        Args:
            asset_id (int): The asset ID.
            pagination_options (PaginationOptions, optional): Pagination settings.

        Returns:
            PaginatedResponse[UnitListOutput]: A paginated list of units.

        Example:
        ```python
        from nortech import Nortech
        from nortech.gateways.nortech_api import PaginationOptions

        nortech = Nortech()

        # List all units in an asset
        units = nortech.metadata.unit.list_by_asset_id(123)

        # List with pagination
        units = nortech.metadata.unit.list_by_asset_id(123, PaginationOptions(size=10, sortBy="name"))

        print(units)
        # PaginatedResponse(
        #     size=2,
        #     next=None,
        #     data=[
        #         UnitListOutput(
        #             id=1,
        #             name="my-unit"
        #         ),
        #         UnitListOutput(
        #             id=2,
        #             name="another-unit"
        #         )
        #     ]
        # )
        ```

        """
        return unit_service.list_asset_units(self.nortech_api, asset_id, pagination_options)


class Device:
    def __init__(self, nortech_api: NortechAPI):
        self.nortech_api = nortech_api

    def get(self, device: int | DeviceInputDict | DeviceInput | DeviceOutput | DeviceListOutput) -> DeviceOutput:
        """Get a device by ID or input.

        Args:
            device (int | DeviceInputDict | DeviceInput | DeviceOutput | DeviceListOutput): The device identifier, which can be:
                - *int*: The device "ID".
                - [DeviceInputDict](#deviceinputdict): A dictionary representation of a device input.
                - [DeviceInput](#deviceinput): A pydantic model representing a device input.
                - [DeviceOutput](#deviceoutput): A pydantic model representing a device output. Obtained from requesting a device metadata.
                - [DeviceListOutput](#devicelistoutput): A pydantic model representing a listed device output. Obtained from requesting devices metadata.

        Returns:
            DeviceOutput: The device details.

        Example:
        ```python
        from nortech import Nortech
        from nortech.core.values.device import DeviceInput

        nortech = Nortech()

        # Get by ID
        device = nortech.metadata.device.get(123)

        # Get by input dict
        device = nortech.metadata.device.get(
            {"workspace": "my-workspace", "asset": "my-asset", "division": "my-division", "device": "my-device"}
        )

        # Get by DeviceInput pydantic object
        device = nortech.metadata.device.get(
            DeviceInput(workspace="my-workspace", asset="my-asset", division="my-division", device="my-device")
        )

        print(device)
        # DeviceOutput(
        #     id=123,
        #     name="my-device",
        #     type="my-type",
        #     onboarded=True,
        #     created_at=datetime.datetime(2024, 1, 1, 0, 0, 0, 0),
        #     updated_at=datetime.datetime(2024, 1, 1, 0, 0, 0, 0),
        #     workspace=MetadataOutput(
        #         id=123,
        #         name="my-workspace"
        #     ),
        #     asset=MetadataOutput(
        #         id=456,
        #         name="my-asset"
        #     ),
        #     division=MetadataOutput(
        #         id=789,
        #         name="my-division"
        #     )
        # )

        ```

        """
        return device_service.get_workspace_asset_division_device(self.nortech_api, device)

    def list(
        self,
        division: int | DivisionInputDict | DivisionInput | DivisionOutput | DivisionListOutput,
        pagination_options: PaginationOptions[Literal["id", "name", "type", "onboarded"]] | None = None,
    ) -> PaginatedResponse[DeviceListOutput]:
        """List all devices in a division.

        Args:
            division (int | DivisionInputDict | DivisionInput | DivisionOutput | DivisionListOutput): The division identifier, which can be:
                - *int*: The division "ID".
                - [DivisionInputDict](#divisioninputdict): A dictionary representation of a division input.
                - [DivisionInput](#divisioninput): A pydantic model representing a division input.
                - [DivisionOutput](#divisionoutput): A pydantic model representing a division output.
                - [DivisionListOutput](#divisionlistoutput): A pydantic model representing a listed division output.
            pagination_options (PaginationOptions, optional): Pagination settings.

        Returns:
            PaginatedResponse[DeviceListOutput]: A paginated list of devices.

        Example:
        ```python
        from nortech import Nortech
        from nortech.gateways.nortech_api import PaginationOptions
        from nortech.core.values.division import DivisionInput

        nortech = Nortech()

        # List all devices in a division
        devices = nortech.metadata.device.list(123)  # using division ID

        # List with pagination
        devices = nortech.metadata.device.list(
            {"workspace": "my-workspace", "asset": "my-asset", "division": "my-division"},  # using DivisionInputDict
            PaginationOptions(size=10, sortBy="name"),
        )

        # Using DivisionInput pydantic object
        devices = nortech.metadata.device.list(
            DivisionInput(workspace="my-workspace", asset="my-asset", division="my-division")
        )

        print(devices)
        # PaginatedResponse(
        #     size=2,
        #     next=None,
        #     data=[
        #         DeviceListOutput(
        #             id=1,
        #             name="my-device",
        #             type="my-type",
        #             onboarded=True
        #         ),
        #         DeviceListOutput(
        #             id=2,
        #             name="another-device",
        #             type="another-type",
        #             onboarded=False
        #         )
        #     ]
        # )

        ```

        """
        return device_service.list_workspace_asset_division_devices(self.nortech_api, division, pagination_options)

    def list_by_workspace_id(
        self,
        workspace_id: int,
        pagination_options: PaginationOptions[Literal["id", "name", "type", "onboarded"]] | None = None,
    ) -> PaginatedResponse[DeviceListOutput]:
        """List all devices in a workspace.

        Args:
            workspace_id (int): The workspace ID.
            pagination_options (PaginationOptions, optional): Pagination settings.

        Returns:
            PaginatedResponse[DeviceListOutput]: A paginated list of devices.

        Example:
        ```python
        from nortech import Nortech
        from nortech.gateways.nortech_api import PaginationOptions

        nortech = Nortech()

        # List all devices in a workspace
        devices = nortech.metadata.device.list_by_workspace_id(123)

        # List with pagination
        devices = nortech.metadata.device.list_by_workspace_id(123, PaginationOptions(size=10, sortBy="name"))

        print(devices)
        # PaginatedResponse(
        #     size=2,
        #     next=None,
        #     data=[
        #         DeviceListOutput(
        #             id=1,
        #             name="my-device",
        #             type="my-type",
        #             onboarded=True
        #         ),
        #         DeviceListOutput(
        #             id=2,
        #             name="another-device",
        #             type="another-type",
        #             onboarded=False
        #         )
        #     ]
        # )

        ```

        """
        return device_service.list_workspace_devices(self.nortech_api, workspace_id, pagination_options)

    def list_by_asset_id(
        self,
        asset_id: int,
        pagination_options: PaginationOptions[Literal["id", "name", "type", "onboarded"]] | None = None,
    ) -> PaginatedResponse[DeviceListOutput]:
        """List all devices in an asset.

        Args:
            asset_id (int): The asset ID.
            pagination_options (PaginationOptions, optional): Pagination settings.

        Returns:
            PaginatedResponse[DeviceListOutput]: A paginated list of devices.

        Example:
        ```python
        from nortech import Nortech
        from nortech.gateways.nortech_api import PaginationOptions

        nortech = Nortech()

        # List all devices in an asset
        devices = nortech.metadata.device.list_by_asset_id(123)

        # List with pagination
        devices = nortech.metadata.device.list_by_asset_id(123, PaginationOptions(size=10, sortBy="name"))

        print(devices)
        # PaginatedResponse(
        #     size=2,
        #     next=None,
        #     data=[
        #         DeviceListOutput(
        #             id=1,
        #             name="my-device",
        #             type="my-type",
        #             onboarded=True
        #         ),
        #         DeviceListOutput(
        #             id=2,
        #             name="another-device",
        #             type="another-type",
        #             onboarded=False
        #         )
        #     ]
        # )

        ```

        """
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
        """Get a signal by ID or input.

        Args:
            signal (int | SignalInputDict | SignalInput | SignalOutput | SignalListOutput | SignalDeviceInputDict | SignalDeviceInput): The signal identifier, which can be:
                - *int*: The signal "ID".
                - [SignalInputDict](#signalinputdict): A dictionary representation of a signal input.
                - [SignalInput](#signalinput): A pydantic model representing a signal input.
                - [SignalOutput](#signaloutput): A pydantic model representing a signal output. Obtained from requesting a signal metadata.
                - [SignalListOutput](#signallistoutput): A pydantic model representing a listed signal output. Obtained from requesting signals metadata.
                - [SignalDeviceInputDict](#signaldeviceinputdict): A dictionary representation of a device signal input.
                - [SignalDeviceInput](#signaldeviceinput): A pydantic model representing a device signal input.

        Returns:
            SignalOutput: The signal details.

        Example:
        ```python
        from nortech import Nortech
        from nortech.core.values.signal import SignalDeviceInput, SignalInput

        nortech = Nortech()

        # Get by ID
        signal = nortech.metadata.signal.get(123)

        # Get unit signal by input dict
        signal = nortech.metadata.signal.get(
            {
                "workspace": "my-workspace",
                "asset": "my-asset",
                "division": "my-division",
                "unit": "my-unit",
                "signal": "my-signal",
            }
        )

        # Get device signal by input dict
        signal = nortech.metadata.signal.get(
            {
                "workspace": "my-workspace",
                "asset": "my-asset",
                "division": "my-division",
                "device": "my-device",
                "signal": "my-signal",
            }
        )

        # Get by SignalInput pydantic object
        signal = nortech.metadata.signal.get(
            SignalInput(
                workspace="my-workspace", asset="my-asset", division="my-division", unit="my-unit", signal="my-signal"
            )
        )

        # Get by SignalDeviceInput pydantic object
        signal = nortech.metadata.signal.get(
        SignalDeviceInput(
                workspace="my-workspace", asset="my-asset", division="my-division", device="my-device", signal="my-signal"
            )
        )

        print(signal)
        # SignalOutput(
        #     id=123,
        #     name="my-signal",
        #     physical_unit="°C",
        #     data_type="float64",
        #     description="Temperature sensor",
        #     long_description="Main temperature sensor for the unit",
        #     created_at=datetime.datetime(2024, 1, 1, 0, 0, 0, 0),
        #     updated_at=datetime.datetime(2024, 1, 1, 0, 0, 0, 0),
        #     workspace=MetadataOutput(
        #         id=123,
        #         name="my-workspace"
        #     ),
        #     asset=MetadataOutput(
        #         id=456,
        #         name="my-asset"
        #     ),
        #     division=MetadataOutput(
        #         id=789,
        #         name="my-division"
        #     ),
        #     unit=MetadataOutput(
        #         id=101,
        #         name="my-unit"
        #     )
        #     device=MetadataOutput(
        #         id=101,
        #         name="my-device"
        #     )
        # )

        ```

        """
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
        unit_or_device: int | UnitInputDict | UnitInput | UnitOutput | DeviceInputDict | DeviceInput | DeviceOutput,
        pagination_options: PaginationOptions[
            Literal["id", "name", "physical_unit", "data_type", "description", "long_description"]
        ]
        | None = None,
    ) -> PaginatedResponse[SignalListOutput]:
        """List all signals in a unit or device.

        Args:
            unit_or_device (int | UnitInputDict | UnitInput | UnitOutput | DeviceInputDict | DeviceInput | DeviceOutput): The unit or device identifier, which can be:
                - *int*: The unit/device "ID".
                - [UnitInputDict](#unitinputdict): A dictionary representation of a unit input.
                - [UnitInput](#unitinput): A pydantic model representing a unit input.
                - [UnitOutput](#unitoutput): A pydantic model representing a unit output.
                - [DeviceInputDict](#deviceinputdict): A dictionary representation of a device input.
                - [DeviceInput](#deviceinput): A pydantic model representing a device input.
                - [DeviceOutput](#deviceoutput): A pydantic model representing a device output.
            pagination_options (PaginationOptions, optional): Pagination settings.

        Returns:
            PaginatedResponse[SignalListOutput]: A paginated list of signals.

        Example:
        ```python
        from nortech import Nortech
        from nortech.gateways.nortech_api import PaginationOptions
        from nortech.core.values.device import DeviceInput
        from nortech.core.values.unit import UnitInput

        nortech = Nortech()

        # List all signals in a unit
        signals = nortech.metadata.signal.list(123)  # using unit ID

        # List unit signals with pagination
        signals = nortech.metadata.signal.list(
            {"workspace": "my-workspace", "asset": "my-asset", "division": "my-division", "unit": "my-unit"},
            PaginationOptions(size=10, sortBy="name"),
        )

        # List device signals with pagination
        signals = nortech.metadata.signal.list(
            {"workspace": "my-workspace", "asset": "my-asset", "division": "my-division", "device": "my-device"},
            PaginationOptions(size=10, sortBy="name"),
        )

        # Using UnitInput pydantic object
        signals = nortech.metadata.signal.list(
            UnitInput(workspace="my-workspace", asset="my-asset", division="my-division", unit="my-unit")
        )

        # Using DeviceInput pydantic object
        signals = nortech.metadata.signal.list(
            DeviceInput(workspace="my-workspace", asset="my-asset", division="my-division", device="my-device")
        )

        print(signals)
        # PaginatedResponse(
        #     size=2,
        #     next=None,
        #     data=[
        #         SignalListOutput(
        #             id=1,
        #             name="my-signal",
        #             physical_unit="°C",
        #             data_type="float64",
        #             description="Temperature sensor",
        #             long_description="Main temperature sensor for the unit"
        #         ),
        #         SignalListOutput(
        #             id=2,
        #             name="another-signal",
        #             physical_unit="bar",
        #             data_type="float64",
        #             description="Pressure sensor",
        #             long_description="Main pressure sensor for the unit"
        #         )
        #     ]
        # )

        ```

        """
        if isinstance(unit_or_device, dict):
            if "device" in unit_or_device:
                unit_or_device = DeviceInput.model_validate(unit_or_device)
            else:
                unit_or_device = UnitInput.model_validate(unit_or_device)

        if isinstance(unit_or_device, DeviceInput) or isinstance(unit_or_device, DeviceOutput):
            return signal_service.list_workspace_asset_division_device_signals(
                self.nortech_api, unit_or_device, pagination_options
            )

        return signal_service.list_workspace_asset_division_unit_signals(
            self.nortech_api, unit_or_device, pagination_options
        )

    def list_by_workspace_id(
        self,
        workspace_id: int,
        pagination_options: PaginationOptions[
            Literal["id", "name", "physical_unit", "data_type", "description", "long_description"]
        ]
        | None = None,
    ) -> PaginatedResponse[SignalListOutput]:
        """List all signals in a workspace.

        Args:
            workspace_id (int): The workspace ID.
            pagination_options (PaginationOptions, optional): Pagination settings.

        Returns:
            PaginatedResponse[SignalListOutput]: A paginated list of signals.

        Example:
        ```python
        from nortech import Nortech
        from nortech.gateways.nortech_api import PaginationOptions

        nortech = Nortech()

        # List all signals in a workspace
        signals = nortech.metadata.signal.list_by_workspace_id(123)

        # List with pagination
        signals = nortech.metadata.signal.list_by_workspace_id(123, PaginationOptions(size=10, sortBy="name"))

        print(signals)
        # PaginatedResponse(
        #     size=2,
        #     next=None,
        #     data=[
        #         SignalListOutput(
        #             id=1,
        #             name="my-signal",
        #             physical_unit="°C",
        #             data_type="float64",
        #             description="Temperature sensor",
        #             long_description="Main temperature sensor for the unit"
        #         ),
        #         SignalListOutput(
        #             id=2,
        #             name="another-signal",
        #             physical_unit="bar",
        #             data_type="float64",
        #             description="Pressure sensor",
        #             long_description="Main pressure sensor for the unit"
        #         )
        #     ]
        # )

        ```

        """
        return signal_service.list_workspace_signals(self.nortech_api, workspace_id, pagination_options)

    def list_by_asset_id(
        self,
        asset_id: int,
        pagination_options: PaginationOptions[
            Literal["id", "name", "physical_unit", "data_type", "description", "long_description"]
        ]
        | None = None,
    ) -> PaginatedResponse[SignalListOutput]:
        """List all signals in an asset.

        Args:
            asset_id (int): The asset ID.
            pagination_options (PaginationOptions, optional): Pagination settings.

        Returns:
            PaginatedResponse[SignalListOutput]: A paginated list of signals.

        Example:
        ```python
        from nortech import Nortech
        from nortech.gateways.nortech_api import PaginationOptions

        nortech = Nortech()

        # List all signals in an asset
        signals = nortech.metadata.signal.list_by_asset_id(123)

        # List with pagination
        signals = nortech.metadata.signal.list_by_asset_id(123, PaginationOptions(size=10, sortBy="name"))

        print(signals)
        # PaginatedResponse(
        #     size=2,
        #     next=None,
        #     data=[
        #         SignalListOutput(
        #             id=1,
        #             name="my-signal",
        #             physical_unit="°C",
        #             data_type="float64",
        #             description="Temperature sensor",
        #             long_description="Main temperature sensor for the unit"
        #         ),
        #         SignalListOutput(
        #             id=2,
        #             name="another-signal",
        #             physical_unit="bar",
        #             data_type="float64",
        #             description="Pressure sensor",
        #             long_description="Main pressure sensor for the unit"
        #         )
        #     ]
        # )


        ```

        """
        return signal_service.list_asset_signals(self.nortech_api, asset_id, pagination_options)

    def list_by_division_id(
        self,
        division_id: int,
        pagination_options: PaginationOptions[
            Literal["id", "name", "physical_unit", "data_type", "description", "long_description"]
        ]
        | None = None,
    ) -> PaginatedResponse[SignalListOutput]:
        """List all signals in a division.

        Args:
            division_id (int): The division ID.
            pagination_options (PaginationOptions, optional): Pagination settings.

        Returns:
            PaginatedResponse[SignalListOutput]: A paginated list of signals.

        Example:
        ```python
        from nortech import Nortech
        from nortech.gateways.nortech_api import PaginationOptions

        nortech = Nortech()

        # List all signals in a division
        signals = nortech.metadata.signal.list_by_division_id(123)

        # List with pagination
        signals = nortech.metadata.signal.list_by_division_id(123, PaginationOptions(size=10, sortBy="name"))

        print(signals)
        # PaginatedResponse(
        #     size=2,
        #     next=None,
        #     data=[
        #         SignalListOutput(
        #             id=1,
        #             name="my-signal",
        #             physical_unit="°C",
        #             data_type="float64",
        #             description="Temperature sensor",
        #             long_description="Main temperature sensor for the unit"
        #         ),
        #         SignalListOutput(
        #             id=2,
        #             name="another-signal",
        #             physical_unit="bar",
        #             data_type="float64",
        #             description="Pressure sensor",
        #             long_description="Main pressure sensor for the unit"
        #         )
        #     ]
        # )


        ```

        """
        return signal_service.list_division_signals(self.nortech_api, division_id, pagination_options)


__all__ = ["MetadataOutput", "NextRef"]
