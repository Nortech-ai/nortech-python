import pytest
from requests_mock import Mocker

from nortech import Nortech
from nortech.metadata import (
    AssetInput,
    DivisionInput,
    DivisionListOutput,
    DivisionOutput,
    PaginatedResponse,
)


def test_list_workspace_asset_divisions_from_input(
    nortech: Nortech,
    division_list_output: DivisionListOutput,
    paginated_division_list_output: PaginatedResponse[DivisionOutput],
    requests_mock: Mocker,
):
    requests_mock.get(
        f"{nortech.settings.URL}/api/v1/workspaces/test_workspace/assets/test_asset/divisions",
        text=paginated_division_list_output.model_dump_json(by_alias=True),
    )

    divisions = nortech.metadata.division.list(
        AssetInput(workspace="test_workspace", asset="test_asset"),
    )
    assert divisions.data == [division_list_output]


def test_list_workspace_asset_divisions_from_input_dict(
    nortech: Nortech,
    division_list_output: DivisionListOutput,
    paginated_division_list_output: PaginatedResponse[DivisionOutput],
    requests_mock: Mocker,
):
    requests_mock.get(
        f"{nortech.settings.URL}/api/v1/workspaces/test_workspace/assets/test_asset/divisions",
        text=paginated_division_list_output.model_dump_json(by_alias=True),
    )

    divisions = nortech.metadata.division.list(
        {"workspace": "test_workspace", "asset": "test_asset"},
    )
    assert divisions.data == [division_list_output]


def test_list_workspace_asset_division_error(
    nortech: Nortech,
    requests_mock: Mocker,
):
    requests_mock.get(
        f"{nortech.settings.URL}/api/v1/workspaces/test_workspace/assets/test_asset/divisions", status_code=404
    )

    with pytest.raises(AssertionError) as err:
        nortech.metadata.division.list(
            AssetInput(workspace="test_workspace", asset="test_asset"),
        )
    assert "Fetch failed." in str(err.value)


def test_get_workspace_asset_division_with_input(
    nortech: Nortech,
    division_output: DivisionOutput,
    requests_mock,
):
    requests_mock.get(
        f"{nortech.settings.URL}/api/v1/workspaces/test_workspace/assets/test_asset/divisions/test_division",
        text=division_output.model_dump_json(by_alias=True),
    )

    division = nortech.metadata.division.get(
        DivisionInput(workspace="test_workspace", asset="test_asset", division="test_division"),
    )
    assert division == division_output


def test_get_workspace_asset_division_with_input_dict(
    nortech: Nortech,
    division_output: DivisionOutput,
    requests_mock,
):
    requests_mock.get(
        f"{nortech.settings.URL}/api/v1/workspaces/test_workspace/assets/test_asset/divisions/test_division",
        text=division_output.model_dump_json(by_alias=True),
    )

    division = nortech.metadata.division.get(
        division={"workspace": "test_workspace", "asset": "test_asset", "division": "test_division"},
    )
    assert division == division_output


def test_get_workspace_asset_division_with_output(
    nortech: Nortech,
    division_output: DivisionOutput,
    requests_mock,
):
    requests_mock.get(
        f"{nortech.settings.URL}/api/v1/divisions/1",
        text=division_output.model_dump_json(by_alias=True),
    )

    division = nortech.metadata.division.get(division=division_output)
    assert division == division_output


def test_get_workspace_asset_division_with_list_output(
    nortech: Nortech,
    division_output: DivisionOutput,
    division_list_output: DivisionListOutput,
    requests_mock,
):
    requests_mock.get(
        f"{nortech.settings.URL}/api/v1/divisions/1",
        text=division_output.model_dump_json(by_alias=True),
    )

    division = nortech.metadata.division.get(division=division_list_output)
    assert division == division_output


def test_get_workspace_asset_division_error(
    nortech: Nortech,
    requests_mock: Mocker,
):
    requests_mock.get(
        f"{nortech.settings.URL}/api/v1/workspaces/test_workspace/assets/test_asset/divisions/test_division",
        status_code=404,
    )

    with pytest.raises(AssertionError) as err:
        nortech.metadata.division.get(
            DivisionInput(workspace="test_workspace", asset="test_asset", division="test_division"),
        )
    assert "Fetch failed." in str(err.value)


def test_list_workspace_divisions(
    nortech: Nortech,
    division_list_output: DivisionListOutput,
    paginated_division_list_output: PaginatedResponse[DivisionOutput],
    requests_mock: Mocker,
):
    requests_mock.get(
        f"{nortech.settings.URL}/api/v1/workspaces/1/divisions",
        text=paginated_division_list_output.model_dump_json(by_alias=True),
    )

    divisions = nortech.metadata.division.list_by_workspace_id(workspace_id=1)
    assert divisions.data == [division_list_output]


def test_list_workspace_divisions_error(
    nortech: Nortech,
    requests_mock: Mocker,
):
    requests_mock.get(f"{nortech.settings.URL}/api/v1/workspaces/1/divisions", status_code=404)

    with pytest.raises(AssertionError) as err:
        nortech.metadata.division.list_by_workspace_id(workspace_id=1)
    assert "Fetch failed." in str(err.value)


def test_list_asset_divisions(
    nortech: Nortech,
    division_list_output: DivisionListOutput,
    paginated_division_list_output: PaginatedResponse[DivisionOutput],
    requests_mock: Mocker,
):
    requests_mock.get(
        f"{nortech.settings.URL}/api/v1/assets/1/divisions",
        text=paginated_division_list_output.model_dump_json(by_alias=True),
    )

    divisions = nortech.metadata.division.list(asset=1)
    assert divisions.data == [division_list_output]


def test_list_asset_divisions_error(
    nortech: Nortech,
    requests_mock: Mocker,
):
    requests_mock.get(f"{nortech.settings.URL}/api/v1/assets/1/divisions", status_code=404)

    with pytest.raises(AssertionError) as err:
        nortech.metadata.division.list(asset=1)
    assert "Fetch failed." in str(err.value)


def test_get_division(
    nortech: Nortech,
    division_output: DivisionOutput,
    requests_mock,
):
    requests_mock.get(
        f"{nortech.settings.URL}/api/v1/divisions/1",
        text=division_output.model_dump_json(by_alias=True),
    )

    division = nortech.metadata.division.get(1)
    assert division == division_output


def test_get_division_error(
    nortech: Nortech,
    requests_mock,
):
    requests_mock.get(f"{nortech.settings.URL}/api/v1/divisions/1", status_code=404)

    with pytest.raises(AssertionError) as err:
        nortech.metadata.division.get(1)
    assert "Fetch failed." in str(err.value)
