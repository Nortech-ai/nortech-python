from __future__ import annotations

from typing import Sequence

from pandas import DataFrame
from polars import DataFrame as PolarsDataFrame
from polars import LazyFrame

import nortech.datatools.handlers.download as download_handlers
import nortech.datatools.handlers.pandas as pandas_handlers
import nortech.datatools.handlers.polars as polars_handlers
from nortech.datatools.services.nortech_api import Format
from nortech.datatools.values.windowing import TimeWindow
from nortech.gateways.nortech_api import NortechAPI
from nortech.metadata.values.signal import (
    SignalInput,
    SignalInputDict,
    SignalListOutput,
    SignalOutput,
)


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
        signals: Sequence[int | SignalInput | SignalInputDict | SignalOutput | SignalListOutput],
        time_window: TimeWindow,
        output_path: str,
        file_format: Format,
    ):
        """Download data for the specified signals within the given time window. If experimental features are enabled, live data will also be downloaded.

        Args:
            signals (Sequence[int | SignalInput | SignalInputDict | SignalOutput | SignalListOutput]): A list of signals to download, which can be of the following types:
                - int: The signal "ID".
                - [SignalInputDict](#signalinputdict): A dictionary representation of a signal input.
                - [SignalInput](#signalinput): A pydantic model representing a signal input.
                - [SignalOutput](#signaloutput): A pydantic model representing a signal output. Obtained from requesting a signal metadata.
                - [SignalListOutput](#signallistoutput): A pydantic model representing a listed signal output. Obtained from requesting signals metadata.
            time_window (TimeWindow): The time window for which data should be downloaded.
            output_path (str): The file path where the downloaded data will be saved.
            file_format (Format): The format of the output file. Can be "parquet", "csv", or "json".

        Raises:
            NotImplementedError: If the time window corresponds to hot storage, which is not yet supported.

        Example:
        ```python
        from datetime import datetime

        from nortech import Nortech
        from nortech.core.values.signal import SignalInput, SignalInputDict
        from nortech.datatools.values.windowing import TimeWindow

        # Initialize the Nortech client
        nortech = Nortech()

        # Define signals to download
        signal1: SignalInputDict = {
            "workspace": "workspace1",
            "asset": "asset1",
            "division": "division1",
            "unit": "unit1",
            "signal": "signal1",
        }
        signal2 = 789  # Signal ID
        signal3 = SignalInput(workspace="workspace2", asset="asset2", division="division2", unit="unit2", signal="signal2")

        fetched_signals = nortech.metadata.signal.list(  # Fetched signals
            {"workspace": "workspace3", "asset": "asset3", "division": "division3", "unit": "unit3"}
        ).data

        # Define the time window for data download
        my_time_window = TimeWindow(start=datetime(2023, 1, 1), end=datetime(2023, 1, 31))

        # Specify the output path and file format
        output_path = "path/to/output"
        file_format = "parquet"

        # Call the download_data function with manually defined signals or fetched signals
        nortech.datatools.download.download_data(
            signals=[signal1, signal2, signal3] + fetched_signals,
            time_window=my_time_window,
            output_path=output_path,
            file_format=file_format,
        )

        ```

        """
        return download_handlers.download_data(self.nortech_api, signals, time_window, output_path, file_format)


