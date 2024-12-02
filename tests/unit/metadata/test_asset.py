import pytest
from requests_mock import Mocker

from nortech import Nortech
from nortech.metadata import AssetInput, AssetListOutput, AssetOutput, PaginatedResponse, WorkspaceInput
from nortech.metadata.values.workspace import WorkspaceListOutput, WorkspaceOutput


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


def test_list_workspace_assets_from_output(
    nortech: Nortech,
    workspace_output: WorkspaceOutput,
    asset_list_output: AssetListOutput,
    paginated_asset_list_output: PaginatedResponse[AssetListOutput],
    requests_mock: Mocker,
):
    requests_mock.get(
        f"{nortech.settings.URL}/api/v1/workspaces/1/assets",
        text=paginated_asset_list_output.model_dump_json(by_alias=True),
    )

    assets = nortech.metadata.asset.list(workspace=workspace_output)
    assert assets.data == [asset_list_output]


def test_list_workspace_assets_from_list_output(
    nortech: Nortech,
    workspace_list_output: list[WorkspaceListOutput],
    asset_list_output: AssetListOutput,
    paginated_asset_list_output: PaginatedResponse[AssetListOutput],
    requests_mock: Mocker,
):
    requests_mock.get(
        f"{nortech.settings.URL}/api/v1/workspaces/1/assets",
        text=paginated_asset_list_output.model_dump_json(by_alias=True),
    )

    assets = nortech.metadata.asset.list(workspace=workspace_list_output[0])
    assert assets.data == [asset_list_output]


def test_list_workspace_assets_from_int(
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


def test_list_workspace_assets_from_str(
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


def test_list_workspace_assets_error(
    nortech: Nortech,
    requests_mock: Mocker,
):
    requests_mock.get(f"{nortech.settings.URL}/api/v1/workspaces/test_workspace/assets", status_code=404)

    with pytest.raises(AssertionError) as err:
        nortech.metadata.asset.list(workspace="test_workspace")
    assert "Fetch failed." in str(err.value)


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


def test_get_workspace_asset_with_output(
    nortech: Nortech,
    asset_output: AssetOutput,
    requests_mock,
):
    requests_mock.get(
        f"{nortech.settings.URL}/api/v1/assets/1",
        text=asset_output.model_dump_json(by_alias=True),
    )

    asset = nortech.metadata.asset.get(asset=asset_output)
    assert asset == asset_output


def test_get_workspace_asset_with_list_output(
    nortech: Nortech,
    asset_output: AssetOutput,
    asset_list_output: AssetListOutput,
    requests_mock,
):
    requests_mock.get(f"{nortech.settings.URL}/api/v1/assets/1", text=asset_output.model_dump_json(by_alias=True))

    asset = nortech.metadata.asset.get(asset=asset_list_output)
    assert asset == asset_output


def test_get_workspace_asset_error(
    nortech: Nortech,
    requests_mock: Mocker,
):
    requests_mock.get(
        f"{nortech.settings.URL}/api/v1/workspaces/test_workspace/assets/test_asset",
        status_code=404,
    )

    with pytest.raises(AssertionError) as err:
        nortech.metadata.asset.get(asset=AssetInput(workspace="test_workspace", asset="test_asset"))
    assert "Fetch failed." in str(err.value)


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


def test_get_asset_error(
    nortech: Nortech,
    requests_mock,
):
    requests_mock.get(f"{nortech.settings.URL}/api/v1/assets/1", status_code=404)

    with pytest.raises(AssertionError) as err:
        nortech.metadata.asset.get(asset=1)
    assert "Fetch failed." in str(err.value)
