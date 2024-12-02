from datetime import datetime, timedelta, timezone
from io import BytesIO

import numpy as np
import pandas as pd
import pandas.testing as pdt
from requests_mock import Mocker

from nortech import Nortech
from nortech.datatools import TimeWindow
from nortech.metadata import SignalInput, SignalInputDict, SignalOutput


def test_get_df(
    nortech: Nortech,
    data_signal_input: SignalInput,
    data_signal_input_dict: SignalInputDict,
    data_signal_output: SignalOutput,
    data_signal_output_id_1: SignalOutput,
    data_signal_output_id_2: SignalOutput,
    data_signal_inputs: list[SignalInput],
    requests_mock: Mocker,
):
    requests_mock.post(
        f"{nortech.settings.URL}/api/v1/signals",
        text=f"[{data_signal_output_id_1.model_dump_json(by_alias=True)},{data_signal_output_id_2.model_dump_json(by_alias=True)}]",
    )

    end = datetime.now(timezone.utc) - timedelta(days=1, seconds=10)
    time_window = TimeWindow(
        start=end - timedelta(days=1),
        end=end,
    )

    parquet_df = pd.DataFrame(
        {
            "timestamp": pd.date_range(end=end, periods=24, freq="h").round("ms").astype("datetime64[ms, UTC]"),
            **{signal.hash(): np.random.rand(24) for signal in data_signal_inputs},
        }
    )

    parquet_content = BytesIO()
    parquet_df.to_parquet(parquet_content, index=False, engine="pyarrow")
    parquet_content.seek(0)

    parquet_url = "http://parquet.file/"

    requests_mock.post(
        nortech.settings.URL + "/api/v1/historical-data/sync",
        json={"outputFile": parquet_url},
    )

    requests_mock.get(
        parquet_url,
        content=parquet_content.getvalue(),
    )

    df = nortech.datatools.pandas.get_df(
        signals=[data_signal_input, data_signal_input_dict, data_signal_output, 2],
        time_window=time_window,
    )
    pdt.assert_frame_equal(
        df,
        parquet_df.rename(columns={signal.hash(): f"{signal.path}" for signal in data_signal_inputs}).set_index(
            "timestamp"
        ),
    )

    assert requests_mock.call_count == 3
    get_signals_request = requests_mock.request_history[0]
    get_historical_data_request = requests_mock.request_history[1]
    get_parquet_request = requests_mock.request_history[2]
    assert get_signals_request is not None
    assert get_signals_request.json() == {"signals": [1, 2]}
    assert get_historical_data_request is not None
    assert get_historical_data_request.json() == {
        "signals": [signal.model_dump_with_rename() for signal in data_signal_inputs],
        "timeWindow": {
            "start": time_window.start.isoformat().replace("+00:00", "Z"),
            "end": time_window.end.isoformat().replace("+00:00", "Z"),
        },
    }
    assert get_parquet_request is not None
    assert get_parquet_request.url == parquet_url


