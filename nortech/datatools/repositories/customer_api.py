import hashlib
from datetime import timezone
from enum import Enum
from io import BytesIO
from os import environ, getenv
from tempfile import NamedTemporaryFile
from typing import List

from pandas import DataFrame, read_csv, to_datetime
from polars import Datetime, col, from_pandas, read_parquet
from pydantic import BaseModel, field_serializer
from requests import Session
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from nortech.datatools.values.signals import (
    Signal,
    TimeWindow,
)

customer_API_URL = getenv("CUSTOMER_API_URL", "https://api.apps.nor.tech")
session = Session()
retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504], allowed_methods=["GET","POST"], raise_on_status=False)
session.mount(customer_API_URL, HTTPAdapter(max_retries=retries))


class GetHotStorageSignals(BaseModel):
    signals: List[Signal]
    time_window: TimeWindow

    @field_serializer("time_window")
    def serialize_dt(self, time_window: TimeWindow, _info):
        return {
            "start": time_window.start.astimezone(timezone.utc)
            .isoformat()
            .replace("+00:00", "Z"),
            "end": time_window.end.astimezone(timezone.utc)
            .isoformat()
            .replace("+00:00", "Z"),
        }


class Format(str, Enum):
    PARQUET = "parquet"
    JSON = "json"
    CSV = "csv"


def get_lazy_polars_df_from_customer_api(
    signal_list: List[Signal], time_window: TimeWindow
):
    customer_API_token = environ["CUSTOMER_API_TOKEN"]

    hot_storage_endpoint = customer_API_URL + "/timescale"

    response = session.post(
        url=hot_storage_endpoint,
        json=GetHotStorageSignals(
            signals=signal_list,
            time_window=time_window,
        ).model_dump(),
        headers={"Authorization": f"Bearer {customer_API_token}"},
    )

    try:
        assert response.status_code == 200 or response.status_code == 404
    except AssertionError:
        if response.status_code == 500:
            raise AssertionError(
                f"Failed to get hot storage data. "
                f"Status code: {response.status_code}. "
                f"Response: {response.json()}"
            )
        else:
            raise AssertionError(
                f"Failed to get hot storage data. "
                f"Status code: {response.status_code}. "
            )

    if response.status_code == 200:
        with NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(response.content)
            tmp_file_path = tmp_file.name

        df = read_csv(tmp_file_path, low_memory=False)
        df["timestamp"] = to_datetime(df["timestamp"], format="mixed")
    else:
        df = DataFrame({signal.ADUS: [] for signal in signal_list})
        df["timestamp"] = []

    return (
        (
            from_pandas(df)
            .with_columns(col("timestamp").cast(Datetime("ms")))
            .lazy()
            .with_columns(
                col("timestamp").dt.replace_time_zone("UTC"),
            )
            .with_columns(
                col("timestamp").dt.convert_time_zone(str(time_window.start.tzinfo)),
            )
        )
        .unique("timestamp")
        .sort("timestamp")
    )


def hash_signal_ADUS(signal_name: str) -> str:
    return hashlib.sha256(signal_name.encode()).hexdigest()


def get_lazy_polars_df_from_customer_api_historical_data(
    signal_list: List[Signal], time_window: TimeWindow
):
    customer_API_token = environ["CUSTOMER_API_TOKEN"]

    historical_data_endpoint = customer_API_URL + "/api/v1/historical-data/sync"

    request_json = {
        "signals": [
            {
                "rename": hash_signal_ADUS(signal.ADUS),
                **signal.model_dump(),
            }
            for signal in signal_list
        ],
        "timeWindow": {
            "start": str(
                time_window.start.astimezone(timezone.utc)
                .isoformat()
                .replace("+00:00", "Z")
            ),
            "end": str(
                time_window.end.astimezone(timezone.utc)
                .isoformat()
                .replace("+00:00", "Z")
            ),
        },
    }

    response = session.post(
        url=historical_data_endpoint,
        json=request_json,
        headers={"Authorization": f"Bearer {customer_API_token}"},
    )

    try:
        assert response.status_code == 200
    except AssertionError:
        raise AssertionError(
            f"Failed to get historical data. "
            f"Status code: {response.status_code}. "
            f"Response: {response.text}"
        )

    response_json = response.json()

    response = session.get(response_json["outputFile"])
    response.raise_for_status()

    lazy_df = (
        read_parquet(BytesIO(response.content))
        .rename(
            {hash_signal_ADUS(signal.ADUS): f"{signal.ADUS}" for signal in signal_list}
        )
        .with_columns(
            col("timestamp").dt.replace_time_zone("UTC"),
        )
        .with_columns(
            col("timestamp").dt.convert_time_zone(str(time_window.start.tzinfo)),
        )
        .lazy()
    )

    return lazy_df
