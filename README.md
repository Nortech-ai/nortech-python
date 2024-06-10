# nortech-python

The official Python library for Nortech AI.

## Install

You can install using pip:

```bash
pip install nortech
```

Or if you are using poetry:

```bash
poetry add nortech
```

## nortech.datatools



### S3

#### Config

Setup your environment variables with the `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` provided to you:

```bash
export AWS_ACCESS_KEY_ID="<AWS_ACCESS_KEY_ID>"
export AWS_SECRET_ACCESS_KEY="<AWS_SECRET_ACCESS_KEY>"
```

If you have an `AWS_SESSION_TOKEN` instead:

```bash
export AWS_SESSION_TOKEN="<AWS_SESSION_TOKEN>"
```

As an alternative you can use the [AWS CLI](https://aws.amazon.com/cli/):

```bash
aws configure
```

#### Examples

To get a DataFrame with the requested signals:

1. Go to your `Signal Search` interface.
2. Select the desired signals.
3. Select the `DataTools` exported columns and copy the resulting `search_json`.
4. Use the `search_json` and speficy a `TimeWindow` as in the examples bellow.

##### Pandas DataFrame

In order to get a [pandas](https://pandas.pydata.org/docs/) DataFrame use the `get_df`:

```python
from datetime import datetime

from nortech.datatools import get_df, TimeWindow

search_json = """[
    {
        "name": "signal_1",
        "dataType": "float",
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
        "dataType": "float",
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
        "dataType": "float",
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
        "dataType": "float",
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
        "dataType": "float",
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
        "dataType": "float",
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
        "dataType": "float",
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
        "dataType": "float",
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
        "dataType": "float",
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
