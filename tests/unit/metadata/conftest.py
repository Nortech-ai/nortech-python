from datetime import datetime

import pytest

from nortech.metadata import (
    AssetInput,
    AssetInputDict,
    AssetListOutput,
    AssetOutput,
    DeviceInput,
    DeviceInputDict,
    DeviceListOutput,
    DeviceOutput,
    DivisionInput,
    DivisionInputDict,
    DivisionListOutput,
    DivisionOutput,
    MetadataOutput,
    NextRef,
    PaginatedResponse,
    SignalInput,
    SignalInputDict,
    SignalListOutput,
    SignalOutput,
    UnitInput,
    UnitInputDict,
    UnitListOutput,
    UnitOutput,
    WorkspaceInput,
    WorkspaceInputDict,
    WorkspaceListOutput,
    WorkspaceOutput,
)


@pytest.fixture(scope="session", name="workspace_input")
def workspace_input_fixture() -> WorkspaceInput:
    return WorkspaceInput(workspace="test_workspace")


@pytest.fixture(scope="session", name="workspace_input_dict")
def workspace_input_dict_fixture() -> WorkspaceInputDict:
    return {"workspace": "test_workspace"}


@pytest.fixture(scope="session", name="workspace_list_output")
def workspace_list_output_fixture() -> list[WorkspaceListOutput]:
    return [
        WorkspaceListOutput(id=1, name="test_workspace", description="test_description"),
        WorkspaceListOutput(id=2, name="test_workspace_2", description="test_description_2"),
        WorkspaceListOutput(id=3, name="test_workspace_3", description="test_description_3"),
        WorkspaceListOutput(id=4, name="test_workspace_4", description="test_description_4"),
    ]


@pytest.fixture(scope="session", name="paginated_workspace_list_output")
def paginated_workspace_list_output_fixture(
    workspace_list_output: list[WorkspaceListOutput],
) -> PaginatedResponse[WorkspaceListOutput]:
    return PaginatedResponse[WorkspaceListOutput](
        size=len(workspace_list_output),
        data=workspace_list_output,
        next=None,
    )


@pytest.fixture(scope="session", name="paginated_workspace_list_output_first_page")
def paginated_workspace_list_output_first_page_fixture(
    workspace_list_output: list[WorkspaceListOutput],
) -> PaginatedResponse[WorkspaceListOutput]:
    return PaginatedResponse[WorkspaceListOutput](
        size=2,
        data=workspace_list_output[:2],
        next=NextRef(token="test_token"),  # noqa: S106
    )


@pytest.fixture(scope="session", name="paginated_workspace_list_output_second_page")
def paginated_workspace_list_output_second_page_fixture(
    workspace_list_output: list[WorkspaceListOutput],
) -> PaginatedResponse[WorkspaceListOutput]:
    return PaginatedResponse[WorkspaceListOutput](
        size=2,
        data=workspace_list_output[2:],
        next=None,
    )


@pytest.fixture(scope="session", name="workspace_output")
def workspace_output_fixture() -> WorkspaceOutput:
    return WorkspaceOutput(
        id=1,
        name="test_workspace",
        description="test_description",
        created_at=datetime.now(),  # type: ignore
        updated_at=datetime.now(),  # type: ignore
    )


@pytest.fixture(scope="session", name="asset_input")
def asset_input_fixture() -> AssetInput:
    return AssetInput(asset="test_asset", workspace="test_workspace")


@pytest.fixture(scope="session", name="asset_input_dict")
def asset_input_dict_fixture() -> AssetInputDict:
    return {"asset": "test_asset", "workspace": "test_workspace"}


@pytest.fixture(scope="session", name="asset_list_output")
def asset_list_output_fixture() -> AssetListOutput:
    return AssetListOutput(id=1, name="test_asset", description="test_description")


@pytest.fixture(scope="session", name="paginated_asset_list_output")
def paginated_asset_list_output_fixture(
    asset_list_output: AssetListOutput,
) -> PaginatedResponse[AssetListOutput]:
    return PaginatedResponse[AssetListOutput](
        size=1,
        data=[asset_list_output],
        next=None,
    )


@pytest.fixture(scope="session", name="asset_output")
def asset_output_fixture() -> AssetOutput:
    return AssetOutput(
        id=1,
        name="test_asset",
        description="test_description",
        workspace=MetadataOutput(id=1, name="test_workspace"),
        created_at=datetime.now(),  # type: ignore
        updated_at=datetime.now(),  # type: ignore
    )


@pytest.fixture(scope="session", name="division_input")
def division_input_fixture() -> DivisionInput:
    return DivisionInput(division="test_division", asset="test_asset", workspace="test_workspace")


@pytest.fixture(scope="session", name="division_input_dict")
def division_input_dict_fixture() -> DivisionInputDict:
    return {"division": "test_division", "asset": "test_asset", "workspace": "test_workspace"}


@pytest.fixture(scope="session", name="division_list_output")
def division_list_output_fixture() -> DivisionListOutput:
    return DivisionListOutput(id=1, name="test_division", description="test_description")


@pytest.fixture(scope="session", name="paginated_division_list_output")
def paginated_division_list_output_fixture(
    division_list_output: DivisionListOutput,
) -> PaginatedResponse[DivisionListOutput]:
    return PaginatedResponse[DivisionListOutput](
        size=1,
        data=[division_list_output],
        next=None,
    )