def test_get_df_empty(
    nortech: Nortech,
    data_signal_input: SignalInput,
    data_signal_input_dict: SignalInputDict,
    data_signal_output: SignalOutput,
    data_signal_output_id_1: SignalOutput,
    data_signal_output_id_2: SignalOutput,
    data_signal_inputs: list[SignalInput],
    requests_mock: Mocker,
):
    requests_mock.post(
        f"{nortech.settings.URL}/api/v1/signals",
        text=f"[{data_signal_output_id_1.model_dump_json(by_alias=True)},{data_signal_output_id_2.model_dump_json(by_alias=True)}]",
    )

    end = datetime.now(timezone.utc) - timedelta(days=1, seconds=10)
    time_window = TimeWindow(
        start=end - timedelta(days=1),
        end=end,
    )

    requests_mock.post(
        nortech.settings.URL + "/api/v1/historical-data/sync",
        status_code=404,
    )

    df = nortech.datatools.pandas.get_df(
        signals=[data_signal_input, data_signal_input_dict, data_signal_output, 2],
        time_window=time_window,
    )
    signals = [
        f"{data_signal_output_id_1.workspace.name}/{data_signal_output_id_1.asset.name}/{data_signal_output_id_1.division.name}/{data_signal_output_id_1.unit.name}/{data_signal_output_id_1.name}",
        f"{data_signal_output_id_2.workspace.name}/{data_signal_output_id_2.asset.name}/{data_signal_output_id_2.division.name}/{data_signal_output_id_2.unit.name}/{data_signal_output_id_2.name}",
        f"{data_signal_input.workspace}/{data_signal_input.asset}/{data_signal_input.division}/{data_signal_input.unit}/{data_signal_input.signal}",
        f"{data_signal_input_dict['workspace']}/{data_signal_input_dict['asset']}/{data_signal_input_dict['division']}/{data_signal_input_dict['unit']}/{data_signal_input_dict['signal']}",
    ]
    pdt.assert_frame_equal(
        df,
        pd.DataFrame(columns=["timestamp"] + signals)
        .astype(
            {
                "timestamp": "datetime64[ms, UTC]",
                **{signal: "float64" for signal in signals},
            }
        )
        .set_index("timestamp"),
    )

    assert requests_mock.call_count == 2
    get_signals_request = requests_mock.request_history[0]
    get_historical_data_request = requests_mock.request_history[1]
    assert get_signals_request is not None
    assert get_signals_request.json() == {"signals": [1, 2]}
    assert get_historical_data_request is not None
    assert get_historical_data_request.json() == {
        "signals": [signal.model_dump_with_rename() for signal in data_signal_inputs],
        "timeWindow": {
            "start": time_window.start.isoformat().replace("+00:00", "Z"),
            "end": time_window.end.isoformat().replace("+00:00", "Z"),
        },
    }


def test_get_df_hot_experimental(
    nortech: Nortech,
    data_signal_input: SignalInput,
    data_signal_input_dict: SignalInputDict,
    data_signal_output: SignalOutput,
    data_signal_output_id_1: SignalOutput,
    data_signal_output_id_2: SignalOutput,
    data_signal_inputs: list[SignalInput],
    requests_mock: Mocker,
):
    nortech.settings.EXPERIMENTAL_FEATURES = True

    requests_mock.post(
        f"{nortech.settings.URL}/api/v1/signals",
        text=f"[{data_signal_output_id_1.model_dump_json(by_alias=True)},{data_signal_output_id_2.model_dump_json(by_alias=True)}]",
    )

    end = datetime.now(timezone.utc) + timedelta(seconds=10)
    time_window = TimeWindow(
        start=end - timedelta(days=1),
        end=end,
    )

    csv_df = pd.DataFrame(
        {
            "timestamp": pd.date_range(end=time_window.end, periods=24, freq="h")
            .round("ms")
            .astype("datetime64[ms, UTC]"),
            **{
                signal: np.random.rand(24)
                for signal in [
                    data_signal_input.path,
                    SignalInput.model_validate(data_signal_input_dict).path,
                    data_signal_output.to_signal_input().path,
                    data_signal_output_id_1.to_signal_input().path,
                ]
            },
        }
    )

    csv_content = BytesIO()
    csv_df.to_csv(csv_content, index=False)
    csv_content.seek(0)

    requests_mock.post(
        nortech.settings.URL + "/timescale",
        content=csv_content.getvalue(),
    )

    data_signal_input = data_signal_input.model_copy(update={"signal": "test_signal_1"})
    data_signal_input_dict["signal"] = "test_signal_2"
    data_signal_output = data_signal_output.model_copy(update={"name": "test_signal_3"})

    df = nortech.datatools.pandas.get_df(
        signals=[data_signal_input, data_signal_input_dict, data_signal_output, 2],
        time_window=time_window,
    )
    pdt.assert_frame_equal(df, csv_df.set_index("timestamp"))

    assert requests_mock.call_count == 2
    get_signals_request = requests_mock.request_history[0]
    get_timescale_request = requests_mock.request_history[1]
    assert get_signals_request is not None
    assert get_signals_request.json() == {"signals": [1, 2]}
    assert get_timescale_request is not None
    assert get_timescale_request.json() == {
        "signals": [signal.model_dump() for signal in data_signal_inputs],
        "time_window": {
            "start": time_window.start.isoformat().replace("+00:00", "Z"),
            "end": time_window.end.isoformat().replace("+00:00", "Z"),
        },
    }


