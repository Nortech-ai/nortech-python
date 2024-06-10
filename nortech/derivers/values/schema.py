import typing
from datetime import datetime
from enum import Enum
from typing import (
    Any,
    Callable,
    Generic,
    List,
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
    float = "float"
    boolean = "boolean"
    string = "string"
    json = "json"


class DeriverSchemaConfiguration(BaseModel):
    name: str = Field()
    description: str = Field()
    dataType: DataTypeEnum = Field()


class DeriverSchemaOutput(BaseModel):
    name: str = Field()
    description: str = Field()
    dataType: DataTypeEnum = Field()
    physicalQuantity: Optional[PhysicalQuantity] = Field()


class SuggestedInput(DeriverSchemaOutput):
    create_deriver_schema: Callable[[], "DeriverSchema"] = Field()


def InputField(
    description: str,
    physicalQuantity: Optional[PhysicalQuantity],
    suggestedInputs: List[Any] = [],
):
    return Field(
        description=description,
        json_schema_extra={
            "physicalQuantity": physicalQuantity.model_dump()
            if physicalQuantity
            else None,
            "suggestedInputsFromOtherDerivers": [
                output.model_dump()
                for output in map(suggested_input_to_output_schema, suggestedInputs)
            ],
        },
    )


def get_actual_type(field_annotation) -> DataTypeEnum:
    # Extract the actual type from Optional or Union hints
    if get_origin(field_annotation) in (Union, typing.Optional):
        # Assuming the first argument is the desired type and not None
        actual_type = next(t for t in get_args(field_annotation) if t is not type(None))
    else:
        actual_type = field_annotation

    # Convert actual_type to DataTypeEnum
    if actual_type in [int, float]:
        return DataTypeEnum.float
    elif actual_type is bool:
        return DataTypeEnum.boolean
    elif actual_type is str:
        return DataTypeEnum.string
    else:
        return DataTypeEnum.json


def suggested_input_to_output_schema(
    suggested_input,
) -> SuggestedInput:
    field_name, field = suggested_input

    json_schema_extra = field.json_schema_extra
    physicalQuantity = (
        PhysicalQuantity(**json_schema_extra["physicalQuantity"])
        if json_schema_extra["physicalQuantity"]
        else None
    )
    create_deriver_schema = json_schema_extra["create_deriver_schema"]  # type: ignore

    assert field.description is not None
    assert field.annotation is not None

    actual_type = get_actual_type(field.annotation)

    return SuggestedInput(
        name=field_name,
        description=field.description,
        dataType=actual_type,
        physicalQuantity=physicalQuantity,
        create_deriver_schema=create_deriver_schema,
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
    timestamp: datetime = Field(description="Timestamp for the input")

    model_config = ConfigDict(
        extra="forbid",
    )


class DeriverOutputSchema(PartialInput, metaclass=ModelMeta):
    timestamp: datetime = Field(description="Timestamp for the output")

    model_config = ConfigDict(
        extra="forbid",
    )


PartialInputType = TypeVar("PartialInputType", bound=PartialInput)


InputType = TypeVar("InputType", bound=DeriverInputSchema)
OutputType = TypeVar("OutputType", bound=DeriverOutputSchema)
ConfigurationType = TypeVar("ConfigurationType", bound=BaseModel)


class DeriverSchema(BaseModel, Generic[InputType, OutputType, ConfigurationType]):
    name: str = Field()
    description: str = Field()

    inputs: Type[InputType] = Field()
    outputs: Type[OutputType] = Field()
    configurations: Type[ConfigurationType] = Field()
    transform_stream: Callable[
        [Stream[InputType], ConfigurationType], Stream[OutputType]
    ] = Field()

    model_config = ConfigDict(arbitrary_types_allowed=True)


def OutputField(
    description: str,
    physicalQuantity: Optional[PhysicalQuantity],
    create_deriver_schema: Callable[[], DeriverSchema],
):
    return Field(
        description=description,
        json_schema_extra={
            "physicalQuantity": physicalQuantity.model_dump()
            if physicalQuantity
            else None,
            "create_deriver_schema": create_deriver_schema,  # type: ignore
        },
    )


class DeriverSchemaOutputWithDAG(DeriverSchemaOutput):
    deriverSchemaDAG: "DeriverSchemaDAG" = Field()


class DeriverSchemaInput(BaseModel, Generic[InputType, OutputType, ConfigurationType]):
    name: str = Field()
    description: str = Field()
    dataType: DataTypeEnum = Field()

    physicalQuantity: Optional[PhysicalQuantity] = Field()

    suggestedInputsFromOtherDerivers: List["DeriverSchemaOutputWithDAG"] = Field(
        default_factory=list
    )


class DeriverSchemaDAG(BaseModel):
    name: str = Field()
    description: str = Field()

    inputs: List[DeriverSchemaInput] = Field()
    outputs: List[DeriverSchemaOutput] = Field()
    configurations: List[DeriverSchemaConfiguration] = Field()

    script: str = Field()
