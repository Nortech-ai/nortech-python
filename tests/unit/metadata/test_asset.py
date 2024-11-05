from requests_mock import Mocker

from nortech import Nortech
from nortech.core import AssetInput, AssetListOutput, AssetOutput, PaginatedResponse, WorkspaceInput


def test_list_workspace_assets_from_id(
    nortech: Nortech,
    asset_list_output: AssetListOutput,
    paginated_asset_list_output: PaginatedResponse[AssetListOutput],
    requests_mock: Mocker,
):
    requests_mock.get(
        f"{nortech.settings.URL}/api/v1/workspaces/1/assets",
        text=paginated_asset_list_output.model_dump_json(by_alias=True),
    )

    assets = nortech.metadata.asset.list(workspace=1)
    assert assets.data == [asset_list_output]


def test_list_workspace_assets_from_name(
    nortech: Nortech,
    asset_list_output: AssetListOutput,
    paginated_asset_list_output: PaginatedResponse[AssetListOutput],
    requests_mock: Mocker,
):
    requests_mock.get(
        f"{nortech.settings.URL}/api/v1/workspaces/test_workspace/assets",
        text=paginated_asset_list_output.model_dump_json(by_alias=True),
    )

    assets = nortech.metadata.asset.list(workspace="test_workspace")
    assert assets.data == [asset_list_output]


def test_list_workspace_assets_from_input(
    nortech: Nortech,
    asset_list_output: AssetListOutput,
    paginated_asset_list_output: PaginatedResponse[AssetListOutput],
    requests_mock: Mocker,
):
    requests_mock.get(
        f"{nortech.settings.URL}/api/v1/workspaces/test_workspace/assets",
        text=paginated_asset_list_output.model_dump_json(by_alias=True),
    )

    assets = nortech.metadata.asset.list(workspace=WorkspaceInput(workspace="test_workspace"))
    assert assets.data == [asset_list_output]


def test_list_workspace_assets_from_input_dict(
    nortech: Nortech,
    asset_list_output: AssetListOutput,
    paginated_asset_list_output: PaginatedResponse[AssetListOutput],
    requests_mock: Mocker,
):
    requests_mock.get(
        f"{nortech.settings.URL}/api/v1/workspaces/test_workspace/assets",
        text=paginated_asset_list_output.model_dump_json(by_alias=True),
    )

    assets = nortech.metadata.asset.list(workspace={"workspace": "test_workspace"})
    assert assets.data == [asset_list_output]


def test_get_workspace_asset_404(
    nortech: Nortech,
    asset_output: AssetOutput,
    requests_mock: Mocker,
):
    requests_mock.get(
        f"{nortech.settings.URL}/api/v1/workspaces/test_workspace/assets/test_asset",
        status_code=404,
    )

    asset = nortech.metadata.asset.get(asset=AssetInput(workspace="test_workspace", asset="test_asset"))
    assert asset is None


def test_get_workspace_asset_with_input(
    nortech: Nortech,
    asset_output: AssetOutput,
    requests_mock,
):
    requests_mock.get(
        f"{nortech.settings.URL}/api/v1/workspaces/test_workspace/assets/test_asset",
        text=asset_output.model_dump_json(by_alias=True),
    )

    asset = nortech.metadata.asset.get(asset=AssetInput(workspace="test_workspace", asset="test_asset"))
    assert asset == asset_output


def test_get_workspace_asset_with_input_dict(
    nortech: Nortech,
    asset_output: AssetOutput,
    requests_mock,
):
    requests_mock.get(
        f"{nortech.settings.URL}/api/v1/workspaces/test_workspace/assets/test_asset",
        text=asset_output.model_dump_json(by_alias=True),
    )

    asset = nortech.metadata.asset.get(asset={"workspace": "test_workspace", "asset": "test_asset"})
    assert asset == asset_output


def test_get_asset_404(
    nortech: Nortech,
    requests_mock,
):
    requests_mock.get(f"{nortech.settings.URL}/api/v1/assets/1", status_code=404)

    asset = nortech.metadata.asset.get(asset=1)
    assert asset is None


def test_get_asset(
    nortech: Nortech,
    asset_output: AssetOutput,
    requests_mock,
):
    requests_mock.get(
        f"{nortech.settings.URL}/api/v1/assets/1",
        text=asset_output.model_dump_json(by_alias=True),
    )

    asset = nortech.metadata.asset.get(asset=1)
    assert asset == asset_output