def test_get_df_hot_empty_experimental(
    nortech: Nortech,
    data_signal_input: SignalInput,
    data_signal_input_dict: SignalInputDict,
    data_signal_output: SignalOutput,
    data_signal_output_id_1: SignalOutput,
    data_signal_output_id_2: SignalOutput,
    data_signal_inputs: list[SignalInput],
    requests_mock: Mocker,
):
    nortech.settings.EXPERIMENTAL_FEATURES = True

    requests_mock.post(
        f"{nortech.settings.URL}/api/v1/signals",
        text=f"[{data_signal_output_id_1.model_dump_json(by_alias=True)},{data_signal_output_id_2.model_dump_json(by_alias=True)}]",
    )

    end = datetime.now(timezone.utc) + timedelta(seconds=10)
    time_window = TimeWindow(
        start=end - timedelta(days=1),
        end=end,
    )

    requests_mock.post(
        nortech.settings.URL + "/timescale",
        status_code=404,
    )

    df = nortech.datatools.pandas.get_df(
        signals=[data_signal_input, data_signal_input_dict, data_signal_output, 2],
        time_window=time_window,
    )
    signals = [
        f"{data_signal_output_id_1.workspace.name}/{data_signal_output_id_1.asset.name}/{data_signal_output_id_1.division.name}/{data_signal_output_id_1.unit.name}/{data_signal_output_id_1.name}",
        f"{data_signal_output_id_2.workspace.name}/{data_signal_output_id_2.asset.name}/{data_signal_output_id_2.division.name}/{data_signal_output_id_2.unit.name}/{data_signal_output_id_2.name}",
        f"{data_signal_input.workspace}/{data_signal_input.asset}/{data_signal_input.division}/{data_signal_input.unit}/{data_signal_input.signal}",
        f"{data_signal_input_dict['workspace']}/{data_signal_input_dict['asset']}/{data_signal_input_dict['division']}/{data_signal_input_dict['unit']}/{data_signal_input_dict['signal']}",
    ]
    pdt.assert_frame_equal(
        df,
        pd.DataFrame(columns=["timestamp"] + signals)
        .astype(
            {
                "timestamp": "datetime64[ms, UTC]",
                **{signal: "float64" for signal in signals},
            }
        )
        .set_index("timestamp"),
    )

    assert requests_mock.call_count == 2
    get_signals_request = requests_mock.request_history[0]
    get_timescale_request = requests_mock.request_history[1]
    assert get_signals_request is not None
    assert get_signals_request.json() == {"signals": [1, 2]}
    assert get_timescale_request is not None
    assert get_timescale_request.json() == {
        "signals": [signal.model_dump() for signal in data_signal_inputs],
        "time_window": {
            "start": time_window.start.isoformat().replace("+00:00", "Z"),
            "end": time_window.end.isoformat().replace("+00:00", "Z"),
        },
    }


def test_get_df_cold_experimental(
    nortech: Nortech,
    data_signal_input: SignalInput,
    data_signal_input_dict: SignalInputDict,
    data_signal_output: SignalOutput,
    data_signal_output_id_1: SignalOutput,
    data_signal_output_id_2: SignalOutput,
    data_signal_inputs: list[SignalInput],
    requests_mock: Mocker,
):
    nortech.settings.EXPERIMENTAL_FEATURES = True

    requests_mock.post(
        f"{nortech.settings.URL}/api/v1/signals",
        text=f"[{data_signal_output_id_1.model_dump_json(by_alias=True)},{data_signal_output_id_2.model_dump_json(by_alias=True)}]",
    )

    end = datetime.now(timezone.utc) - timedelta(days=1, seconds=10)
    time_window = TimeWindow(
        start=end - timedelta(days=1),
        end=end,
    )

    parquet_df = pd.DataFrame(
        {
            "timestamp": pd.date_range(end=end, periods=24, freq="h").round("ms").astype("datetime64[ms, UTC]"),
            **{signal.hash(): np.random.rand(24) for signal in data_signal_inputs},
        }
    )

    parquet_content = BytesIO()
    parquet_df.to_parquet(parquet_content, index=False, engine="pyarrow")
    parquet_content.seek(0)

    parquet_url = "http://parquet.file/"

    requests_mock.post(
        nortech.settings.URL + "/api/v1/historical-data/sync",
        json={"outputFile": parquet_url},
    )

    requests_mock.get(
        parquet_url,
        content=parquet_content.getvalue(),
    )

    df = nortech.datatools.pandas.get_df(
        signals=[data_signal_input, data_signal_input_dict, data_signal_output, 2],
        time_window=time_window,
    )
    pdt.assert_frame_equal(
        df,
        parquet_df.rename(columns={signal.hash(): f"{signal.path}" for signal in data_signal_inputs}).set_index(
            "timestamp"
        ),
    )

    assert requests_mock.call_count == 3
    get_signals_request = requests_mock.request_history[0]
    get_historical_data_request = requests_mock.request_history[1]
    get_parquet_request = requests_mock.request_history[2]
    assert get_signals_request is not None
    assert get_signals_request.json() == {"signals": [1, 2]}
    assert get_historical_data_request is not None
    assert get_historical_data_request.json() == {
        "signals": [signal.model_dump_with_rename() for signal in data_signal_inputs],
        "timeWindow": {
            "start": time_window.start.isoformat().replace("+00:00", "Z"),
            "end": time_window.end.isoformat().replace("+00:00", "Z"),
        },
    }
    assert get_parquet_request is not None
    assert get_parquet_request.url == parquet_url


