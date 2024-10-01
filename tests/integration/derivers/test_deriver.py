from datetime import datetime, timezone

import pandas as pd
from pytest import raises

from nortech.derivers.handlers.deriver import deploy_deriver, run_deriver_locally
from nortech.derivers.services.customer_api import CustomerWorkspace
from nortech.derivers.values.instance import Deriver, DeriverInput, DeriverOutput
from nortech.derivers.values.physical_units import celsius
from nortech.shared.gateways.customer_api import CustomerAPI, CustomerAPISettings


def create_test_schema():
    from typing import Optional

    import bytewax.operators as op
    from bytewax.dataflow import Stream
    from pydantic import BaseModel

    from nortech.derivers.values.physical_units import temperature
    from nortech.derivers.values.schema import (
        DeriverInputSchema,
        DeriverOutputSchema,
        DeriverSchema,
        InputField,
        OutputField,
    )

    class Input(DeriverInputSchema):
        input_signal: Optional[float] = InputField(
            description="Input signal description",
            physicalQuantity=temperature,
        )

    class Output(DeriverOutputSchema):
        output_signal: Optional[float] = OutputField(
            description="Output signal description",
            physicalQuantity=temperature,
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
        customer="Customer",
        workspace="Workspace",
        asset="Asset",
        division="Division",
        unit="Unit",
        signal="Signal",
        physicalUnit=celsius,
    )
}

outputs = {
    deriver_schema.outputs.output_signal: DeriverOutput(
        customer="Customer",
        workspace="Workspace",
        asset="Asset",
        division="Division",
        unit="Unit",
        signal="Signal",
        physicalUnit=celsius,
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
    create_deriver_schema=create_test_schema,
)


def test_deriver_schema_fail():
    from nortech.derivers.values.physical_units import temperature

    def create_test_schema_with_missing_import():
        from typing import Optional

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
            input_signal: Optional[float] = InputField(
                description="Input signal description",
                physicalQuantity=temperature,
            )

        class Output(DeriverOutputSchema):
            output_signal: Optional[float] = OutputField(
                description="Output signal description",
                physicalQuantity=temperature,
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
            customer="Customer",
            workspace="Workspace",
            asset="Asset",
            division="Division",
            unit="Unit",
            signal="Signal",
            physicalUnit=celsius,
        )
    }

    outputs = {
        deriver_schema.outputs.output_signal: DeriverOutput(
            customer="Customer",
            workspace="Workspace",
            asset="Asset",
            division="Division",
            unit="Unit",
            signal="Signal",
            physicalUnit=celsius,
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


def test_deriver_deploy(requests_mock):
    customer_api_url = "https://api.apps.nor.tech"

    customer_API = CustomerAPI(
        settings=CustomerAPISettings(
            URL=customer_api_url,
            TOKEN="test",
        )
    )

    customer_workspace = CustomerWorkspace(
        customer_name="Customer",
        workspace_name="Workspace",
    )

    mock_response_data = {
        "status": "success",
        "data": {"message": "Deriver deployed successfully"},
    }

    requests_mock.post(
        url=customer_api_url + "/api/v1/derivers/createDeriver",
        json=mock_response_data,
    )

    deriver_diff = deploy_deriver(
        customer_API=customer_API,
        customer_workspace=customer_workspace,
        deriver=deriver,
        dry_run=True,
    )

    assert requests_mock.call_count == 1

    assert deriver_diff == mock_response_data


def test_deriver_run_locally():
    size = 100
    df = pd.DataFrame(
        {
            "timestamp": pd.date_range(start="2023-01-01", periods=size, freq="s", tz=timezone.utc),
            "input_signal": [float(i) for i in range(100)],
        }
    ).set_index("timestamp")

    output_deriver = run_deriver_locally(df=df, deriver=deriver)

    renamed_df = df.rename(columns={"input_signal": "output_signal"})
    print(output_deriver)
    print(renamed_df)

    assert output_deriver.equals(renamed_df)
