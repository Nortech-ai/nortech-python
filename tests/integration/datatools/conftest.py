from datetime import datetime, timedelta, timezone
from os import environ
from typing import List

import pytest

environ["CUSTOMER_API_TOKEN"] = "test_token"

from nortech.datatools import TimeWindow
from nortech.shared.gateways.customer_api import CustomerAPISettings


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
def signals() -> List[str]:
    return [
        "asset_1/division_1/unit_1/signal_1",
        "asset_1/division_1/unit_1/signal_2",
        "asset_2/division_2/unit_2/signal_3",
    ]


@pytest.fixture(scope="session")
def time_window() -> TimeWindow:
    end = datetime.now(timezone.utc) - timedelta(days=1)
    start = end - timedelta(days=4)

    return TimeWindow(
        start=start,
        end=end,
    )


@pytest.fixture(scope="session")
def customer_api_settings() -> CustomerAPISettings:
    return CustomerAPISettings()
