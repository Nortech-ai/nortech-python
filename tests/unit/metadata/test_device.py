from requests_mock import Mocker

from nortech import Nortech
from nortech.core import DeviceInput, DeviceListOutput, DeviceOutput, DivisionInput, PaginatedResponse


def test_list_workspace_asset_division_devices_from_input(
    nortech: Nortech,
    device_list_output: DeviceListOutput,
    paginated_device_list_output: PaginatedResponse[DeviceOutput],
    requests_mock: Mocker,
):
    requests_mock.get(
        f"{nortech.settings.URL}/api/v1/workspaces/test_workspace/assets/test_asset/divisions/test_division/devices",
        text=paginated_device_list_output.model_dump_json(by_alias=True),
    )

    divisions = nortech.metadata.device.list(
        DivisionInput(workspace="test_workspace", asset="test_asset", division="test_division"),
    )
    assert divisions.data == [device_list_output]


def test_list_workspace_asset_division_devices_from_input_dict(
    nortech: Nortech,
    device_list_output: DeviceListOutput,
    paginated_device_list_output: PaginatedResponse[DeviceOutput],
    requests_mock: Mocker,
):
    requests_mock.get(
        f"{nortech.settings.URL}/api/v1/workspaces/test_workspace/assets/test_asset/divisions/test_division/devices",
        text=paginated_device_list_output.model_dump_json(by_alias=True),
    )

    divisions = nortech.metadata.device.list(
        {"workspace": "test_workspace", "asset": "test_asset", "division": "test_division"},
    )
    assert divisions.data == [device_list_output]


def test_get_workspace_asset_division_device_404(
    nortech: Nortech,
    requests_mock: Mocker,
):
    requests_mock.get(
        f"{nortech.settings.URL}/api/v1/workspaces/test_workspace/assets/test_asset/divisions/test_division/devices/test_device",
        status_code=404,
    )

    division = nortech.metadata.device.get(
        DeviceInput(
            workspace="test_workspace",
            asset="test_asset",
            division="test_division",
            device="test_device",
        ),
    )
    assert division is None


def test_get_workspace_asset_division_device_with_input(
    nortech: Nortech,
    device_output: DeviceOutput,
    requests_mock,
):
    requests_mock.get(
        f"{nortech.settings.URL}/api/v1/workspaces/test_workspace/assets/test_asset/divisions/test_division/devices/test_device",
        text=device_output.model_dump_json(by_alias=True),
    )

    division = nortech.metadata.device.get(
        DeviceInput(
            workspace="test_workspace",
            asset="test_asset",
            division="test_division",
            device="test_device",
        ),
    )
    assert division == device_output


def test_get_workspace_asset_division_device_with_input_dict(
    nortech: Nortech,
    device_output: DeviceOutput,
    requests_mock,
):
    requests_mock.get(
        f"{nortech.settings.URL}/api/v1/workspaces/test_workspace/assets/test_asset/divisions/test_division/devices/test_device",
        text=device_output.model_dump_json(by_alias=True),
    )

    division = nortech.metadata.device.get(
        {
            "workspace": "test_workspace",
            "asset": "test_asset",
            "division": "test_division",
            "device": "test_device",
        },
    )
    assert division == device_output


def test_list_workspace_devices(
    nortech: Nortech,
    device_list_output: DeviceListOutput,
    paginated_device_list_output: PaginatedResponse[DeviceOutput],
    requests_mock: Mocker,
):
    requests_mock.get(
        f"{nortech.settings.URL}/api/v1/workspaces/1/devices",
        text=paginated_device_list_output.model_dump_json(by_alias=True),
    )

    divisions = nortech.metadata.device.list_by_workspace_id(1)
    assert divisions.data == [device_list_output]


def test_list_asset_devices(
    nortech: Nortech,
    device_list_output: DeviceListOutput,
    paginated_device_list_output: PaginatedResponse[DeviceOutput],
    requests_mock: Mocker,
):
    requests_mock.get(
        f"{nortech.settings.URL}/api/v1/assets/1/devices",
        text=paginated_device_list_output.model_dump_json(by_alias=True),
    )

    divisions = nortech.metadata.device.list_by_asset_id(1)
    assert divisions.data == [device_list_output]


def test_list_division_devices(
    nortech: Nortech,
    device_list_output: DeviceListOutput,
    paginated_device_list_output: PaginatedResponse[DeviceOutput],
    requests_mock: Mocker,
):
    requests_mock.get(
        f"{nortech.settings.URL}/api/v1/divisions/1/devices",
        text=paginated_device_list_output.model_dump_json(by_alias=True),
    )

    divisions = nortech.metadata.device.list(division=1)
    assert divisions.data == [device_list_output]


def test_get_device_404(
    nortech: Nortech,
    requests_mock,
):
    requests_mock.get(f"{nortech.settings.URL}/api/v1/devices/1", status_code=404)
    division = nortech.metadata.device.get(device=1)
    assert division is None


def test_get_device(
    nortech: Nortech,
    device_output: DeviceOutput,
    requests_mock,
):
    requests_mock.get(
        f"{nortech.settings.URL}/api/v1/devices/1",
        text=device_output.model_dump_json(by_alias=True),
    )

    division = nortech.metadata.device.get(device=1)
    assert division == device_output
