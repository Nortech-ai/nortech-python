from __future__ import annotations

from typing import Literal

from nortech.common.gateways.nortech_api import (
    NortechAPI,
    PaginatedResponse,
    PaginationOptions,
    validate_response,
)
from nortech.metadata.services.device import (
    DeviceInput,
    DeviceInputDict,
    DeviceOutput,
    parse_device_input,
)
from nortech.metadata.services.unit import UnitInput, UnitInputDict, UnitOutput, parse_unit_input
from nortech.metadata.values.signal import (
    SignalDeviceInput,
    SignalDeviceInputDict,
    SignalInput,
    SignalInputDict,
    SignalListOutput,
    SignalOutput,
    parse_signal_device_input,
    parse_signal_input,
)


def list_workspace_asset_division_unit_signals(
    nortech_api: NortechAPI,
    unit: UnitInputDict | UnitInput | UnitOutput,
    pagination_options: PaginationOptions[
        Literal["id", "name", "physical_unit", "data_type", "description", "long_description"]
    ]
    | None = None,
):
    unit_input = parse_unit_input(unit)
    response = nortech_api.get(
        url=f"/api/v1/workspaces/{unit_input.workspace}/assets/{unit_input.asset}/divisions/{unit_input.division}/units/{unit_input.unit}/signals",
        params=pagination_options.model_dump(exclude_none=True, by_alias=True) if pagination_options else None,
    )
    validate_response(response, [200])

    resp = PaginatedResponse[SignalListOutput].model_validate(
        {**response.json(), "pagination_options": pagination_options}
    )

    if nortech_api.ignore_pagination and resp.next and resp.next.token:
        next_resp = list_workspace_asset_division_unit_signals(nortech_api, unit, resp.next_pagination_options())
        return resp.model_copy(
            update={
                "data": resp.data + next_resp.data,
                "size": resp.size + next_resp.size,
                "next": next_resp.next,
            }
        )

    return resp


def get_workspace_asset_division_unit_signal(
    nortech_api: NortechAPI, signal: SignalInputDict | SignalInput | SignalOutput
):
    signal_input = parse_signal_input(signal)
    response = nortech_api.get(
        url=f"/api/v1/workspaces/{signal_input.workspace}/assets/{signal_input.asset}/divisions/{signal_input.division}/units/{signal_input.unit}/signals/{signal_input.signal}",
    )
    validate_response(response, [200, 404])
    if response.status_code == 404:
        return None
    return SignalOutput.model_validate(response.json())


def list_workspace_asset_division_device_signals(
    nortech_api: NortechAPI,
    device: DeviceInputDict | DeviceInput | DeviceOutput,
    pagination_options: PaginationOptions[
        Literal["id", "name", "physical_unit", "data_type", "description", "long_description"]
    ]
    | None = None,
):
    device_input = parse_device_input(device)
    response = nortech_api.get(
        url=f"/api/v1/workspaces/{device_input.workspace}/assets/{device_input.asset}/divisions/{device_input.division}/devices/{device_input.device}/signals",
        params=pagination_options.model_dump(exclude_none=True, by_alias=True) if pagination_options else None,
    )
    validate_response(response, [200])

    resp = PaginatedResponse[SignalListOutput].model_validate(
        {**response.json(), "pagination_options": pagination_options}
    )

    if nortech_api.ignore_pagination and resp.next and resp.next.token:
        next_resp = list_workspace_asset_division_device_signals(nortech_api, device, resp.next_pagination_options())
        return resp.model_copy(
            update={
                "data": resp.data + next_resp.data,
                "size": resp.size + next_resp.size,
                "next": next_resp.next,
            }
        )

    return resp


def get_workspace_asset_division_device_signal(
    nortech_api: NortechAPI, signal: SignalDeviceInputDict | SignalDeviceInput | SignalOutput
):
    signal_input = parse_signal_device_input(signal)
    response = nortech_api.get(
        url=f"/api/v1/workspaces/{signal_input.workspace}/assets/{signal_input.asset}/divisions/{signal_input.division}/devices/{signal_input.device}/signals/{signal_input.signal}",
    )
    validate_response(response, [200, 404])
    if response.status_code == 404:
        return None
    return SignalOutput.model_validate(response.json())


def list_workspace_signals(
    nortech_api: NortechAPI,
    workspace_id: int,
    pagination_options: PaginationOptions[
        Literal["id", "name", "physical_unit", "data_type", "description", "long_description"]
    ]
    | None = None,
):
    response = nortech_api.get(
        url=f"/api/v1/workspaces/{workspace_id}/signals",
        params=pagination_options.model_dump(exclude_none=True, by_alias=True) if pagination_options else None,
    )
    validate_response(response, [200])

    resp = PaginatedResponse[SignalListOutput].model_validate(
        {**response.json(), "pagination_options": pagination_options}
    )

    if nortech_api.ignore_pagination and resp.next and resp.next.token:
        next_resp = list_workspace_signals(nortech_api, workspace_id, resp.next_pagination_options())
        return resp.model_copy(
            update={
                "data": resp.data + next_resp.data,
                "size": resp.size + next_resp.size,
                "next": next_resp.next,
            }
        )

    return resp


