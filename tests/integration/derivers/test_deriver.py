from __future__ import annotations

from datetime import datetime, timezone
from unittest.mock import patch

import pandas as pd
from pytest import raises
from requests_mock import Mocker

from nortech import Nortech
from nortech.derivers import (
    Deriver,
    DeriverDiffs,
    DeriverInput,
    DeriverOutput,
    physical_units,
    run_deriver_locally,
    visualize_deriver,
    visualize_deriver_schema,
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
        pass

    def transform_stream(
        stream: Stream[Input],
        config: Configurations,
    ) -> Stream[Output]:
        output_stream = op.map(
            step_id="map_output",
            up=stream,
            mapper=lambda input_message: Output(
                timestamp=input_message.timestamp,
                output_signal=input_message.input_signal,
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


deriver_schema_without_suggested_inputs = create_test_schema()


def create_test_schema_with_suggested_inputs():
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
            suggested_inputs=[deriver_schema_without_suggested_inputs.outputs.output_signal],
        )

    class Output(DeriverOutputSchema):
        output_signal: float | None = OutputField(
            description="Output signal description",
            physical_quantity=physical_units.temperature,
            create_deriver_schema=create_test_schema_with_suggested_inputs,
        )

    class Configurations(BaseModel):
        pass

    def transform_stream(
        stream: Stream[Input],
        config: Configurations,
    ) -> Stream[Output]:
        output_stream = op.map(
            step_id="map_output",
            up=stream,
            mapper=lambda input_message: Output(
                timestamp=input_message.timestamp,
                output_signal=input_message.input_signal,
            ),
        )

        return output_stream

    return DeriverSchema(
        name="Test Schema with suggested inputs",
        description="Test Schema description with suggested inputs",
        inputs=Input,
        outputs=Output,
        configurations=Configurations,
        transform_stream=transform_stream,
    )


deriver_schema = create_test_schema_with_suggested_inputs()

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

configurations = deriver_schema.configurations()

deriver = Deriver(
    name="Test Deriver",
    description="Test Deriver description",
    inputs=inputs,
    outputs=outputs,
    configurations=configurations,
    start_at=datetime(2022, 1, 1, 0, 0, 0),
    create_deriver_schema=create_test_schema_with_suggested_inputs,
)


def test_deriver_schema_fail():
    from nortech.derivers import physical_units

    def create_test_schema_with_missing_import():
        import bytewax.operators as op
        from bytewax.dataflow import Stream
        from pydantic import BaseModel

        from nortech.derivers.values.schema import (
            DeriverInputSchema,
            DeriverOutputSchema,
            DeriverSchema,
            InputField,
            OutputField,
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
            pass

        def transform_stream(
            stream: Stream[Input],
            config: Configurations,
        ) -> Stream[Output]:
            output_stream = op.map(
                step_id="map_output",
                up=stream,
                mapper=lambda input_message: Output(
                    timestamp=input_message.timestamp,
                    output_signal=input_message.input_signal,
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

    configurations = deriver_schema.configurations()

    with raises(NameError):
        Deriver(
            name="Test Deriver",
            description="Test Deriver description",
            inputs=inputs,
            outputs=outputs,
            configurations=configurations,
            start_at=datetime(2022, 1, 1, 0, 0, 0),
            create_deriver_schema=create_test_schema_with_missing_import,
        )


def test_deriver_deploy(nortech: Nortech, requests_mock: Mocker):
    mock_response_data = {
        "deriverSchemas": {},
        "derivers": {},
    }

    requests_mock.post(
        url=nortech.settings.URL + "/api/v1/derivers",
        json=mock_response_data,
    )

    deriver_diff = nortech.derivers.deploy_deriver(
        deriver=deriver,
        dry_run=True,
    )

    assert requests_mock.call_count == 1

    assert deriver_diff == DeriverDiffs.model_validate(mock_response_data)


def test_deriver_run_locally():
    size = 100
    df = pd.DataFrame(
        {
            "timestamp": pd.date_range(start="2023-01-01", periods=size, freq="s", tz=timezone.utc),
            "input_signal": [float(i) for i in range(size)],
        }
    ).set_index("timestamp")

    output_deriver = run_deriver_locally(df=df, deriver=deriver)

    renamed_df = df.rename(columns={"input_signal": "output_signal"})
    print(output_deriver)
    print(renamed_df)

    assert output_deriver.equals(renamed_df)


def test_visualize_deriver(snapshot):
    with patch("nortech.derivers.handlers.deriver.display") as mock_display:
        visualize_deriver(deriver=deriver)

        # Verify display was called once
        assert mock_display.call_count == 1

        # Get the Markdown object that was passed to display
        markdown_obj = mock_display.call_args[0][0]

        snapshot.assert_match(markdown_obj.data, "markdown_obj.txt")


def test_visualize_deriver_schema(snapshot):
    with patch("nortech.derivers.handlers.deriver.display") as mock_display:
        visualize_deriver_schema(create_deriver_schema=deriver.create_deriver_schema)

        # Verify display was called once
        assert mock_display.call_count == 1

        # Get the Markdown object that was passed to display
        markdown_obj = mock_display.call_args[0][0]

        snapshot.assert_match(markdown_obj.data, "markdown_obj.txt")
