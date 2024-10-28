from requests_mock import Mocker

from nortech.common.gateways.nortech_api import NortechAPI, PaginatedResponse
from nortech.metadata.services.signal import (
    get_signal,
    get_signals,
    get_workspace_asset_division_device_signal,
    get_workspace_asset_division_unit_signal,
    list_asset_signals,
    list_device_signals,
    list_division_signals,
    list_unit_signals,
    list_workspace_asset_division_device_signals,
    list_workspace_asset_division_unit_signals,
    list_workspace_signals,
    parse_signal_input_or_output_or_id_union_to_signal_input,
)
from nortech.metadata.values.device import DeviceInput
from nortech.metadata.values.signal import (
    SignalDeviceInput,
    SignalInput,
    SignalInputDict,
    SignalListOutput,
    SignalOutput,
)
from nortech.metadata.values.unit import UnitInput


def test_list_workspace_asset_division_unit_signals_from_input(
    nortech_api: NortechAPI,
    signal_list_output: SignalListOutput,
    paginated_signal_list_output: PaginatedResponse[SignalOutput],
    requests_mock: Mocker,
):
    requests_mock.get(
        f"{nortech_api.settings.URL}/api/v1/workspaces/test_workspace/assets/test_asset/divisions/test_division/units/test_unit/signals",
        text=paginated_signal_list_output.model_dump_json(by_alias=True),
    )

    signals = list_workspace_asset_division_unit_signals(
        nortech_api,
        UnitInput(
            workspace="test_workspace",
            asset="test_asset",
            division="test_division",
            unit="test_unit",
        ),
    )
    assert signals.data == [signal_list_output]


def test_list_workspace_asset_division_unit_signals_from_input_dict(
    nortech_api: NortechAPI,
    signal_list_output: SignalListOutput,
    paginated_signal_list_output: PaginatedResponse[SignalOutput],
    requests_mock: Mocker,
):
    requests_mock.get(
        f"{nortech_api.settings.URL}/api/v1/workspaces/test_workspace/assets/test_asset/divisions/test_division/units/test_unit/signals",
        text=paginated_signal_list_output.model_dump_json(by_alias=True),
    )

    signals = list_workspace_asset_division_unit_signals(
        nortech_api,
        {
            "workspace": "test_workspace",
            "asset": "test_asset",
            "division": "test_division",
            "unit": "test_unit",
        },
    )
    assert signals.data == [signal_list_output]


def test_list_workspace_asset_division_device_signals_from_input(
    nortech_api: NortechAPI,
    signal_list_output: SignalListOutput,
    paginated_signal_list_output: PaginatedResponse[SignalOutput],
    requests_mock: Mocker,
):
    requests_mock.get(
        f"{nortech_api.settings.URL}/api/v1/workspaces/test_workspace/assets/test_asset/divisions/test_division/devices/test_device/signals",
        text=paginated_signal_list_output.model_dump_json(by_alias=True),
    )

    signals = list_workspace_asset_division_device_signals(
        nortech_api,
        DeviceInput(
            workspace="test_workspace",
            asset="test_asset",
            division="test_division",
            device="test_device",
        ),
    )
    assert signals.data == [signal_list_output]


def test_list_workspace_asset_division_device_signals_from_input_dict(
    nortech_api: NortechAPI,
    signal_list_output: SignalListOutput,
    paginated_signal_list_output: PaginatedResponse[SignalOutput],
    requests_mock: Mocker,
):
    requests_mock.get(
        f"{nortech_api.settings.URL}/api/v1/workspaces/test_workspace/assets/test_asset/divisions/test_division/devices/test_device/signals",
        text=paginated_signal_list_output.model_dump_json(by_alias=True),
    )

    signals = list_workspace_asset_division_device_signals(
        nortech_api,
        {
            "workspace": "test_workspace",
            "asset": "test_asset",
            "division": "test_division",
            "device": "test_device",
        },
    )
    assert signals.data == [signal_list_output]


