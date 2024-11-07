from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import (
    Any,
    Protocol,
    Sequence,
    Tuple,
    Type,
    TypeVar,
)

import bytewax.operators as op
import pandas as pd
from bytewax.dataflow import Stream, operator
from bytewax.operators.windowing import EventClock, TumblingWindower, collect_window
from pandas import DataFrame
from pydantic import BaseModel

from nortech.derivers.values.schema import DeriverInputSchema, InputType

FilteredInputType = TypeVar("FilteredInputType", bound=DeriverInputSchema)

T = TypeVar("T")


@operator
def key_all(step_id: str, up: Stream[T]) -> op.KeyedStream[T]:
    return op.key_on(step_id="key_on", up=up, key=lambda _: "ALL")


@operator
def unkey_all(step_id: str, up: op.KeyedStream[T]) -> Stream[T]:
    return op.map(step_id="map", up=up, mapper=lambda item: item[1])


@operator
def filter_none(
    step_id: str, up: Stream[InputType], filtered_type: Type[FilteredInputType]
) -> Stream[FilteredInputType]:
    def filter_none_mapper(
        item: InputType,
    ) -> FilteredInputType | None:
        model_dict = item.model_dump()

        if not all(value is not None for value in model_dict.values()):
            return None
        return filtered_type(**model_dict)

    return op.filter_map(step_id="filter", up=up, mapper=filter_none_mapper)


@operator
def ffill(step_id: str, up: Stream[InputType]) -> Stream[InputType]:
    def ffill_mapper(state: dict[str, Any] | None, item: InputType):
        if state is None:
            state = {}

        for key, value in item.model_dump().items():
            if value is not None:
                state[key] = value

        for key, value in state.items():
            setattr(item, key, value)

        return state, item

    keyed_all_stream = key_all(step_id="key_all", up=up)

    ffilled_keyed_stream = op.stateful_map(
        step_id="stateful_map",
        up=keyed_all_stream,
        mapper=ffill_mapper,
    )

    return unkey_all(step_id="unkey_all", up=ffilled_keyed_stream)


class ResampleFunction(Protocol):
    def __call__(self, df: DataFrame, frequency: timedelta) -> DataFrame: ...


@dataclass
class Resampler:
    downsample_function: ResampleFunction
    upsample_function: ResampleFunction


def smart_resample(df: DataFrame, frequency: timedelta, resampler: Resampler) -> DataFrame:
    return resampler.downsample_function(df, frequency)


@operator
def resample(step_id: str, up: Stream[InputType], frequency: timedelta, resampler: Resampler):
    def ts_getter(item: InputType) -> datetime:
        return item.timestamp

    clock_config = EventClock(
        ts_getter=ts_getter,
        wait_for_system_duration=timedelta(seconds=0),
    )

    window_config = TumblingWindower(
        length=frequency,
        align_to=datetime(year=2022, month=1, day=1, tzinfo=timezone.utc),
    )

    keyed_all_stream = key_all(step_id="key_all", up=up)

    keyed_collected_windows_stream = collect_window(
        step_id="collect_window",
        up=keyed_all_stream,
        clock=clock_config,
        windower=window_config,
    )

    collected_windows_stream = unkey_all(step_id="unkey_all", up=keyed_collected_windows_stream.down)

    windows_stream = op.map(
        step_id="remove_window_metadata",
        up=collected_windows_stream,
        mapper=lambda item: item[1],
    )

    df_stream = op.map(
        step_id="to_df",
        up=windows_stream,
        mapper=lambda items: (
            items[0].model_construct,
            pd.DataFrame([item.model_dump() for item in items]).set_index("timestamp"),
        ),
    )

    resampled_df_stream = op.map(
        step_id="resample_df",
        up=df_stream,
        mapper=lambda df: (
            df[0],
            smart_resample(df=df[1], frequency=frequency, resampler=resampler),
        ),
    )

    def flat_mapper(
        item: Tuple[Any, pd.DataFrame],
    ) -> Iterable[InputType]:
        df_with_index_as_column = item[1].reset_index()
        df_with_index_as_column = df_with_index_as_column.where(pd.notna(df_with_index_as_column), None)
        return map(
            lambda model_dict: item[0](**model_dict),
            df_with_index_as_column.to_dict("records"),
        )

    resampled_stream = op.flat_map(
        step_id="flat_map",
        up=resampled_df_stream,
        mapper=flat_mapper,
    )

    return resampled_stream


@operator
def list_to_dataframe(step_id: str, up: Stream[Sequence[BaseModel]]) -> Stream[DataFrame]:
    def list_to_df_mapper(items: Sequence[BaseModel]) -> DataFrame:
        return pd.DataFrame.from_records(item.model_dump() for item in items).set_index("timestamp")

    return op.map(step_id="list_to_dataframe", up=up, mapper=list_to_df_mapper)
