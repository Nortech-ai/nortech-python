from __future__ import annotations

from typing import Sequence

from pandas import DataFrame

from nortech.datatools.handlers.polars import get_polars_df
from nortech.datatools.values.windowing import TimeWindow
from nortech.gateways.nortech_api import NortechAPI
from nortech.metadata.values.signal import SignalInput, SignalInputDict, SignalListOutput, SignalOutput


def get_df(
    nortech_api: NortechAPI,
    signals: Sequence[SignalInput | SignalInputDict | SignalOutput | SignalListOutput | int],
    time_window: TimeWindow,
) -> DataFrame:
    polars_df = get_polars_df(nortech_api=nortech_api, signals=signals, time_window=time_window)

    df = polars_df.to_pandas().set_index("timestamp")

    return df
