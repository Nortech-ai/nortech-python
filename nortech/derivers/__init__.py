from __future__ import annotations

from datetime import datetime
from typing import Literal

from pandas import DataFrame

from nortech.datatools.values.windowing import TimeWindow
from nortech.derivers.handlers.deriver import (
    create_deriver,
    get_deriver,
    list_derivers,
    run_deriver_locally_with_df,
    run_deriver_locally_with_source_data,
    update_deriver,
)
from nortech.derivers.services import operators as operators
from nortech.derivers.values.deriver import (
    Deriver,
    DeriverInput,
    DeriverInputs,
    DeriverOutput,
    DeriverOutputs,
    validate_deriver,
)
from nortech.gateways.nortech_api import NortechAPI
from nortech.metadata.values.pagination import PaginationOptions


class Derivers:
    """
    Client for interacting with the Nortech Derivers API.

    Attributes:
        nortech_api (NortechAPI): The Nortech API client.


    """

    def __init__(self, nortech_api: NortechAPI):
        self.nortech_api = nortech_api

    def list(
        self,
        pagination_options: PaginationOptions[Literal["id", "name", "description"]] | None = None,
    ):
        """
        List derivers.

        Args:
            pagination_options (PaginationOptions, optional): The pagination options. Defaults to None.

        Returns:
            PaginatedResponse[DeployedDeriver]: Paginated response of derivers.


        """
        return list_derivers(self.nortech_api, pagination_options)

    def get(
        self,
        deriver: str | type[Deriver],
    ):
        """
        Get a deriver.

        Args:
            deriver (type[Deriver]): Deriver class to fetch or deriver class name.

        Returns:
            DeployedDeriver: Deployed deriver.

        """
        return get_deriver(self.nortech_api, deriver)

    def create(
        self,
        deriver: type[Deriver],
        start_at: datetime | None = None,
        description: str | None = None,
        create_parents: bool = False,
    ):
        """
        Create a deriver.

        Args:
            deriver (type[Deriver]): Deriver class to create.
            start_at (datetime | None, optional): The start time for the deriver. Defaults to current time.
            description (str | None, optional): The description for the deriver. Defaults to None.
            create_parents (bool, optional): Whether to create parent entities. Defaults to False.

        Returns:
            DeployedDeriver: Deployed deriver.

        """
        return create_deriver(self.nortech_api, deriver, start_at, description, create_parents)

    def update(
        self,
        deriver: type[Deriver],
        start_at: datetime | None = None,
        description: str | None = None,
        create_parents: bool = False,
        keep_data: bool = False,
    ):
        """
        Update a deriver.

        Args:
            deriver (type[Deriver]): Deriver class to update.
            start_at (datetime | None, optional): The start time for the deriver. Defaults to current time.
            description (str | None, optional): The description for the deriver. Defaults to None.
            create_parents (bool, optional): Whether to create parent workspaces. Defaults to False.
            keep_data (bool, optional): Whether to keep the data. Defaults to False.

        Returns:
            DeployedDeriver: Deployed deriver.


        """
        return update_deriver(self.nortech_api, deriver, start_at, description, create_parents, keep_data=keep_data)

    def run_locally_with_df(
        self,
        deriver: type[Deriver],
        df: DataFrame,
        batch_size: int = 10000,
    ) -> DataFrame:
        """
        Run a deriver locally on a DataFrame. The dataframe must have a timestamp index and columns equal to the input names in the deriver definition.

        Args:
            deriver (Deriver): The deriver to run.
            batch_size (int, optional): The batch size for processing. Defaults to 10000.
            df (DataFrame): The input DataFrame.

        Returns:
            DataFrame: The processed DataFrame with derived signals.

        """
        validate_deriver(deriver)
        return run_deriver_locally_with_df(
            deriver=deriver,
            batch_size=batch_size,
            df=df,
        )

    def run_locally_with_source_data(
        self,
        deriver: type[Deriver],
        time_window: TimeWindow,
        batch_size: int = 10000,
    ) -> DataFrame:
        """
        Run a deriver locally by fetching its inputs signal data for a given time window.

        Args:
            deriver (Deriver): The deriver to run.
            time_window (TimeWindow): The time window to process.
            batch_size (int, optional): The batch size for processing. Defaults to 10000.

        Returns:
            DataFrame: The processed DataFrame with derived signals.

        """
        validate_deriver(deriver)
        return run_deriver_locally_with_source_data(
            nortech_api=self.nortech_api,
            deriver=deriver,
            batch_size=batch_size,
            time_window=time_window,
        )


__all__ = [
    "Derivers",
    "Deriver",
    "DeriverInputs",
    "DeriverOutputs",
    "DeriverInput",
    "DeriverOutput",
    "operators",
    "TimeWindow",
    "PaginationOptions",
]
