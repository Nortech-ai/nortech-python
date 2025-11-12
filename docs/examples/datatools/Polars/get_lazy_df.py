from datetime import datetime

from nortech import Nortech
from nortech.datatools.values.windowing import TimeWindow
from nortech.metadata.values.signal import SignalInput, SignalInputDict

# Initialize the Nortech client
nortech = Nortech()

# Define signals to download
signal1: SignalInputDict = {
    "workspace": "workspace1",
    "asset": "asset1",
    "division": "division1",
    "unit": "unit1",
    "signal": "signal1",
}
signal2 = 789  # Signal ID
signal3 = SignalInput(workspace="workspace2", asset="asset2", division="division2", unit="unit2", signal="signal2")

fetched_signals = nortech.metadata.signal.list(  # Fetched signals
    {"workspace": "workspace3", "asset": "asset3", "division": "division3", "unit": "unit3"}
).data

# Define the time window for data download
my_time_window = TimeWindow(start=datetime(2023, 1, 1), end=datetime(2023, 1, 31))

# Call the get_df function with manually defined signals or fetched signals
df = nortech.datatools.polars.get_lazy_df(
    signals=[signal1, signal2, signal3] + fetched_signals,
    time_window=my_time_window,
)

print(df.columns)
# [
#     "timestamp",
#     "workspace_1/asset_1/division_1/unit_1/signal_1",
#     "workspace_1/asset_1/division_1/unit_1/signal_2",
#     "workspace_2/asset_2/division_2/unit_2/signal_3",
#     "workspace_3/asset_3/division_3/unit_3/signal_4",
#     "workspace_3/asset_3/division_3/unit_3/signal_5",
# ]
