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
        """
        Download data for the specified signals within the given time window. If experimental features are enabled, live data will also be downloaded.

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
        """
        Retrieve a pandas DataFrame for the specified signals within the given time window. If experimental features are enabled, live data will also be retrieved.

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
        """
        Retrieve a polars LazyFrame for the specified signals within the given time window. If experimental features are enabled, live data will also be retrieved.

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

        """
        return polars_handlers.get_lazy_polars_df(self.nortech_api, signals, time_window)

    def get_df(
        self,
        signals: Sequence[int | SignalInput | SignalInputDict | SignalOutput | SignalListOutput],
        time_window: TimeWindow,
    ) -> PolarsDataFrame:
        """
        Retrieve a polars DataFrame for the specified signals within the given time window. If experimental features are enabled, live data will also be retrieved.

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

        """
        return polars_handlers.get_polars_df(self.nortech_api, signals, time_window)


__all__ = ["Format"]
