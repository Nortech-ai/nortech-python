from collections import defaultdict
from typing import List

from nortech.datatools.values.signals import ParquetPaths, Signal, SignalConfig


def get_parquet_paths_from_search_list(signal_list: List[Signal]) -> ParquetPaths:
    parquet_paths: ParquetPaths = defaultdict(list)

    for signal in signal_list:
        location = signal.location

        ADUS = signal.ADUS
        column_name = signal.column_name
        data_type = signal.dataType

        parquet_paths[location].append(
            SignalConfig(column_name=column_name, data_type=data_type, ADUS=ADUS)
        )

    return parquet_paths
