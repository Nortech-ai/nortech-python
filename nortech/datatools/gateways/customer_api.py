import hashlib
from datetime import timezone
from enum import Enum
from io import BytesIO
from tempfile import NamedTemporaryFile
from typing import List
from urllib.parse import urljoin

from pandas import DataFrame, read_csv, to_datetime
from polars import (
    Datetime,
    col,
    from_pandas,
    read_parquet,
)
from pydantic import BaseModel, Field, field_serializer
from pydantic_settings import BaseSettings, SettingsConfigDict
from requests import Session, get
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from nortech.datatools.values.signals import (
    Signal,
    TimeWindow,
)


class CustomerAPISettings(BaseSettings):
    URL: str = Field(default="https://api.apps.nor.tech")
    TOKEN: str = Field(default=...)

    model_config = SettingsConfigDict(env_prefix="CUSTOMER_API_")


class CustomerAPI(Session):
    def __init__(self, settings: CustomerAPISettings):
        super().__init__()
        self.settings = settings
        self.mount(
            settings.URL,
            HTTPAdapter(
                max_retries=Retry(
                    total=5,
                    backoff_factor=1,
                    status_forcelist=[502, 503, 504],
                    allowed_methods=["GET", "POST"],
                    raise_on_status=False,
                )
            ),
        )
        self.headers = {"Authorization": f"Bearer {settings.TOKEN}"}

    def request(self, method, url, *args, **kwargs):
        joined_url = urljoin(self.settings.URL, url)
        return super().request(method, joined_url, *args, **kwargs)


class GetHotStorageSignals(BaseModel):
    signals: List[Signal]
    time_window: TimeWindow

    @field_serializer("time_window")
    def serialize_dt(self, time_window: TimeWindow, _info):
        return {
            "start": time_window.start.astimezone(timezone.utc).isoformat().replace("+00:00", "Z"),
            "end": time_window.end.astimezone(timezone.utc).isoformat().replace("+00:00", "Z"),
        }


class Format(str, Enum):
    PARQUET = "parquet"
    JSON = "json"
    CSV = "csv"


def get_lazy_polars_df_from_customer_api(customerAPI: CustomerAPI, signal_list: List[Signal], time_window: TimeWindow):
    response = customerAPI.post(
        url="/timescale",
        json=GetHotStorageSignals(
            signals=signal_list,
            time_window=time_window,
        ).model_dump(),
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
            raise AssertionError(f"Failed to get hot storage data. " f"Status code: {response.status_code}. ")

    if response.status_code == 200:
        with NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(response.content)
            tmp_file_path = tmp_file.name

        df = read_csv(tmp_file_path, low_memory=False)
        df["timestamp"] = to_datetime(df["timestamp"], format="mixed")
    else:
        df = DataFrame({"timestamp": [], **{signal.ADUS: [] for signal in signal_list}}).astype(
            {"timestamp": "datetime64[ms, UTC]"}
        )

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
    customerAPI: CustomerAPI, signal_list: List[Signal], time_window: TimeWindow
):
    request_json = {
        "signals": [
            {
                "rename": hash_signal_ADUS(signal.ADUS),
                **signal.model_dump(),
            }
            for signal in signal_list
        ],
        "timeWindow": {
            "start": str(time_window.start.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")),
            "end": str(time_window.end.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")),
        },
    }

    response = customerAPI.post(
        url="/api/v1/historical-data/sync",
        json=request_json,
    )

    try:
        assert response.status_code == 200 or response.status_code == 404
    except AssertionError:
        raise AssertionError(
            f"Failed to get historical data. " f"Status code: {response.status_code}. " f"Response: {response.text}"
        )

    if response.status_code == 404:
        df = DataFrame({"timestamp": [], **{signal.ADUS: [] for signal in signal_list}}).astype(
            {"timestamp": "datetime64[ms, UTC]"}
        )
        return from_pandas(df).lazy()

    response_json = response.json()

    response = get(response_json["outputFile"])
    response.raise_for_status()

    lazy_df = (
        read_parquet(BytesIO(response.content))
        .rename({hash_signal_ADUS(signal.ADUS): f"{signal.ADUS}" for signal in signal_list})
        .with_columns(
            col("timestamp").dt.replace_time_zone("UTC"),
        )
        .with_columns(
            col("timestamp").dt.convert_time_zone(str(time_window.start.tzinfo)),
        )
        .lazy()
    )

    return lazy_df


def download_data_from_customer_api_historical_data(
    customer_API: CustomerAPI, signal_list: List[Signal], time_window: TimeWindow, output_path: str
):
    request_json = {
        "signals": [
            {
                "rename": hash_signal_ADUS(signal.ADUS),
                **signal.model_dump(),
            }
            for signal in signal_list
        ],
        "timeWindow": {
            "start": str(time_window.start.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")),
            "end": str(time_window.end.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")),
        },
    }

    response = customer_API.post(
        url="/api/v1/historical-data/sync",
        json=request_json,
    )

    try:
        assert response.status_code == 200
    except AssertionError:
        raise AssertionError(
            f"Failed to get historical data. " f"Status code: {response.status_code}. " f"Response: {response.text}"
        )

    response_json = response.json()

    with get(response_json["outputFile"], stream=True) as r:
        r.raise_for_status()
        with open(output_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
