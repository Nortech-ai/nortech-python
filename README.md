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

- **Metadata**: Access and manage metadata such as workspaces, assets, divisions, units and signals.
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

For comprehensive documentation including all available methods, parameters, and detailed examples, see the [Documentation](docs/index.md).
