# nortech-python

The official Python library for Nortech AI.

## Table of Contents
- [Install](#install)
- [Config](#config) 
- [Overview](#overview)
  - [nortech.metadata](#nortechmetadata)
  - [nortech.datatools](#nortechdatatools)
  - [nortech.derivers](#nortechderivers)
- [Examples](#examples)
  - [Pandas DataFrame](#pandas-dataframe)
  - [Polars DataFrame](#polars-dataframe)
  - [Polars LazyFrame](#polars-lazyframe)

## Install

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

Setup your environment variables with your `NORTECH_API_TOKEN`:

```bash
export NORTECH_API_TOKEN="<NORTECH_API_TOKEN>"
```

Alternatively you can create a `.env` file in the root directory of your project with the content:

```bash
NORTECH_API_TOKEN="<NORTECH_API_TOKEN>"
```

## Overview

The `NortechAPI` class is your connection point to the Nortech API (documented at https://api.apps.nor.tech/docs). The package is organized into three main sections:

### nortech.metadata

Contains functionalities to access and manage your metadata, including:
- Workspaces
- Assets
- Divisions
- Units
- Signals

### nortech.datatools

Provides tools for fetching signal data, with support for:
- Pandas DataFrames
- Polars DataFrames
- Time window queries
- Signal filtering

### nortech.derivers

Enables creation and management of derivers - which allow you to compute new signals based on existing ones. Features include:
- Creating deriver schemas
- Deploying derivers
- Managing deriver configurations
- Testing derivers locally


### Examples

To get a DataFrame with the requested signals:

1. Go to your `Signal Search` interface.
2. Select the desired signals.
3. Select the `DataTools` exported columns and copy the resulting `search_json`.
4. Use the `search_json` and speficy a `TimeWindow` as in the examples bellow.

##### Pandas DataFrame

In order to get a [pandas](https://pandas.pydata.org/docs/) DataFrame use the `get_df` handler:

```python
from datetime import datetime

from nortech.datatools import get_df, TimeWindow

search_json = """[
    {
        "name": "signal_1",
        "data_type": "float",
        "alias": 0,
        "asset": {
            "name": "asset_1"
        },
        "division": {
            "name": "division_1"
        },
        "unit": {
            "name": "unit_1"
        },
        "storage": {
            "bucket": "nortech-test",
            "path": "scope_1_group_0"
        }
    },
    {
        "name": "signal_2",
        "data_type": "float",
        "alias": 1,
        "asset": {
            "name": "asset_1"
        },
        "division": {
            "name": "division_1"
        },
        "unit": {
            "name": "unit_1"
        },
        "storage": {
            "bucket": "nortech-test",
            "path": "scope_1_group_0"
        }
    },
    {
        "name": "signal_3",
        "data_type": "float",
        "alias": 0,
        "asset": {
            "name": "asset_2"
        },
        "division": {
            "name": "division_2"
        },
        "unit": {
            "name": "unit_2"
        },
        "storage": {
            "bucket": "nortech-test",
            "path": "scope_1_group_1"
        }
    }
]"""

time_window = TimeWindow(
            start=datetime(2020, 1, 1),
            end=datetime(2020, 1, 5),
)
df = get_df(search_json=search_json, time_window=time_window)

assert list(df.columns) == [
    'asset_1/division_1/unit_1/signal_1',
    'asset_1/division_1/unit_1/signal_2',
    'asset_2/division_2/unit_2/signal_3'
]
```

##### Polars DataFrame

In order to get a [polars](https://pola-rs.github.io/polars/py-polars/html/reference/) DataFrame use the `get_polars_df`:

```python
from datetime import datetime

from nortech.datatools import get_polars_df, TimeWindow

search_json = """[
    {
        "name": "signal_1",
        "data_type": "float",
        "alias": 0,
        "asset": {
            "name": "asset_1"
        },
        "division": {
            "name": "division_1"
        },
        "unit": {
            "name": "unit_1"
        },
        "storage": {
            "bucket": "nortech-test",
            "path": "scope_1_group_0"
        }
    },
    {
        "name": "signal_2",
        "data_type": "float",
        "alias": 1,
        "asset": {
            "name": "asset_1"
        },
        "division": {
            "name": "division_1"
        },
        "unit": {
            "name": "unit_1"
        },
        "storage": {
            "bucket": "nortech-test",
            "path": "scope_1_group_0"
        }
    },
    {
        "name": "signal_3",
        "data_type": "float",
        "alias": 0,
        "asset": {
            "name": "asset_2"
        },
        "division": {
            "name": "division_2"
        },
        "unit": {
            "name": "unit_2"
        },
        "storage": {
            "bucket": "nortech-test",
            "path": "scope_1_group_1"
        }
    }
]"""

time_window = TimeWindow(
            start=datetime(2020, 1, 1),
            end=datetime(2020, 1, 5),
)
polars_df = get_polars_df(search_json=search_json, time_window=time_window)

assert polars_df.columns == [
    'timestamp',
    'asset_1/division_1/unit_1/signal_1',
    'asset_1/division_1/unit_1/signal_2',
    'asset_2/division_2/unit_2/signal_3'
]
```

##### Polars LazyFrame

In order to get a [polars](https://pola-rs.github.io/polars/py-polars/html/reference/) LazyFrame use the `get_lazy_polars_df`:

```python
from datetime import datetime

from nortech.datatools import get_lazy_polars_df, TimeWindow

search_json = """[
    {
        "name": "signal_1",
        "data_type": "float",
        "alias": 0,
        "asset": {
            "name": "asset_1"
        },
        "division": {
            "name": "division_1"
        },
        "unit": {
            "name": "unit_1"
        },
        "storage": {
            "bucket": "nortech-test",
            "path": "scope_1_group_0"
        }
    },
    {
        "name": "signal_2",
        "data_type": "float",
        "alias": 1,
        "asset": {
            "name": "asset_1"
        },
        "division": {
            "name": "division_1"
        },
        "unit": {
            "name": "unit_1"
        },
        "storage": {
            "bucket": "nortech-test",
            "path": "scope_1_group_0"
        }
    },
    {
        "name": "signal_3",
        "data_type": "float",
        "alias": 0,
        "asset": {
            "name": "asset_2"
        },
        "division": {
            "name": "division_2"
        },
        "unit": {
            "name": "unit_2"
        },
        "storage": {
            "bucket": "nortech-test",
            "path": "scope_1_group_1"
        }
    }
]"""

time_window = TimeWindow(
            start=datetime(2020, 1, 1),
            end=datetime(2020, 1, 5),
)
lazy_polars_df = get_lazy_polars_df(search_json=search_json, time_window=time_window)

assert lazy_polars_df.columns == [
    'timestamp',
    'asset_1/division_1/unit_1/signal_1',
    'asset_1/division_1/unit_1/signal_2',
    'asset_2/division_2/unit_2/signal_3'
]
```
