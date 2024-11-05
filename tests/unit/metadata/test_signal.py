from requests_mock import Mocker

from nortech import Nortech
from nortech.core import (
    DeviceInput,
    PaginatedResponse,
    SignalDeviceInput,
    SignalInput,
    SignalInputDict,
    SignalListOutput,
    SignalOutput,
    UnitInput,
)
from nortech.core.services.signal import parse_signal_input_or_output_or_id_union_to_signal_input


def test_list_workspace_asset_division_unit_signals_from_input(
    nortech: Nortech,
    signal_list_output: SignalListOutput,
    paginated_signal_list_output: PaginatedResponse[SignalOutput],
    requests_mock: Mocker,
):
    requests_mock.get(
        f"{nortech.settings.URL}/api/v1/workspaces/test_workspace/assets/test_asset/divisions/test_division/units/test_unit/signals",
        text=paginated_signal_list_output.model_dump_json(by_alias=True),
    )

    signals = nortech.metadata.signal.list(
        UnitInput(
            workspace="test_workspace",
            asset="test_asset",
            division="test_division",
            unit="test_unit",
        ),
    )
    assert signals.data == [signal_list_output]


def test_list_workspace_asset_division_unit_signals_from_input_dict(
    nortech: Nortech,
    signal_list_output: SignalListOutput,
    paginated_signal_list_output: PaginatedResponse[SignalOutput],
    requests_mock: Mocker,
):
    requests_mock.get(
        f"{nortech.settings.URL}/api/v1/workspaces/test_workspace/assets/test_asset/divisions/test_division/units/test_unit/signals",
        text=paginated_signal_list_output.model_dump_json(by_alias=True),
    )

    signals = nortech.metadata.signal.list(
        {
            "workspace": "test_workspace",
            "asset": "test_asset",
            "division": "test_division",
            "unit": "test_unit",
        },
    )
    assert signals.data == [signal_list_output]


def test_list_workspace_asset_division_device_signals_from_input(
    nortech: Nortech,
    signal_list_output: SignalListOutput,
    paginated_signal_list_output: PaginatedResponse[SignalOutput],
    requests_mock: Mocker,
):
    requests_mock.get(
        f"{nortech.settings.URL}/api/v1/workspaces/test_workspace/assets/test_asset/divisions/test_division/devices/test_device/signals",
        text=paginated_signal_list_output.model_dump_json(by_alias=True),
    )

    signals = nortech.metadata.signal.list(
        DeviceInput(
            workspace="test_workspace",
            asset="test_asset",
            division="test_division",
            device="test_device",
        ),
    )
    assert signals.data == [signal_list_output]


def test_list_workspace_asset_division_device_signals_from_input_dict(
    nortech: Nortech,
    signal_list_output: SignalListOutput,
    paginated_signal_list_output: PaginatedResponse[SignalOutput],
    requests_mock: Mocker,
):
    requests_mock.get(
        f"{nortech.settings.URL}/api/v1/workspaces/test_workspace/assets/test_asset/divisions/test_division/devices/test_device/signals",
        text=paginated_signal_list_output.model_dump_json(by_alias=True),
    )

    signals = nortech.metadata.signal.list(
        {
            "workspace": "test_workspace",
            "asset": "test_asset",
            "division": "test_division",
            "device": "test_device",
        },
    )
    assert signals.data == [signal_list_output]


def test_get_workspace_asset_division_unit_signal_404(
    nortech: Nortech,
    requests_mock: Mocker,
):
    requests_mock.get(
        f"{nortech.settings.URL}/api/v1/workspaces/test_workspace/assets/test_asset/divisions/test_division/units/test_unit/signals/test_signal",
        status_code=404,
    )

    signal = nortech.metadata.signal.get(
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
    nortech: Nortech,
    signal_output: SignalOutput,
    requests_mock,
):
    requests_mock.get(
        f"{nortech.settings.URL}/api/v1/workspaces/test_workspace/assets/test_asset/divisions/test_division/units/test_unit/signals/test_signal",
        text=signal_output.model_dump_json(by_alias=True),
    )

    signal = nortech.metadata.signal.get(
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
    nortech: Nortech,
    signal_output: SignalOutput,
    requests_mock,
):
    requests_mock.get(
        f"{nortech.settings.URL}/api/v1/workspaces/test_workspace/assets/test_asset/divisions/test_division/units/test_unit/signals/test_signal",
        text=signal_output.model_dump_json(by_alias=True),
    )

    signal = nortech.metadata.signal.get(
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
    nortech: Nortech,
    requests_mock,
):
    requests_mock.get(
        f"{nortech.settings.URL}/api/v1/workspaces/test_workspace/assets/test_asset/divisions/test_division/devices/test_device/signals/test_signal",
        status_code=404,
    )

    signal = nortech.metadata.signal.get(
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
    nortech: Nortech,
    signal_output: SignalOutput,
    requests_mock,
):
    requests_mock.get(
        f"{nortech.settings.URL}/api/v1/workspaces/test_workspace/assets/test_asset/divisions/test_division/devices/test_device/signals/test_signal",
        text=signal_output.model_dump_json(by_alias=True),
    )

    signal = nortech.metadata.signal.get(
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
    nortech: Nortech,
    signal_output: SignalOutput,
    requests_mock,
):
    requests_mock.get(
        f"{nortech.settings.URL}/api/v1/workspaces/test_workspace/assets/test_asset/divisions/test_division/devices/test_device/signals/test_signal",
        text=signal_output.model_dump_json(by_alias=True),
    )

    signal = nortech.metadata.signal.get(
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
    nortech: Nortech,
    signal_list_output: SignalListOutput,
    paginated_signal_list_output: PaginatedResponse[SignalOutput],
    requests_mock: Mocker,
):
    requests_mock.get(
        f"{nortech.settings.URL}/api/v1/workspaces/1/signals",
        text=paginated_signal_list_output.model_dump_json(by_alias=True),
    )

    signals = nortech.metadata.signal.list_by_workspace_id(1)
    assert signals.data == [signal_list_output]