def test_get_df_cold_empty_experimental(
    nortech: Nortech,
    data_signal_input: SignalInput,
    data_signal_input_dict: SignalInputDict,
    data_signal_output: SignalOutput,
    data_signal_output_id_1: SignalOutput,
    data_signal_output_id_2: SignalOutput,
    data_signal_inputs: list[SignalInput],
    requests_mock: Mocker,
):
    nortech.settings.EXPERIMENTAL_FEATURES = True

    requests_mock.post(
        f"{nortech.settings.URL}/api/v1/signals",
        text=f"[{data_signal_output_id_1.model_dump_json(by_alias=True)},{data_signal_output_id_2.model_dump_json(by_alias=True)}]",
    )

    end = datetime.now(timezone.utc) - timedelta(days=1, seconds=10)
    time_window = TimeWindow(
        start=end - timedelta(days=1),
        end=end,
    )

    requests_mock.post(
        nortech.settings.URL + "/api/v1/historical-data/sync",
        status_code=404,
    )

    df = nortech.datatools.pandas.get_df(
        signals=[data_signal_input, data_signal_input_dict, data_signal_output, 2],
        time_window=time_window,
    )
    signals = [
        f"{data_signal_output_id_1.workspace.name}/{data_signal_output_id_1.asset.name}/{data_signal_output_id_1.division.name}/{data_signal_output_id_1.unit.name}/{data_signal_output_id_1.name}",
        f"{data_signal_output_id_2.workspace.name}/{data_signal_output_id_2.asset.name}/{data_signal_output_id_2.division.name}/{data_signal_output_id_2.unit.name}/{data_signal_output_id_2.name}",
        f"{data_signal_input.workspace}/{data_signal_input.asset}/{data_signal_input.division}/{data_signal_input.unit}/{data_signal_input.signal}",
        f"{data_signal_input_dict['workspace']}/{data_signal_input_dict['asset']}/{data_signal_input_dict['division']}/{data_signal_input_dict['unit']}/{data_signal_input_dict['signal']}",
    ]
    pdt.assert_frame_equal(
        df,
        pd.DataFrame(columns=["timestamp"] + signals)
        .astype(
            {
                "timestamp": "datetime64[ms, UTC]",
                **{signal: "float64" for signal in signals},
            }
        )
        .set_index("timestamp"),
    )

    assert requests_mock.call_count == 2
    get_signals_request = requests_mock.request_history[0]
    get_historical_data_request = requests_mock.request_history[1]
    assert get_signals_request is not None
    assert get_signals_request.json() == {"signals": [1, 2]}
    assert get_historical_data_request is not None
    assert get_historical_data_request.json() == {
        "signals": [signal.model_dump_with_rename() for signal in data_signal_inputs],
        "timeWindow": {
            "start": time_window.start.isoformat().replace("+00:00", "Z"),
            "end": time_window.end.isoformat().replace("+00:00", "Z"),
        },
    }