class Pandas:
    def __init__(self, nortech_api: NortechAPI):
        self.nortech_api = nortech_api

    def get_df(
        self,
        signals: Sequence[int | SignalInput | SignalInputDict | SignalOutput | SignalListOutput],
        time_window: TimeWindow,
    ) -> DataFrame:
        """Retrieve a pandas DataFrame for the specified signals within the given time window. If experimental features are enabled, live data will also be retrieved.

        Args:
            signals (Sequence[int | SignalInput | SignalInputDict | SignalOutput | SignalListOutput]): A list of signals to download, which can be of the following types:
                - *int*: The signal "ID".
                - [SignalInputDict](#signalinputdict): A dictionary representation of a signal input.
                - [SignalInput](#signalinput): A pydantic model representing a signal input.
                - [SignalOutput](#signaloutput): A pydantic model representing a signal output. Obtained from requesting a signal metadata.
                - [SignalListOutput](#signallistoutput): A pydantic model representing a listed signal output. Obtained from requesting signals metadata.
            time_window (TimeWindow): The time window for which data should be retrieved.

        Returns:
            DataFrame: A pandas DataFrame containing the data.

        Raises:
            NoSignalsRequestedError: Raised when no signals are requested.
            InvalidTimeWindow: Raised when the start date is after the end date.

        Example:
        ```python
        from datetime import datetime

        from nortech import Nortech
        from nortech.core.values.signal import SignalInput, SignalInputDict
        from nortech.datatools.values.windowing import TimeWindow

        # Initialize the Nortech client
        nortech = Nortech()

        # Define signals to download
        signal1: SignalInputDict = {
            "workspace": "workspace1",
            "asset": "asset1",
            "division": "division1",
            "unit": "unit1",
            "signal": "signal1",
        }
        signal2 = 789  # Signal ID
        signal3 = SignalInput(workspace="workspace2", asset="asset2", division="division2", unit="unit2", signal="signal2")

        fetched_signals = nortech.metadata.signal.list(  # Fetched signals
            {"workspace": "workspace3", "asset": "asset3", "division": "division3", "unit": "unit3"}
        ).data

        # Define the time window for data download
        my_time_window = TimeWindow(start=datetime(2023, 1, 1), end=datetime(2023, 1, 31))

        # Call the get_df function with manually defined signals or fetched signals
        df = nortech.datatools.pandas.get_df(
            signals=[signal1, signal2, signal3] + fetched_signals,
            time_window=my_time_window,
        )

        print(df.columns)
        # [
        #     "timestamp",
        #     "workspace_1/asset_1/division_1/unit_1/signal_1",
        #     "workspace_1/asset_1/division_1/unit_1/signal_2",
        #     "workspace_2/asset_2/division_2/unit_2/signal_3",
        #     "workspace_3/asset_3/division_3/unit_3/signal_4",
        #     "workspace_3/asset_3/division_3/unit_3/signal_5",
        # ]

        ```

        """
        return pandas_handlers.get_df(self.nortech_api, signals, time_window)


