from datetime import datetime
from typing import Any, Callable, Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field, model_validator

from nortech.core.values.signal import SignalInput
from nortech.derivers.services.physical_units import get_physical_quantity
from nortech.derivers.services.schema import check_create_deriver_schema_imports
from nortech.derivers.values.physical_units_schema import PhysicalUnit
from nortech.derivers.values.schema import (
    ConfigurationType,
    DeriverSchema,
    InputType,
    OutputType,
)


class DeriverInput(SignalInput):
    model_config = ConfigDict(populate_by_name=True)

    physical_unit: PhysicalUnit = Field(alias="physicalUnit")


class DeriverOutput(SignalInput):
    model_config = ConfigDict(populate_by_name=True)

    physical_unit: PhysicalUnit = Field(alias="physicalUnit")


DeriverInputType = TypeVar("DeriverInputType", bound=DeriverInput)
DeriverOutputType = TypeVar("DeriverOutputType", bound=DeriverOutput)


class Deriver(
    BaseModel,
    Generic[InputType, OutputType, ConfigurationType, DeriverInputType, DeriverOutputType],
):
    name: str
    description: str

    inputs: dict[Any, DeriverInputType]
    outputs: dict[Any, DeriverOutputType]
    configurations: ConfigurationType

    start_at: datetime

    create_deriver_schema: Callable[[], DeriverSchema[InputType, OutputType, ConfigurationType]]

    @model_validator(mode="before")
    @classmethod
    def parse_inputs_outputs(cls, values):
        # Parse inputs
        inputs = values.get("inputs")

        for deriver_schema_input, deriver_input in inputs.items():
            try:
                deriver_schema_input_physical_quantity = get_physical_quantity(deriver_schema_input)
            except ValueError:
                continue

            if deriver_schema_input_physical_quantity != deriver_input.physical_unit.physical_quantity:
                raise ValueError(
                    f"Physical quantity mismatch for {deriver_schema_input[0]}, "
                    "physical quantity of the physical unit of the input is "
                    f"{deriver_schema_input_physical_quantity.name}, but the "
                    f"physical quantity of the input is {deriver_input.physical_unit.physical_quantity.name}."
                )

        parsed_inputs = {str(key[0]): value for key, value in inputs.items() if isinstance(key, tuple) and len(key) > 0}
        values["inputs"] = parsed_inputs

        # Parse outputs
        outputs = values.get("outputs")

        for deriver_schema_ouput, deriver_output in outputs.items():
            try:
                deriver_schema_output_physical_quantity = get_physical_quantity(deriver_schema_ouput)
            except ValueError:
                continue

            if deriver_schema_output_physical_quantity != deriver_output.physical_unit.physical_quantity:
                raise ValueError(
                    f"Physical quantity mismatch for {deriver_schema_ouput[0]}, "
                    "physical quantity of the physical unit of "
                    f"the output is {deriver_schema_output_physical_quantity.name}, "
                    f"but the physical quantity of the input is {deriver_output.physical_unit.physical_quantity.name}."
                )

        parsed_outputs = {
            str(key[0]): value for key, value in outputs.items() if isinstance(key, tuple) and len(key) > 0
        }
        values["outputs"] = parsed_outputs

        create_deriver_schema = values.get("create_deriver_schema")
        check_create_deriver_schema_imports(create_deriver_schema)

        return values
