from __future__ import annotations

import typing
from datetime import datetime
from enum import Enum
from typing import (
    Any,
    Callable,
    Generic,
    Optional,
    Type,
    TypeVar,
    Union,
    get_args,
    get_origin,
)

from bytewax.dataflow import Stream
from pydantic import BaseModel, ConfigDict, Field
from pydantic._internal._model_construction import ModelMetaclass
from typing_extensions import dataclass_transform

from nortech.derivers.values.physical_units_schema import PhysicalQuantity


class DataTypeEnum(str, Enum):
    """Enumeration of supported data types.

    Attributes:
        float: Floating point number type
        boolean: Boolean type
        string: String type
        json: JSON type

    """

    float = "float"
    boolean = "boolean"
    string = "string"
    json = "json"


class DeriverSchemaConfiguration(BaseModel):
    """Pydantic model for deriver schema configuration data.

    Attributes:
        name (str): The name of the configuration parameter.
        description (str): A description of the configuration parameter.
        data_type (DataTypeEnum): The data type of the configuration parameter.

    """

    model_config = ConfigDict(populate_by_name=True)

    name: str
    description: str
    data_type: DataTypeEnum = Field(alias="dataType")


class DeriverSchemaOutput(BaseModel):
    """Pydantic model for deriver schema output data.

    Attributes:
        name (str): The name of the output.
        description (str): A description of the output.
        data_type (DataTypeEnum): The data type of the output.
        physical_quantity (PhysicalQuantity | None): The physical quantity of the output, if applicable.

    """

    model_config = ConfigDict(populate_by_name=True)

    name: str
    description: str
    data_type: DataTypeEnum = Field(alias="dataType")
    physical_quantity: PhysicalQuantity | None = Field(alias="physicalQuantity")


class SuggestedInput(DeriverSchemaOutput):
    """Pydantic model for suggested input data.

    Attributes:
        name (str): The name of the suggested input.
        description (str): A description of the suggested input.
        data_type (DataTypeEnum): The data type of the suggested input.
        physical_quantity (PhysicalQuantity | None): The physical quantity of the suggested input, if applicable.
        create_deriver_schema (Callable[[], DeriverSchema]): Function that creates the deriver schema for this input.

    """

    create_deriver_schema: Callable[[], "DeriverSchema"] = Field(alias="createDeriverSchema")


def InputField(  # noqa: N802
    description: str,
    physical_quantity: PhysicalQuantity | None,
    suggested_inputs: list[Any] | None = None,
):
    """Create an input field with metadata.

    Args:
        description (str): Description of the input field.
        physical_quantity (PhysicalQuantity | None): Physical quantity of the input field.
        suggested_inputs (list[Any] | None, optional): List of suggested inputs. Defaults to None.

    Returns:
        Field: A pydantic Field with the specified metadata.

    """
    return Field(
        description=description,
        json_schema_extra={
            "physical_quantity": physical_quantity.model_dump() if physical_quantity else None,
            "suggested_inputs_from_other_derivers": [
                output.model_dump() for output in map(suggested_input_to_output_schema, suggested_inputs or [])
            ],
        },
    )


def get_actual_type(field_annotation) -> DataTypeEnum:
    # Extract the actual type from Optional or Union hints
    if get_origin(field_annotation) in (Union, Optional):
        # Assuming the first argument is the desired type and not None
        actual_type = next(t for t in get_args(field_annotation) if t is not None)
    else:
        actual_type = field_annotation

    # Convert actual_type to DataTypeEnum
    if actual_type in [int, float]:
        return DataTypeEnum.float
    if actual_type is bool:
        return DataTypeEnum.boolean
    if actual_type is str:
        return DataTypeEnum.string
    return DataTypeEnum.json


def suggested_input_to_output_schema(
    suggested_input,
) -> SuggestedInput:
    field_name, field = suggested_input

    json_schema_extra = field.json_schema_extra
    physical_quantity = (
        PhysicalQuantity(**json_schema_extra["physical_quantity"]) if json_schema_extra["physical_quantity"] else None
    )
    create_deriver_schema = json_schema_extra["create_deriver_schema"]  # type: ignore

    assert field.description is not None
    assert field.annotation is not None

    actual_type = get_actual_type(field.annotation)

    return SuggestedInput(
        name=field_name,
        description=field.description,
        dataType=actual_type,
        physicalQuantity=physical_quantity,
        createDeriverSchema=create_deriver_schema,
    )


# Define a custom metaclass that overrides __getattr__
@dataclass_transform(kw_only_default=True, field_specifiers=(Field, InputField))
class ModelMeta(ModelMetaclass):
    if not typing.TYPE_CHECKING:  # pragma: no branch

        def __getattr__(self, name: str) -> Any:
            if name == "timestamp":
                raise AttributeError("Timestamp should not be referenced")

            if name in self.model_fields:
                return (name, self.model_fields[name])

            return super().__getattr__(name)


