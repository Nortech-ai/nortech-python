from __future__ import annotations

from nortech.derivers import get_physical_quantity, physical_units


def test_get_quantity_from_input():
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

        temperature = physical_units.PhysicalQuantity(
            name="Temperature",
            description="Temperature is a physical quantity that quantitatively expresses the attribute of hotness or coldness.",
            SIUnit=str(physical_units.unit_registry.kelvin),
            SIUnitSymbol=f"{physical_units.unit_registry.kelvin:~}",
        )

        class Input(DeriverInputSchema):
            input_signal: float | None = InputField(
                description="Input signal description",
                physical_quantity=temperature,
            )

        class Output(DeriverOutputSchema):
            output_signal: float | None = OutputField(
                description="Output signal description",
                physical_quantity=temperature,
                create_deriver_schema=create_test_schema,
            )

        class Configurations(BaseModel):
            pass

        def transform_stream(
            stream: Stream[Input],
            config: Configurations,
        ) -> Stream[Output]:
            return op.map(
                step_id="map_output",
                up=stream,
                mapper=lambda input_message: Output(
                    timestamp=input_message.timestamp,
                    output_signal=input_message.input_signal,
                ),
            )

        return DeriverSchema(
            name="Test Schema",
            description="Test Schema description",
            inputs=Input,
            outputs=Output,
            configurations=Configurations,
            transform_stream=transform_stream,
        )

    deriver_schema = create_test_schema()

    input_physical_quantity = get_physical_quantity(deriver_io=deriver_schema.inputs.input_signal)

    assert input_physical_quantity == physical_units.PhysicalQuantity(
        name="Temperature",
        description="Temperature is a physical quantity that quantitatively "
        "expresses the attribute of hotness or coldness.",
        SIUnit=str(physical_units.unit_registry.kelvin),
        SIUnitSymbol=f"{physical_units.unit_registry.kelvin:~}",
    )

    output_physical_quantity = get_physical_quantity(deriver_io=deriver_schema.outputs.output_signal)

    assert output_physical_quantity == physical_units.PhysicalQuantity(
        name="Temperature",
        description="Temperature is a physical quantity that quantitatively "
        "expresses the attribute of hotness or coldness.",
        SIUnit=str(physical_units.unit_registry.kelvin),
        SIUnitSymbol=f"{physical_units.unit_registry.kelvin:~}",
    )
