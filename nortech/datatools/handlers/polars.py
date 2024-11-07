from __future__ import annotations

from polars import DataFrame, LazyFrame, concat, lit
from urllib3.util import Timeout

from nortech.core.gateways.nortech_api import (
    NortechAPI,
)
from nortech.core.services.signal import (
    parse_signal_input_or_output_or_id_union_to_signal_input,
)
from nortech.core.values.signal import SignalInput, SignalInputDict, SignalListOutput, SignalOutput
from nortech.datatools.services.nortech_api import (
    get_lazy_polars_df_from_cold_storage,
    get_lazy_polars_df_from_hot_storage,
)
from nortech.datatools.services.storage import (
    cast_hot_schema_to_cold_schema,
    get_hot_and_cold_time_windows,
)
from nortech.datatools.values.windowing import ColdWindow, HotWindow, TimeWindow


def get_lazy_polars_df(
    nortech_api: NortechAPI,
    signals: list[SignalInput | SignalInputDict | SignalOutput | SignalListOutput | int],
    time_window: TimeWindow,
    timeout: Timeout | None = None,
) -> LazyFrame:
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
    signals: list[SignalInput | SignalInputDict | SignalOutput | SignalListOutput | int],
    time_window: TimeWindow,
    timeout: Timeout | None = None,
) -> DataFrame:
    lazy_polars_df = get_lazy_polars_df(nortech_api, signals, time_window, timeout)
    polars_df = lazy_polars_df.collect()

    return polars_df