def test_get_df_hot_and_cold_experimental(
    nortech: Nortech,
    data_signal_input: SignalInput,
    data_signal_input_dict: SignalInputDict,
    data_signal_output: SignalOutput,
    data_signal_output_id_1: SignalOutput,
    data_signal_output_id_2: SignalOutput,
    data_signal_inputs: list[SignalInput],
    requests_mock: Mocker,
):
    nortech.settings.EXPERIMENTAL_FEATURES = True

    requests_mock.post(
        f"{nortech.settings.URL}/api/v1/signals",
        text=f"[{data_signal_output_id_1.model_dump_json(by_alias=True)},{data_signal_output_id_2.model_dump_json(by_alias=True)}]",
    )

    end = datetime.now(timezone.utc)
    start_hot = end_cold = end - timedelta(days=1, seconds=10)
    start_cold = start_hot - timedelta(days=1)

    time_window = TimeWindow(
        start=start_cold,
        end=end,
    )

    csv_df = pd.DataFrame(
        {
            "timestamp": pd.date_range(end=end, periods=24, freq="h").round("ms").astype("datetime64[ms, UTC]"),
            **{
                signal: np.random.rand(24)
                for signal in [
                    data_signal_input.path,
                    SignalInput.model_validate(data_signal_input_dict).path,
                    data_signal_output.to_signal_input().path,
                    data_signal_output_id_1.to_signal_input().path,
                ]
            },
        }
    )
    parquet_df = pd.DataFrame(
        {
            "timestamp": pd.date_range(end=end_cold, periods=24, freq="h").round("ms").astype("datetime64[ms, UTC]"),
            **{signal.hash(): np.random.rand(24) for signal in data_signal_inputs},
        }
    )

    csv_content = BytesIO()
    csv_df.to_csv(csv_content, index=False)
    csv_content.seek(0)

    requests_mock.post(
        nortech.settings.URL + "/timescale",
        content=csv_content.getvalue(),
    )

    parquet_content = BytesIO()
    parquet_df.to_parquet(parquet_content, index=False, engine="pyarrow")
    parquet_content.seek(0)

    parquet_url = "http://parquet.file/"

    requests_mock.post(
        nortech.settings.URL + "/api/v1/historical-data/sync",
        json={"outputFile": parquet_url},
    )

    requests_mock.get(
        parquet_url,
        content=parquet_content.getvalue(),
    )

    df = nortech.datatools.pandas.get_df(
        signals=[data_signal_input, data_signal_input_dict, data_signal_output, 2],
        time_window=time_window,
    )
    pdt.assert_frame_equal(
        df.sort_index().reset_index(drop=True),
        pd.concat(
            [
                csv_df,
                parquet_df.rename(columns={signal.hash(): f"{signal.path}" for signal in data_signal_inputs}),
            ]
        )
        .set_index("timestamp")
        .sort_index()
        .reset_index(drop=True),
    )

    assert requests_mock.call_count == 4
    get_signals_request = requests_mock.request_history[0]
    get_timescale_request = requests_mock.request_history[1]
    get_historical_data_request = requests_mock.request_history[2]
    get_parquet_request = requests_mock.request_history[3]
    assert get_signals_request is not None
    assert get_signals_request.json() == {"signals": [1, 2]}
    assert get_timescale_request is not None
    assert get_timescale_request.json()["signals"] == [signal.model_dump() for signal in data_signal_inputs]
    assert get_timescale_request.json()["time_window"]["end"] == time_window.end.isoformat().replace("+00:00", "Z")
    assert get_historical_data_request is not None
    assert get_historical_data_request.json()["signals"] == [
        signal.model_dump_with_rename() for signal in data_signal_inputs
    ]
    assert get_historical_data_request.json()["timeWindow"]["start"] == time_window.start.isoformat().replace(
        "+00:00", "Z"
    )
    assert get_parquet_request is not None
    assert get_parquet_request.url == parquet_url


