from datetime import datetime
from typing import Any, Callable, Dict, Generic, TypeVar

from pydantic import BaseModel, Field, model_validator

from nortech.derivers.services.physical_units import get_physical_quantity
from nortech.derivers.services.schema import check_create_deriver_schema_imports
from nortech.derivers.values.physical_units_schema import PhysicalUnit
from nortech.derivers.values.schema import (
    ConfigurationType,
    DeriverSchema,
    InputType,
    OutputType,
)


class CWADUS(BaseModel):
    customer: str = Field()
    workspace: str = Field()
    asset: str = Field()
    division: str = Field()
    unit: str = Field()
    signal: str = Field()


class DeriverInput(CWADUS):
    physicalUnit: PhysicalUnit


class DeriverOutput(CWADUS):
    physicalUnit: PhysicalUnit


DeriverInputType = TypeVar("DeriverInputType", bound=DeriverInput)
DeriverOutputType = TypeVar("DeriverOutputType", bound=DeriverOutput)


class Deriver(
    BaseModel,
    Generic[
        InputType, OutputType, ConfigurationType, DeriverInputType, DeriverOutputType
    ],
):
    name: str = Field()
    description: str = Field()

    inputs: Dict[Any, DeriverInputType] = Field()
    outputs: Dict[Any, DeriverOutputType] = Field()
    configurations: ConfigurationType = Field()

    start_at: datetime = Field()

    create_deriver_schema: Callable[
        [], DeriverSchema[InputType, OutputType, ConfigurationType]
    ] = Field()

    @model_validator(mode="before")
    def parse_inputs_outputs(cls, values):
        # Parse inputs
        inputs = values.get("inputs")

        for deriver_schema_input, deriver_input in inputs.items():
            try:
                deriver_schema_input_physical_quantity = get_physical_quantity(
                    deriver_schema_input
                )
            except ValueError:
                continue

            if (
                deriver_schema_input_physical_quantity
                != deriver_input.physicalUnit.physicalQuantity
            ):
                raise ValueError(
                    f"Physical quantity mismatch for {deriver_schema_input[0]}, physical quantity of the physical unit of the input is {deriver_schema_input_physical_quantity.name}, but the physical quantity of the input is {deriver_input.physicalUnit.physicalQuantity.name}."
                )

        parsed_inputs = {
            str(key[0]): value
            for key, value in inputs.items()
            if isinstance(key, tuple) and len(key) > 0
        }
        values["inputs"] = parsed_inputs

        # Parse outputs
        outputs = values.get("outputs")

        for deriver_schema_ouput, deriver_output in outputs.items():
            try:
                deriver_schema_output_physical_quantity = get_physical_quantity(
                    deriver_schema_ouput
                )
            except ValueError:
                continue

            if (
                deriver_schema_output_physical_quantity
                != deriver_output.physicalUnit.physicalQuantity
            ):
                raise ValueError(
                    f"Physical quantity mismatch for {deriver_schema_ouput[0]}, physical quantity of the physical unit of the output is {deriver_schema_output_physical_quantity.name}, but the physical quantity of the input is {deriver_output.physicalUnit.physicalQuantity.name}."
                )

        parsed_outputs = {
            str(key[0]): value
            for key, value in outputs.items()
            if isinstance(key, tuple) and len(key) > 0
        }
        values["outputs"] = parsed_outputs

        create_deriver_schema = values.get("create_deriver_schema")
        check_create_deriver_schema_imports(create_deriver_schema)

        return values
