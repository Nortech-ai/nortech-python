from datetime import datetime, timezone
from io import BytesIO
from os import environ
from unittest.mock import patch

import numpy as np
import pandas as pd

from nortech.datatools.handlers.pandas import get_df
from nortech.datatools.values.signals import TimeWindow


@patch("nortech.datatools.repositories.customer_api.post")
def test_get_df(mock_post, fake_S3_data, search_json: str, time_window: TimeWindow):
    environ["CUSTOMER_API_TOKEN"] = "mocked_customer_api_token"

    now = datetime.now(timezone.utc)

    csv_df = pd.DataFrame(
        {
            "timestamp": pd.date_range(end=now, periods=24, freq="h").round("ms"),
            "asset_1/division_1/unit_1/signal_1": np.random.rand(24),
            "asset_1/division_1/unit_1/signal_2": np.random.rand(24),
            "asset_2/division_2/unit_2/signal_3": np.random.rand(24),
        }
    )

    csv_df["timestamp"] = csv_df["timestamp"].dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

    csv_content = BytesIO()
    csv_df.to_csv(csv_content, index=False)
    csv_content.seek(0)

    mock_post.return_value.status_code = 200
    mock_post.return_value.content = csv_content.getvalue()

    new_time_window = TimeWindow(
        start=time_window.start,
        end=now,
    )

    df = get_df(search_json=search_json, time_window=new_time_window)

    assert df.index.name == "timestamp"

    assert list(df.columns) == [
        "asset_1/division_1/unit_1/signal_1",
        "asset_1/division_1/unit_1/signal_2",
        "asset_2/division_2/unit_2/signal_3",
    ]

    assert df.shape == (117, 3)