class Polars:
    def __init__(self, nortech_api: NortechAPI):
        self.nortech_api = nortech_api

    def get_lazy_df(
        self,
        signals: Sequence[int | SignalInput | SignalInputDict | SignalOutput | SignalListOutput],
        time_window: TimeWindow,
    ) -> LazyFrame:
        """Retrieve a polars LazyFrame for the specified signals within the given time window. If experimental features are enabled, live data will also be retrieved.

        Args:
            signals (Sequence[int | SignalInput | SignalInputDict | SignalOutput | SignalListOutput]): A list of signals to download, which can be of the following types:
                - *int*: The signal "ID".
                - [SignalInputDict](#signalinputdict): A dictionary representation of a signal input.
                - [SignalInput](#signalinput): A pydantic model representing a signal input.
                - [SignalOutput](#signaloutput): A pydantic model representing a signal output. Obtained from requesting a signal metadata.
                - [SignalListOutput](#signallistoutput): A pydantic model representing a listed signal output. Obtained from requesting signals metadata.
            time_window (TimeWindow): The time window for which data should be retrieved.

        Returns:
            LazyFrame: A polars LazyFrame containing the data.

        Raises:
            NoSignalsRequestedError: Raised when no signals are requested.
            InvalidTimeWindow: Raised when the start date is after the end date.

        Example:
        ```python
        from datetime import datetime

        from nortech import Nortech
        from nortech.core.values.signal import SignalInput, SignalInputDict
        from nortech.datatools.values.windowing import TimeWindow

        # Initialize the Nortech client
        nortech = Nortech()

        # Define signals to download
        signal1: SignalInputDict = {
            "workspace": "workspace1",
            "asset": "asset1",
            "division": "division1",
            "unit": "unit1",
            "signal": "signal1",
        }
        signal2 = 789  # Signal ID
        signal3 = SignalInput(workspace="workspace2", asset="asset2", division="division2", unit="unit2", signal="signal2")

        fetched_signals = nortech.metadata.signal.list(  # Fetched signals
            {"workspace": "workspace3", "asset": "asset3", "division": "division3", "unit": "unit3"}
        ).data

        # Define the time window for data download
        my_time_window = TimeWindow(start=datetime(2023, 1, 1), end=datetime(2023, 1, 31))

        # Call the get_df function with manually defined signals or fetched signals
        df = nortech.datatools.polars.get_lazy_df(
            signals=[signal1, signal2, signal3] + fetched_signals,
            time_window=my_time_window,
        )

        print(df.columns)
        # [
        #     "timestamp",
        #     "workspace_1/asset_1/division_1/unit_1/signal_1",
        #     "workspace_1/asset_1/division_1/unit_1/signal_2",
        #     "workspace_2/asset_2/division_2/unit_2/signal_3",
        #     "workspace_3/asset_3/division_3/unit_3/signal_4",
        #     "workspace_3/asset_3/division_3/unit_3/signal_5",
        # ]

        ```

        """
        return polars_handlers.get_lazy_polars_df(self.nortech_api, signals, time_window)

    def get_df(
        self,
        signals: Sequence[int | SignalInput | SignalInputDict | SignalOutput | SignalListOutput],
        time_window: TimeWindow,
    ) -> PolarsDataFrame:
        """Retrieve a polars DataFrame for the specified signals within the given time window. If experimental features are enabled, live data will also be retrieved.

        Args:
            signals (Sequence[int | SignalInput | SignalInputDict | SignalOutput | SignalListOutput]): A list of signals to download, which can be of the following types:
                - *int*: The signal "ID".
                - [SignalInputDict](#signalinputdict): A dictionary representation of a signal input.
                - [SignalInput](#signalinput): A pydantic model representing a signal input.
                - [SignalOutput](#signaloutput): A pydantic model representing a signal output. Obtained from requesting a signal metadata.
                - [SignalListOutput](#signallistoutput): A pydantic model representing a listed signal output. Obtained from requesting signals metadata.
            time_window (TimeWindow): The time window for which data should be retrieved.

        Returns:
            DataFrame: A polars DataFrame containing the data.

        Raises:
            NoSignalsRequestedError: Raised when no signals are requested.
            InvalidTimeWindow: Raised when the start date is after the end date.

        Example:
        ```python
        from datetime import datetime

        from nortech import Nortech
        from nortech.core.values.signal import SignalInput, SignalInputDict
        from nortech.datatools.values.windowing import TimeWindow

        # Initialize the Nortech client
        nortech = Nortech()

        # Define signals to download
        signal1: SignalInputDict = {
            "workspace": "workspace1",
            "asset": "asset1",
            "division": "division1",
            "unit": "unit1",
            "signal": "signal1",
        }
        signal2 = 789  # Signal ID
        signal3 = SignalInput(workspace="workspace2", asset="asset2", division="division2", unit="unit2", signal="signal2")

        fetched_signals = nortech.metadata.signal.list(  # Fetched signals
            {"workspace": "workspace3", "asset": "asset3", "division": "division3", "unit": "unit3"}
        ).data

        # Define the time window for data download
        my_time_window = TimeWindow(start=datetime(2023, 1, 1), end=datetime(2023, 1, 31))

        # Call the get_df function with manually defined signals or fetched signals
        df = nortech.datatools.polars.get_df(
            signals=[signal1, signal2, signal3] + fetched_signals,
            time_window=my_time_window,
        )

        print(df.columns)
        # [
        #     "timestamp",
        #     "workspace_1/asset_1/division_1/unit_1/signal_1",
        #     "workspace_1/asset_1/division_1/unit_1/signal_2",
        #     "workspace_2/asset_2/division_2/unit_2/signal_3",
        #     "workspace_3/asset_3/division_3/unit_3/signal_4",
        #     "workspace_3/asset_3/division_3/unit_3/signal_5",
        # ]

        ```

        """
        return polars_handlers.get_polars_df(self.nortech_api, signals, time_window)


__all__ = ["Format"]
