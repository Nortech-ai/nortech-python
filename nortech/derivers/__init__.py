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

    Example:
    To define a deriver, you need to create a class that inherits from the Deriver class.
    The class must have two inner classes: Inputs and Outputs.
    The Inputs class must inherit from DeriverInputs and the Outputs class must inherit from DeriverOutputs.
    The Inputs class must define the inputs of the deriver.
    The Outputs class must define the outputs of the deriver.
    The run method must be defined and return a bytewax stream.

    ```python
    import bytewax.operators as op

    from nortech.derivers import Deriver, DeriverInput, DeriverInputs, DeriverOutput, DeriverOutputs


    class MyDeriver(Deriver):
        class Inputs(DeriverInputs):
            input_1: float | None = DeriverInput(
                workspace="workspace1", asset="asset1", division="division1", unit="unit1", signal="signal1"
            )
            input_2: float | None = DeriverInput(
                workspace="workspace2", asset="asset2", division="division2", unit="unit2", signal="signal2"
            )

        class Outputs(DeriverOutputs):
            output_1: float = DeriverOutput(
                workspace="workspace1",
                asset="asset1",
                division="division1",
                unit="unit1",
                signal="new_signal1",
                description="output_1",
                long_description="output_1_long_description",
                physical_unit="m/s",
            )
            output_2: str = DeriverOutput(
                workspace="workspace2",
                asset="asset2",
                division="division2",
                unit="unit2",
                signal="new_signal2",
                description="output_2",
                long_description="output_2_long_description",
                physical_unit="m/s",
            )

        def run(self, inputs: op.Stream[Inputs]) -> op.Stream[Outputs]:
            return op.map(
                "",
                inputs,
                lambda _input: self.Outputs(
                    timestamp=_input.timestamp,
                    output_1=_input.input_1 or 0,
                    output_2=str(_input.input_2),
                ),
            )
    ```

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

        Example:
        ```python
        # Define Deriver
        class MyDeriver(Deriver):
            ...


        nortech = Nortech()
        derivers = nortech.derivers.list()
        print(derivers)
        # PaginatedResponse(
        #     size=1,
        #     next=None,
        #     data=[
        #         DeployedDeriverList(
        #             deriver=MyDeriver,
        #             description="my-description",
        #             start_at=None,
        #         )
        #     ],
        # )
        ```

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

        Example:
        ```python
        # Define Deriver
        class MyDeriver(Deriver):
            ...

        nortech = Nortech()
        derivers = nortech.derivers.get(MyDeriver)
        print(derivers)
        # DeployedDeriver(
        #     deriver=MyDeriver,
        #     description="my-description",
        #     start_at="2025-01-01T12:00:00Z",
        #     inputs=[
        #         SignalOutputNoDevice(
        #             id=1,
        #             name="input_1",
        #             description="input_1",
        #             long_description="input_1_long_description",
        #             data_type="float",
        #             physical_unit="m/s",
        #             created_at="2025-01-01T12:00:00Z",
        #             updated_at="2025-01-01T12:00:00Z",
        #             workspace=MetadataOutput(
        #                 id=1,
        #                 name="workspace1",
        #             ),
        #             asset=MetadataOutput(
        #                 id=1,
        #                 name="asset1",
        #             ),
        #             division=MetadataOutput(
        #                 id=1,
        #                 name="division1",
        #             ),
        #             unit=MetadataOutput(
        #                 id=1,
        #                 name="unit1",
        #             ),
        #         ),
        #     ],
        #     outputs=[
        #         SignalOutputNoDevice(
        #             id=2,
        #             name="output_1",
        #             description="output_1",
        #             long_description="output_1_long_description",
        #             data_type="float",
        #             physical_unit="m/s",
        #             created_at="2025-01-01T12:00:00Z",
        #             updated_at="2025-01-01T12:00:00Z",
        #             workspace=MetadataOutput(
        #                 id=1,
        #                 name="workspace1",
        #             ),
        #             asset=MetadataOutput(
        #                 id=1,
        #                 name="asset1",
        #             ),
        #             division=MetadataOutput(
        #                 id=1,
        #                 name="division1",
        #             ),
        #             unit=MetadataOutput(
        #                 id=1,
        #                 name="unit1",
        #             ),
        #         ),
        #     ]
        # )
        ```

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

        Example:
        ```python
        # Define Deriver
        class MyDeriver(Deriver):
            ...

        nortech = Nortech()
        derivers = nortech.derivers.create(MyDeriver, start_at=datetime.now(timezone.utc), description="my-description")
        print(derivers)
        # DeployedDeriver(
        #     deriver=MyDeriver,
        #     description="my-description",
        #     start_at=None,
        #     inputs=[
        #         SignalOutputNoDevice(
        #             id=1,
        #             name="input_1",
        #             description="input_1",
        #             long_description="input_1_long_description",
        #             data_type="float",
        #             physical_unit="m/s",
        #             created_at="2025-01-01T12:00:00Z",
        #             updated_at="2025-01-01T12:00:00Z",
        #             workspace=MetadataOutput(
        #                 id=1,
        #                 name="workspace1",
        #             ),
        #             asset=MetadataOutput(
        #                 id=1,
        #                 name="asset1",
        #             ),
        #             division=MetadataOutput(
        #                 id=1,
        #                 name="division1",
        #             ),
        #             unit=MetadataOutput(
        #                 id=1,
        #                 name="unit1",
        #             ),
        #         ),
        #     ],
        #     outputs=[
        #         SignalOutputNoDevice(
        #             id=2,
        #             name="output_1",
        #             description="output_1",
        #             long_description="output_1_long_description",
        #             data_type="float",
        #             physical_unit="m/s",
        #             created_at="2025-01-01T12:00:00Z",
        #             updated_at="2025-01-01T12:00:00Z",
        #             workspace=MetadataOutput(
        #                 id=1,
        #                 name="workspace1",
        #             ),
        #             asset=MetadataOutput(
        #                 id=1,
        #                 name="asset1",
        #             ),
        #             division=MetadataOutput(
        #                 id=1,
        #                 name="division1",
        #             ),
        #             unit=MetadataOutput(
        #                 id=1,
        #                 name="unit1",
        #             ),
        #         ),
        #     ]
        # )
        ```

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

        Example:
        ```python
        # Define Deriver
        class MyDeriver(Deriver):
            ...

        nortech = Nortech()
        derivers = nortech.derivers.update(MyDeriver, start_at=datetime.now(timezone.utc), description="my-description")
        print(derivers)
        # DeployedDeriver(
        #     deriver=MyDeriver,
        #     description="my-description",
        #     start_at=None,
        #     inputs=[
        #         SignalOutputNoDevice(
        #             id=1,
        #             name="input_1",
        #             description="input_1",
        #             long_description="input_1_long_description",
        #             data_type="float",
        #             physical_unit="m/s",
        #             created_at="2025-01-01T12:00:00Z",
        #             updated_at="2025-01-01T12:00:00Z",
        #             workspace=MetadataOutput(
        #                 id=1,
        #                 name="workspace1",
        #             ),
        #             asset=MetadataOutput(
        #                 id=1,
        #                 name="asset1",
        #             ),
        #             division=MetadataOutput(
        #                 id=1,
        #                 name="division1",
        #             ),
        #             unit=MetadataOutput(
        #                 id=1,
        #                 name="unit1",
        #             ),
        #         ),
        #     ],
        #     outputs=[
        #         SignalOutputNoDevice(
        #             id=2,
        #             name="output_1",
        #             description="output_1",
        #             long_description="output_1_long_description",
        #             data_type="float",
        #             physical_unit="m/s",
        #             created_at="2025-01-01T12:00:00Z",
        #             updated_at="2025-01-01T12:00:00Z",
        #             workspace=MetadataOutput(
        #                 id=1,
        #                 name="workspace1",
        #             ),
        #             asset=MetadataOutput(
        #                 id=1,
        #                 name="asset1",
        #             ),
        #             division=MetadataOutput(
        #                 id=1,
        #                 name="division1",
        #             ),
        #             unit=MetadataOutput(
        #                 id=1,
        #                 name="unit1",
        #             ),
        #         ),
        #     ]
        # )
        ```

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

        Example:
        ```python
        from datetime import datetime, timezone

        from nortech import Nortech
        from nortech.derivers import Deriver, TimeWindow

        class MyDeriver(Deriver):
            ...

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
        ```

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

        Example:
        ```python
        from datetime import datetime, timezone

        from nortech import Nortech
        from nortech.derivers import Deriver, TimeWindow

        class MyDeriver(Deriver):
            ...

        nortech = Nortech()

        # Create input DataFrame or use nortech.datatools to get data
        df = pd.DataFrame(
            {
                "timestamp": pd.date_range(start="2023-01-01", periods=100, freq="s", tz=timezone.utc),
                "input_signal": [float(i) for i in range(100)],
            }
        ).set_index("timestamp")

        # Run the deriver locally
        result_df = nortech.derivers.run_locally_with_source_data(MyDeriver, time_window=TimeWindow(start=datetime.now(timezone.utc), end=datetime.now(timezone.utc)))

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
        ```

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
