from __future__ import annotations

from datetime import datetime, timedelta, timezone

import bytewax.operators as op
import pandas as pd
from bytewax.dataflow import Dataflow
from bytewax.testing import TestingSink, TestingSource, run_main

from nortech.derivers import DeriverInputSchema
from nortech.derivers import operators as internal_op


def test_key_all():
    # Create test data
    df = pd.DataFrame(
        {
            "timestamp": pd.date_range(start="2023-01-01", periods=5, freq="s", tz=timezone.utc),
            "value": [1.0, 2.0, 3.0, 4.0, 5.0],
        }
    )
    flow = Dataflow("test_key_all")

    input_source = TestingSource(
        df.to_dict(orient="records"),
    )
    stream = op.input("input", flow, input_source)
    # Apply key_all operator
    keyed_stream = internal_op.key_all("test_key", stream)

    output_list = []
    output = TestingSink(output_list)

    op.output("output", keyed_stream, output)

    run_main(flow)

    assert output_list == [
        ("ALL", {"timestamp": pd.Timestamp("2023-01-01 00:00:00+0000", tz="UTC"), "value": 1.0}),
        ("ALL", {"timestamp": pd.Timestamp("2023-01-01 00:00:01+0000", tz="UTC"), "value": 2.0}),
        ("ALL", {"timestamp": pd.Timestamp("2023-01-01 00:00:02+0000", tz="UTC"), "value": 3.0}),
        ("ALL", {"timestamp": pd.Timestamp("2023-01-01 00:00:03+0000", tz="UTC"), "value": 4.0}),
        ("ALL", {"timestamp": pd.Timestamp("2023-01-01 00:00:04+0000", tz="UTC"), "value": 5.0}),
    ]


def test_unkey_all():
    df = pd.DataFrame(
        {
            "timestamp": pd.date_range(start="2023-01-01", periods=5, freq="s", tz=timezone.utc),
            "value": [1.0, 2.0, 3.0, 4.0, 5.0],
        }
    )

    flow = Dataflow("test_key_all")

    input_source = TestingSource(
        df.to_dict(orient="records"),
    )
    stream = op.input("input", flow, input_source)
    # Apply key_all operator
    keyed_stream = internal_op.key_all("test_key", stream)
    unkeyed_stream = internal_op.unkey_all("test_unkey", keyed_stream)

    output_list = []
    output = TestingSink(output_list)

    op.output("output", unkeyed_stream, output)

    run_main(flow)

    assert output_list == df.to_dict(orient="records")


def test_filter_none():
    class TestInput(DeriverInputSchema):
        timestamp: datetime
        value: float | None

    class FilteredInput(DeriverInputSchema):
        timestamp: datetime
        value: float

    input_messages = [
        TestInput(timestamp=datetime(2023, 1, 1, 0, 0, 1, tzinfo=timezone.utc), value=1.0),
        TestInput(timestamp=datetime(2023, 1, 1, 0, 0, 2, tzinfo=timezone.utc), value=None),
        TestInput(timestamp=datetime(2023, 1, 1, 0, 0, 3, tzinfo=timezone.utc), value=3.0),
        TestInput(timestamp=datetime(2023, 1, 1, 0, 0, 4, tzinfo=timezone.utc), value=None),
        TestInput(timestamp=datetime(2023, 1, 1, 0, 0, 5, tzinfo=timezone.utc), value=5.0),
    ]

    flow = Dataflow("test_filter_none")

    input_source = TestingSource(input_messages)
    stream = op.input("input", flow, input_source)

    # Filter None values
    filtered_stream = internal_op.filter_none("test_filter", stream, FilteredInput)

    output_list = []
    output = TestingSink(output_list)

    op.output("output", filtered_stream, output)

    run_main(flow)

    assert output_list == [
        FilteredInput(timestamp=datetime(2023, 1, 1, 0, 0, 1, tzinfo=timezone.utc), value=1.0),
        FilteredInput(timestamp=datetime(2023, 1, 1, 0, 0, 3, tzinfo=timezone.utc), value=3.0),
        FilteredInput(timestamp=datetime(2023, 1, 1, 0, 0, 5, tzinfo=timezone.utc), value=5.0),
    ]


