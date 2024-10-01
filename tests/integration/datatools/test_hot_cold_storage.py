from datetime import datetime, timedelta, timezone
from io import BytesIO
from typing import List
from unittest.mock import patch

import numpy as np
import pandas as pd
import pandas.testing as pdt

from nortech.datatools.handlers.pandas import get_df
from nortech.datatools.services.customer_api import (
    hash_signal_ADUS,
)
from nortech.datatools.values.signals import TimeWindow
from nortech.shared.gateways.customer_api import CustomerAPISettings


@patch("nortech.datatools.handlers.polars.get_lazy_polars_df_from_customer_api_historical_data")
def test_get_df_hot(
    get_cold_storage_mock,
    search_json: str,
    signals: List[str],
    customer_api_settings: CustomerAPISettings,
    requests_mock,
):
    end = datetime.now(timezone.utc) + timedelta(seconds=10)
    time_window = TimeWindow(
        start=end - timedelta(days=1),
        end=end,
    )

    csv_df = pd.DataFrame(
        {
            "timestamp": pd.date_range(end=end, periods=24, freq="h").round("ms").astype("datetime64[ms, UTC]"),
            **{signal: np.random.rand(24) for signal in signals},
        }
    )

    csv_content = BytesIO()
    csv_df.to_csv(csv_content, index=False)
    csv_content.seek(0)

    requests_mock.post(
        customer_api_settings.URL + "/timescale",
        content=csv_content.getvalue(),
    )

    df = get_df(search_json=search_json, time_window=time_window)

    get_cold_storage_mock.assert_not_called()
    assert requests_mock.call_count == 1

    pdt.assert_frame_equal(df, csv_df.set_index("timestamp"))


@patch("nortech.datatools.handlers.polars.get_lazy_polars_df_from_customer_api_historical_data")
def test_get_df_hot_empty(
    get_cold_storage_mock,
    search_json: str,
    signals: List[str],
    customer_api_settings: CustomerAPISettings,
    requests_mock,
):
    end = datetime.now(timezone.utc) + timedelta(seconds=10)
    time_window = TimeWindow(
        start=end - timedelta(days=1),
        end=end,
    )

    requests_mock.post(
        customer_api_settings.URL + "/timescale",
        status_code=404,
    )

    df = get_df(search_json=search_json, time_window=time_window)

    get_cold_storage_mock.assert_not_called()
    assert requests_mock.call_count == 1

    pdt.assert_frame_equal(
        df,
        pd.DataFrame(columns=["timestamp"] + signals)
        .astype(
            {
                "timestamp": "datetime64[ms, UTC]",
                **{signal: "float64" for signal in signals},
            }
        )
        .set_index("timestamp"),
    )


@patch("nortech.datatools.handlers.polars.get_lazy_polars_df_from_customer_api")
def test_get_df_cold(
    get_hot_storage_mock,
    search_json: str,
    signals: List[str],
    customer_api_settings: CustomerAPISettings,
    requests_mock,
):
    end = datetime.now(timezone.utc) - timedelta(days=1, seconds=10)
    time_window = TimeWindow(
        start=end - timedelta(days=1),
        end=end,
    )

    parquet_df = pd.DataFrame(
        {
            "timestamp": pd.date_range(end=end, periods=24, freq="h").round("ms").astype("datetime64[ms, UTC]"),
            **{hash_signal_ADUS(signal): np.random.rand(24) for signal in signals},
        }
    )

    parquet_content = BytesIO()
    parquet_df.to_parquet(parquet_content, index=False, engine="pyarrow")
    parquet_content.seek(0)

    parquet_url = "http://parquet.file"

    requests_mock.post(
        customer_api_settings.URL + "/api/v1/historical-data/sync",
        json={"outputFile": parquet_url},
    )

    requests_mock.get(
        parquet_url,
        content=parquet_content.getvalue(),
    )

    df = get_df(search_json=search_json, time_window=time_window)

    get_hot_storage_mock.assert_not_called()
    assert requests_mock.call_count == 2

    pdt.assert_frame_equal(
        df,
        parquet_df.rename(columns={hash_signal_ADUS(signal): f"{signal}" for signal in signals}).set_index("timestamp"),
    )


@patch("nortech.datatools.handlers.polars.get_lazy_polars_df_from_customer_api")
def test_get_df_cold_empty(
    get_hot_storage_mock,
    search_json: str,
    signals: List[str],
    customer_api_settings: CustomerAPISettings,
    requests_mock,
):
    end = datetime.now(timezone.utc) - timedelta(days=1, seconds=10)
    time_window = TimeWindow(
        start=end - timedelta(days=1),
        end=end,
    )

    requests_mock.post(
        customer_api_settings.URL + "/api/v1/historical-data/sync",
        status_code=404,
    )

    df = get_df(search_json=search_json, time_window=time_window)

    get_hot_storage_mock.assert_not_called()
    assert requests_mock.call_count == 1

    pdt.assert_frame_equal(
        df,
        pd.DataFrame(columns=["timestamp"] + signals)
        .astype(
            {
                "timestamp": "datetime64[ms, UTC]",
                **{signal: "float64" for signal in signals},
            }
        )
        .set_index("timestamp"),
    )


