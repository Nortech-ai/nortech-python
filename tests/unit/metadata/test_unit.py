from requests_mock import Mocker

from nortech.common.gateways.nortech_api import NortechAPI, PaginatedResponse
from nortech.metadata.services.unit import (
    get_unit,
    get_workspace_asset_division_unit,
    list_asset_units,
    list_division_units,
    list_workspace_asset_division_units,
    list_workspace_units,
)
from nortech.metadata.values.division import DivisionInput
from nortech.metadata.values.unit import UnitInput, UnitListOutput, UnitOutput


def test_list_workspace_asset_division_units_from_input(
    nortech_api: NortechAPI,
    unit_list_output: UnitListOutput,
    paginated_unit_list_output: PaginatedResponse[UnitOutput],
    requests_mock: Mocker,
):
    requests_mock.get(
        f"{nortech_api.settings.URL}/api/v1/workspaces/test_workspace/assets/test_asset/divisions/test_division/units",
        text=paginated_unit_list_output.model_dump_json(by_alias=True),
    )

    divisions = list_workspace_asset_division_units(
        nortech_api,
        DivisionInput(workspace="test_workspace", asset="test_asset", division="test_division"),
    )
    assert divisions.data == [unit_list_output]


def test_list_workspace_asset_division_units_from_input_dict(
    nortech_api: NortechAPI,
    unit_list_output: UnitListOutput,
    paginated_unit_list_output: PaginatedResponse[UnitOutput],
    requests_mock: Mocker,
):
    requests_mock.get(
        f"{nortech_api.settings.URL}/api/v1/workspaces/test_workspace/assets/test_asset/divisions/test_division/units",
        text=paginated_unit_list_output.model_dump_json(by_alias=True),
    )

    divisions = list_workspace_asset_division_units(
        nortech_api,
        {"workspace": "test_workspace", "asset": "test_asset", "division": "test_division"},
    )
    assert divisions.data == [unit_list_output]


def test_get_workspace_asset_division_unit_404(
    nortech_api: NortechAPI,
    requests_mock: Mocker,
):
    requests_mock.get(
        f"{nortech_api.settings.URL}/api/v1/workspaces/test_workspace/assets/test_asset/divisions/test_division/units/test_unit",
        status_code=404,
    )

    division = get_workspace_asset_division_unit(
        nortech_api,
        UnitInput(
            workspace="test_workspace",
            asset="test_asset",
            division="test_division",
            unit="test_unit",
        ),
    )
    assert division is None


def test_get_workspace_asset_division_unit_with_input(
    nortech_api: NortechAPI,
    unit_output: UnitOutput,
    requests_mock,
):
    requests_mock.get(
        f"{nortech_api.settings.URL}/api/v1/workspaces/test_workspace/assets/test_asset/divisions/test_division/units/test_unit",
        text=unit_output.model_dump_json(by_alias=True),
    )

    division = get_workspace_asset_division_unit(
        nortech_api,
        UnitInput(
            workspace="test_workspace",
            asset="test_asset",
            division="test_division",
            unit="test_unit",
        ),
    )
    assert division == unit_output


def test_get_workspace_asset_division_unit_with_input_dict(
    nortech_api: NortechAPI,
    unit_output: UnitOutput,
    requests_mock,
):
    requests_mock.get(
        f"{nortech_api.settings.URL}/api/v1/workspaces/test_workspace/assets/test_asset/divisions/test_division/units/test_unit",
        text=unit_output.model_dump_json(by_alias=True),
    )

    division = get_workspace_asset_division_unit(
        nortech_api,
        {
            "workspace": "test_workspace",
            "asset": "test_asset",
            "division": "test_division",
            "unit": "test_unit",
        },
    )
    assert division == unit_output


def test_list_workspace_units(
    nortech_api: NortechAPI,
    unit_list_output: UnitListOutput,
    paginated_unit_list_output: PaginatedResponse[UnitOutput],
    requests_mock: Mocker,
):
    requests_mock.get(
        f"{nortech_api.settings.URL}/api/v1/workspaces/1/units",
        text=paginated_unit_list_output.model_dump_json(by_alias=True),
    )

    divisions = list_workspace_units(nortech_api, 1)
    assert divisions.data == [unit_list_output]


def test_list_asset_units(
    nortech_api: NortechAPI,
    unit_list_output: UnitListOutput,
    paginated_unit_list_output: PaginatedResponse[UnitOutput],
    requests_mock: Mocker,
):
    requests_mock.get(
        f"{nortech_api.settings.URL}/api/v1/assets/1/units",
        text=paginated_unit_list_output.model_dump_json(by_alias=True),
    )

    divisions = list_asset_units(nortech_api, 1)
    assert divisions.data == [unit_list_output]


def test_list_division_units(
    nortech_api: NortechAPI,
    unit_list_output: UnitListOutput,
    paginated_unit_list_output: PaginatedResponse[UnitOutput],
    requests_mock: Mocker,
):
    requests_mock.get(
        f"{nortech_api.settings.URL}/api/v1/divisions/1/units",
        text=paginated_unit_list_output.model_dump_json(by_alias=True),
    )

    divisions = list_division_units(nortech_api, 1)
    assert divisions.data == [unit_list_output]


def test_get_unit_404(
    nortech_api: NortechAPI,
    requests_mock,
):
    requests_mock.get(f"{nortech_api.settings.URL}/api/v1/units/1", status_code=404)
    division = get_unit(nortech_api, 1)
    assert division is None


def test_get_unit(
    nortech_api: NortechAPI,
    unit_output: UnitOutput,
    requests_mock,
):
    requests_mock.get(
        f"{nortech_api.settings.URL}/api/v1/units/1",
        text=unit_output.model_dump_json(by_alias=True),
    )

    division = get_unit(nortech_api, 1)
    assert division == unit_output
