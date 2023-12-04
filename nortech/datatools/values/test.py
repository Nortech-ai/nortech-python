from datetime import datetime

from nortech.datatools import TimeWindow, get_lazy_polars_df

search_json = """[
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
]"""

time_window = TimeWindow(
    start=datetime(2020, 1, 1),
    end=datetime(2020, 1, 1),
)
lazy_polars_df = get_lazy_polars_df(search_json=search_json, time_window=time_window)

assert lazy_polars_df.columns == [
    "timestamp",
    "asset_1/division_1/unit_1/signal_1",
    "asset_1/division_1/unit_1/signal_2",
    "asset_2/division_2/unit_2/signal_3",
]
