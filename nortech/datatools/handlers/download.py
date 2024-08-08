from nortech.datatools.gateways.customer_api import (
    CustomerAPI,
    download_data_from_customer_api_historical_data,
)
from nortech.datatools.services.storage import get_hot_and_cold_time_windows
from nortech.datatools.values.signals import TimeWindow, get_signal_list_from_search_json
from nortech.datatools.values.windowing import ColdWindow, HotWindow
from nortech.derivers.services.logger import logger


def download_data(customer_API: CustomerAPI, search_json: str, time_window: TimeWindow, output_path: str):
    signal_list = get_signal_list_from_search_json(search_json=search_json)

    time_windows = get_hot_and_cold_time_windows(time_window=time_window)

    if isinstance(time_windows, ColdWindow):
        download_data_from_customer_api_historical_data(
            customer_API=customer_API,
            signal_list=signal_list,
            time_window=time_windows.time_window,
            output_path=output_path,
        )
    elif isinstance(time_windows, HotWindow):
        raise NotImplementedError("Hot storage is not available for download yet. Use get DataFrame functions instead.")
    else:
        logger.warning("Hot storage is not available for download yet. Limiting time window to cold storage.")

        download_data_from_customer_api_historical_data(
            customer_API=customer_API,
            signal_list=signal_list,
            time_window=time_windows.cold_storage_time_window,
            output_path=output_path,
        )
