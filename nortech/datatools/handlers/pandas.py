from __future__ import annotations

from pandas import DataFrame

from nortech.common.gateways.nortech_api import NortechAPI
from nortech.datatools.handlers.polars import get_polars_df
from nortech.datatools.values.windowing import TimeWindow
from nortech.metadata.values.signal import SignalInput, SignalInputDict, SignalOutput


def get_df(
    nortech_api: NortechAPI,
    signals: list[SignalInput | SignalInputDict | SignalOutput | int],
    time_window: TimeWindow,
) -> DataFrame:
    """
    Retrieves a pandas DataFrame for the specified signals within the given time window.

    Parameters
    ----------
    nortech_api : NortechAPI
        The API client for Nortech API.
    signals : list[SignalInput | SignalInputDict | SignalOutput | int]
        A list of signals to retrieve, which can be of the following types:
        - SignalInputDict: A dictionary representation of a signal input.
          Example: {"workspace": "my_workspace", "asset": "my_asset", "division": "my_division", "unit": "my_unit", "signal": "my_signal"}
        - SignalInput: A pydantic model representing an input signal.
          Example: SignalInput(workspace="my_workspace", asset="my_asset", division="my_division", unit="my_unit", signal="my_signal")
        - SignalOutput: A pydantic model representing an output signal. Obtained
          from a signal metadata request.
        - int: Corresponds to a signalId, which is an integer identifier for a signal.
          Example: 789
    time_window : TimeWindow
        The time window for which data should be retrieved.

    Returns
    -------
    DataFrame
        A pandas DataFrame containing the data.

    Raises
    ------
    NoSignalsRequestedError
        Raised when no signals are requested.
    InvalidTimeWindow
        Raised when the start date is after the end date.

    Example
    -------
    >>> from datetime import datetime
    >>> from nortech.datatools import get_df, TimeWindow
    >>> from nortech.metadata.values.signal import SignalInput
    >>>
    >>> # Define signals to retrieve
    >>> signal1 = {"workspace": "workspace1", "asset": "asset1", "division": "division1", "unit": "unit1", "signal": "signal1"}
    >>> signal2 = 789  # Signal ID
    >>> signal3 = SignalInput(workspace="workspace2", asset="asset2", division="division2", unit="unit2", signal="signal3")
    >>>
    >>> # Define the time window for data retrieval
    >>> my_time_window = TimeWindow(start=datetime(2020, 1, 1), end=datetime(2020, 1, 31))
    >>>
    >>> # Call the get_df function
    >>> df = get_df(
    ...     nortech_api=nortech_api,
    ...     signals=[signal1, signal2, signal3],
    ...     time_window=my_time_window
    ... )
    >>> df.columns
    [
        'timestamp',
        'workspace_1/asset_1/division_1/unit_1/signal_1',
        'workspace_1/asset_1/division_1/unit_1/signal_2',
        'workspace_2/asset_2/division_2/unit_2/signal_3'
    ]
    """
    polars_df = get_polars_df(nortech_api=nortech_api, signals=signals, time_window=time_window)

    df = polars_df.to_pandas().set_index("timestamp")

    return df