class PartialInput(BaseModel):
    timestamp: datetime = Field(description="Timestamp")

    model_config = ConfigDict(
        extra="allow",
    )


class DeriverInputSchema(PartialInput, metaclass=ModelMeta):
    """Pydantic model for deriver schema input data.

    Attributes:
        timestamp (datetime): The timestamp for the input.

    """

    timestamp: datetime = Field(description="Timestamp for the input")

    model_config = ConfigDict(
        extra="forbid",
    )


class DeriverOutputSchema(PartialInput, metaclass=ModelMeta):
    """Pydantic model for deriver schema output data.

    Attributes:
        timestamp (datetime): The timestamp for the output.

    """

    timestamp: datetime = Field(description="Timestamp for the output")

    model_config = ConfigDict(
        extra="forbid",
    )


PartialInputType = TypeVar("PartialInputType", bound=PartialInput)


InputType = TypeVar("InputType", bound=DeriverInputSchema)
OutputType = TypeVar("OutputType", bound=DeriverOutputSchema)
ConfigurationType = TypeVar("ConfigurationType", bound=BaseModel)


class DeriverSchema(BaseModel, Generic[InputType, OutputType, ConfigurationType]):
    """Pydantic model for a deriver schema.

    Attributes:
        name (str): The name of the deriver.
        description (str): A description of the deriver.
        inputs (Type[InputType]): The input schema type.
        outputs (Type[OutputType]): The output schema type.
        configurations (Type[ConfigurationType]): The configuration schema type.
        transform_stream (Callable): Function that transforms input stream to output stream given a configuration.

    """

    name: str
    description: str

    inputs: Type[InputType]
    outputs: Type[OutputType]
    configurations: Type[ConfigurationType]
    transform_stream: Callable[[Stream[InputType], ConfigurationType], Stream[OutputType]]

    model_config = ConfigDict(arbitrary_types_allowed=True)


def OutputField(  # noqa: N802
    description: str,
    physical_quantity: PhysicalQuantity | None,
    create_deriver_schema: Callable[[], DeriverSchema],
):
    """Create an output field with metadata.

    Args:
        description (str): Description of the output field.
        physical_quantity (PhysicalQuantity | None): Physical quantity of the output field.
        create_deriver_schema (Callable[[], DeriverSchema]): Function that creates the deriver schema.

    Returns:
        Field: A pydantic Field with the specified metadata.

    """
    return Field(
        description=description,
        json_schema_extra={
            "physical_quantity": physical_quantity.model_dump() if physical_quantity else None,
            "create_deriver_schema": create_deriver_schema,  # type: ignore
        },
    )


class DeriverSchemaOutputWithDAG(DeriverSchemaOutput):
    """Pydantic model for deriver schema output with DAG information.

    Attributes:
        name (str): The name of the output.
        description (str): A description of the output.
        data_type (DataTypeEnum): The data type of the output.
        physical_quantity (PhysicalQuantity | None): The physical quantity of the output, if applicable.
        deriver_schema_dag (DeriverSchemaDAG): The DAG associated with this output.

    """

    deriver_schema_dag: "DeriverSchemaDAG"


class DeriverSchemaInput(BaseModel, Generic[InputType, OutputType, ConfigurationType]):
    """Pydantic model for deriver schema input with suggested inputs.

    Attributes:
        name (str): The name of the input.
        description (str): A description of the input.
        data_type (DataTypeEnum): The data type of the input.
        physical_quantity (PhysicalQuantity | None): The physical quantity of the input.
        suggested_inputs_from_other_derivers (list[DeriverSchemaOutputWithDAG]): List of suggested inputs.

    """

    model_config = ConfigDict(populate_by_name=True)

    name: str
    description: str
    data_type: DataTypeEnum = Field(alias="dataType")

    physical_quantity: PhysicalQuantity | None = Field(alias="physicalQuantity")

    suggested_inputs_from_other_derivers: list["DeriverSchemaOutputWithDAG"] = Field(
        default_factory=list, alias="suggestedInputsFromOtherDerivers"
    )


class DeriverSchemaDAG(BaseModel):
    """Pydantic model for a deriver schema DAG.

    Attributes:
        name (str): The name of the deriver schema.
        description (str): A description of the deriver schema.
        inputs (list[DeriverSchemaInput]): List of inputs in the deriver schema.
        outputs (list[DeriverSchemaOutput]): List of outputs in the deriver schema.
        configurations (list[DeriverSchemaConfiguration]): List of configurations in the deriver schema.
        script (str): The script associated with this deriver schema.

    """

    name: str
    description: str

    inputs: list[DeriverSchemaInput]
    outputs: list[DeriverSchemaOutput]
    configurations: list[DeriverSchemaConfiguration]

    script: str
