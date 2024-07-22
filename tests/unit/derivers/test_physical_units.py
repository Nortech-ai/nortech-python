from nortech.derivers.services.physical_units import get_physical_quantity
from nortech.derivers.values.physical_units import unit_registry
from nortech.derivers.values.physical_units_schema import PhysicalQuantity


def test_get_quantity_from_input():
    def create_test_schema():
        from typing import Optional

        import bytewax.operators as op
        from bytewax.dataflow import Stream
        from pydantic import BaseModel

        from nortech.derivers.values.physical_units import unit_registry
        from nortech.derivers.values.physical_units_schema import PhysicalQuantity
        from nortech.derivers.values.schema import (
            DeriverInputSchema,
            DeriverOutputSchema,
            DeriverSchema,
            InputField,
            OutputField,
        )

        temperature = PhysicalQuantity(
            name="Temperature",
            description="Temperature is a physical quantity that quantitatively expresses the attribute of hotness or coldness.",
            SIUnit=str(unit_registry.kelvin),
            SIUnitSymbol=f"{unit_registry.kelvin:~}",
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

    input_physical_quantity = get_physical_quantity(deriver_io=deriver_schema.inputs.input_signal)

    assert input_physical_quantity == PhysicalQuantity(
        name="Temperature",
        description="Temperature is a physical quantity that quantitatively expresses the attribute of hotness or coldness.",
        SIUnit=str(unit_registry.kelvin),
        SIUnitSymbol=f"{unit_registry.kelvin:~}",
    )

    output_physical_quantity = get_physical_quantity(deriver_io=deriver_schema.outputs.output_signal)

    assert output_physical_quantity == PhysicalQuantity(
        name="Temperature",
        description="Temperature is a physical quantity that quantitatively expresses the attribute of hotness or coldness.",
        SIUnit=str(unit_registry.kelvin),
        SIUnitSymbol=f"{unit_registry.kelvin:~}",
    )
