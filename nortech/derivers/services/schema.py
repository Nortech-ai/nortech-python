from inspect import getsource
from re import DOTALL, sub
from textwrap import dedent
from typing import Callable, List, Type

from pydantic import BaseModel

from nortech.derivers.values.physical_units_schema import PhysicalQuantity
from nortech.derivers.values.schema import (
    ConfigurationType,
    DeriverSchema,
    DeriverSchemaConfiguration,
    DeriverSchemaDAG,
    DeriverSchemaInput,
    DeriverSchemaOutput,
    DeriverSchemaOutputWithDAG,
    InputType,
    OutputType,
    get_actual_type,
)


def input_schema_to_deriver_schema_inputs(
    input_schema: Type[BaseModel],
) -> List[DeriverSchemaInput]:
    input_fields = (
        (field_name, field)
        for field_name, field in input_schema.model_fields.items()
        if field_name != "timestamp"
    )

    return [
        DeriverSchemaInput(
            name=field_name,
            description=field.description,  # type: ignore
            dataType=get_actual_type(field.annotation),
            physicalQuantity=PhysicalQuantity(
                **field.json_schema_extra["physicalQuantity"]  # type: ignore  # noqa: E501
            )
            if field.json_schema_extra["physicalQuantity"]  # type: ignore
            else None,
            suggestedInputsFromOtherDerivers=[
                DeriverSchemaOutputWithDAG(
                    **suggestedInputFromOtherDeriver,
                    deriverSchemaDAG=get_deriver_schema_DAG(
                        suggestedInputFromOtherDeriver["create_deriver_schema"]
                    ),
                )
                for suggestedInputFromOtherDeriver in field.json_schema_extra[  # type: ignore
                    "suggestedInputsFromOtherDerivers"
                ]
            ],
        )
        for field_name, field in input_fields
    ]


def output_schema_to_deriver_schema_outputs(
    output_schema: Type[BaseModel],
) -> List[DeriverSchemaOutput]:
    output_fields = (
        (field_name, field)
        for field_name, field in output_schema.model_fields.items()
        if field_name != "timestamp"
    )

    return [
        DeriverSchemaOutput(
            name=field_name,
            description=field.description,  # type: ignore
            dataType=get_actual_type(field.annotation),
            physicalQuantity=PhysicalQuantity(
                **field.json_schema_extra["physicalQuantity"]  # type: ignore
            )
            if field.json_schema_extra["physicalQuantity"]  # type: ignore
            else None,
        )
        for field_name, field in output_fields
    ]


def config_schema_to_config_dict(
    config_schema: Type[BaseModel],
) -> List[DeriverSchemaConfiguration]:
    return [
        DeriverSchemaConfiguration(
            name=field_name,
            description=field.description,  # type: ignore
            dataType=get_actual_type(field.annotation),
        )
        for field_name, field in config_schema.model_fields.items()
    ]


def get_deriver_schema_DAG(
    create_deriver_schema: Callable[[], DeriverSchema],
) -> DeriverSchemaDAG:
    script = getsource(create_deriver_schema)

    deriver_schema = create_deriver_schema()
    inputs = input_schema_to_deriver_schema_inputs(input_schema=deriver_schema.inputs)
    outputs = output_schema_to_deriver_schema_outputs(
        output_schema=deriver_schema.outputs,
    )
    configurations = config_schema_to_config_dict(
        config_schema=deriver_schema.configurations
    )

    return DeriverSchemaDAG(
        name=deriver_schema.name,
        description=deriver_schema.description,
        inputs=inputs,
        outputs=outputs,
        configurations=configurations,
        script=script,
    )


def check_create_deriver_schema_imports(
    create_deriver_schema: Callable[
        [], DeriverSchema[InputType, OutputType, ConfigurationType]
    ],
):
    # Retrieve the source code of the function
    source_code = dedent(getsource(create_deriver_schema))

    pattern = r"suggestedInputs=\[.*?\],?\s*"
    source_code_without_suggested_inputs = sub(pattern, "", source_code, flags=DOTALL)

    # Define a clean global environment for execution
    clean_env = {}

    # Execute the function within the clean environment
    try:
        exec(source_code_without_suggested_inputs, clean_env)
        # Call the function by its name in the clean environment
        clean_env[create_deriver_schema.__name__]()
    except NameError as e:
        raise NameError(
            "Missing import inside the function. Ensure all imports are defined within the function."
        ) from e
    except Exception as e:
        raise e
