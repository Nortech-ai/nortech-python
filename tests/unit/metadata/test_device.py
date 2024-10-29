from requests_mock import Mocker

from nortech.core.gateways.nortech_api import NortechAPI, PaginatedResponse
from nortech.core.services.device import (
    get_device,
    get_workspace_asset_division_device,
    list_asset_devices,
    list_division_devices,
    list_workspace_asset_division_devices,
    list_workspace_devices,
)
from nortech.core.values.device import DeviceInput, DeviceListOutput, DeviceOutput
from nortech.core.values.division import DivisionInput


def test_list_workspace_asset_division_devices_from_input(
    nortech_api: NortechAPI,
    device_list_output: DeviceListOutput,
    paginated_device_list_output: PaginatedResponse[DeviceOutput],
    requests_mock: Mocker,
):
    requests_mock.get(
        f"{nortech_api.settings.URL}/api/v1/workspaces/test_workspace/assets/test_asset/divisions/test_division/devices",
        text=paginated_device_list_output.model_dump_json(by_alias=True),
    )

    divisions = list_workspace_asset_division_devices(
        nortech_api,
        DivisionInput(workspace="test_workspace", asset="test_asset", division="test_division"),
    )
    assert divisions.data == [device_list_output]


def test_list_workspace_asset_division_devices_from_input_dict(
    nortech_api: NortechAPI,
    device_list_output: DeviceListOutput,
    paginated_device_list_output: PaginatedResponse[DeviceOutput],
    requests_mock: Mocker,
):
    requests_mock.get(
        f"{nortech_api.settings.URL}/api/v1/workspaces/test_workspace/assets/test_asset/divisions/test_division/devices",
        text=paginated_device_list_output.model_dump_json(by_alias=True),
    )

    divisions = list_workspace_asset_division_devices(
        nortech_api,
        {"workspace": "test_workspace", "asset": "test_asset", "division": "test_division"},
    )
    assert divisions.data == [device_list_output]


def test_get_workspace_asset_division_device_404(
    nortech_api: NortechAPI,
    requests_mock: Mocker,
):
    requests_mock.get(
        f"{nortech_api.settings.URL}/api/v1/workspaces/test_workspace/assets/test_asset/divisions/test_division/devices/test_device",
        status_code=404,
    )

    division = get_workspace_asset_division_device(
        nortech_api,
        DeviceInput(
            workspace="test_workspace",
            asset="test_asset",
            division="test_division",
            device="test_device",
        ),
    )
    assert division is None


def test_get_workspace_asset_division_device_with_input(
    nortech_api: NortechAPI,
    device_output: DeviceOutput,
    requests_mock,
):
    requests_mock.get(
        f"{nortech_api.settings.URL}/api/v1/workspaces/test_workspace/assets/test_asset/divisions/test_division/devices/test_device",
        text=device_output.model_dump_json(by_alias=True),
    )

    division = get_workspace_asset_division_device(
        nortech_api,
        DeviceInput(
            workspace="test_workspace",
            asset="test_asset",
            division="test_division",
            device="test_device",
        ),
    )
    assert division == device_output


def test_get_workspace_asset_division_device_with_input_dict(
    nortech_api: NortechAPI,
    device_output: DeviceOutput,
    requests_mock,
):
    requests_mock.get(
        f"{nortech_api.settings.URL}/api/v1/workspaces/test_workspace/assets/test_asset/divisions/test_division/devices/test_device",
        text=device_output.model_dump_json(by_alias=True),
    )

    division = get_workspace_asset_division_device(
        nortech_api,
        {
            "workspace": "test_workspace",
            "asset": "test_asset",
            "division": "test_division",
            "device": "test_device",
        },
    )
    assert division == device_output


def test_list_workspace_devices(
    nortech_api: NortechAPI,
    device_list_output: DeviceListOutput,
    paginated_device_list_output: PaginatedResponse[DeviceOutput],
    requests_mock: Mocker,
):
    requests_mock.get(
        f"{nortech_api.settings.URL}/api/v1/workspaces/1/devices",
        text=paginated_device_list_output.model_dump_json(by_alias=True),
    )

    divisions = list_workspace_devices(nortech_api, 1)
    assert divisions.data == [device_list_output]


def test_list_asset_devices(
    nortech_api: NortechAPI,
    device_list_output: DeviceListOutput,
    paginated_device_list_output: PaginatedResponse[DeviceOutput],
    requests_mock: Mocker,
):
    requests_mock.get(
        f"{nortech_api.settings.URL}/api/v1/assets/1/devices",
        text=paginated_device_list_output.model_dump_json(by_alias=True),
    )

    divisions = list_asset_devices(nortech_api, 1)
    assert divisions.data == [device_list_output]


def test_list_division_devices(
    nortech_api: NortechAPI,
    device_list_output: DeviceListOutput,
    paginated_device_list_output: PaginatedResponse[DeviceOutput],
    requests_mock: Mocker,
):
    requests_mock.get(
        f"{nortech_api.settings.URL}/api/v1/divisions/1/devices",
        text=paginated_device_list_output.model_dump_json(by_alias=True),
    )

    divisions = list_division_devices(nortech_api, 1)
    assert divisions.data == [device_list_output]


def test_get_device_404(
    nortech_api: NortechAPI,
    requests_mock,
):
    requests_mock.get(f"{nortech_api.settings.URL}/api/v1/devices/1", status_code=404)
    division = get_device(nortech_api, 1)
    assert division is None


def test_get_device(
    nortech_api: NortechAPI,
    device_output: DeviceOutput,
    requests_mock,
):
    requests_mock.get(
        f"{nortech_api.settings.URL}/api/v1/devices/1",
        text=device_output.model_dump_json(by_alias=True),
    )

    division = get_device(nortech_api, 1)
    assert division == device_output