def test_ffill():
    class TestInput(DeriverInputSchema):
        timestamp: datetime
        value: float | None

    input_messages = [
        TestInput(timestamp=datetime(2023, 1, 1, 0, 0, 1, tzinfo=timezone.utc), value=1.0),
        TestInput(timestamp=datetime(2023, 1, 1, 0, 0, 2, tzinfo=timezone.utc), value=None),
        TestInput(timestamp=datetime(2023, 1, 1, 0, 0, 3, tzinfo=timezone.utc), value=3.0),
        TestInput(timestamp=datetime(2023, 1, 1, 0, 0, 4, tzinfo=timezone.utc), value=None),
        TestInput(timestamp=datetime(2023, 1, 1, 0, 0, 5, tzinfo=timezone.utc), value=5.0),
    ]

    flow = Dataflow("test_ffill")

    input_source = TestingSource(input_messages)
    stream = op.input("input", flow, input_source)

    filled_stream = internal_op.ffill("test_ffill", stream)

    output_list = []
    output = TestingSink(output_list)

    op.output("output", filled_stream, output)

    run_main(flow)

    assert output_list == [
        TestInput(timestamp=datetime(2023, 1, 1, 0, 0, 1, tzinfo=timezone.utc), value=1.0),
        TestInput(timestamp=datetime(2023, 1, 1, 0, 0, 2, tzinfo=timezone.utc), value=1.0),
        TestInput(timestamp=datetime(2023, 1, 1, 0, 0, 3, tzinfo=timezone.utc), value=3.0),
        TestInput(timestamp=datetime(2023, 1, 1, 0, 0, 4, tzinfo=timezone.utc), value=3.0),
        TestInput(timestamp=datetime(2023, 1, 1, 0, 0, 5, tzinfo=timezone.utc), value=5.0),
    ]


def test_resample():
    class TestInput(DeriverInputSchema):
        timestamp: datetime
        value: float

    input_messages = [
        TestInput(timestamp=datetime(2023, 1, 1, 0, 0, i, tzinfo=timezone.utc), value=float(i)) for i in range(10)
    ]

    flow = Dataflow("test_resample")

    input_source = TestingSource(input_messages)
    stream = op.input("input", flow, input_source)

    resampled_stream = internal_op.resample(
        "test_resample",
        stream,
        frequency=timedelta(seconds=2),
        resampler=internal_op.Resampler(
            downsample_function=lambda df, frequency: df.resample(frequency).mean(),
            upsample_function=lambda df, frequency: df.resample(frequency).ffill(),
        ),
    )

    output_list = []
    output = TestingSink(output_list)

    op.output("output", resampled_stream, output)

    run_main(flow)

    assert output_list == [
        TestInput(timestamp=datetime(2023, 1, 1, 0, 0, 0, tzinfo=timezone.utc), value=0.5),
        TestInput(timestamp=datetime(2023, 1, 1, 0, 0, 2, tzinfo=timezone.utc), value=2.5),
        TestInput(timestamp=datetime(2023, 1, 1, 0, 0, 4, tzinfo=timezone.utc), value=4.5),
        TestInput(timestamp=datetime(2023, 1, 1, 0, 0, 6, tzinfo=timezone.utc), value=6.5),
        TestInput(timestamp=datetime(2023, 1, 1, 0, 0, 8, tzinfo=timezone.utc), value=8.5),
    ]


def test_list_to_dataframe():
    class TestInput(DeriverInputSchema):
        timestamp: datetime
        value: float

    test_data = [
        [TestInput(timestamp=datetime(2023, 1, 1, 0, 0, i, tzinfo=timezone.utc), value=float(i)) for i in range(5)]
    ]

    flow = Dataflow("test_list_to_dataframe")

    input_source = TestingSource(test_data)
    stream = op.input("input", flow, input_source)

    df_stream = internal_op.list_to_dataframe("test_df", stream)

    output_list = []
    output = TestingSink(output_list)

    op.output("output", df_stream, output)

    run_main(flow)

    expected_df = pd.DataFrame(
        {
            "timestamp": [datetime(2023, 1, 1, 0, 0, i, tzinfo=timezone.utc) for i in range(5)],
            "value": [0.0, 1.0, 2.0, 3.0, 4.0],
        }
    ).set_index("timestamp")

    for df in output_list:
        assert df.equals(expected_df)
