from __future__ import annotations

from urllib3.util import Timeout

from nortech.core.services.logger import logger
from nortech.core.services.signal import (
    parse_signal_input_or_output_or_id_union_to_signal_input,
)
from nortech.core.values.signal import SignalInput, SignalInputDict, SignalListOutput, SignalOutput
from nortech.datatools.services.nortech_api import (
    Format,
    NortechAPI,
    download_data_from_cold_storage,
)
from nortech.datatools.services.storage import get_hot_and_cold_time_windows
from nortech.datatools.values.windowing import ColdWindow, HotWindow, TimeWindow


def download_data(
    nortech_api: NortechAPI,
    signals: list[SignalInput | SignalInputDict | SignalOutput | SignalListOutput | int],
    time_window: TimeWindow,
    output_path: str,
    file_format: Format,
    timeout: Timeout | None = None,
):
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
