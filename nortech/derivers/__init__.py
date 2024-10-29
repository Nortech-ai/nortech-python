from __future__ import annotations

from typing import Callable

from pandas import DataFrame
from urllib3.util import Timeout

import nortech.derivers.handlers.deriver as deriver_handlers
from nortech.core.gateways.nortech_api import NortechAPI
from nortech.derivers.values.instance import (
    Deriver,
    DeriverInputType,
    DeriverOutputType,
)
from nortech.derivers.values.schema import (
    ConfigurationType,
    DeriverSchema,
    InputType,
    OutputType,
)


class Derivers:
    def __init__(self, nortech_api: NortechAPI):
        self.nortech_api = nortech_api

    def deploy_deriver(
        self, deriver: Deriver, workspace: str | None = None, dry_run: bool = True, timeout: Timeout | None = None
    ):
        return deriver_handlers.deploy_deriver(self.nortech_api, deriver, workspace, dry_run, timeout)

    def visualize_deriver_schema(self, create_deriver_schema: Callable[[], DeriverSchema]):
        return deriver_handlers.visualize_deriver_schema(create_deriver_schema)

    def visualize_deriver(self, deriver: Deriver):
        return deriver_handlers.visualize_deriver(deriver)

    def run_deriver_locally(
        self,
        df: DataFrame,
        deriver: Deriver[InputType, OutputType, ConfigurationType, DeriverInputType, DeriverOutputType],
        batch_size: int = 10000,
    ):
        return deriver_handlers.run_deriver_locally(df, deriver, batch_size)
