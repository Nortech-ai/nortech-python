from __future__ import annotations

from typing import Callable

from pandas import DataFrame

from nortech.derivers.handlers.deriver import (
    deploy_deriver,
    run_deriver_locally,
    visualize_deriver,
    visualize_deriver_schema,
)
from nortech.derivers.services import operators as operators
from nortech.derivers.services.nortech_api import DeriverDiffs
from nortech.derivers.services.physical_units import get_physical_quantity
from nortech.derivers.values import physical_units
from nortech.derivers.values.instance import (
    Deriver,
    DeriverInput,
    DeriverInputType,
    DeriverOutput,
    DeriverOutputType,
)
from nortech.derivers.values.schema import (
    ConfigurationType,
    DeriverInputSchema,
    DeriverOutputSchema,
    DeriverSchema,
    InputField,
    InputType,
    OutputField,
    OutputType,
)
from nortech.gateways.nortech_api import NortechAPI


class Derivers:
    """Client for interacting with the Nortech Derivers API.

    Attributes:
        nortech_api (NortechAPI): The Nortech API client.

    """

    def __init__(self, nortech_api: NortechAPI):
        self.nortech_api = nortech_api

    def deploy_deriver(self, deriver: Deriver, workspace: str | None = None, dry_run: bool = True) -> DeriverDiffs:
        """Deploy a deriver to a workspace.

        Args:
            deriver (Deriver): The deriver to deploy.
            workspace (str, optional): The workspace to deploy to. Defaults to None.
            dry_run (bool, optional): Whether to perform a dry run. Defaults to True.

        Returns:
            DeriverDiffs: The deriver diffs.

        Example:
        ```python
        from datetime import datetime

        from pydantic import Field

        from nortech import Nortech
        from nortech.derivers import (
            Deriver,
            DeriverInput,
            DeriverOutput,
            physical_units,
        )


        def create_test_schema():
            import bytewax.operators as op
            from bytewax.dataflow import Stream
            from pydantic import BaseModel

            from nortech.derivers import (
                DeriverInputSchema,
                DeriverOutputSchema,
                DeriverSchema,
                InputField,
                OutputField,
                physical_units,
            )

            class Input(DeriverInputSchema):
                input_signal: float | None = InputField(
                    description="Input signal description",
                    physical_quantity=physical_units.temperature,
                )

            class Output(DeriverOutputSchema):
                output_signal: float | None = OutputField(
                    description="Output signal description",
                    physical_quantity=physical_units.temperature,
                    create_deriver_schema=create_test_schema,
                )

            class Configurations(BaseModel):
                configuration_value: float = Field(
                    description="Configuration value description",
                )

            def transform_stream(
                stream: Stream[Input],
                config: Configurations,
            ) -> Stream[Output]:
                output_stream = op.map(
                    step_id="map_output",
                    up=stream,
                    mapper=lambda input_message: Output(
                        timestamp=input_message.timestamp,
                        output_signal=input_message.input_signal * config.configuration_value
                        if input_message.input_signal is not None
                        else None,
                    ),
                )

                return output_stream

            return DeriverSchema(
                name="Test Schema",
                description="Test Schema description",
                inputs=Input,
                outputs=Output,
                configurations=Configurations,
                transform_stream=transform_stream,
            )


        deriver_schema = create_test_schema()

        inputs = {
            deriver_schema.inputs.input_signal: DeriverInput(
                workspace="Workspace",
                asset="Asset",
                division="Division",
                unit="Unit",
                signal="Signal",
                physicalUnit=physical_units.celsius,
            )
        }

        outputs = {
            deriver_schema.outputs.output_signal: DeriverOutput(
                workspace="Workspace",
                asset="Asset",
                division="Division",
                unit="Unit",
                signal="Signal",
                physicalUnit=physical_units.celsius,
            )
        }

        configurations = deriver_schema.configurations(
            configuration_value=2.0,
        )

        deriver = Deriver(
            name="Test Deriver",
            description="Test Deriver description",
            inputs=inputs,
            outputs=outputs,
            configurations=configurations,
            start_at=datetime(2022, 1, 1, 0, 0, 0),
            create_deriver_schema=create_test_schema,
        )

        nortech = Nortech()

        diffs = nortech.derivers.deploy_deriver(deriver)

        print(diffs)
        # DeriverDiffs(
        #     deriver_schemas={
        #         "Test Schema": SchemaDiff(
        #             old=Schema(
        #                 id=1,
        #                 hash="hash",
        #                 history_id=1,
        #                 created_at=datetime(2022, 1, 1, 0, 0, 0),
        #                 updated_at=datetime(2022, 1, 1, 0, 0, 0),
        #             ),
        #             new=Schema(
        #                 id=1,
        #                 hash="hash",
        #                 history_id=1,
        #                 created_at=datetime(2022, 1, 1, 0, 0, 0),
        #                 updated_at=datetime(2022, 1, 1, 0, 0, 0),
        #             ),
        #         )
        #     },
        #     derivers={
        #         "Test Deriver": SchemaDiff(
        #             old=Schema(
        #                 id=1,
        #                 hash="hash",
        #                 history_id=1,
        #                 created_at=datetime(2022, 1, 1, 0, 0, 0),
        #                 updated_at=datetime(2022, 1, 1, 0, 0, 0),
        #             ),
        #             new=Schema(
        #                 id=1,
        #                 hash="hash",
        #                 history_id=1,
        #                 created_at=datetime(2022, 1, 1, 0, 0, 0),
        #                 updated_at=datetime(2022, 1, 1, 0, 0, 0),
        #             ),
        #         )
        #     },
        # )
        ```

        """
        return deploy_deriver(self.nortech_api, deriver, workspace, dry_run)

    def visualize_deriver_schema(self, create_deriver_schema: Callable[[], DeriverSchema]) -> None:
        """Visualize a deriver schema as a mermaid diagram rendered as markdown in all frontends.

        By default all representations will be computed and sent to the frontends.
        Frontends can decide which representation is used and how.

        In terminal IPython this will be similar to using :func:`print`, for use in richer
        frontends see Jupyter notebook examples with rich display logic.

        Args:
            create_deriver_schema (Callable[[], DeriverSchema]): A function that creates a deriver schema.

        Example:
        ```python
        from nortech import Nortech

        nortech = Nortech()

        # Define a function that creates a Deriver Schema
        def create_test_schema():
            ...
            return DeriverSchema(...)

        # Visualize the schema
        nortech.derivers.visualize_deriver_schema(create_test_schema)
        ```

        """
        return visualize_deriver_schema(create_deriver_schema)

    def visualize_deriver(self, deriver: Deriver) -> None:
        """Visualize a deriver as a mermaid diagram rendered as markdown in all frontends.

        By default all representations will be computed and sent to the frontends.
        Frontends can decide which representation is used and how.

        In terminal IPython this will be similar to using :func:`print`, for use in richer
        frontends see Jupyter notebook examples with rich display logic.

        Args:
            deriver (Deriver): The deriver to visualize.

        Example:
        ```python
        from nortech import Nortech

        nortech = Nortech()

        # Create Deriver
        deriver = ...

        # Visualize the deriver
        nortech.derivers.visualize_deriver(deriver)
        ```

        """
        return visualize_deriver(deriver)

    def run_deriver_locally(
        self,
        df: DataFrame,
        deriver: Deriver[InputType, OutputType, ConfigurationType, DeriverInputType, DeriverOutputType],
        batch_size: int = 10000,
    ) -> DataFrame:
        """Run a deriver locally on a DataFrame.

        Args:
            df (DataFrame): The input DataFrame.
            deriver (Deriver): The deriver to run.
            batch_size (int, optional): The batch size for processing. Defaults to 10000.

        Returns:
            DataFrame: The processed DataFrame with derived signals.

        Example:
        ```python
        from datetime import timezone

        import pandas as pd

        from nortech import Nortech

        nortech = Nortech()

        # Create Deriver
        deriver = ...

        # Create input DataFrame or use nortech.datatools to get data
        df = pd.DataFrame(
            {
                "timestamp": pd.date_range(start="2023-01-01", periods=100, freq="s", tz=timezone.utc),
                "input_signal": [float(i) for i in range(100)],
            }
        ).set_index("timestamp")

        # Run the deriver locally
        result_df = nortech.derivers.run_deriver_locally(df, deriver, batch_size=5000)

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
        return run_deriver_locally(df, deriver, batch_size)


__all__ = [
    "Deriver",
    "DeriverInput",
    "DeriverOutput",
    "physical_units",
    "DeriverInputSchema",
    "DeriverOutputSchema",
    "DeriverSchema",
    "InputField",
    "OutputField",
    "get_physical_quantity",
    "operators",
]
