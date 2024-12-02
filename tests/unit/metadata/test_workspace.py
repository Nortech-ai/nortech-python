import pytest
from requests_mock import Mocker

from nortech import Nortech
from nortech.metadata import PaginatedResponse, PaginationOptions, WorkspaceInput, WorkspaceListOutput, WorkspaceOutput


def test_list_workspaces(
    nortech: Nortech,
    workspace_list_output: list[WorkspaceListOutput],
    paginated_workspace_list_output: PaginatedResponse[WorkspaceListOutput],
    requests_mock: Mocker,
):
    requests_mock.get(
        f"{nortech.settings.URL}/api/v1/workspaces",
        text=paginated_workspace_list_output.model_dump_json(by_alias=True),
    )

    workspaces = nortech.metadata.workspace.list()
    assert workspaces.data == workspace_list_output


def test_list_workspaces_ignore_pagination(
    nortech: Nortech,
    workspace_list_output: list[WorkspaceListOutput],
    paginated_workspace_list_output_first_page: PaginatedResponse[WorkspaceListOutput],
    paginated_workspace_list_output_second_page: PaginatedResponse[WorkspaceListOutput],
    requests_mock: Mocker,
):
    requests_mock.register_uri(
        "GET",
        f"{nortech.settings.URL}/api/v1/workspaces",
        [
            {
                "text": paginated_workspace_list_output_first_page.model_dump_json(by_alias=True),
                "status_code": 200,
            },
            {
                "text": paginated_workspace_list_output_second_page.model_dump_json(by_alias=True),
                "status_code": 200,
            },
        ],
    )

    workspaces = nortech.metadata.workspace.list(pagination_options=PaginationOptions(size=2))
    assert workspaces.data == workspace_list_output
    assert requests_mock.call_count == 2
    assert requests_mock.request_history[1].qs == {"nexttoken": ["test_token"], "size": ["2"]}


def test_list_workspaces_with_pagination(
    nortech: Nortech,
    workspace_list_output: list[WorkspaceListOutput],
    paginated_workspace_list_output_first_page: PaginatedResponse[WorkspaceListOutput],
    requests_mock: Mocker,
):
    nortech.api.ignore_pagination = False
    requests_mock.get(
        f"{nortech.settings.URL}/api/v1/workspaces",
        text=paginated_workspace_list_output_first_page.model_dump_json(by_alias=True),
    )

    workspaces = nortech.metadata.workspace.list(pagination_options=PaginationOptions(size=2))
    assert workspaces.data == workspace_list_output[:2]
    assert requests_mock.call_count == 1


def test_list_workspaces_error(
    nortech: Nortech,
    requests_mock: Mocker,
):
    requests_mock.get(f"{nortech.settings.URL}/api/v1/workspaces", status_code=404)

    with pytest.raises(AssertionError) as err:
        nortech.metadata.workspace.list()
    assert "Fetch failed." in str(err.value)


def test_get_workspace_with_id(
    nortech: Nortech,
    workspace_output: WorkspaceOutput,
    requests_mock: Mocker,
):
    requests_mock.get(
        f"{nortech.settings.URL}/api/v1/workspaces/1",
        text=workspace_output.model_dump_json(by_alias=True),
    )

    workspace = nortech.metadata.workspace.get(workspace=1)
    assert workspace == workspace_output


def test_get_workspace_with_name(
    nortech: Nortech,
    workspace_output: WorkspaceOutput,
    requests_mock: Mocker,
):
    requests_mock.get(
        f"{nortech.settings.URL}/api/v1/workspaces/test_workspace",
        text=workspace_output.model_dump_json(by_alias=True),
    )

    workspace = nortech.metadata.workspace.get(workspace="test_workspace")
    assert workspace == workspace_output


def test_get_workspace_with_input(
    nortech: Nortech,
    workspace_output: WorkspaceOutput,
    requests_mock: Mocker,
):
    requests_mock.get(
        f"{nortech.settings.URL}/api/v1/workspaces/test_workspace",
        text=workspace_output.model_dump_json(by_alias=True),
    )

    workspace = nortech.metadata.workspace.get(workspace=WorkspaceInput(workspace="test_workspace"))
    assert workspace == workspace_output


def test_get_workspace_with_input_dict(
    nortech: Nortech,
    workspace_output: WorkspaceOutput,
    requests_mock: Mocker,
):
    requests_mock.get(
        f"{nortech.settings.URL}/api/v1/workspaces/test_workspace",
        text=workspace_output.model_dump_json(by_alias=True),
    )

    workspace = nortech.metadata.workspace.get(workspace={"workspace": "test_workspace"})
    assert workspace == workspace_output


def test_get_workspace_with_output(
    nortech: Nortech,
    workspace_output: WorkspaceOutput,
    requests_mock: Mocker,
):
    requests_mock.get(
        f"{nortech.settings.URL}/api/v1/workspaces/1",
        text=workspace_output.model_dump_json(by_alias=True),
    )

    workspace = nortech.metadata.workspace.get(workspace=workspace_output)
    assert workspace == workspace_output


def test_get_workspace_with_list_output(
    nortech: Nortech,
    workspace_output: WorkspaceOutput,
    workspace_list_output: list[WorkspaceListOutput],
    requests_mock: Mocker,
):
    requests_mock.get(
        f"{nortech.settings.URL}/api/v1/workspaces/1",
        text=workspace_output.model_dump_json(by_alias=True),
    )

    workspace = nortech.metadata.workspace.get(workspace=workspace_list_output[0])
    assert workspace == workspace_output


def test_get_workspace_error(
    nortech: Nortech,
    requests_mock: Mocker,
):
    requests_mock.get(
        f"{nortech.settings.URL}/api/v1/workspaces/1",
        status_code=404,
    )

    with pytest.raises(AssertionError) as err:
        nortech.metadata.workspace.get(workspace=1)
    assert "Fetch failed." in str(err.value)
