from __future__ import annotations

from urllib3.util import Timeout

from nortech.common.services.logger import logger
from nortech.datatools.services.nortech_api import (
    Format,
    NortechAPI,
    download_data_from_cold_storage,
)
from nortech.datatools.services.storage import get_hot_and_cold_time_windows
from nortech.datatools.values.windowing import ColdWindow, HotWindow, TimeWindow
from nortech.metadata.services.signal import (
    parse_signal_input_or_output_or_id_union_to_signal_input,
)
from nortech.metadata.values.signal import SignalInput, SignalInputDict, SignalOutput


def download_data(
    nortech_api: NortechAPI,
    signals: list[SignalInput | SignalInputDict | SignalOutput | int],
    time_window: TimeWindow,
    output_path: str,
    file_format: Format,
    timeout: Timeout | None = None,
):
    """
    Downloads data for the specified signals within the given time window.

    Parameters
    ----------
    nortech_api : NortechAPI
        The API client for Nortech API.
    signals : list[SignalInput | SignalInputDict | SignalOutput | int]
        A list of signals to download, which can be of the following types:
        - SignalInputDict: A dictionary representation of a signal input.
          Example: {"workspace": "my_workspace", "asset": "my_asset", "division": "my_division", "unit": "my_unit", "signal": "my_signal"}
        - SignalInput: A pydantic model representing an input signal.
          Example: SignalInput(workspace="my_workspace", asset="my_asset", division="my_division", unit="my_unit", signal="my_signal")
        - SignalOutput: A pydantic model representing an output signal. Obtained
          from a signal metadata request.
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
    >>> from nortech.datatools.services.nortech_api import NortechAPI
    >>> from nortech.datatools.values.windowing import TimeWindow
    >>> from nortech.metadata.values.signal import SignalInput
    >>>
    >>> # Initialize the Nortech API client
    >>> nortech_api = NortechAPI()
    >>>
    >>> # Define signals to download
    >>> signal1 = {"workspace": "workspace1", "asset": "asset1", "division": "division1", "unit": "unit1", "signal": "signal1"}
    >>> signal2 = 789  # Signal ID
    >>> signal3 = SignalInput(workspace="workspace2", asset="asset2", division="division2", unit="unit2", signal="signal2")
    >>>
    >>> # Define the time window for data download
    >>> my_time_window = TimeWindow(start="2023-01-01T00:00:00Z", end="2023-01-31T23:59:59Z")
    >>>
    >>> # Specify the output path and file format
    >>> output_path = 'path/to/output'
    >>> file_format = "parquet"
    >>>
    >>> # Call the download_data function
    >>> download_data(
    ...     nortech_api=nortech_api,
    ...     signals=[signal1, signal2, signal3],
    ...     time_window=my_time_window,
    ...     output_path=output_path,
    ...     file_format=file_format
    ... )
    """
    signal_inputs = parse_signal_input_or_output_or_id_union_to_signal_input(nortech_api, signals)
    time_windows = get_hot_and_cold_time_windows(time_window=time_window)

    if isinstance(time_windows, ColdWindow):
        download_data_from_cold_storage(
            nortech_api=nortech_api,
            signals=signal_inputs,
            time_window=time_windows.time_window,
            output_path=output_path,
            file_format=file_format,
            timeout=timeout,
        )
    elif isinstance(time_windows, HotWindow):
        raise NotImplementedError("Hot storage is not available for download yet. Use get DataFrame functions instead.")
    else:
        logger.warning("Hot storage is not available for download yet. Limiting time window to cold storage.")

        download_data_from_cold_storage(
            nortech_api=nortech_api,
            signals=signal_inputs,
            time_window=time_windows.cold_storage_time_window,
            output_path=output_path,
            file_format=file_format,
            timeout=timeout,
        )
