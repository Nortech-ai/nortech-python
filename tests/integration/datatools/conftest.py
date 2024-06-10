import subprocess
from datetime import datetime, timedelta, timezone
from io import BytesIO
from os import environ, getenv

import boto3
import numpy as np
import pandas as pd
import pytest

from nortech.datatools import TimeWindow


@pytest.fixture(scope="session")
def search_json() -> str:
    return """
    [
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
    ]
    """


@pytest.fixture(scope="session")
def time_window() -> TimeWindow:
    end = datetime.now(timezone.utc) - timedelta(days=1)
    start = end - timedelta(days=4)

    return TimeWindow(
        start=start,
        end=end,
    )


def date_range(start: datetime, end: datetime, delta: timedelta):
    current = start
    while current < end:
        yield current
        current += delta


@pytest.fixture(scope="session")
def moto_server():
    moto_server = subprocess.Popen(["moto_server", "s3", "-p", "5000"])
    yield moto_server
    moto_server.kill()


@pytest.fixture(scope="session")
def fake_S3_data(moto_server, time_window: TimeWindow):
    environ["AWS_ACCESS_KEY_ID"] = "mocked_access_key"
    environ["AWS_SECRET_ACCESS_KEY"] = "mocked_secret_key"
    environ["AWS_SESSION_TOKEN"] = "mocked_token"
    environ["AWS_ENDPOINT_URL"] = "http://localhost:5000"

    s3 = boto3.resource(
        "s3", region_name="us-east-1", endpoint_url=getenv("AWS_ENDPOINT_URL")
    )
    bucket = s3.create_bucket(Bucket="nortech-test")  # type: ignore

    delta = timedelta(days=1)
    for date in date_range(start=time_window.start, end=time_window.end, delta=delta):
        df = pd.DataFrame(
            {f"alias_{i}": np.random.rand(24) for i in range(4)},
            index=pd.date_range(date, periods=24, freq="h").view("int64") // 10**6,
        )
        df.index.name = "timestamp"
        parquet_buffer = BytesIO()
        df.to_parquet(parquet_buffer)

        bucket.put_object(
            Key=f"scope_1_group_0/year={date.year}/month={date.month:02d}/day={date.day:02d}/{date.day}.parquet",
            Body=parquet_buffer.getvalue(),
        )
        bucket.put_object(
            Key=f"scope_1_group_1/year={date.year}/month={date.month:02d}/day={date.day:02d}/{date.day}.parquet",
            Body=parquet_buffer.getvalue(),
        )
