from __future__ import annotations

from polars import DataFrame, LazyFrame, concat, lit
from urllib3.util import Timeout

from nortech.common.gateways.nortech_api import (
    NortechAPI,
)
from nortech.datatools.services.nortech_api import (
    get_lazy_polars_df_from_cold_storage,
    get_lazy_polars_df_from_hot_storage,
)
from nortech.datatools.services.storage import (
    cast_hot_schema_to_cold_schema,
    get_hot_and_cold_time_windows,
)
from nortech.datatools.values.windowing import ColdWindow, HotWindow, TimeWindow
from nortech.metadata.services.signal import (
    parse_signal_input_or_output_or_id_union_to_signal_input,
)
from nortech.metadata.values.signal import SignalInput, SignalInputDict, SignalOutput


def get_lazy_polars_df(
    nortech_api: NortechAPI,
    signals: list[SignalInput | SignalInputDict | SignalOutput | int],
    time_window: TimeWindow,
    timeout: Timeout | None = None,
) -> LazyFrame:
    """
    Retrieves a polars LazyFrame for the specified signals within the given time window.

    Parameters
    ----------
    nortech_api : NortechAPI
        The API client for Nortech API.
    signals : list[SignalInput | SignalInputDict | SignalOutput | int]
        A list of signals to retrieve, which can be of the following types:
        - SignalInputDict: A dictionary representation of a signal input.
          Example: {"workspace": "my_workspace", "asset": "my_asset", "division": "my_division", "unit": "my_unit", "signal": "my_signal"}
        - SignalInput: A pydantic model representing an input signal.
          Example: SignalInput(workspace="my_workspace", asset="my_asset", division="my_division", unit="my_unit", signal="my_signal")
        - SignalOutput: A pydantic model representing an output signal. Obtained
          from a signal metadata request.
        - int: Corresponds to a signalId, which is an integer identifier for a signal.
          Example: 789
    time_window : TimeWindow
        The time window for which data should be retrieved.
    timeout : Timeout | None, optional
        The timeout setting for the API request.

    Returns
    -------
    LazyFrame
        A polars LazyFrame containing the data.

    Raises
    ------
    NoSignalsRequestedError
        Raised when no signals are requested.
    InvalidTimeWindow
        Raised when the start date is after the end date.

    Example
    -------
    >>> from datetime import datetime
    >>> from nortech.datatools import get_lazy_polars_df, TimeWindow
    >>> from nortech.metadata.values.signal import SignalInput
    >>>
    >>> # Define signals to retrieve
    >>> signal1 = {"workspace": "workspace1", "asset": "asset1", "division": "division1", "unit": "unit1", "signal": "signal1"}
    >>> signal2 = 789  # Signal ID
    >>> signal3 = SignalInput(workspace="workspace2", asset="asset2", division="division2", unit="unit2", signal="signal3")
    >>>
    >>> # Define the time window for data retrieval
    >>> my_time_window = TimeWindow(start=datetime(2020, 1, 1), end=datetime(2020, 1, 31))
    >>>
    >>> # Call the get_lazy_polars_df function
    >>> lazy_polars_df = get_lazy_polars_df(
    ...     nortech_api=nortech_api,
    ...     signals=[signal1, signal2, signal3],
    ...     time_window=my_time_window
    ... )
    >>> lazy_polars_df.columns
    [
        'timestamp',
        'workspace_1/asset_1/division_1/unit_1/signal_1',
        'workspace_1/asset_1/division_1/unit_1/signal_2',
        'workspace_2/asset_2/division_2/unit_2/signal_3'
    ]
    """
    signal_inputs = parse_signal_input_or_output_or_id_union_to_signal_input(nortech_api, signals)
    time_windows = get_hot_and_cold_time_windows(time_window=time_window)

    if isinstance(time_windows, ColdWindow):
        return get_lazy_polars_df_from_cold_storage(
            nortech_api=nortech_api,
            signals=signal_inputs,
            time_window=time_windows.time_window,
            timeout=timeout,
        )

    if isinstance(time_windows, HotWindow):
        return get_lazy_polars_df_from_hot_storage(
            nortech_api=nortech_api,
            signals=signal_inputs,
            time_window=time_windows.time_window,
            timeout=timeout,
        )

    hot_lazy_polars_df = get_lazy_polars_df_from_hot_storage(
        nortech_api=nortech_api,
        signals=signal_inputs,
        time_window=time_windows.hot_storage_time_window,
        timeout=timeout,
    )

    cold_lazy_polars_df = get_lazy_polars_df_from_cold_storage(
        nortech_api=nortech_api,
        signals=signal_inputs,
        time_window=time_windows.cold_storage_time_window,
        timeout=timeout,
    )

    hot_lazy_polars_df_casted = cast_hot_schema_to_cold_schema(
        cold_lazy_polars_df=cold_lazy_polars_df,
        hot_lazy_polars_df=hot_lazy_polars_df,
    )

    # Get all unique columns from both dataframes and sort them
    all_columns = sorted(
        set(hot_lazy_polars_df_casted.collect_schema().names()).union(set(cold_lazy_polars_df.collect_schema().names()))
    )

    # Add missing columns in hot_lazy_polars_df_casted
    missing_in_hot = set(all_columns) - set(hot_lazy_polars_df_casted.collect_schema().names())
    for column in missing_in_hot:
        hot_lazy_polars_df_casted = hot_lazy_polars_df_casted.with_columns(lit(None).alias(column))

    # Add missing columns in cold_lazy_polars_df
    missing_in_cold = set(all_columns) - set(cold_lazy_polars_df.collect_schema().names())
    for column in missing_in_cold:
        cold_lazy_polars_df = cold_lazy_polars_df.with_columns(lit(None).alias(column))

    # Reorder columns to match the sorted list
    hot_lazy_polars_df_casted = hot_lazy_polars_df_casted.select(all_columns)
    cold_lazy_polars_df = cold_lazy_polars_df.select(all_columns)

    # Now concatenate the dataframes
    return concat([hot_lazy_polars_df_casted, cold_lazy_polars_df]).unique("timestamp").sort("timestamp")


