from __future__ import annotations

from pandas import DataFrame
from polars import DataFrame as PolarsDataFrame
from polars import LazyFrame
from urllib3.util import Timeout

import nortech.datatools.handlers.download as download_handlers
import nortech.datatools.handlers.pandas as pandas_handlers
import nortech.datatools.handlers.polars as polars_handlers
from nortech.core.gateways.nortech_api import NortechAPI
from nortech.core.values.signal import SignalInput, SignalInputDict, SignalListOutput, SignalOutput
from nortech.datatools.services.nortech_api import Format
from nortech.datatools.values.windowing import TimeWindow


class Datatools:
    def __init__(self, nortech_api: NortechAPI):
        self.download = Download(nortech_api)
        self.pandas = Pandas(nortech_api)
        self.polars = Polars(nortech_api)


class Download:
    def __init__(self, nortech_api: NortechAPI):
        self.nortech_api = nortech_api

    def download_data(
        self,
        signals: list[SignalInput | SignalInputDict | SignalOutput | SignalListOutput | int],
        time_window: TimeWindow,
        output_path: str,
        file_format: Format,
        timeout: Timeout | None = None,
    ):
        """
        Downloads data for the specified signals within the given time window.

        Parameters
        ----------
        signals : list[SignalInput | SignalInputDict | SignalOutput | int]
            A list of signals to download, which can be of the following types:
            - SignalInputDict: A dictionary representation of a signal input.
                Example: {"workspace": "my_workspace", "asset": "my_asset", "division": "my_division", "unit": "my_unit", "signal": "my_signal"}
            - SignalInput: A pydantic model representing an input signal.
                Example: SignalInput(workspace="my_workspace", asset="my_asset", division="my_division", unit="my_unit", signal="my_signal")
            - SignalOutput: A pydantic model representing an output signal. Obtained from a signal metadata request.
            - int: Corresponds to a signalId, which is an integer identifier for a signal.
                Example: 789
        time_window : TimeWindow
            The time window for which data should be downloaded.
        output_path : str
            The file path where the downloaded data will be saved.
        file_format : "parquet" | "csv" | "json"
            The format of the output file. Can be "parquet", "csv", or "json".
        timeout : Timeout | None, optional
            The timeout setting for the download operation.

        Raises
        ------
        NotImplementedError
            If the time window corresponds to hot storage, which is not yet supported.

        Example
        -------
        >>> from datetime import datetime
        >>>
        >>> from nortech import Nortech
        >>> from nortech.core.values.signal import SignalInput, SignalInputDict
        >>> from nortech.datatools.values.windowing import TimeWindow
        >>>
        >>> # Initialize the Nortech client
        >>> nortech = Nortech()
        >>>
        >>> # Define signals to download
        >>> signal1: SignalInputDict = {
        ...     "workspace": "workspace1",
        ...     "asset": "asset1",
        ...     "division": "division1",
        ...     "unit": "unit1",
        ...     "signal": "signal1",
        ... }
        >>> signal2 = 789  # Signal ID
        >>> signal3 = SignalInput(workspace="workspace2", asset="asset2", division="division2", unit="unit2", signal="signal2")
        >>>
        >>> # Define the time window for data download
        >>> my_time_window = TimeWindow(start=datetime(2023, 1, 1), end=datetime(2023, 1, 31))
        >>>
        >>> # Specify the output path and file format
        >>> output_path = "path/to/output"
        >>> file_format = "parquet"
        >>>
        >>> # Call the download_data function
        >>> nortech.datatools.download.download_data(
        ...     signals=[signal1, signal2, signal3],
        ...     time_window=my_time_window,
        ...     output_path=output_path,
        ...     file_format=file_format
        ... )
        """
        return download_handlers.download_data(
            self.nortech_api, signals, time_window, output_path, file_format, timeout
        )