@pytest.fixture(scope="session", name="division_output")
def division_output_fixture() -> DivisionOutput:
    return DivisionOutput(
        id=1,
        name="test_division",
        description="test_description",
        workspace=MetadataOutput(id=1, name="test_workspace"),
        asset=MetadataOutput(id=1, name="test_asset"),
        created_at=datetime.now(),  # type: ignore
        updated_at=datetime.now(),  # type: ignore
    )


@pytest.fixture(scope="session", name="unit_input")
def unit_input_fixture() -> UnitInput:
    return UnitInput(unit="test_unit", division="test_division", asset="test_asset", workspace="test_workspace")


@pytest.fixture(scope="session", name="unit_input_dict")
def unit_input_dict_fixture() -> UnitInputDict:
    return {
        "unit": "test_unit",
        "division": "test_division",
        "asset": "test_asset",
        "workspace": "test_workspace",
    }


@pytest.fixture(scope="session", name="unit_list_output")
def unit_list_output_fixture() -> UnitListOutput:
    return UnitListOutput(id=1, name="test_unit")


@pytest.fixture(scope="session", name="paginated_unit_list_output")
def paginated_unit_list_output_fixture(
    unit_list_output: UnitListOutput,
) -> PaginatedResponse[UnitListOutput]:
    return PaginatedResponse[UnitListOutput](
        size=1,
        data=[unit_list_output],
        next=None,
    )


@pytest.fixture(scope="session", name="unit_output")
def unit_output_fixture() -> UnitOutput:
    return UnitOutput(
        id=1,
        name="test_unit",
        workspace=MetadataOutput(id=1, name="test_workspace"),
        asset=MetadataOutput(id=1, name="test_asset"),
        division=MetadataOutput(id=1, name="test_division"),
        created_at=datetime.now(),  # type: ignore
        updated_at=datetime.now(),  # type: ignore
    )


@pytest.fixture(scope="session", name="device_input")
def device_input_fixture() -> DeviceInput:
    return DeviceInput(
        device="test_device",
        division="test_division",
        asset="test_asset",
        workspace="test_workspace",
    )


@pytest.fixture(scope="session", name="device_input_dict")
def device_input_dict_fixture() -> DeviceInputDict:
    return {
        "device": "test_device",
        "division": "test_division",
        "asset": "test_asset",
        "workspace": "test_workspace",
    }


@pytest.fixture(scope="session", name="device_list_output")
def device_list_output_fixture() -> DeviceListOutput:
    return DeviceListOutput(id=1, name="test_device", type="test_type", onboarded=True)


@pytest.fixture(scope="session", name="paginated_device_list_output")
def paginated_device_list_output_fixture(
    device_list_output: DeviceListOutput,
) -> PaginatedResponse[DeviceListOutput]:
    return PaginatedResponse[DeviceListOutput](
        size=1,
        data=[device_list_output],
        next=None,
    )


@pytest.fixture(scope="session", name="device_output")
def device_output_fixture() -> DeviceOutput:
    return DeviceOutput(
        id=1,
        name="test_device",
        type="test_type",
        onboarded=True,
        workspace=MetadataOutput(id=1, name="test_workspace"),
        asset=MetadataOutput(id=1, name="test_asset"),
        division=MetadataOutput(id=1, name="test_division"),
        created_at=datetime.now(),  # type: ignore
        updated_at=datetime.now(),  # type: ignore
    )


@pytest.fixture(scope="session", name="signal_input")
def signal_input_fixture() -> SignalInput:
    return SignalInput(
        signal="test_signal",
        unit="test_unit",
        asset="test_asset",
        division="test_division",
        workspace="test_workspace",
    )


@pytest.fixture(scope="session", name="signal_input_dict")
def signal_input_dict_fixture() -> SignalInputDict:
    return {
        "signal": "test_signal",
        "unit": "test_unit",
        "asset": "test_asset",
        "division": "test_division",
        "workspace": "test_workspace",
    }


@pytest.fixture(scope="session", name="signal_list_output")
def signal_list_output_fixture() -> SignalListOutput:
    return SignalListOutput(
        id=1,
        name="test_signal",
        description="test_description",
        physicalUnit="test_physical_unit",
        dataType="float",
        longDescription="test_long_description",
    )


@pytest.fixture(scope="session", name="paginated_signal_list_output")
def paginated_signal_list_output_fixture(
    signal_list_output: SignalListOutput,
) -> PaginatedResponse[SignalListOutput]:
    return PaginatedResponse[SignalListOutput](
        size=1,
        data=[signal_list_output],
        next=None,
    )


@pytest.fixture(scope="session", name="signal_output")
def signal_output_fixture() -> SignalOutput:
    return SignalOutput(
        id=1,
        name="test_signal",
        description="test_description",
        physicalUnit="test_physical_unit",
        dataType="float",
        longDescription="test_long_description",
        workspace=MetadataOutput(id=1, name="test_workspace"),
        asset=MetadataOutput(id=1, name="test_asset"),
        division=MetadataOutput(id=1, name="test_division"),
        unit=MetadataOutput(id=1, name="test_unit"),
        device=MetadataOutput(id=1, name="test_device"),
        createdAt=datetime.now(),
        updatedAt=datetime.now(),
    )
