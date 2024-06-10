from datetime import timezone
from os import environ, getenv
from tempfile import NamedTemporaryFile
from typing import List

from pandas import DataFrame, read_csv, to_datetime
from polars import Datetime, col, from_pandas
from pydantic import BaseModel, field_serializer
from requests import post

from nortech.datatools.values.signals import (
    Signal,
    TimeWindow,
)


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


def get_lazy_polars_df_from_customer_api(
    signal_list: List[Signal], time_window: TimeWindow
):
    customer_API_URL = getenv("CUSTOMER_API_URL", "https://api.apps.nor.tech")
    customer_API_token = environ["CUSTOMER_API_TOKEN"]

    hot_storage_endpoint = customer_API_URL + "/timescale"

    response = post(
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
