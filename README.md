# nortech-python
[![codecov](https://codecov.io/github/Nortech-ai/nortech-python/graph/badge.svg)](https://codecov.io/github/Nortech-ai/nortech-python)

The official Python library for Nortech AI.

## Table of Contents
- [Overview](#overview)
- [Dependencies](#dependencies)
- [Installation](#installation)
- [Config](#config)
- [Pagination](#pagination)
- [Examples](#examples)
  - [Pandas DataFrame](#pandas-dataframe)
  - [Polars DataFrame](#polars-dataframe)
  - [Polars LazyFrame](#polars-lazyframe)

## Overview

The `nortech-python` library is the official Python client for interacting with the Nortech AI platform. It provides a comprehensive interface to access and manage various components of the Nortech ecosystem, including metadata, data tools, and derivers.

The `Nortech` class serves as the primary entry point for the library. It encapsulates the core functionalities and provides a unified interface to interact with the Nortech API. It has 3 main components:

- **Metadata**: Access and manage metadata such as workspaces, assets, divisions, units, devices, and signals.
- **Datatools**: Fetch and manipulate signal data, supporting both Pandas and Polars DataFrames, time window queries, and signal filtering.
- **Derivers**: Create and manage derivers, which allow computation of new signals based on existing ones. This includes creating deriver schemas, deploying derivers, managing configurations, and testing locally.

The `Nortech` class is designed to be flexible, allowing customization of API settings such as the base URL, API key, pagination behavior, and user agent. This makes it easy to integrate the library into various environments and workflows.

## Dependencies

This package relies heavily in the following packages, and it is recommended that users have basic knowledge of them:
- [Pydantic](https://docs.pydantic.dev/latest/) - Used for schema validation and manipulation.
- [Pandas](https://pandas.pydata.org/docs/) or [Polars](https://docs.pola.rs/api/python/stable/reference/index.html) - Used for managing signal datasets.

## Installation

You can install using pip:

```bash
pip install nortech
```

Or if you are using poetry:

```bash
poetry add nortech
```

Or if you are using UV:

```bash
uv add nortech
```

## Config

Setup your environment variables with your NortechAPI Key:

```bash
export NORTECH_API_KEY="<NORTECH_API_KEY>"
```

Alternatively you can create a `.env` file in the root directory of your project with the content:

```bash
NORTECH_API_KEY="<NORTECH_API_KEY>"
```

The `Nortech` class can also recieve all configurations during initialization.

## Pagination

This feature is implemented like in the [API](https://api.apps.nor.tech/docs#section/Pagination). By default it is disabled. To enable it add the following line to your config:
```bash
NORTECH_API_IGNORE_PAGINATION=False
```

Listing functions, mostly present in the `nortech.metadata` section, have an optional `PaginationOptions` input object.
This object has 4 fields:
- size - Defines the maximum number of items to be returned by the function.
- sort_by - Defines which item field should be used for sorting.
- sort_order - Defines the sorting order, ascending or descending.
- next_token - Used to fetch the next page. Obtained from a previous request.

These functions return a `PaginatedResponse` object containing 3 functions:
- size - Number of items returned.
- data - List of items returned.
- next.token - Token that can be used in the `PaginationOptions` to fetch the next page.

`PaginatedResponse` also has a `next_pagination_options` method that returns a `PaginationOptions`, which can also be used to fetch the next page.

## Examples

### nortech.datatools

To get a DataFrame with the requested signals:

1. Go to your `Signal Search` interface.
2. Select the desired signals.
3. Select the `DataTools` exported columns and copy the resulting `search_json`.
4. Use the `signals` field and speficy a `TimeWindow` as in the examples bellow.

##### Pandas DataFrame

In order to get a [pandas](https://pandas.pydata.org/docs/) DataFrame use the `get_df` handler:

```python
from datetime import datetime

from nortech import Nortech
from nortech.core.values.signal import SignalInput, SignalInputDict
from nortech.datatools.values.windowing import TimeWindow

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

# Define the time window for data download
my_time_window = TimeWindow(start=datetime(2023, 1, 1), end=datetime(2023, 1, 31))

# Call the get_df function
df = nortech.datatools.pandas.get_df(
    signals=[signal1, signal2, signal3],
    time_window=my_time_window,
)

print(df.columns)
# Output
# [
#     'timestamp',
#     'workspace_1/asset_1/division_1/unit_1/signal_1',
#     'workspace_1/asset_1/division_1/unit_1/signal_2',
#     'workspace_2/asset_2/division_2/unit_2/signal_3'
# ]
```

##### Polars DataFrame

In order to get a [polars](https://pola-rs.github.io/polars/py-polars/html/reference/) DataFrame use the `get_df`:

```python
from datetime import datetime

from nortech import Nortech
from nortech.core.values.signal import SignalInput, SignalInputDict
from nortech.datatools.values.windowing import TimeWindow

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

# Define the time window for data download
my_time_window = TimeWindow(start=datetime(2023, 1, 1), end=datetime(2023, 1, 31))

# Call the get_df function
polars_df = nortech.datatools.polars.get_df(
    signals=[signal1, signal2, signal3],
    time_window=my_time_window,
)

print(polars_df.columns)
# Output:
# [
#     'timestamp',
#     'workspace_1/asset_1/division_1/unit_1/signal_1',
#     'workspace_1/asset_1/division_1/unit_1/signal_2',
#     'workspace_2/asset_2/division_2/unit_2/signal_3'
# ]
```

##### Polars LazyFrame

In order to get a [polars](https://pola-rs.github.io/polars/py-polars/html/reference/) LazyFrame use the `get_lazy_df`:

```python
from datetime import datetime

from nortech import Nortech
from nortech.core.values.signal import SignalInput, SignalInputDict
from nortech.datatools.values.windowing import TimeWindow

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

# Define the time window for data download
my_time_window = TimeWindow(start=datetime(2023, 1, 1), end=datetime(2023, 1, 31))

# Call the get_lazy_df function
lazy_polars_df = nortech.datatools.polars.get_lazy_df(
    signals=[signal1, signal2, signal3],
    time_window=my_time_window,
)

print(lazy_polars_df.columns)
# Output:
# [
#     'timestamp',
#     'workspace_1/asset_1/division_1/unit_1/signal_1',
#     'workspace_1/asset_1/division_1/unit_1/signal_2',
#     'workspace_2/asset_2/division_2/unit_2/signal_3'
# ]
```