def test_list_asset_signals(
    nortech: Nortech,
    signal_list_output: SignalListOutput,
    paginated_signal_list_output: PaginatedResponse[SignalOutput],
    requests_mock: Mocker,
):
    requests_mock.get(
        f"{nortech.settings.URL}/api/v1/assets/1/signals",
        text=paginated_signal_list_output.model_dump_json(by_alias=True),
    )

    signals = nortech.metadata.signal.list_by_asset_id(1)
    assert signals.data == [signal_list_output]


def test_list_division_signals(
    nortech: Nortech,
    signal_list_output: SignalListOutput,
    paginated_signal_list_output: PaginatedResponse[SignalOutput],
    requests_mock: Mocker,
):
    requests_mock.get(
        f"{nortech.settings.URL}/api/v1/divisions/1/signals",
        text=paginated_signal_list_output.model_dump_json(by_alias=True),
    )

    signals = nortech.metadata.signal.list_by_division_id(1)
    assert signals.data == [signal_list_output]


def test_list_signals(
    nortech: Nortech,
    signal_list_output: SignalListOutput,
    paginated_signal_list_output: PaginatedResponse[SignalOutput],
    requests_mock: Mocker,
):
    requests_mock.get(
        f"{nortech.settings.URL}/api/v1/units/1/signals",
        text=paginated_signal_list_output.model_dump_json(by_alias=True),
    )

    signals = nortech.metadata.signal.list(1)
    assert signals.data == [signal_list_output]


def test_get_signal_404(
    nortech: Nortech,
    requests_mock,
):
    requests_mock.get(f"{nortech.settings.URL}/api/v1/signals/1", status_code=404)
    signal = nortech.metadata.signal.get(1)
    assert signal is None


def test_get_signal(
    nortech: Nortech,
    signal_output: SignalOutput,
    requests_mock,
):
    requests_mock.get(
        f"{nortech.settings.URL}/api/v1/signals/1",
        text=signal_output.model_dump_json(by_alias=True),
    )

    signal = nortech.metadata.signal.get(1)
    assert signal == signal_output


def test_get_signals(
    nortech: Nortech,
    signal_output: SignalOutput,
    signal_input: SignalInput,
    signal_input_dict: SignalInputDict,
    requests_mock: Mocker,
):
    requests_mock.post(
        f"{nortech.settings.URL}/api/v1/signals",
        text=f"[{signal_output.model_dump_json(by_alias=True)}]",
    )

    signals = nortech.metadata.signal.get_signals([signal_input, signal_input_dict, signal_output, 1])
    assert signals == [signal_output]
    assert requests_mock.last_request is not None
    assert requests_mock.last_request.json() == {
        "signals": [signal_input.model_dump(by_alias=True), signal_input_dict, signal_output.id, 1]
    }


def test_parse_signal_input_or_output_or_id_union_to_signal_input(
    nortech: Nortech,
    signal_output: SignalOutput,
    signal_input: SignalInput,
    signal_input_dict: SignalInputDict,
    requests_mock: Mocker,
):
    requests_mock.post(
        f"{nortech.settings.URL}/api/v1/signals",
        text=f"[{signal_output.model_dump_json(by_alias=True)}]",
    )

    signal_inputs = parse_signal_input_or_output_or_id_union_to_signal_input(
        nortech.api, [signal_input, signal_input_dict, signal_output, 1]
    )
    assert signal_inputs == [signal_input, signal_input, signal_input, signal_input]
    assert requests_mock.last_request is not None
    assert requests_mock.last_request.json() == {"signals": [1]}
