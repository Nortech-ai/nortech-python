from __future__ import annotations

import ast
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, TypeVar

import bytewax.operators as op
from pydantic import BaseModel, ConfigDict, Field

from nortech.derivers.values.errors import InvalidDeriverError
from nortech.metadata.values.signal import CreateSignalInput, SignalInput


def DeriverInput(workspace: str, asset: str, division: str, unit: str, signal: str):  # noqa: N802
    return Field(
        title="DeriverInput",
        json_schema_extra={
            "workspace": workspace,
            "asset": asset,
            "division": division,
            "unit": unit,
            "signal": signal,
        },
        default=None,
    )


def DeriverOutput(  # noqa: N802
    workspace: str,
    asset: str,
    division: str,
    unit: str,
    signal: str,
    physical_unit: str | None = None,
    description: str | None = None,
    long_description: str | None = None,
):
    return Field(
        title="DeriverOutput",
        json_schema_extra={
            "workspace": workspace,
            "asset": asset,
            "division": division,
            "unit": unit,
            "signal": signal,
            "physical_unit": physical_unit,
            "description": description,
            "long_description": long_description,
        },
    )


class DeriverIO(BaseModel):
    timestamp: datetime = Field(description="Timestamp")

    model_config = ConfigDict(
        extra="allow",
    )


def get_type_from_json_schema(type_str: str | list[str]) -> type:
    type_map = {
        "string": str,
        "number": float,
        "integer": int,
        "boolean": bool,
        "null": type(None),
        "object": dict,
        "array": list,
    }
    if isinstance(type_str, list):
        types = [get_type_from_json_schema(item) for item in type_str]
        if len(types) == 0 or len(types) > 2:
            raise InvalidDeriverError(f"Unsupported type: {type_str}")
        elif len(types) == 2:
            if types[0] == type(None):  # noqa: E721
                return types[1]
            else:
                return types[0]
        else:
            return types[0]
    else:
        normalized = type_str.strip().lower()
        if normalized not in type_map:
            raise InvalidDeriverError(f"Unsupported JSON Schema type: {type_str}")
        return type_map[normalized]


class DeriverInputs(DeriverIO):
    @classmethod
    def list_types(cls) -> list[tuple[str, type]]:
        return [
            (
                field,
                get_type_from_json_schema(
                    value.get(
                        "type",
                        list(map(lambda x: x.get("type"), value.get("anyOf", []))),
                    )
                ),
            )
            for field, value in cls.model_json_schema()["properties"].items()
            if value.get("title") == "DeriverInput"
        ]

    @classmethod
    def list(cls) -> list[tuple[str, SignalInput]]:
        return [
            (field, SignalInput.model_validate(value))
            for field, value in cls.model_json_schema()["properties"].items()
            if value.get("title") == "DeriverInput"
        ]


InputType = TypeVar("InputType", bound=DeriverInputs)


class DeriverOutputs(DeriverIO):
    @classmethod
    def list_types(cls) -> list[tuple[str, type]]:
        return [
            (
                field,
                get_type_from_json_schema(
                    value.get(
                        "type",
                        list(map(lambda x: x.get("type"), value.get("anyOf", []))),
                    )
                ),
            )
            for field, value in cls.model_json_schema()["properties"].items()
            if value.get("title") == "DeriverOutput"
        ]

    @classmethod
    def list(cls) -> list[tuple[str, CreateSignalInput]]:
        return [
            (field, CreateSignalInput.model_validate(value))
            for field, value in cls.model_json_schema()["properties"].items()
            if value.get("title") == "DeriverOutput"
        ]


OutputType = TypeVar("OutputType", bound=DeriverOutputs)


class Deriver(ABC):
    class Inputs(DeriverInputs):
        pass

    class Outputs(DeriverOutputs):
        pass

    @abstractmethod
    def run(self, stream: op.Stream[Inputs]) -> op.Stream[Outputs]:
        raise NotImplementedError


def validate_deriver(deriver: type) -> type[Deriver]:
    if not issubclass(deriver, Deriver):
        raise InvalidDeriverError("Deriver must be a subclass of Deriver.")

    deriver_inputs = deriver.Inputs.list_types()
    if len(deriver_inputs) == 0:
        raise InvalidDeriverError("Deriver must have at least one input.")

    deriver_outputs = deriver.Outputs.list_types()
    if len(deriver_outputs) == 0:
        raise InvalidDeriverError("Deriver must have at least one output.")
    for name, typ in deriver_outputs:
        if typ not in [float, str, bool, dict, list]:
            raise InvalidDeriverError(
                f"Deriver output '{name}' has type '{typ.__name__}', which is not allowed. Allowed types: float, str, bool, dict, list."
            )

    try:
        deriver().run(None)  # type: ignore
    except Exception as e:
        if isinstance(e, NotImplementedError) or (
            isinstance(e, TypeError)
            and f"Can't instantiate abstract class {deriver.__name__} with abstract method run" in str(e)
        ):
            raise InvalidDeriverError("Deriver must implement the run method.")  # noqa: B904
        return deriver
    return deriver


def get_deriver_from_script(script: str) -> type[Deriver]:
    tree = ast.parse(script)
    if len(tree.body) != 1:
        raise InvalidDeriverError("Script must define exactly one class.")

    class_def = tree.body[0]
    if not isinstance(class_def, ast.ClassDef):
        raise InvalidDeriverError("Script must define a class.")

    namespace: dict[str, Any] = {}
    exec(script, globals(), namespace)  # noqa: S102

    cls = namespace.get(class_def.name)
    if isinstance(cls, type):
        return validate_deriver(cls)
    raise InvalidDeriverError("No valid Deriver subclass found in script.")
