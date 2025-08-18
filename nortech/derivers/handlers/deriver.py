from __future__ import annotations

from datetime import datetime
from typing import Literal

import bytewax.operators as op
from bytewax.dataflow import Dataflow
from bytewax.testing import TestingSink, TestingSource, run_main
from pandas import DataFrame, DatetimeIndex, isna

from nortech.datatools.handlers.pandas import get_df
from nortech.datatools.values.windowing import TimeWindow
from nortech.derivers.services.nortech_api import create_deriver as create_deriver_api
from nortech.derivers.services.nortech_api import get_deriver as get_deriver_api
from nortech.derivers.services.nortech_api import list_derivers as list_derivers_api
from nortech.derivers.services.nortech_api import update_deriver as update_deriver_api
from nortech.derivers.values.deriver import Deriver, validate_deriver
from nortech.gateways.nortech_api import NortechAPI
from nortech.metadata.values.pagination import PaginationOptions


def list_derivers(
    nortech_api: NortechAPI,
    pagination_options: PaginationOptions[Literal["id", "name", "description"]] | None = None,
):
    return list_derivers_api(
        nortech_api=nortech_api,
        pagination_options=pagination_options,
    )


def get_deriver(
    nortech_api: NortechAPI,
    deriver: str | type[Deriver],
):
    if not isinstance(deriver, str):
        validate_deriver(deriver)
        deriver = deriver.__name__

    return get_deriver_api(
        nortech_api=nortech_api,
        deriver=deriver,
    )


def create_deriver(
    nortech_api: NortechAPI,
    deriver: type[Deriver],
    start_at: datetime | None = None,
    description: str | None = None,
    create_parents: bool = False,
):
    validate_deriver(deriver)
    return create_deriver_api(
        nortech_api=nortech_api,
        deriver=deriver,
        start_at=start_at,
        description=description,
        create_parents=create_parents,
    )


def update_deriver(
    nortech_api: NortechAPI,
    deriver: type[Deriver],
    start_at: datetime | None = None,
    description: str | None = None,
    create_parents: bool = False,
    keep_data: bool = False,
):
    validate_deriver(deriver)
    return update_deriver_api(
        nortech_api=nortech_api,
        deriver=deriver,
        start_at=start_at,
        description=description,
        create_parents=create_parents,
        keep_data=keep_data,
    )


def run_deriver_locally_with_df(
    deriver: type[Deriver],
    df: DataFrame,
    batch_size: int = 10000,
):
    validate_deriver(deriver)

    if not isinstance(df.index, DatetimeIndex):
        raise ValueError("df must have a datetime index")

    df_timezone = df.index.tz
    df.index = df.index.tz_convert("UTC")

    def df_to_inputs(df: DataFrame):
        for deriver_input in df.reset_index().to_dict("records"):
            input_with_none = {k: (None if isna(v) else v) for k, v in deriver_input.items()}
            yield deriver.Inputs.model_validate(input_with_none)

    source = TestingSource(ib=df_to_inputs(df), batch_size=batch_size)
    flow = Dataflow(deriver.__name__)
    stream = op.input("input", flow, source)
    transformed_stream = deriver().run(stream)

    output_list: list[Deriver.Outputs] = []
    output_sink = TestingSink(output_list)
    op.output("out", transformed_stream, output_sink)

    run_main(flow)

    df_out = DataFrame([output.model_dump(by_alias=True) for output in output_list])
    if "timestamp" in df_out.columns:
        df_out = df_out.set_index("timestamp").tz_convert(df_timezone)
    return df_out


def run_deriver_locally_with_source_data(
    nortech_api: NortechAPI,
    deriver: type[Deriver],
    time_window: TimeWindow,
    batch_size: int = 10000,
):
    inputs = deriver.Inputs.list()
    df = get_df(nortech_api, signals=[_input for _, _input in inputs], time_window=time_window)
    path_to_name = {_input.path: name for name, _input in inputs}
    df = df.rename(columns=path_to_name)

    return run_deriver_locally_with_df(deriver, df, batch_size)
