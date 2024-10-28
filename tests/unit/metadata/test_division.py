from requests_mock import Mocker

from nortech.common.gateways.nortech_api import NortechAPI, PaginatedResponse
from nortech.metadata.services.division import (
    get_division,
    get_workspace_asset_division,
    list_asset_divisions,
    list_workspace_asset_divisions,
    list_workspace_divisions,
)
from nortech.metadata.values.asset import AssetInput
from nortech.metadata.values.division import DivisionInput, DivisionListOutput, DivisionOutput


def test_list_workspace_asset_divisions_from_input(
    nortech_api: NortechAPI,
    division_list_output: DivisionListOutput,
    paginated_division_list_output: PaginatedResponse[DivisionOutput],
    requests_mock: Mocker,
):
    requests_mock.get(
        f"{nortech_api.settings.URL}/api/v1/workspaces/test_workspace/assets/test_asset/divisions",
        text=paginated_division_list_output.model_dump_json(by_alias=True),
    )

    divisions = list_workspace_asset_divisions(nortech_api, AssetInput(workspace="test_workspace", asset="test_asset"))
    assert divisions.data == [division_list_output]


def test_list_workspace_asset_divisions_from_input_dict(
    nortech_api: NortechAPI,
    division_list_output: DivisionListOutput,
    paginated_division_list_output: PaginatedResponse[DivisionOutput],
    requests_mock: Mocker,
):
    requests_mock.get(
        f"{nortech_api.settings.URL}/api/v1/workspaces/test_workspace/assets/test_asset/divisions",
        text=paginated_division_list_output.model_dump_json(by_alias=True),
    )

    divisions = list_workspace_asset_divisions(nortech_api, {"workspace": "test_workspace", "asset": "test_asset"})
    assert divisions.data == [division_list_output]


def test_get_workspace_asset_division_404(
    nortech_api: NortechAPI,
    division_output: DivisionOutput,
    requests_mock: Mocker,
):
    requests_mock.get(
        f"{nortech_api.settings.URL}/api/v1/workspaces/test_workspace/assets/test_asset/divisions/test_division",
        status_code=404,
    )

    division = get_workspace_asset_division(
        nortech_api,
        DivisionInput(workspace="test_workspace", asset="test_asset", division="test_division"),
    )
    assert division is None


def test_get_workspace_asset_division_with_input(
    nortech_api: NortechAPI,
    division_output: DivisionOutput,
    requests_mock,
):
    requests_mock.get(
        f"{nortech_api.settings.URL}/api/v1/workspaces/test_workspace/assets/test_asset/divisions/test_division",
        text=division_output.model_dump_json(by_alias=True),
    )

    division = get_workspace_asset_division(
        nortech_api,
        DivisionInput(workspace="test_workspace", asset="test_asset", division="test_division"),
    )
    assert division == division_output


def test_get_workspace_asset_division_with_input_dict(
    nortech_api: NortechAPI,
    division_output: DivisionOutput,
    requests_mock,
):
    requests_mock.get(
        f"{nortech_api.settings.URL}/api/v1/workspaces/test_workspace/assets/test_asset/divisions/test_division",
        text=division_output.model_dump_json(by_alias=True),
    )

    division = get_workspace_asset_division(
        nortech_api,
        {"workspace": "test_workspace", "asset": "test_asset", "division": "test_division"},
    )
    assert division == division_output


def test_list_workspace_divisions(
    nortech_api: NortechAPI,
    division_list_output: DivisionListOutput,
    paginated_division_list_output: PaginatedResponse[DivisionOutput],
    requests_mock: Mocker,
):
    requests_mock.get(
        f"{nortech_api.settings.URL}/api/v1/workspaces/1/divisions",
        text=paginated_division_list_output.model_dump_json(by_alias=True),
    )

    divisions = list_workspace_divisions(nortech_api, 1)
    assert divisions.data == [division_list_output]


def test_list_asset_divisions(
    nortech_api: NortechAPI,
    division_list_output: DivisionListOutput,
    paginated_division_list_output: PaginatedResponse[DivisionOutput],
    requests_mock: Mocker,
):
    requests_mock.get(
        f"{nortech_api.settings.URL}/api/v1/assets/1/divisions",
        text=paginated_division_list_output.model_dump_json(by_alias=True),
    )

    divisions = list_asset_divisions(nortech_api, 1)
    assert divisions.data == [division_list_output]


def test_get_division_404(
    nortech_api: NortechAPI,
    requests_mock,
):
    requests_mock.get(f"{nortech_api.settings.URL}/api/v1/divisions/1", status_code=404)
    division = get_division(nortech_api, 1)
    assert division is None


def test_get_division(
    nortech_api: NortechAPI,
    division_output: DivisionOutput,
    requests_mock,
):
    requests_mock.get(
        f"{nortech_api.settings.URL}/api/v1/divisions/1",
        text=division_output.model_dump_json(by_alias=True),
    )

    division = get_division(nortech_api, 1)
    assert division == division_output
