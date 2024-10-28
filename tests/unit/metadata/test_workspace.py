from requests_mock import Mocker

from nortech.common.gateways.nortech_api import NortechAPI, PaginatedResponse, PaginationOptions
from nortech.metadata.services.workspace import get_workspace, list_workspaces
from nortech.metadata.values.workspace import WorkspaceInput, WorkspaceListOutput, WorkspaceOutput


def test_list_workspaces(
    nortech_api: NortechAPI,
    workspace_list_output: list[WorkspaceListOutput],
    paginated_workspace_list_output: PaginatedResponse[WorkspaceListOutput],
    requests_mock: Mocker,
):
    requests_mock.get(
        f"{nortech_api.settings.URL}/api/v1/workspaces",
        text=paginated_workspace_list_output.model_dump_json(by_alias=True),
    )

    workspaces = list_workspaces(nortech_api)
    assert workspaces.data == workspace_list_output


def test_list_workspaces_ignore_pagination(
    nortech_api: NortechAPI,
    workspace_list_output: list[WorkspaceListOutput],
    paginated_workspace_list_output_first_page: PaginatedResponse[WorkspaceListOutput],
    paginated_workspace_list_output_second_page: PaginatedResponse[WorkspaceListOutput],
    requests_mock: Mocker,
):
    requests_mock.register_uri(
        "GET",
        f"{nortech_api.settings.URL}/api/v1/workspaces",
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

    workspaces = list_workspaces(nortech_api, PaginationOptions(size=2))
    assert workspaces.data == workspace_list_output
    assert requests_mock.call_count == 2
    assert requests_mock.request_history[1].qs == {"nexttoken": ["test_token"], "size": ["2"]}


def test_list_workspaces_with_pagination(
    nortech_api: NortechAPI,
    workspace_list_output: list[WorkspaceListOutput],
    paginated_workspace_list_output_first_page: PaginatedResponse[WorkspaceListOutput],
    requests_mock: Mocker,
):
    nortech_api.ignore_pagination = False
    requests_mock.get(
        f"{nortech_api.settings.URL}/api/v1/workspaces",
        text=paginated_workspace_list_output_first_page.model_dump_json(by_alias=True),
    )

    workspaces = list_workspaces(nortech_api, PaginationOptions(size=2))
    assert workspaces.data == workspace_list_output[:2]
    assert requests_mock.call_count == 1


def test_get_workspace_404(
    nortech_api: NortechAPI,
    requests_mock: Mocker,
):
    requests_mock.get(
        f"{nortech_api.settings.URL}/api/v1/workspaces/1",
        status_code=404,
    )

    workspace = get_workspace(nortech_api, 1)
    assert workspace is None


def test_get_workspace_with_id(
    nortech_api: NortechAPI,
    workspace_output: WorkspaceOutput,
    requests_mock: Mocker,
):
    requests_mock.get(
        f"{nortech_api.settings.URL}/api/v1/workspaces/1",
        text=workspace_output.model_dump_json(by_alias=True),
    )

    workspace = get_workspace(nortech_api, 1)
    assert workspace == workspace_output


def test_get_workspace_with_name(
    nortech_api: NortechAPI,
    workspace_output: WorkspaceOutput,
    requests_mock: Mocker,
):
    requests_mock.get(
        f"{nortech_api.settings.URL}/api/v1/workspaces/test_workspace",
        text=workspace_output.model_dump_json(by_alias=True),
    )

    workspace = get_workspace(nortech_api, "test_workspace")
    assert workspace == workspace_output


def test_get_workspace_with_input(
    nortech_api: NortechAPI,
    workspace_output: WorkspaceOutput,
    requests_mock: Mocker,
):
    requests_mock.get(
        f"{nortech_api.settings.URL}/api/v1/workspaces/test_workspace",
        text=workspace_output.model_dump_json(by_alias=True),
    )

    workspace = get_workspace(nortech_api, WorkspaceInput(workspace="test_workspace"))
    assert workspace == workspace_output


def test_get_workspace_with_input_dict(
    nortech_api: NortechAPI,
    workspace_output: WorkspaceOutput,
    requests_mock: Mocker,
):
    requests_mock.get(
        f"{nortech_api.settings.URL}/api/v1/workspaces/test_workspace",
        text=workspace_output.model_dump_json(by_alias=True),
    )

    workspace = get_workspace(nortech_api, {"workspace": "test_workspace"})
    assert workspace == workspace_output
