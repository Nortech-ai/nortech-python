from __future__ import annotations

from pandas import DataFrame
from urllib3.util import Timeout

from nortech.core.gateways.nortech_api import NortechAPI
from nortech.core.values.signal import SignalInput, SignalInputDict, SignalListOutput, SignalOutput
from nortech.datatools.handlers.polars import get_polars_df
from nortech.datatools.values.windowing import TimeWindow


def get_df(
    nortech_api: NortechAPI,
    signals: list[SignalInput | SignalInputDict | SignalOutput | SignalListOutput | int],
    time_window: TimeWindow,
    timeout: Timeout | None = None,
) -> DataFrame:
    polars_df = get_polars_df(nortech_api=nortech_api, signals=signals, time_window=time_window, timeout=timeout)

    df = polars_df.to_pandas().set_index("timestamp")

    return df