def test_get_workspace_asset_division_unit_signal_404(
    nortech_api: NortechAPI,
    requests_mock: Mocker,
):
    requests_mock.get(
        f"{nortech_api.settings.URL}/api/v1/workspaces/test_workspace/assets/test_asset/divisions/test_division/units/test_unit/signals/test_signal",
        status_code=404,
    )

    signal = get_workspace_asset_division_unit_signal(
        nortech_api,
        SignalInput(
            workspace="test_workspace",
            asset="test_asset",
            division="test_division",
            unit="test_unit",
            signal="test_signal",
        ),
    )
    assert signal is None


def test_get_workspace_asset_division_unit_signal_with_input(
    nortech_api: NortechAPI,
    signal_output: SignalOutput,
    requests_mock,
):
    requests_mock.get(
        f"{nortech_api.settings.URL}/api/v1/workspaces/test_workspace/assets/test_asset/divisions/test_division/units/test_unit/signals/test_signal",
        text=signal_output.model_dump_json(by_alias=True),
    )

    signal = get_workspace_asset_division_unit_signal(
        nortech_api,
        SignalInput(
            workspace="test_workspace",
            asset="test_asset",
            division="test_division",
            unit="test_unit",
            signal="test_signal",
        ),
    )
    assert signal == signal_output


def test_get_workspace_asset_division_unit_signal_with_input_dict(
    nortech_api: NortechAPI,
    signal_output: SignalOutput,
    requests_mock,
):
    requests_mock.get(
        f"{nortech_api.settings.URL}/api/v1/workspaces/test_workspace/assets/test_asset/divisions/test_division/units/test_unit/signals/test_signal",
        text=signal_output.model_dump_json(by_alias=True),
    )

    signal = get_workspace_asset_division_unit_signal(
        nortech_api,
        {
            "workspace": "test_workspace",
            "asset": "test_asset",
            "division": "test_division",
            "unit": "test_unit",
            "signal": "test_signal",
        },
    )
    assert signal == signal_output


def test_get_workspace_asset_division_device_signal_404(
    nortech_api: NortechAPI,
    requests_mock,
):
    requests_mock.get(
        f"{nortech_api.settings.URL}/api/v1/workspaces/test_workspace/assets/test_asset/divisions/test_division/devices/test_device/signals/test_signal",
        status_code=404,
    )

    signal = get_workspace_asset_division_device_signal(
        nortech_api,
        SignalDeviceInput(
            workspace="test_workspace",
            asset="test_asset",
            division="test_division",
            device="test_device",
            signal="test_signal",
        ),
    )
    assert signal is None


def test_get_workspace_asset_division_device_signal_with_input(
    nortech_api: NortechAPI,
    signal_output: SignalOutput,
    requests_mock,
):
    requests_mock.get(
        f"{nortech_api.settings.URL}/api/v1/workspaces/test_workspace/assets/test_asset/divisions/test_division/devices/test_device/signals/test_signal",
        text=signal_output.model_dump_json(by_alias=True),
    )

    signal = get_workspace_asset_division_device_signal(
        nortech_api,
        SignalDeviceInput(
            workspace="test_workspace",
            asset="test_asset",
            division="test_division",
            device="test_device",
            signal="test_signal",
        ),
    )
    assert signal == signal_output


def test_get_workspace_asset_division_device_signal_with_input_dict(
    nortech_api: NortechAPI,
    signal_output: SignalOutput,
    requests_mock,
):
    requests_mock.get(
        f"{nortech_api.settings.URL}/api/v1/workspaces/test_workspace/assets/test_asset/divisions/test_division/devices/test_device/signals/test_signal",
        text=signal_output.model_dump_json(by_alias=True),
    )

    signal = get_workspace_asset_division_device_signal(
        nortech_api,
        {
            "workspace": "test_workspace",
            "asset": "test_asset",
            "division": "test_division",
            "device": "test_device",
            "signal": "test_signal",
        },
    )
    assert signal == signal_output


def test_list_workspace_signals(
    nortech_api: NortechAPI,
    signal_list_output: SignalListOutput,
    paginated_signal_list_output: PaginatedResponse[SignalOutput],
    requests_mock: Mocker,
):
    requests_mock.get(
        f"{nortech_api.settings.URL}/api/v1/workspaces/1/signals",
        text=paginated_signal_list_output.model_dump_json(by_alias=True),
    )

    signals = list_workspace_signals(nortech_api, 1)
    assert signals.data == [signal_list_output]


