from polars import DataFrame, LazyFrame

from nortech.datatools.repositories.S3 import get_lazy_polars_df_from_S3
from nortech.datatools.services.config import get_parquet_paths_from_search_list
from nortech.datatools.values.signals import (
    TimeWindow,
    get_signal_list_from_search_json,
)


def get_lazy_polars_df(search_json: str, time_window: TimeWindow) -> LazyFrame:
    """
    This function retrieves a polars LazyFrame based on the provided search_json and time_window.

    Parameters
    ----------
    search_json : str
        The json string result from Signal search.
    time_window : TimeWindow
        The time window for which to retrieve data.

    Returns
    -------
    LazyFrame
        A LazyFrame containing the data.

    Raises
    ------
    NoSignalsRequestedError
        Raised when no signals are requested.
    InvalidTimeWindow
        Raised when the start date is after the end date.

    Example
    -------
    >>> from nortech.datatools import get_lazy_polars_df, TimeWindow
    >>> search_json = \"""[
        {
            "name": "signal_1",
            "dataType": "float",
            "alias": 0,
            "asset": {
                "name": "asset_1"
            },
            "division": {
                "name": "division_1"
            },
            "unit": {
                "name": "unit_1"
            },
            "storage": {
                "bucket": "nortech-test",
                "path": "scope_1_group_0"
            }
        },
        {
            "name": "signal_2",
            "dataType": "float",
            "alias": 1,
            "asset": {
                "name": "asset_1"
            },
            "division": {
                "name": "division_1"
            },
            "unit": {
                "name": "unit_1"
            },
            "storage": {
                "bucket": "nortech-test",
                "path": "scope_1_group_0"
            }
        },
        {
            "name": "signal_3",
            "dataType": "float",
            "alias": 0,
            "asset": {
                "name": "asset_2"
            },
            "division": {
                "name": "division_2"
            },
            "unit": {
                "name": "unit_2"
            },
            "storage": {
                "bucket": "nortech-test",
                "path": "scope_1_group_1"
            }
        }
    ]\"""
    >>> time_window = TimeWindow(
                start=datetime(2020, 1, 1),
                end=datetime(2020, 1, 1),
        )
    >>> lazy_polars_df = get_lazy_polars_df(search_json=search_json, time_window=time_window)
    >>> lazy_polars_df.columns
        ['timestamp', 'asset_1/division_1/unit_1/signal_1', 'asset_1/division_1/unit_1/signal_2', 'asset_2/division_2/unit_2/signal_3']
    """
    signal_list = get_signal_list_from_search_json(search_json=search_json)
    parquet_paths = get_parquet_paths_from_search_list(signal_list=signal_list)
    lazy_polars_df = get_lazy_polars_df_from_S3(
        parquet_paths=parquet_paths, time_window=time_window
    )

    return lazy_polars_df


def get_polars_df(search_json: str, time_window: TimeWindow) -> DataFrame:
    """
    This function retrieves a polars DataFrame based on the provided search_json and time_window.

    Parameters
    ----------
    search_json : str
        The json string result from Signal search.
    time_window : TimeWindow
        The time window for which to retrieve data.

    Returns
    -------
    LazyFrame
        A LazyFrame containing the data.

    Raises
    ------
    NoSignalsRequestedError
        Raised when no signals are requested.
    InvalidTimeWindow
        Raised when the start date is after the end date.

    Example
    -------
    >>> from nortech.datatools import get_polars_df, TimeWindow
    >>> search_json = \"""[
        {
            "name": "signal_1",
            "dataType": "float",
            "alias": 0,
            "asset": {
                "name": "asset_1"
            },
            "division": {
                "name": "division_1"
            },
            "unit": {
                "name": "unit_1"
            },
            "storage": {
                "bucket": "nortech-test",
                "path": "scope_1_group_0"
            }
        },
        {
            "name": "signal_2",
            "dataType": "float",
            "alias": 1,
            "asset": {
                "name": "asset_1"
            },
            "division": {
                "name": "division_1"
            },
            "unit": {
                "name": "unit_1"
            },
            "storage": {
                "bucket": "nortech-test",
                "path": "scope_1_group_0"
            }
        },
        {
            "name": "signal_3",
            "dataType": "float",
            "alias": 0,
            "asset": {
                "name": "asset_2"
            },
            "division": {
                "name": "division_2"
            },
            "unit": {
                "name": "unit_2"
            },
            "storage": {
                "bucket": "nortech-test",
                "path": "scope_1_group_1"
            }
        }
    ]\"""
    >>> time_window = TimeWindow(
                start=datetime(2020, 1, 1),
                end=datetime(2020, 1, 1),
        )
    >>> polars_df = get_polars_df(search_json=search_json, time_window=time_window)
    >>> polars_df.columns
        ['timestamp', 'asset_1/division_1/unit_1/signal_1', 'asset_1/division_1/unit_1/signal_2', 'asset_2/division_2/unit_2/signal_3']
    """
    lazy_polars_df = get_lazy_polars_df(
        search_json=search_json, time_window=time_window
    )
    polars_df = lazy_polars_df.collect()

    return polars_df
