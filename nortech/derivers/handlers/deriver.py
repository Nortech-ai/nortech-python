from __future__ import annotations

from hashlib import sha256
from typing import Callable

import bytewax.operators as op
from bytewax.dataflow import Dataflow
from bytewax.testing import TestingSink, TestingSource, run_main
from IPython.display import Markdown, display
from pandas import DataFrame, DatetimeIndex, isna
from pint import Quantity

from nortech.derivers.services.nortech_api import create_deriver
from nortech.derivers.services.schema import (
    get_deriver_schema_dag,
)
from nortech.derivers.services.visualize import (
    create_deriver_schema_dag_mermaid,
    create_deriver_schema_subgraph,
)
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
from nortech.gateways.nortech_api import NortechAPI


def deploy_deriver(
    nortech_api: NortechAPI,
    deriver: Deriver,
    workspace: str | None = None,
    dry_run: bool = True,
):
    deriver_schema_dag = get_deriver_schema_dag(deriver.create_deriver_schema)

    deriver_diffs = create_deriver(
        nortech_api=nortech_api,
        workspace=workspace,
        deriver=deriver,
        deriver_schema_dag=deriver_schema_dag,
        dry_run=dry_run,
    )

    return deriver_diffs


def visualize_deriver_schema(create_deriver_schema: Callable[[], DeriverSchema]):
    deriver_schema_dag = get_deriver_schema_dag(create_deriver_schema)

    mermaid = """
```mermaid
flowchart LR
"""

    mermaid = create_deriver_schema_dag_mermaid(mermaid=mermaid, deriver_schema_dag=deriver_schema_dag)

    mermaid += """
```
"""

    display(Markdown(mermaid))


def visualize_deriver(deriver: Deriver):
    deriver_schema_dag = get_deriver_schema_dag(deriver.create_deriver_schema)

    mermaid = f"""
```mermaid
flowchart LR
    subgraph "Deriver ({deriver.name})"
"""

    mermaid += create_deriver_schema_subgraph(deriver_schema_dag=deriver_schema_dag)

    for input_name, deriver_input in deriver.inputs.items():
        mermaid += f"""
            {sha256(deriver.name.encode()).hexdigest()[:8]}_{deriver_input.signal}["{deriver_input.signal}<br/>[{deriver_input.physical_unit.symbol.replace(' ', '')}]"] --> {sha256(deriver_schema_dag.name.encode()).hexdigest()[:8]}_{input_name}
        """

    for output_name, deriver_output in deriver.outputs.items():
        mermaid += f"""
            {sha256(deriver_schema_dag.name.encode()).hexdigest()[:8]}_{output_name} --> {sha256(deriver.name.encode()).hexdigest()[:8]}_{output_name}["{output_name}<br/>[{deriver_output.physical_unit.symbol.replace(' ', '')}]"]
        """

    mermaid += """
end
```
"""

    display(Markdown(mermaid))


def run_deriver_locally(
    df: DataFrame,
    deriver: Deriver[InputType, OutputType, ConfigurationType, DeriverInputType, DeriverOutputType],
    batch_size: int = 10000,
):
    deriver_schema = deriver.create_deriver_schema()

    if not isinstance(df.index, DatetimeIndex):
        raise ValueError("df must have a datetime index")

    df_timezone = df.index.tz
    df.index = df.index.tz_convert("UTC")

    def df_to_inputs(df: DataFrame):
        for deriver_input in df.reset_index().to_dict("records"):
            input_with_none = {k: (None if isna(v) else v) for k, v in deriver_input.items()}

            yield deriver_schema.inputs(**input_with_none)  # type: ignore

    source = TestingSource(ib=df_to_inputs(df), batch_size=batch_size)  # type: ignore

    flow = Dataflow(deriver.name)

    stream = op.input("input", flow, source)

    input_model_fields = dict(deriver_schema.inputs.model_fields.items())

    def convert_input(inp):
        for input_name, deriver_input in deriver.inputs.items():
            if (
                input_name != "timestamp"
                and input_model_fields[input_name].json_schema_extra["physical_quantity"]  # type: ignore
                is not None
            ):
                si_unit: str = input_model_fields[input_name].json_schema_extra[  # type: ignore
                    "physical_quantity"
                ]["si_unit_symbol"]

                value = inp.__getattr__(input_name)
                if value is not None:
                    inp.__setattr__(
                        input_name,
                        Quantity(value, deriver_input.physical_unit.symbol).to(si_unit).magnitude,
                    )

        return inp

    converted_input_stream = op.map("convert_input", stream, convert_input)

    transformed_stream = deriver_schema.transform_stream(converted_input_stream, deriver.configurations)

    output_model_fields = dict(deriver_schema.outputs.model_fields.items())

    def convert_output(out):
        for output_name, output in deriver.outputs.items():
            if (
                output_name != "timestamp"
                and output_model_fields[output_name].json_schema_extra["physical_quantity"]  # type: ignore
                is not None
            ):
                si_unit: str = output_model_fields[output_name].json_schema_extra[  # type: ignore
                    "physical_quantity"
                ]["si_unit_symbol"]

                value = out.__getattr__(output_name)
                if value is not None:
                    out.__setattr__(
                        output_name,
                        Quantity(value, si_unit).to(output.physical_unit.symbol).magnitude,
                    )

        return out

    converted_output_stream = op.map("convert_output", transformed_stream, convert_output)

    output_list: list[OutputType] = []
    output_sink = TestingSink(output_list)

    op.output("out", converted_output_stream, output_sink)

    run_main(flow)

    return (
        DataFrame([output.model_dump(by_alias=True) for output in output_list])
        .set_index("timestamp")
        .tz_convert(df_timezone)
    )