def test_get_df_hot_and_cold_cold_empty_experimental(
    nortech: Nortech,
    data_signal_input: SignalInput,
    data_signal_input_dict: SignalInputDict,
    data_signal_output: SignalOutput,
    data_signal_output_id_1: SignalOutput,
    data_signal_output_id_2: SignalOutput,
    data_signal_inputs: list[SignalInput],
    requests_mock: Mocker,
):
    nortech.settings.EXPERIMENTAL_FEATURES = True

    requests_mock.post(
        f"{nortech.settings.URL}/api/v1/signals",
        text=f"[{data_signal_output_id_1.model_dump_json(by_alias=True)},{data_signal_output_id_2.model_dump_json(by_alias=True)}]",
    )

    end = datetime.now(timezone.utc)
    start_hot = end - timedelta(days=1, seconds=10)
    start_cold = start_hot - timedelta(days=1)

    time_window = TimeWindow(
        start=start_cold,
        end=end,
    )

    csv_df = pd.DataFrame(
        {
            "timestamp": pd.date_range(end=end, periods=24, freq="h").round("ms").astype("datetime64[ms, UTC]"),
            **{
                signal: np.random.rand(24)
                for signal in [
                    data_signal_input.path,
                    SignalInput.model_validate(data_signal_input_dict).path,
                    data_signal_output.to_signal_input().path,
                    data_signal_output_id_1.to_signal_input().path,
                ]
            },
        }
    )

    csv_content = BytesIO()
    csv_df.to_csv(csv_content, index=False)
    csv_content.seek(0)

    requests_mock.post(
        nortech.settings.URL + "/timescale",
        content=csv_content.getvalue(),
    )

    requests_mock.post(
        nortech.settings.URL + "/api/v1/historical-data/sync",
        status_code=404,
    )

    df = nortech.datatools.pandas.get_df(
        signals=[data_signal_input, data_signal_input_dict, data_signal_output, 2],
        time_window=time_window,
    )

    assert requests_mock.call_count == 3
    pdt.assert_frame_equal(df, csv_df.set_index("timestamp"))

    assert requests_mock.call_count == 3
    get_signals_request = requests_mock.request_history[0]
    get_timescale_request = requests_mock.request_history[1]
    get_historical_data_request = requests_mock.request_history[2]
    assert get_signals_request is not None
    assert get_signals_request.json() == {"signals": [1, 2]}
    assert get_timescale_request is not None
    assert get_timescale_request.json()["signals"] == [signal.model_dump() for signal in data_signal_inputs]
    assert get_timescale_request.json()["time_window"]["end"] == time_window.end.isoformat().replace("+00:00", "Z")
    assert get_historical_data_request is not None
    assert get_historical_data_request.json()["signals"] == [
        signal.model_dump_with_rename() for signal in data_signal_inputs
    ]
    assert get_historical_data_request.json()["timeWindow"]["start"] == time_window.start.isoformat().replace(
        "+00:00", "Z"
    )


def test_get_df_hot_and_cold_hot_empty_experimental(
    nortech: Nortech,
    data_signal_input: SignalInput,
    data_signal_input_dict: SignalInputDict,
    data_signal_output: SignalOutput,
    data_signal_output_id_1: SignalOutput,
    data_signal_output_id_2: SignalOutput,
    data_signal_inputs: list[SignalInput],
    requests_mock: Mocker,
):
    nortech.settings.EXPERIMENTAL_FEATURES = True

    requests_mock.post(
        f"{nortech.settings.URL}/api/v1/signals",
        text=f"[{data_signal_output_id_1.model_dump_json(by_alias=True)},{data_signal_output_id_2.model_dump_json(by_alias=True)}]",
    )

    end = datetime.now(timezone.utc)
    start_hot = end_cold = end - timedelta(days=1, seconds=10)
    start_cold = start_hot - timedelta(days=1)

    time_window = TimeWindow(
        start=start_cold,
        end=end,
    )

    parquet_df = pd.DataFrame(
        {
            "timestamp": pd.date_range(end=end_cold, periods=24, freq="h").round("ms").astype("datetime64[ms, UTC]"),
            **{signal.hash(): np.random.rand(24) for signal in data_signal_inputs},
        }
    )

    parquet_content = BytesIO()
    parquet_df.to_parquet(parquet_content, index=False, engine="pyarrow")
    parquet_content.seek(0)

    parquet_url = "http://parquet.file/"

    requests_mock.post(
        nortech.settings.URL + "/api/v1/historical-data/sync",
        json={"outputFile": parquet_url},
    )

    requests_mock.get(
        parquet_url,
        content=parquet_content.getvalue(),
    )

    requests_mock.post(
        nortech.settings.URL + "/timescale",
        status_code=404,
    )

    df = nortech.datatools.pandas.get_df(
        signals=[data_signal_input, data_signal_input_dict, data_signal_output, 2],
        time_window=time_window,
    )
    pdt.assert_frame_equal(
        df,
        parquet_df.rename(columns={signal.hash(): f"{signal.path}" for signal in data_signal_inputs})
        .set_index("timestamp")
        .sort_index(axis=1),
    )

    assert requests_mock.call_count == 4
    get_signals_request = requests_mock.request_history[0]
    get_timescale_request = requests_mock.request_history[1]
    get_historical_data_request = requests_mock.request_history[2]
    get_parquet_request = requests_mock.request_history[3]
    assert get_signals_request is not None
    assert get_signals_request.json() == {"signals": [1, 2]}
    assert get_timescale_request is not None
    assert get_timescale_request.json()["signals"] == [signal.model_dump() for signal in data_signal_inputs]
    assert get_timescale_request.json()["time_window"]["end"] == time_window.end.isoformat().replace("+00:00", "Z")
    assert get_historical_data_request is not None
    assert get_historical_data_request.json()["signals"] == [
        signal.model_dump_with_rename() for signal in data_signal_inputs
    ]
    assert get_historical_data_request.json()["timeWindow"]["start"] == time_window.start.isoformat().replace(
        "+00:00", "Z"
    )
    assert get_parquet_request is not None
    assert get_parquet_request.url == parquet_url


