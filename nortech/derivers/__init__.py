from __future__ import annotations

from typing import Callable

from pandas import DataFrame
from urllib3.util import Timeout

from nortech.core.gateways.nortech_api import NortechAPI
from nortech.derivers.handlers.deriver import (
    deploy_deriver,
    run_deriver_locally,
    visualize_deriver,
    visualize_deriver_schema,
)
from nortech.derivers.services.physical_units import get_physical_quantity
from nortech.derivers.values import physical_units
from nortech.derivers.values.instance import (
    Deriver,
    DeriverInput,
    DeriverInputType,
    DeriverOutput,
    DeriverOutputType,
)
from nortech.derivers.values.schema import (
    ConfigurationType,
    DeriverInputSchema,
    DeriverOutputSchema,
    DeriverSchema,
    InputField,
    InputType,
    OutputField,
    OutputType,
)


class Derivers:
    def __init__(self, nortech_api: NortechAPI):
        self.nortech_api = nortech_api

    def deploy_deriver(
        self, deriver: Deriver, workspace: str | None = None, dry_run: bool = True, timeout: Timeout | None = None
    ):
        return deploy_deriver(self.nortech_api, deriver, workspace, dry_run, timeout)

    def visualize_deriver_schema(self, create_deriver_schema: Callable[[], DeriverSchema]):
        return visualize_deriver_schema(create_deriver_schema)

    def visualize_deriver(self, deriver: Deriver):
        return visualize_deriver(deriver)

    def run_deriver_locally(
        self,
        df: DataFrame,
        deriver: Deriver[InputType, OutputType, ConfigurationType, DeriverInputType, DeriverOutputType],
        batch_size: int = 10000,
    ):
        return run_deriver_locally(df, deriver, batch_size)


__all__ = [
    "Deriver",
    "DeriverInput",
    "DeriverOutput",
    "physical_units",
    "DeriverInputSchema",
    "DeriverOutputSchema",
    "DeriverSchema",
    "InputField",
    "OutputField",
    "get_physical_quantity",
]