class Pandas:
    def __init__(self, nortech_api: NortechAPI):
        self.nortech_api = nortech_api

    def get_df(
        self,
        signals: list[SignalInput | SignalInputDict | SignalOutput | SignalListOutput | int],
        time_window: TimeWindow,
        timeout: Timeout | None = None,
    ) -> DataFrame:
        """
        Retrieves a pandas DataFrame for the specified signals within the given time window.

        Parameters
        ----------
        signals : list[SignalInput | SignalInputDict | SignalOutput | int]
            A list of signals to retrieve, which can be of the following types:
            - SignalInputDict: A dictionary representation of a signal input.
                Example: {"workspace": "my_workspace", "asset": "my_asset", "division": "my_division", "unit": "my_unit", "signal": "my_signal"}
            - SignalInput: A pydantic model representing an input signal.
                Example: SignalInput(workspace="my_workspace", asset="my_asset", division="my_division", unit="my_unit", signal="my_signal")
            - SignalOutput: A pydantic model representing an output signal. Obtained from a signal metadata request.
            - int: Corresponds to a signalId, which is an integer identifier for a signal.
                Example: 789
        time_window : TimeWindow
            The time window for which data should be retrieved.
        timeout : Timeout | None, optional
            The timeout setting for the API request.

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
        >>>
        >>> from nortech import Nortech
        >>> from nortech.core.values.signal import SignalInput, SignalInputDict
        >>> from nortech.datatools.values.windowing import TimeWindow
        >>>
        >>> # Initialize the Nortech client
        >>> nortech = Nortech()
        >>>
        >>> # Define signals to download
        >>> signal1: SignalInputDict = {
        ...     "workspace": "workspace1",
        ...     "asset": "asset1",
        ...     "division": "division1",
        ...     "unit": "unit1",
        ...     "signal": "signal1",
        ... }
        >>> signal2 = 789  # Signal ID
        >>> signal3 = SignalInput(workspace="workspace2", asset="asset2", division="division2", unit="unit2", signal="signal2")
        >>>
        >>> # Define the time window for data download
        >>> my_time_window = TimeWindow(start=datetime(2023, 1, 1), end=datetime(2023, 1, 31))
        >>>
        >>> # Call the get_df function
        >>> df = nortech.datatools.pandas.get_df(
        ...     signals=[signal1, signal2, signal3],
        ...     time_window=my_time_window,
        ... )
        >>> df.columns
        [
            'timestamp',
            'workspace_1/asset_1/division_1/unit_1/signal_1',
            'workspace_1/asset_1/division_1/unit_1/signal_2',
            'workspace_2/asset_2/division_2/unit_2/signal_3'
        ]
        """
        return pandas_handlers.get_df(self.nortech_api, signals, time_window, timeout)


