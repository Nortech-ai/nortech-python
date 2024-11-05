from requests_mock import Mocker

from nortech import Nortech
from nortech.core import (
    DivisionInput,
    PaginatedResponse,
    UnitInput,
    UnitListOutput,
    UnitOutput,
)


def test_list_workspace_asset_division_units_from_input(
    nortech: Nortech,
    unit_list_output: UnitListOutput,
    paginated_unit_list_output: PaginatedResponse[UnitOutput],
    requests_mock: Mocker,
):
    requests_mock.get(
        f"{nortech.settings.URL}/api/v1/workspaces/test_workspace/assets/test_asset/divisions/test_division/units",
        text=paginated_unit_list_output.model_dump_json(by_alias=True),
    )

    divisions = nortech.metadata.unit.list(
        DivisionInput(workspace="test_workspace", asset="test_asset", division="test_division"),
    )
    assert divisions.data == [unit_list_output]


def test_list_workspace_asset_division_units_from_input_dict(
    nortech: Nortech,
    unit_list_output: UnitListOutput,
    paginated_unit_list_output: PaginatedResponse[UnitOutput],
    requests_mock: Mocker,
):
    requests_mock.get(
        f"{nortech.settings.URL}/api/v1/workspaces/test_workspace/assets/test_asset/divisions/test_division/units",
        text=paginated_unit_list_output.model_dump_json(by_alias=True),
    )

    divisions = nortech.metadata.unit.list(
        {"workspace": "test_workspace", "asset": "test_asset", "division": "test_division"},
    )
    assert divisions.data == [unit_list_output]


def test_get_workspace_asset_division_unit_404(
    nortech: Nortech,
    requests_mock: Mocker,
):
    requests_mock.get(
        f"{nortech.settings.URL}/api/v1/workspaces/test_workspace/assets/test_asset/divisions/test_division/units/test_unit",
        status_code=404,
    )

    division = nortech.metadata.unit.get(
        UnitInput(
            workspace="test_workspace",
            asset="test_asset",
            division="test_division",
            unit="test_unit",
        ),
    )
    assert division is None


def test_get_workspace_asset_division_unit_with_input(
    nortech: Nortech,
    unit_output: UnitOutput,
    requests_mock,
):
    requests_mock.get(
        f"{nortech.settings.URL}/api/v1/workspaces/test_workspace/assets/test_asset/divisions/test_division/units/test_unit",
        text=unit_output.model_dump_json(by_alias=True),
    )

    division = nortech.metadata.unit.get(
        UnitInput(
            workspace="test_workspace",
            asset="test_asset",
            division="test_division",
            unit="test_unit",
        ),
    )
    assert division == unit_output


def test_get_workspace_asset_division_unit_with_input_dict(
    nortech: Nortech,
    unit_output: UnitOutput,
    requests_mock,
):
    requests_mock.get(
        f"{nortech.settings.URL}/api/v1/workspaces/test_workspace/assets/test_asset/divisions/test_division/units/test_unit",
        text=unit_output.model_dump_json(by_alias=True),
    )

    division = nortech.metadata.unit.get(
        {
            "workspace": "test_workspace",
            "asset": "test_asset",
            "division": "test_division",
            "unit": "test_unit",
        },
    )
    assert division == unit_output


def test_list_workspace_units(
    nortech: Nortech,
    unit_list_output: UnitListOutput,
    paginated_unit_list_output: PaginatedResponse[UnitOutput],
    requests_mock: Mocker,
):
    requests_mock.get(
        f"{nortech.settings.URL}/api/v1/workspaces/1/units",
        text=paginated_unit_list_output.model_dump_json(by_alias=True),
    )

    divisions = nortech.metadata.unit.list_by_workspace_id(1)
    assert divisions.data == [unit_list_output]


def test_list_asset_units(
    nortech: Nortech,
    unit_list_output: UnitListOutput,
    paginated_unit_list_output: PaginatedResponse[UnitOutput],
    requests_mock: Mocker,
):
    requests_mock.get(
        f"{nortech.settings.URL}/api/v1/assets/1/units",
        text=paginated_unit_list_output.model_dump_json(by_alias=True),
    )

    divisions = nortech.metadata.unit.list_by_asset_id(1)
    assert divisions.data == [unit_list_output]


def test_list_division_units(
    nortech: Nortech,
    unit_list_output: UnitListOutput,
    paginated_unit_list_output: PaginatedResponse[UnitOutput],
    requests_mock: Mocker,
):
    requests_mock.get(
        f"{nortech.settings.URL}/api/v1/divisions/1/units",
        text=paginated_unit_list_output.model_dump_json(by_alias=True),
    )

    divisions = nortech.metadata.unit.list(1)
    assert divisions.data == [unit_list_output]


def test_get_unit_404(
    nortech: Nortech,
    requests_mock,
):
    requests_mock.get(f"{nortech.settings.URL}/api/v1/units/1", status_code=404)
    division = nortech.metadata.unit.get(1)
    assert division is None


def test_get_unit(
    nortech: Nortech,
    unit_output: UnitOutput,
    requests_mock,
):
    requests_mock.get(
        f"{nortech.settings.URL}/api/v1/units/1",
        text=unit_output.model_dump_json(by_alias=True),
    )

    division = nortech.metadata.unit.get(1)
    assert division == unit_output
