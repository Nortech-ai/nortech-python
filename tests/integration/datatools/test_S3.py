from nortech.datatools import TimeWindow, get_lazy_polars_df
from nortech.datatools.handlers.pandas import get_df
from nortech.datatools.handlers.polars import get_polars_df


def test_get__df(fake_S3_data, search_json: str, time_window: TimeWindow):
    df = get_df(search_json=search_json, time_window=time_window)

    assert df.index.name == "timestamp"

    assert list(df.columns) == [
        "asset_1/division_1/unit_1/signal_1",
        "asset_1/division_1/unit_1/signal_2",
        "asset_2/division_2/unit_2/signal_3",
    ]

    assert df.shape == (95, 3)


def test_get_polars_df(fake_S3_data, search_json: str, time_window: TimeWindow):
    polars_df = get_polars_df(search_json=search_json, time_window=time_window)

    assert polars_df.columns == [
        "timestamp",
        "asset_1/division_1/unit_1/signal_1",
        "asset_1/division_1/unit_1/signal_2",
        "asset_2/division_2/unit_2/signal_3",
    ]

    assert polars_df.shape == (95, 4)


def test_get_lazy_polars_df(fake_S3_data, search_json: str, time_window: TimeWindow):
    lazy_polars_df = get_lazy_polars_df(
        search_json=search_json, time_window=time_window
    )

    assert lazy_polars_df.columns == [
        "timestamp",
        "asset_1/division_1/unit_1/signal_1",
        "asset_1/division_1/unit_1/signal_2",
        "asset_2/division_2/unit_2/signal_3",
    ]
