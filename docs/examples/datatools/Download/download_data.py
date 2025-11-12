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

# Specify the output path and file format
output_path = "path/to/output"
file_format = "parquet"

# Call the download_data function with manually defined signals or fetched signals
nortech.datatools.download.download_data(
    signals=[signal1, signal2, signal3] + fetched_signals,
    time_window=my_time_window,
    output_path=output_path,
    file_format=file_format,
)
