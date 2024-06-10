from dataclasses import dataclass

from nortech.datatools.values.signals import TimeWindow


@dataclass
class HotColdWindow:
    hot_storage_time_window: TimeWindow
    cold_storage_time_window: TimeWindow


@dataclass
class HotWindow:
    time_window: TimeWindow


@dataclass
class ColdWindow:
    time_window: TimeWindow
