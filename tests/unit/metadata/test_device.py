import pytest
from requests_mock import Mocker

from nortech import Nortech
from nortech.metadata import DeviceInput, DeviceListOutput, DeviceOutput, DivisionInput, PaginatedResponse
from nortech.metadata.values.division import DivisionListOutput, DivisionOutput


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


def test_list_workspace_asset_division_devices_from_output(
    nortech: Nortech,
    device_list_output: DeviceListOutput,
    division_output: DivisionOutput,
    paginated_device_list_output: PaginatedResponse[DeviceOutput],
    requests_mock: Mocker,
):
    requests_mock.get(
        f"{nortech.settings.URL}/api/v1/divisions/1/devices",
        text=paginated_device_list_output.model_dump_json(by_alias=True),
    )

    divisions = nortech.metadata.device.list(division_output)
    assert divisions.data == [device_list_output]


def test_list_workspace_asset_division_devices_from_list_output(
    nortech: Nortech,
    device_list_output: DeviceListOutput,
    division_list_output: DivisionListOutput,
    paginated_device_list_output: PaginatedResponse[DeviceOutput],
    requests_mock: Mocker,
):
    requests_mock.get(
        f"{nortech.settings.URL}/api/v1/divisions/1/devices",
        text=paginated_device_list_output.model_dump_json(by_alias=True),
    )

    divisions = nortech.metadata.device.list(division_list_output)
    assert divisions.data == [device_list_output]


def test_list_workspace_asset_division_devices_error(
    nortech: Nortech,
    requests_mock: Mocker,
):
    requests_mock.get(
        f"{nortech.settings.URL}/api/v1/workspaces/test_workspace/assets/test_asset/divisions/test_division/devices",
        status_code=404,
    )

    with pytest.raises(AssertionError) as err:
        nortech.metadata.device.list(
            DivisionInput(workspace="test_workspace", asset="test_asset", division="test_division"),
        )
    assert "Fetch failed." in str(err.value)


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


def test_get_workspace_asset_division_device_with_output(
    nortech: Nortech,
    device_output: DeviceOutput,
    requests_mock,
):
    requests_mock.get(
        f"{nortech.settings.URL}/api/v1/devices/1",
        text=device_output.model_dump_json(by_alias=True),
    )

    division = nortech.metadata.device.get(device_output)
    assert division == device_output


def test_get_workspace_asset_division_device_with_list_output(
    nortech: Nortech,
    device_output: DeviceOutput,
    device_list_output: DeviceListOutput,
    requests_mock,
):
    requests_mock.get(f"{nortech.settings.URL}/api/v1/devices/1", text=device_output.model_dump_json(by_alias=True))

    division = nortech.metadata.device.get(device_list_output)
    assert division == device_output


def test_get_workspace_asset_division_device_error(
    nortech: Nortech,
    requests_mock: Mocker,
):
    requests_mock.get(
        f"{nortech.settings.URL}/api/v1/workspaces/test_workspace/assets/test_asset/divisions/test_division/devices/test_device",
        status_code=404,
    )

    with pytest.raises(AssertionError) as err:
        nortech.metadata.device.get(
            DeviceInput(
                workspace="test_workspace",
                asset="test_asset",
                division="test_division",
                device="test_device",
            ),
        )
    assert "Fetch failed." in str(err.value)


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


def test_list_workspace_devices_error(
    nortech: Nortech,
    requests_mock: Mocker,
):
    requests_mock.get(f"{nortech.settings.URL}/api/v1/workspaces/1/devices", status_code=404)

    with pytest.raises(AssertionError) as err:
        nortech.metadata.device.list_by_workspace_id(1)
    assert "Fetch failed." in str(err.value)


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


def test_list_asset_devices_error(
    nortech: Nortech,
    requests_mock: Mocker,
):
    requests_mock.get(f"{nortech.settings.URL}/api/v1/assets/1/devices", status_code=404)

    with pytest.raises(AssertionError) as err:
        nortech.metadata.device.list_by_asset_id(1)
    assert "Fetch failed." in str(err.value)


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


def test_list_division_devices_error(
    nortech: Nortech,
    requests_mock: Mocker,
):
    requests_mock.get(f"{nortech.settings.URL}/api/v1/divisions/1/devices", status_code=404)

    with pytest.raises(AssertionError) as err:
        nortech.metadata.device.list(division=1)
    assert "Fetch failed." in str(err.value)


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


def test_get_device_error(
    nortech: Nortech,
    requests_mock,
):
    requests_mock.get(f"{nortech.settings.URL}/api/v1/devices/1", status_code=404)

    with pytest.raises(AssertionError) as err:
        nortech.metadata.device.get(device=1)
    assert "Fetch failed." in str(err.value)
