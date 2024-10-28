from __future__ import annotations

from datetime import datetime, timedelta, timezone

from polars import LazyFrame, col

from nortech.datatools.values.windowing import ColdWindow, HotColdWindow, HotWindow, TimeWindow


def get_hot_and_cold_time_windows(
    time_window: TimeWindow,
) -> HotColdWindow | HotWindow | ColdWindow:
    start = time_window.start.astimezone(timezone.utc)
    end = time_window.end.astimezone(timezone.utc)

    hot_storage_delta = end - (datetime.now(tz=timezone.utc) - timedelta(days=1))

    hot_storage_start = end - hot_storage_delta
    hot_storage_end = end

    if hot_storage_start > hot_storage_end:
        return ColdWindow(
            time_window=time_window,
        )

    cold_storage_start = start
    cold_storage_end = end - hot_storage_delta

    if cold_storage_start > cold_storage_end:
        return HotWindow(
            time_window=time_window,
        )

    hot_storage_time_window = TimeWindow(
        start=hot_storage_start.astimezone(time_window.start.tzinfo),
        end=hot_storage_end.astimezone(time_window.end.tzinfo),
    )

    cold_storage_time_window = TimeWindow(
        start=cold_storage_start.astimezone(time_window.start.tzinfo),
        end=cold_storage_end.astimezone(time_window.end.tzinfo),
    )

    return HotColdWindow(
        hot_storage_time_window=hot_storage_time_window,
        cold_storage_time_window=cold_storage_time_window,
    )


def cast_hot_schema_to_cold_schema(cold_lazy_polars_df: LazyFrame, hot_lazy_polars_df: LazyFrame):
    cold_schema = cold_lazy_polars_df.collect_schema()

    # Iterate over the schema items and cast the hot DataFrame columns to match the cold DataFrame types
    for column_name, dtype in cold_schema.items():
        if column_name in hot_lazy_polars_df.collect_schema().names():
            hot_lazy_polars_df = hot_lazy_polars_df.with_columns(col(column_name).cast(dtype))

    return hot_lazy_polars_df