def test_list_asset_signals(
    nortech_api: NortechAPI,
    signal_list_output: SignalListOutput,
    paginated_signal_list_output: PaginatedResponse[SignalOutput],
    requests_mock: Mocker,
):
    requests_mock.get(
        f"{nortech_api.settings.URL}/api/v1/assets/1/signals",
        text=paginated_signal_list_output.model_dump_json(by_alias=True),
    )

    signals = list_asset_signals(nortech_api, 1)
    assert signals.data == [signal_list_output]


def test_list_division_signals(
    nortech_api: NortechAPI,
    signal_list_output: SignalListOutput,
    paginated_signal_list_output: PaginatedResponse[SignalOutput],
    requests_mock: Mocker,
):
    requests_mock.get(
        f"{nortech_api.settings.URL}/api/v1/divisions/1/signals",
        text=paginated_signal_list_output.model_dump_json(by_alias=True),
    )

    signals = list_division_signals(nortech_api, 1)
    assert signals.data == [signal_list_output]


def test_list_unit_signals(
    nortech_api: NortechAPI,
    signal_list_output: SignalListOutput,
    paginated_signal_list_output: PaginatedResponse[SignalOutput],
    requests_mock: Mocker,
):
    requests_mock.get(
        f"{nortech_api.settings.URL}/api/v1/units/1/signals",
        text=paginated_signal_list_output.model_dump_json(by_alias=True),
    )

    signals = list_unit_signals(nortech_api, 1)
    assert signals.data == [signal_list_output]


def test_list_device_signals(
    nortech_api: NortechAPI,
    signal_list_output: SignalListOutput,
    paginated_signal_list_output: PaginatedResponse[SignalOutput],
    requests_mock: Mocker,
):
    requests_mock.get(
        f"{nortech_api.settings.URL}/api/v1/devices/1/signals",
        text=paginated_signal_list_output.model_dump_json(by_alias=True),
    )

    signals = list_device_signals(nortech_api, 1)
    assert signals.data == [signal_list_output]


def test_get_signal_404(
    nortech_api: NortechAPI,
    requests_mock,
):
    requests_mock.get(f"{nortech_api.settings.URL}/api/v1/signals/1", status_code=404)
    signal = get_signal(nortech_api, 1)
    assert signal is None


def test_get_signal(
    nortech_api: NortechAPI,
    signal_output: SignalOutput,
    requests_mock,
):
    requests_mock.get(
        f"{nortech_api.settings.URL}/api/v1/signals/1",
        text=signal_output.model_dump_json(by_alias=True),
    )

    signal = get_signal(nortech_api, 1)
    assert signal == signal_output


def test_get_signals(
    nortech_api: NortechAPI,
    signal_output: SignalOutput,
    signal_input: SignalInput,
    signal_input_dict: SignalInputDict,
    requests_mock: Mocker,
):
    requests_mock.post(
        f"{nortech_api.settings.URL}/api/v1/signals",
        text=f"[{signal_output.model_dump_json(by_alias=True)}]",
    )

    signals = get_signals(nortech_api, [signal_input, signal_input_dict, signal_output, 1])
    assert signals == [signal_output]
    assert requests_mock.last_request is not None
    assert requests_mock.last_request.json() == {
        "signals": [signal_input.model_dump(by_alias=True), signal_input_dict, signal_output.id, 1]
    }


def test_parse_signal_input_or_output_or_id_union_to_signal_input(
    nortech_api: NortechAPI,
    signal_output: SignalOutput,
    signal_input: SignalInput,
    signal_input_dict: SignalInputDict,
    requests_mock: Mocker,
):
    requests_mock.post(
        f"{nortech_api.settings.URL}/api/v1/signals",
        text=f"[{signal_output.model_dump_json(by_alias=True)}]",
    )

    signal_inputs = parse_signal_input_or_output_or_id_union_to_signal_input(
        nortech_api, [signal_input, signal_input_dict, signal_output, 1]
    )
    assert signal_inputs == [signal_input, signal_input, signal_input, signal_input]
    assert requests_mock.last_request is not None
    assert requests_mock.last_request.json() == {"signals": [1]}
