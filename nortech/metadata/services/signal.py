from __future__ import annotations

from typing import List, Literal, Sequence

from nortech.gateways.nortech_api import (
    NortechAPI,
    validate_response,
)
from nortech.metadata.services.device import (
    DeviceInput,
    DeviceInputDict,
    DeviceListOutput,
    DeviceOutput,
    parse_device_input,
)
from nortech.metadata.services.unit import UnitInput, UnitInputDict, UnitListOutput, UnitOutput, parse_unit_input
from nortech.metadata.values.pagination import PaginatedResponse, PaginationOptions
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
    unit: int | UnitInputDict | UnitInput | UnitOutput | UnitListOutput,
    pagination_options: PaginationOptions[
        Literal["id", "name", "physical_unit", "data_type", "description", "long_description"]
    ]
    | None = None,
):
    if isinstance(unit, int):
        return list_unit_signals(nortech_api, unit, pagination_options)
    if isinstance(unit, UnitListOutput):
        return list_unit_signals(nortech_api, unit.id, pagination_options)

    unit_input = parse_unit_input(unit)
    response = nortech_api.get(
        url=f"/api/v1/workspaces/{unit_input.workspace}/assets/{unit_input.asset}/divisions/{unit_input.division}/units/{unit_input.unit}/signals",
        params=pagination_options.model_dump(exclude_none=True, by_alias=True) if pagination_options else None,
    )
    validate_response(response)

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
    nortech_api: NortechAPI, signal: int | SignalInputDict | SignalInput | SignalOutput | SignalListOutput
):
    if isinstance(signal, int):
        return get_signal(nortech_api, signal)
    if isinstance(signal, SignalListOutput):
        return get_signal(nortech_api, signal.id)

    signal_input = parse_signal_input(signal)
    response = nortech_api.get(
        url=f"/api/v1/workspaces/{signal_input.workspace}/assets/{signal_input.asset}/divisions/{signal_input.division}/units/{signal_input.unit}/signals/{signal_input.signal}",
    )
    validate_response(response)
    return SignalOutput.model_validate(response.json())


def list_workspace_asset_division_device_signals(
    nortech_api: NortechAPI,
    device: DeviceInputDict | DeviceInput | DeviceOutput | DeviceListOutput,
    pagination_options: PaginationOptions[
        Literal["id", "name", "physical_unit", "data_type", "description", "long_description"]
    ]
    | None = None,
):
    if isinstance(device, DeviceListOutput):
        return list_device_signals(nortech_api, device.id, pagination_options)

    device_input = parse_device_input(device)
    response = nortech_api.get(
        url=f"/api/v1/workspaces/{device_input.workspace}/assets/{device_input.asset}/divisions/{device_input.division}/devices/{device_input.device}/signals",
        params=pagination_options.model_dump(exclude_none=True, by_alias=True) if pagination_options else None,
    )
    validate_response(response)

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
    nortech_api: NortechAPI, signal: SignalDeviceInputDict | SignalDeviceInput | SignalOutput | SignalListOutput
):
    if isinstance(signal, SignalListOutput):
        return get_signal(nortech_api, signal.id)

    signal_input = parse_signal_device_input(signal)
    response = nortech_api.get(
        url=f"/api/v1/workspaces/{signal_input.workspace}/assets/{signal_input.asset}/divisions/{signal_input.division}/devices/{signal_input.device}/signals/{signal_input.signal}",
    )
    validate_response(response)
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
    validate_response(response)

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
    validate_response(response)

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
    validate_response(response)

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
    validate_response(response)

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
    validate_response(response)

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
    validate_response(response)
    return SignalOutput.model_validate(response.json())


def _get_signals(nortech_api: NortechAPI, signals: Sequence[SignalInput | SignalInputDict | SignalListOutput | int]):
    def signal_to_api_input(signal: SignalInput | SignalInputDict | SignalListOutput | int):
        if isinstance(signal, SignalListOutput):
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
    nortech_api: NortechAPI, signals: Sequence[SignalInput | SignalInputDict | SignalOutput | SignalListOutput | int]
):
    signal_ids: List[int] = [
        signal.id if isinstance(signal, SignalListOutput) else signal
        for signal in signals
        if isinstance(signal, int) or isinstance(signal, SignalListOutput)
    ]
    signal_list_from_ids = _get_signals(nortech_api, signal_ids)

    signal_inputs: list[SignalInput] = [
        parse_signal_input(signal)
        for signal in signals
        if not isinstance(signal, int) and not isinstance(signal, SignalListOutput)
    ]
    return [signal.to_signal_input() for signal in signal_list_from_ids] + signal_inputs