def test_get_df_hot_and_cold(
    search_json: str, signals: List[str], customer_api_settings: CustomerAPISettings, requests_mock
):
    end = datetime.now(timezone.utc)
    start_hot = end_cold = end - timedelta(days=1, seconds=10)
    start_cold = start_hot - timedelta(days=1)

    time_window = TimeWindow(
        start=start_cold,
        end=end,
    )

    csv_df = pd.DataFrame(
        {
            "timestamp": pd.date_range(end=end, periods=24, freq="h").round("ms").astype("datetime64[ms, UTC]"),
            **{signal: np.random.rand(24) for signal in signals},
        }
    )
    parquet_df = pd.DataFrame(
        {
            "timestamp": pd.date_range(end=end_cold, periods=24, freq="h").round("ms").astype("datetime64[ms, UTC]"),
            **{hash_signal_ADUS(signal): np.random.rand(24) for signal in signals},
        }
    )

    csv_content = BytesIO()
    csv_df.to_csv(csv_content, index=False)
    csv_content.seek(0)

    requests_mock.post(
        customer_api_settings.URL + "/timescale",
        content=csv_content.getvalue(),
    )

    parquet_content = BytesIO()
    parquet_df.to_parquet(parquet_content, index=False, engine="pyarrow")
    parquet_content.seek(0)

    parquet_url = "http://parquet.file"

    requests_mock.post(
        customer_api_settings.URL + "/api/v1/historical-data/sync",
        json={"outputFile": parquet_url},
    )

    requests_mock.get(
        parquet_url,
        content=parquet_content.getvalue(),
    )

    df = get_df(search_json=search_json, time_window=time_window)

    assert requests_mock.call_count == 3

    pdt.assert_frame_equal(
        df.sort_index().reset_index(drop=True),
        pd.concat(
            [
                csv_df,
                parquet_df.rename(columns={hash_signal_ADUS(signal): f"{signal}" for signal in signals}),
            ]
        )
        .set_index("timestamp")
        .sort_index()
        .reset_index(drop=True),
    )


def test_get_df_hot_and_cold_cold_empty(
    search_json: str, signals: List[str], customer_api_settings: CustomerAPISettings, requests_mock
):
    end = datetime.now(timezone.utc)
    start_hot = end - timedelta(days=1, seconds=10)
    start_cold = start_hot - timedelta(days=1)

    time_window = TimeWindow(
        start=start_cold,
        end=end,
    )

    csv_df = pd.DataFrame(
        {
            "timestamp": pd.date_range(end=end, periods=24, freq="h").round("ms").astype("datetime64[ms, UTC]"),
            **{signal: np.random.rand(24) for signal in signals},
        }
    )

    csv_content = BytesIO()
    csv_df.to_csv(csv_content, index=False)
    csv_content.seek(0)

    requests_mock.post(
        customer_api_settings.URL + "/timescale",
        content=csv_content.getvalue(),
    )

    requests_mock.post(
        customer_api_settings.URL + "/api/v1/historical-data/sync",
        status_code=404,
    )

    df = get_df(search_json=search_json, time_window=time_window)

    assert requests_mock.call_count == 2

    pdt.assert_frame_equal(df, csv_df.set_index("timestamp"))


def test_get_df_hot_and_cold_hot_empty(
    search_json: str, signals: List[str], customer_api_settings: CustomerAPISettings, requests_mock
):
    end = datetime.now(timezone.utc)
    start_hot = end_cold = end - timedelta(days=1, seconds=10)
    start_cold = start_hot - timedelta(days=1)

    time_window = TimeWindow(
        start=start_cold,
        end=end,
    )

    parquet_df = pd.DataFrame(
        {
            "timestamp": pd.date_range(end=end_cold, periods=24, freq="h").round("ms").astype("datetime64[ms, UTC]"),
            **{hash_signal_ADUS(signal): np.random.rand(24) for signal in signals},
        }
    )

    parquet_content = BytesIO()
    parquet_df.to_parquet(parquet_content, index=False, engine="pyarrow")
    parquet_content.seek(0)

    parquet_url = "http://parquet.file"

    requests_mock.post(
        customer_api_settings.URL + "/api/v1/historical-data/sync",
        json={"outputFile": parquet_url},
    )

    requests_mock.get(
        parquet_url,
        content=parquet_content.getvalue(),
    )

    requests_mock.post(
        customer_api_settings.URL + "/timescale",
        status_code=404,
    )

    df = get_df(search_json=search_json, time_window=time_window)

    assert requests_mock.call_count == 3

    pdt.assert_frame_equal(
        df,
        parquet_df.rename(columns={hash_signal_ADUS(signal): f"{signal}" for signal in signals}).set_index("timestamp"),
    )
