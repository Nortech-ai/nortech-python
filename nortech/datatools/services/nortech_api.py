from __future__ import annotations

from datetime import timezone
from io import BytesIO
from tempfile import NamedTemporaryFile
from typing import Literal

from pandas import DataFrame, read_csv, to_datetime
from polars import (
    Datetime,
    col,
    from_pandas,
    read_parquet,
)
from requests import get
from urllib3.util import Timeout

from nortech.core.gateways.nortech_api import NortechAPI, validate_response
from nortech.core.values.signal import SignalInput
from nortech.datatools.values.windowing import TimeWindow


def serialize_hot_storage_time_window(time_window: TimeWindow):
    return {
        "start": time_window.start.astimezone(timezone.utc).isoformat().replace("+00:00", "Z"),
        "end": time_window.end.astimezone(timezone.utc).isoformat().replace("+00:00", "Z"),
    }


def get_lazy_polars_df_from_hot_storage(
    nortech_api: NortechAPI,
    signals: list[SignalInput],
    time_window: TimeWindow,
    timeout: Timeout | None = None,
):
    response = nortech_api.post(
        url="/timescale",
        json={
            "signals": [signal.model_dump(by_alias=True) for signal in signals],
            "time_window": serialize_hot_storage_time_window(time_window),
        },
        timeout=timeout,  # type: ignore
    )

    validate_response(response, valid_status_codes=[200, 404], error_message="Failed to get hot storage data.")

    if response.status_code == 404:
        df = DataFrame({"timestamp": [], **{signal.path: [] for signal in signals}}).astype(
            {"timestamp": "datetime64[ms, UTC]"}
        )
    else:
        with NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(response.content)
            tmp_file_path = tmp_file.name

        df = read_csv(tmp_file_path, low_memory=False)
        df["timestamp"] = to_datetime(df["timestamp"], format="mixed")

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


def get_lazy_polars_df_from_cold_storage(
    nortech_api: NortechAPI,
    signals: list[SignalInput],
    time_window: TimeWindow,
    timeout: Timeout | None = None,
):
    request_json = {
        "signals": [signal.model_dump_with_rename() for signal in signals],
        "timeWindow": {
            "start": str(time_window.start.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")),
            "end": str(time_window.end.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")),
        },
    }

    response = nortech_api.post(
        url="/api/v1/historical-data/sync",
        json=request_json,
        timeout=timeout,  # type: ignore
    )

    validate_response(response, valid_status_codes=[200, 404], error_message="Failed to get cold storage data.")

    if response.status_code == 404:
        df = DataFrame({"timestamp": [], **{signal.path: [] for signal in signals}}).astype(
            {"timestamp": "datetime64[ms, UTC]"}
        )
        return from_pandas(df).lazy()

    response_json = response.json()

    response = get(response_json["outputFile"], timeout=timeout)  # type: ignore
    response.raise_for_status()

    lazy_df = (
        read_parquet(BytesIO(response.content))
        .rename({signal.hash(): f"{signal.path}" for signal in signals})
        .with_columns(
            col("timestamp").dt.replace_time_zone("UTC"),
        )
        .with_columns(
            col("timestamp").dt.convert_time_zone(str(time_window.start.tzinfo)),
        )
        .lazy()
    )

    return lazy_df


Format = Literal["parquet", "json", "csv"]


def download_data_from_cold_storage(
    nortech_api: NortechAPI,
    signals: list[SignalInput],
    time_window: TimeWindow,
    output_path: str,
    file_format: Format = "parquet",
    timeout: Timeout | None = None,
):
    df = get_lazy_polars_df_from_cold_storage(nortech_api, signals, time_window, timeout).collect()

    if file_format == "parquet":
        df.write_parquet(output_path)
    elif file_format == "csv":
        df.write_csv(output_path)
    else:
        df.write_json(output_path)
