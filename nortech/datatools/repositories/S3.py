from datetime import datetime, timedelta, timezone
from os import getenv
from typing import List, Tuple

import pyarrow as pa
from polars import Expr, LazyFrame, col, from_epoch, scan_pyarrow_dataset
from pyarrow import DataType, Schema, schema
from pyarrow.dataset import dataset, partitioning
from s3fs import S3FileSystem

from nortech.datatools.values.errors import InvalidTimeWindow, NoSignalsRequestedError
from nortech.datatools.values.signals import ParquetPaths, SignalConfig, TimeWindow


def generate_date_filter(start_date: datetime, end_date: datetime) -> Expr:
    """
    Generate a filter for a range of dates.

    Parameters
    ----------
    start_date : datetime
        The start date of the range.
    end_date : datetime
        The end date of the range.

    Returns
    -------
    date_filter : Expr
        A filter expression that can be used to filter a DataFrame.

    Raises
    ------
    InvalidTimeWindow
        If the start date is after the end date.
    """
    date_filter = None
    current_date = start_date
    while current_date <= end_date:
        day_filter = (
            (col("year") == current_date.year)
            & (col("month") == current_date.month)
            & (col("day") == current_date.day)
        )
        if date_filter is None:
            date_filter = day_filter
        else:
            date_filter = date_filter | day_filter
        current_date += timedelta(days=1)

    if date_filter is None:
        raise InvalidTimeWindow()

    return date_filter


def get_select_columns(columns: List[SignalConfig]) -> List[Expr]:
    """
    Generate a list of column expressions for the provided columns.

    Parameters
    ----------
    columns : List[SignalConfig]
        A list of SignalConfig objects, each representing a column in the data.

    Returns
    -------
    List[Expr]
        A list of column expressions.
    """
    select_columns = [col("timestamp"), col("year"), col("month"), col("day")]
    for signal in columns:
        select_columns.append(col(signal.column_name).alias(signal.ADUS))

    return select_columns


def get_pyarrow_schema(columns: List[SignalConfig]) -> Schema:
    """
    Generate a PyArrow schema based on the provided columns.

    Parameters
    ----------
    columns : List[SignalConfig]
        A list of SignalConfig objects, each representing a column in the data.

    Returns
    -------
    Schema
        A PyArrow Schema object representing the schema of the data.
    """
    fields: List[Tuple[str, DataType]] = [
        ("timestamp", "int64"),
        ("year", "int32"),
        ("month", "int32"),
        ("day", "int32"),
    ]
    for signal in columns:
        if signal.data_type == "float":
            signal.data_type = "double"
        elif signal.data_type == "json":
            signal.data_type = "string"

        fields.append(
            (
                signal.column_name,
                signal.data_type if signal.data_type != "float" else "double",
            )
        )

    return schema(fields)


def get_lazy_polars_df_from_S3(
    parquet_paths: ParquetPaths, time_window: TimeWindow
) -> LazyFrame:
    """
    This function retrieves a LazyFrame from S3 based on the provided parquet paths and time window.

    Parameters
    ----------
    parquet_paths : ParquetPaths
        A dictionary mapping S3 locations to lists of SignalConfig objects.
    time_window : TimeWindow
        The time window for which to retrieve data.

    Returns
    -------
    LazyFrame
        A LazyFrame containing the data from S3.

    Raises
    ------
    NoSignalsRequestedError
        Raised when no signals are requested.
    InvalidTimeWindow
        Raised when the start date is after the end date.
    """
    start = time_window.start.astimezone(timezone.utc)
    end = time_window.end.astimezone(timezone.utc)

    s3_file_system = S3FileSystem(endpoint_url=getenv("AWS_ENDPOINT_URL"))

    lazy_dfs = None
    for location, columns in parquet_paths.items():
        try:
            pyarrow_ds = dataset(
                location,
                format="parquet",
                filesystem=s3_file_system,
                schema=get_pyarrow_schema(columns=columns),
                partitioning=partitioning(
                    pa.schema(
                        [
                            ("year", pa.int32()),
                            ("month", pa.int32()),
                            ("day", pa.int32()),
                        ]
                    ),
                    flavor="hive",
                ),
                partition_base_dir=location,
            )
            lazy_df = scan_pyarrow_dataset(pyarrow_ds)
        except FileNotFoundError:
            lazy_df = LazyFrame(
                {
                    **{column.column_name: [] for column in columns},
                    "timestamp": [],
                    "year": [],
                    "month": [],
                    "day": [],
                }
            )

        select_columns = get_select_columns(columns=columns)
        lazy_df_select = lazy_df.select(select_columns)

        lazy_df_partition = lazy_df_select.filter(generate_date_filter(start, end))

        lazy_df_without_partition_columns = lazy_df_partition.drop(
            ["year", "month", "day"]
        )

        lazy_df_window = (
            lazy_df_without_partition_columns.with_columns(
                from_epoch("timestamp", "ms").dt.replace_time_zone("UTC"),
            )
            .filter(
                col("timestamp").is_between(
                    lower_bound=start,
                    upper_bound=end,
                    closed="right",
                )
            )
            .with_columns(
                col("timestamp").dt.convert_time_zone(str(time_window.start.tzinfo))
            )
        )

        if lazy_dfs is not None:
            lazy_dfs = lazy_dfs.join(lazy_df_window, on="timestamp", how="outer")
        else:
            lazy_dfs = lazy_df_window

    if lazy_dfs is None:
        raise NoSignalsRequestedError()

    return lazy_dfs.unique("timestamp").sort("timestamp")