def get_polars_df(
    nortech_api: NortechAPI,
    signals: list[SignalInput | SignalInputDict | SignalOutput | int],
    time_window: TimeWindow,
) -> DataFrame:
    """
    Retrieves a polars DataFrame for the specified signals within the given time window.

    Parameters
    ----------
    nortech_api : NortechAPI
        The API client for Nortech API.
    signals : list[SignalInput | SignalInputDict | SignalOutput | int]
        A list of signals to retrieve, which can be of the following types:
        - SignalInputDict: A dictionary representation of a signal input.
          Example: {"workspace": "my_workspace", "asset": "my_asset", "division": "my_division", "unit": "my_unit", "signal": "my_signal"}
        - SignalInput: A pydantic model representing an input signal.
          Example: SignalInput(workspace="my_workspace", asset="my_asset", division="my_division", unit="my_unit", signal="my_signal")
        - SignalOutput: A pydantic model representing an output signal. Obtained
          from a signal metadata request.
        - int: Corresponds to a signalId, which is an integer identifier for a signal.
          Example: 789
    time_window : TimeWindow
        The time window for which data should be retrieved.

    Returns
    -------
    DataFrame
        A polars DataFrame containing the data.

    Raises
    ------
    NoSignalsRequestedError
        Raised when no signals are requested.
    InvalidTimeWindow
        Raised when the start date is after the end date.

    Example
    -------
    >>> from datetime import datetime
    >>> from nortech.datatools import get_polars_df, TimeWindow
    >>> from nortech.metadata.values.signal import SignalInput
    >>>
    >>> # Define signals to retrieve
    >>> signal1 = {"workspace": "workspace1", "asset": "asset1", "division": "division1", "unit": "unit1", "signal": "signal1"}
    >>> signal2 = 789  # Signal ID
    >>> signal3 = SignalInput(workspace="workspace2", asset="asset2", division="division2", unit="unit2", signal="signal3")
    >>>
    >>> # Define the time window for data retrieval
    >>> my_time_window = TimeWindow(start=datetime(2020, 1, 1), end=datetime(2020, 1, 31))
    >>>
    >>> # Call the get_polars_df function
    >>> polars_df = get_polars_df(
    ...     nortech_api=nortech_api,
    ...     signals=[signal1, signal2, signal3],
    ...     time_window=my_time_window
    ... )
    >>> polars_df.columns
    [
        'timestamp',
        'workspace_1/asset_1/division_1/unit_1/signal_1',
        'workspace_1/asset_1/division_1/unit_1/signal_2',
        'workspace_2/asset_2/division_2/unit_2/signal_3'
    ]
    """
    lazy_polars_df = get_lazy_polars_df(nortech_api, signals, time_window)
    polars_df = lazy_polars_df.collect()

    return polars_df