def list_asset_signals(
    nortech_api: NortechAPI,
    asset_id: int,
    pagination_options: PaginationOptions[
        Literal["id", "name", "physical_unit", "data_type", "description", "long_description"]
    ]
    | None = None,
):
    response = nortech_api.get(
        url=f"/api/v1/assets/{asset_id}/signals",
        params=pagination_options.model_dump(exclude_none=True, by_alias=True) if pagination_options else None,
    )
    validate_response(response, [200])

    resp = PaginatedResponse[SignalListOutput].model_validate(
        {**response.json(), "pagination_options": pagination_options}
    )

    if nortech_api.ignore_pagination and resp.next and resp.next.token:
        next_resp = list_asset_signals(nortech_api, asset_id, resp.next_pagination_options())
        return resp.model_copy(
            update={
                "data": resp.data + next_resp.data,
                "size": resp.size + next_resp.size,
                "next": next_resp.next,
            }
        )

    return resp


def list_division_signals(
    nortech_api: NortechAPI,
    division_id: int,
    pagination_options: PaginationOptions[
        Literal["id", "name", "physical_unit", "data_type", "description", "long_description"]
    ]
    | None = None,
):
    response = nortech_api.get(
        url=f"/api/v1/divisions/{division_id}/signals",
        params=pagination_options.model_dump(exclude_none=True, by_alias=True) if pagination_options else None,
    )
    validate_response(response, [200])

    resp = PaginatedResponse[SignalListOutput].model_validate(
        {**response.json(), "pagination_options": pagination_options}
    )

    if nortech_api.ignore_pagination and resp.next and resp.next.token:
        next_resp = list_division_signals(nortech_api, division_id, resp.next_pagination_options())
        return resp.model_copy(
            update={
                "data": resp.data + next_resp.data,
                "size": resp.size + next_resp.size,
                "next": next_resp.next,
            }
        )

    return resp


def list_unit_signals(
    nortech_api: NortechAPI,
    unit_id: int,
    pagination_options: PaginationOptions[
        Literal["id", "name", "physical_unit", "data_type", "description", "long_description"]
    ]
    | None = None,
):
    response = nortech_api.get(
        url=f"/api/v1/units/{unit_id}/signals",
        params=pagination_options.model_dump(exclude_none=True, by_alias=True) if pagination_options else None,
    )
    validate_response(response, [200])

    resp = PaginatedResponse[SignalListOutput].model_validate(
        {**response.json(), "pagination_options": pagination_options}
    )

    if nortech_api.ignore_pagination and resp.next and resp.next.token:
        next_resp = list_unit_signals(nortech_api, unit_id, resp.next_pagination_options())
        return resp.model_copy(
            update={
                "data": resp.data + next_resp.data,
                "size": resp.size + next_resp.size,
                "next": next_resp.next,
            }
        )

    return resp


def list_device_signals(
    nortech_api: NortechAPI,
    device_id: int,
    pagination_options: PaginationOptions[
        Literal["id", "name", "physical_unit", "data_type", "description", "long_description"]
    ]
    | None = None,
):
    response = nortech_api.get(
        url=f"/api/v1/devices/{device_id}/signals",
        params=pagination_options.model_dump(exclude_none=True, by_alias=True) if pagination_options else None,
    )
    validate_response(response, [200])

    resp = PaginatedResponse[SignalListOutput].model_validate(
        {**response.json(), "pagination_options": pagination_options}
    )

    if nortech_api.ignore_pagination and resp.next and resp.next.token:
        next_resp = list_device_signals(nortech_api, device_id, resp.next_pagination_options())
        return resp.model_copy(
            update={
                "data": resp.data + next_resp.data,
                "size": resp.size + next_resp.size,
                "next": next_resp.next,
            }
        )

    return resp


def get_signal(nortech_api: NortechAPI, signal_id: int):
    response = nortech_api.get(
        url=f"/api/v1/signals/{signal_id}",
    )
    validate_response(response, [200, 404])
    if response.status_code == 404:
        return None
    return SignalOutput.model_validate(response.json())


def get_signals(nortech_api: NortechAPI, signals: list[SignalInput | SignalInputDict | SignalOutput | int]):
    def signal_to_api_input(signal: SignalInput | SignalInputDict | SignalOutput | int):
        if isinstance(signal, SignalOutput):
            return signal.id
        elif isinstance(signal, SignalInput):
            return signal.model_dump(by_alias=True)
        else:
            return signal

    response = nortech_api.post(
        url="/api/v1/signals",
        json={"signals": [signal_to_api_input(signal) for signal in signals]},
    )
    validate_response(response, [200], "Failed to get signals.")
    return [SignalOutput.model_validate(signal) for signal in response.json()]


def parse_signal_input_or_output_or_id_union_to_signal_input(
    nortech_api: NortechAPI, signals: list[SignalInput | SignalInputDict | SignalOutput | int]
):
    signal_ids: list[SignalInput | SignalInputDict | SignalOutput | int] = [
        signal for signal in signals if isinstance(signal, int)
    ]
    signals_outputs_to_inputs: list[SignalInput] = [
        signal.to_signal_input() for signal in signals if isinstance(signal, SignalOutput)
    ]
    signal_inputs: list[SignalInput] = [
        parse_signal_input(signal)
        for signal in signals
        if not isinstance(signal, int) and not isinstance(signal, SignalOutput)
    ] + signals_outputs_to_inputs
    signal_list_from_ids = get_signals(nortech_api, signal_ids)
    return [signal.to_signal_input() for signal in signal_list_from_ids] + signal_inputs
