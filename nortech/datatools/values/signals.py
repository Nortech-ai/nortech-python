from dataclasses import dataclass
from datetime import datetime
from json import loads
from typing import Dict, List

from pydantic import BaseModel
from tzlocal import get_localzone

from nortech.datatools.values.errors import InvalidTimeWindow, InvalidTimeZone


@dataclass
class TimeWindow:
    start: datetime
    end: datetime

    def __post_init__(self):
        if self.start.tzinfo is None:
            self.start = self.start.replace(tzinfo=get_localzone())

        if self.end.tzinfo is None:
            self.end = self.end.replace(tzinfo=get_localzone())

        if self.start.tzinfo != self.end.tzinfo:
            raise InvalidTimeZone()

        if self.end < self.start:
            raise InvalidTimeWindow()


@dataclass
class SignalConfig:
    column_name: str
    data_type: str
    ADUS: str


class Asset(BaseModel):
    name: str


class Division(BaseModel):
    name: str


class Unit(BaseModel):
    name: str


class Storage(BaseModel):
    bucket: str
    path: str


class Signal(BaseModel):
    name: str
    dataType: str
    alias: int
    asset: Asset
    division: Division
    unit: Unit
    storage: Storage

    @property
    def location(self) -> str:
        return get_location_from_signal(signal=self)

    @property
    def column_name(self) -> str:
        return get_column_name_from_signal(signal=self)

    @property
    def ADUS(self) -> str:
        return get_ADUS_from_signal(signal=self)


def get_location_from_signal(signal: Signal) -> str:
    return f"{signal.storage.bucket}/{signal.storage.path}"


def get_column_name_from_signal(signal: Signal) -> str:
    return f"alias_{signal.alias}"


def get_ADUS_from_signal(signal: Signal) -> str:
    return (
        f"{signal.asset.name}/{signal.division.name}/{signal.unit.name}/{signal.name}"
    )


def get_signal_list_from_search_json(search_json: str) -> List[Signal]:
    """
    This function takes a JSON string of search results and returns a list of Signal objects.

    Parameters
    ----------
    search_json : str
        A JSON string containing the search results.

    Returns
    -------
    List[Signal]
        A list of Signal objects.
    """
    search_list = loads(search_json)

    for signal in search_list:
        if "adunit" in signal:
            signal["asset"] = signal["adunit"]["asset"]
            signal["division"] = signal["adunit"]["division"]
            signal["unit"] = signal["adunit"]["unit"]
            del signal["adunit"]

    signal_list = [Signal(**signal) for signal in search_list]

    return signal_list


ParquetPaths = Dict[str, List[SignalConfig]]
