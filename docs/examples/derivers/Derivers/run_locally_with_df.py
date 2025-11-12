from datetime import timezone

import pandas as pd

from nortech import Nortech
from nortech.derivers import Deriver


class MyDeriver(Deriver): ...


nortech = Nortech()

# Create input DataFrame
df = pd.DataFrame(
    {
        "timestamp": pd.date_range(start="2023-01-01", periods=100, freq="s", tz=timezone.utc),
        "input_signal": [float(i) for i in range(100)],
    }
).set_index("timestamp")

# Run the deriver locally
result_df = nortech.derivers.run_locally_with_df(MyDeriver, df, batch_size=5000)

print(result_df)
#                            output_signal
# timestamp
# 2023-01-01 00:00:00+00:00            0.0
# 2023-01-01 00:00:01+00:00            2.0
# 2023-01-01 00:00:02+00:00            4.0
# 2023-01-01 00:00:03+00:00            6.0
# 2023-01-01 00:00:04+00:00            8.0
# ...                                  ...
# 2023-01-01 00:01:35+00:00          190.0
# 2023-01-01 00:01:36+00:00          192.0
# 2023-01-01 00:01:37+00:00          194.0
# 2023-01-01 00:01:38+00:00          196.0
# 2023-01-01 00:01:39+00:00          198.0