class Polars:
    def __init__(self, nortech_api: NortechAPI):
        self.nortech_api = nortech_api

    def get_lazy_polars_df(
        self,
        signals: list[SignalInput | SignalInputDict | SignalOutput | SignalListOutput | int],
        time_window: TimeWindow,
        timeout: Timeout | None = None,
    ) -> LazyFrame:
        """
        Retrieves a polars LazyFrame for the specified signals within the given time window.

        Parameters
        ----------
        signals : list[SignalInput | SignalInputDict | SignalOutput | int]
            A list of signals to retrieve, which can be of the following types:
            - SignalInputDict: A dictionary representation of a signal input.
                Example: {"workspace": "my_workspace", "asset": "my_asset", "division": "my_division", "unit": "my_unit", "signal": "my_signal"}
            - SignalInput: A pydantic model representing an input signal.
                Example: SignalInput(workspace="my_workspace", asset="my_asset", division="my_division", unit="my_unit", signal="my_signal")
            - SignalOutput: A pydantic model representing an output signal. Obtained from a signal metadata request.
            - int: Corresponds to a signalId, which is an integer identifier for a signal.
                Example: 789
        time_window : TimeWindow
            The time window for which data should be retrieved.
        timeout : Timeout | None, optional
            The timeout setting for the API request.

        Returns
        -------
        LazyFrame
            A polars LazyFrame containing the data.

        Raises
        ------
        NoSignalsRequestedError
            Raised when no signals are requested.
        InvalidTimeWindow
            Raised when the start date is after the end date.

        Example
        -------
        >>> from datetime import datetime
        >>>
        >>> from nortech import Nortech
        >>> from nortech.core.values.signal import SignalInput, SignalInputDict
        >>> from nortech.datatools.values.windowing import TimeWindow
        >>>
        >>> # Initialize the Nortech client
        >>> nortech = Nortech()
        >>>
        >>> # Define signals to download
        >>> signal1: SignalInputDict = {
        ...     "workspace": "workspace1",
        ...     "asset": "asset1",
        ...     "division": "division1",
        ...     "unit": "unit1",
        ...     "signal": "signal1",
        ... }
        >>> signal2 = 789  # Signal ID
        >>> signal3 = SignalInput(workspace="workspace2", asset="asset2", division="division2", unit="unit2", signal="signal2")
        >>>
        >>> # Define the time window for data download
        >>> my_time_window = TimeWindow(start=datetime(2023, 1, 1), end=datetime(2023, 1, 31))
        >>>
        >>> # Call the get_lazy_polars_df function
        >>> lazy_polars_df = nortech.datatools.polars.get_lazy_polars_df(
        ...     signals=[signal1, signal2, signal3],
        ...     time_window=my_time_window,
        ... )
        >>> lazy_polars_df.columns
        [
            'timestamp',
            'workspace_1/asset_1/division_1/unit_1/signal_1',
            'workspace_1/asset_1/division_1/unit_1/signal_2',
            'workspace_2/asset_2/division_2/unit_2/signal_3'
        ]
        """
        return polars_handlers.get_lazy_polars_df(self.nortech_api, signals, time_window, timeout)

    def get_polars_df(
        self,
        signals: list[SignalInput | SignalInputDict | SignalOutput | SignalListOutput | int],
        time_window: TimeWindow,
        timeout: Timeout | None = None,
    ) -> PolarsDataFrame:
        """
        Retrieves a polars DataFrame for the specified signals within the given time window.

        Parameters
        ----------
        signals : list[SignalInput | SignalInputDict | SignalOutput | int]
            A list of signals to retrieve, which can be of the following types:
            - SignalInputDict: A dictionary representation of a signal input.
                Example: {"workspace": "my_workspace", "asset": "my_asset", "division": "my_division", "unit": "my_unit", "signal": "my_signal"}
            - SignalInput: A pydantic model representing an input signal.
                Example: SignalInput(workspace="my_workspace", asset="my_asset", division="my_division", unit="my_unit", signal="my_signal")
            - SignalOutput: A pydantic model representing an output signal. Obtained from a signal metadata request.
            - int: Corresponds to a signalId, which is an integer identifier for a signal.
                Example: 789
        time_window : TimeWindow
            The time window for which data should be retrieved.

        Returns
        -------
        DataFrame
            A polars DataFrame containing the data.

        Raises
        ------
        NoSignalsRequestedError
            Raised when no signals are requested.
        InvalidTimeWindow
            Raised when the start date is after the end date.

        Example
        -------
        >>> from datetime import datetime
        >>>
        >>> from nortech import Nortech
        >>> from nortech.core.values.signal import SignalInput, SignalInputDict
        >>> from nortech.datatools.values.windowing import TimeWindow
        >>>
        >>> # Initialize the Nortech client
        >>> nortech = Nortech()
        >>>
        >>> # Define signals to download
        >>> signal1: SignalInputDict = {
        ...     "workspace": "workspace1",
        ...     "asset": "asset1",
        ...     "division": "division1",
        ...     "unit": "unit1",
        ...     "signal": "signal1",
        ... }
        >>> signal2 = 789  # Signal ID
        >>> signal3 = SignalInput(workspace="workspace2", asset="asset2", division="division2", unit="unit2", signal="signal2")
        >>>
        >>> # Define the time window for data download
        >>> my_time_window = TimeWindow(start=datetime(2023, 1, 1), end=datetime(2023, 1, 31))
        >>>
        >>> # Call the get_polars_df function
        >>> polars_df = nortech.datatools.polars.get_polars_df(
        ...     signals=[signal1, signal2, signal3],
        ...     time_window=my_time_window,
        ... )
        >>> polars_df.columns
        [
            'timestamp',
            'workspace_1/asset_1/division_1/unit_1/signal_1',
            'workspace_1/asset_1/division_1/unit_1/signal_2',
            'workspace_2/asset_2/division_2/unit_2/signal_3'
        ]
        """
        return polars_handlers.get_polars_df(self.nortech_api, signals, time_window, timeout)


__all__ = ["Format"]
