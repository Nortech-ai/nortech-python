from datetime import datetime, timedelta, timezone
from io import BytesIO
from pathlib import Path

import numpy as np
import pandas as pd
from requests_mock import Mocker

from nortech import Nortech
from nortech.datatools import TimeWindow
from nortech.metadata import SignalInput, SignalOutput


def test_download_data(
    nortech: Nortech,
    data_signal_input: SignalInput,
    data_signal_output_id_1: SignalOutput,
    data_signal_inputs: list[SignalInput],
    requests_mock: Mocker,
    tmp_path: Path,
):
    requests_mock.post(
        f"{nortech.settings.URL}/api/v1/signals",
        text=f"[{data_signal_output_id_1.model_dump_json(by_alias=True)}]",
    )

    end = datetime.now(timezone.utc)
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

    output_file = tmp_path / "test.csv"

    nortech.datatools.download.download_data(
        signals=[data_signal_input],
        time_window=time_window,
        output_path=str(output_file),
        file_format="csv",
    )

    # Verify the file was created and contains data
    assert output_file.exists()
    assert output_file.stat().st_size > 0
    with open(output_file) as f:
        content = f.read()
        assert len(content) > 0
