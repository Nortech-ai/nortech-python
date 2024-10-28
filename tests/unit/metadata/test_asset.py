from requests_mock import Mocker

from nortech.common.gateways.nortech_api import NortechAPI, PaginatedResponse
from nortech.metadata.services.asset import get_asset, get_workspace_asset, list_workspace_assets
from nortech.metadata.values.asset import AssetInput, AssetListOutput, AssetOutput
from nortech.metadata.values.workspace import WorkspaceInput


def test_list_workspace_assets_from_id(
    nortech_api: NortechAPI,
    asset_list_output: AssetListOutput,
    paginated_asset_list_output: PaginatedResponse[AssetListOutput],
    requests_mock: Mocker,
):
    requests_mock.get(
        f"{nortech_api.settings.URL}/api/v1/workspaces/1/assets",
        text=paginated_asset_list_output.model_dump_json(by_alias=True),
    )

    assets = list_workspace_assets(nortech_api, 1)
    assert assets.data == [asset_list_output]


def test_list_workspace_assets_from_name(
    nortech_api: NortechAPI,
    asset_list_output: AssetListOutput,
    paginated_asset_list_output: PaginatedResponse[AssetListOutput],
    requests_mock: Mocker,
):
    requests_mock.get(
        f"{nortech_api.settings.URL}/api/v1/workspaces/test_workspace/assets",
        text=paginated_asset_list_output.model_dump_json(by_alias=True),
    )

    assets = list_workspace_assets(nortech_api, "test_workspace")
    assert assets.data == [asset_list_output]


def test_list_workspace_assets_from_input(
    nortech_api: NortechAPI,
    asset_list_output: AssetListOutput,
    paginated_asset_list_output: PaginatedResponse[AssetListOutput],
    requests_mock: Mocker,
):
    requests_mock.get(
        f"{nortech_api.settings.URL}/api/v1/workspaces/test_workspace/assets",
        text=paginated_asset_list_output.model_dump_json(by_alias=True),
    )

    assets = list_workspace_assets(nortech_api, WorkspaceInput(workspace="test_workspace"))
    assert assets.data == [asset_list_output]


def test_list_workspace_assets_from_input_dict(
    nortech_api: NortechAPI,
    asset_list_output: AssetListOutput,
    paginated_asset_list_output: PaginatedResponse[AssetListOutput],
    requests_mock: Mocker,
):
    requests_mock.get(
        f"{nortech_api.settings.URL}/api/v1/workspaces/test_workspace/assets",
        text=paginated_asset_list_output.model_dump_json(by_alias=True),
    )

    assets = list_workspace_assets(nortech_api, {"workspace": "test_workspace"})
    assert assets.data == [asset_list_output]


def test_get_workspace_asset_404(
    nortech_api: NortechAPI,
    asset_output: AssetOutput,
    requests_mock: Mocker,
):
    requests_mock.get(
        f"{nortech_api.settings.URL}/api/v1/workspaces/test_workspace/assets/test_asset",
        status_code=404,
    )

    asset = get_workspace_asset(nortech_api, AssetInput(workspace="test_workspace", asset="test_asset"))
    assert asset is None


def test_get_workspace_asset_with_input(
    nortech_api: NortechAPI,
    asset_output: AssetOutput,
    requests_mock,
):
    requests_mock.get(
        f"{nortech_api.settings.URL}/api/v1/workspaces/test_workspace/assets/test_asset",
        text=asset_output.model_dump_json(by_alias=True),
    )

    asset = get_workspace_asset(nortech_api, AssetInput(workspace="test_workspace", asset="test_asset"))
    assert asset == asset_output


def test_get_workspace_asset_with_input_dict(
    nortech_api: NortechAPI,
    asset_output: AssetOutput,
    requests_mock,
):
    requests_mock.get(
        f"{nortech_api.settings.URL}/api/v1/workspaces/test_workspace/assets/test_asset",
        text=asset_output.model_dump_json(by_alias=True),
    )

    asset = get_workspace_asset(nortech_api, {"workspace": "test_workspace", "asset": "test_asset"})
    assert asset == asset_output


def test_get_asset_404(
    nortech_api: NortechAPI,
    requests_mock,
):
    requests_mock.get(f"{nortech_api.settings.URL}/api/v1/assets/1", status_code=404)

    asset = get_asset(nortech_api, 1)
    assert asset is None


def test_get_asset(
    nortech_api: NortechAPI,
    asset_output: AssetOutput,
    requests_mock,
):
    requests_mock.get(
        f"{nortech_api.settings.URL}/api/v1/assets/1",
        text=asset_output.model_dump_json(by_alias=True),
    )

    asset = get_asset(nortech_api, 1)
    assert asset == asset_output