def test_get_df_hot_and_cold_hot_and_cold_empty_experimental(
    nortech: Nortech,
    data_signal_input: SignalInput,
    data_signal_input_dict: SignalInputDict,
    data_signal_output: SignalOutput,
    data_signal_output_id_1: SignalOutput,
    data_signal_output_id_2: SignalOutput,
    data_signal_inputs: list[SignalInput],
    requests_mock: Mocker,
):
    nortech.settings.EXPERIMENTAL_FEATURES = True

    requests_mock.post(
        f"{nortech.settings.URL}/api/v1/signals",
        text=f"[{data_signal_output_id_1.model_dump_json(by_alias=True)},{data_signal_output_id_2.model_dump_json(by_alias=True)}]",
    )

    end = datetime.now(timezone.utc)
    start_hot = end - timedelta(days=1, seconds=10)
    start_cold = start_hot - timedelta(days=1)

    time_window = TimeWindow(
        start=start_cold,
        end=end,
    )

    requests_mock.post(
        nortech.settings.URL + "/api/v1/historical-data/sync",
        status_code=404,
    )

    requests_mock.post(
        nortech.settings.URL + "/timescale",
        status_code=404,
    )

    df = nortech.datatools.pandas.get_df(
        signals=[data_signal_input, data_signal_input_dict, data_signal_output, 2],
        time_window=time_window,
    )
    signals = [
        f"{data_signal_output_id_1.workspace.name}/{data_signal_output_id_1.asset.name}/{data_signal_output_id_1.division.name}/{data_signal_output_id_1.unit.name}/{data_signal_output_id_1.name}",
        f"{data_signal_input.workspace}/{data_signal_input.asset}/{data_signal_input.division}/{data_signal_input.unit}/{data_signal_input.signal}",
        f"{data_signal_input_dict['workspace']}/{data_signal_input_dict['asset']}/{data_signal_input_dict['division']}/{data_signal_input_dict['unit']}/{data_signal_input_dict['signal']}",
        f"{data_signal_output.workspace.name}/{data_signal_output.asset.name}/{data_signal_output.division.name}/{data_signal_output.unit.name}/{data_signal_output.name}",
    ]
    pdt.assert_frame_equal(
        df,
        pd.DataFrame(columns=["timestamp"] + signals)
        .astype(
            {
                "timestamp": "datetime64[ms, UTC]",
                **{signal: "float64" for signal in signals},
            }
        )
        .set_index("timestamp")
        .sort_index(axis=1),
    )

    assert requests_mock.call_count == 3
    get_signals_request = requests_mock.request_history[0]
    get_timescale_request = requests_mock.request_history[1]
    get_historical_data_request = requests_mock.request_history[2]
    assert get_signals_request is not None
    assert get_signals_request.json() == {"signals": [1, 2]}
    assert get_timescale_request is not None
    assert get_timescale_request.json()["signals"] == [signal.model_dump() for signal in data_signal_inputs]
    assert get_timescale_request.json()["time_window"]["end"] == time_window.end.isoformat().replace("+00:00", "Z")
    assert get_historical_data_request is not None
    assert get_historical_data_request.json()["signals"] == [
        signal.model_dump_with_rename() for signal in data_signal_inputs
    ]
    assert get_historical_data_request.json()["timeWindow"]["start"] == time_window.start.isoformat().replace(
        "+00:00", "Z"
    )
