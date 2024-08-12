import os
import tempfile
from datetime import datetime, timedelta, timezone
from typing import Dict, Union

import pyarrow as pa
import pyarrow.parquet as pq
from polars import LazyFrame, col

from nortech.datatools.values.signals import TimeWindow
from nortech.datatools.values.windowing import ColdWindow, HotColdWindow, HotWindow


def get_hot_and_cold_time_windows(
    time_window: TimeWindow,
) -> Union[HotColdWindow, HotWindow, ColdWindow]:
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
    cold_schema = cold_lazy_polars_df.schema

    # Iterate over the schema items and cast the hot DataFrame columns to match the cold DataFrame types
    for column_name, dtype in cold_schema.items():
        if column_name in hot_lazy_polars_df.columns:
            hot_lazy_polars_df = hot_lazy_polars_df.with_columns(col(column_name).cast(dtype))

    return hot_lazy_polars_df


def rename_parquet_columns(parquet_file_path: str, column_name_mapping: Dict[str, str]):
    parquet_file = pq.ParquetFile(parquet_file_path)

    old_schema = parquet_file.schema_arrow
    new_fields = [pa.field(column_name_mapping.get(field.name, field.name), field.type) for field in old_schema]
    new_schema = pa.schema(new_fields)

    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_filename = tmp_file.name

    with pq.ParquetWriter(tmp_filename, new_schema) as writer:
        for batch in parquet_file.iter_batches():
            new_batch = pa.RecordBatch.from_arrays(batch.columns, schema=new_schema)
            writer.write_batch(new_batch)

    os.replace(tmp_filename, parquet_file_path)
