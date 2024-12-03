from pydantic import BaseModel

from nortech.metadata.values.time_window import TimeWindow


class HotColdWindow(BaseModel):
    hot_storage_time_window: TimeWindow
    cold_storage_time_window: TimeWindow


class HotWindow(BaseModel):
    time_window: TimeWindow


class ColdWindow(BaseModel):
    time_window: TimeWindow
