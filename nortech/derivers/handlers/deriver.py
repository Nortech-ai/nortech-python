from dataclasses import dataclass
from datetime import datetime
from typing import Callable

import bytewax.operators as op
from bytewax.dataflow import Dataflow
from bytewax.testing import TestingSink, TestingSource, run_main
from IPython.display import Markdown, display
from pandas import DataFrame, DatetimeIndex, isna
from pint import Quantity

from nortech.derivers.gateways.customer_api import (
    CustomerAPI,
    CustomerWorkspace,
    create_deriver,
)
from nortech.derivers.services.schema import (
    get_deriver_schema_DAG,
)
from nortech.derivers.services.visualize import (
    create_deriver_schema_DAG_mermaid,
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


@dataclass
class TimeWindow:
    start: datetime
    end: datetime

    def __post_init__(self):
        assert self.start <= self.end


def deploy_deriver(
    customer_API: CustomerAPI,
    customer_workspace: CustomerWorkspace,
    deriver: Deriver,
    dry_run: bool,
):
    deriver_schema_DAG = get_deriver_schema_DAG(deriver.create_deriver_schema)

    deriver_diffs = create_deriver(
        customer_API=customer_API,
        customer_workspace=customer_workspace,
        deriver=deriver,
        deriver_schema_DAG=deriver_schema_DAG,
        dry_run=dry_run,
    )

    return deriver_diffs


def visualize_deriver_schema(create_deriver_schema: Callable[[], DeriverSchema]):
    deriver_schema_DAG = get_deriver_schema_DAG(create_deriver_schema)

    mermaid = """
```mermaid
flowchart LR
"""

    mermaid = create_deriver_schema_DAG_mermaid(
        mermaid=mermaid, deriver_schema_DAG=deriver_schema_DAG
    )

    mermaid += """
```
"""

    display(Markdown(mermaid))


def visualize_deriver(deriver: Deriver):
    deriver_schema_DAG = get_deriver_schema_DAG(deriver.create_deriver_schema)

    mermaid = f"""
```mermaid
flowchart LR
    subgraph "Deriver ({deriver.name})"
"""

    mermaid += create_deriver_schema_subgraph(deriver_schema_DAG=deriver_schema_DAG)

    for input_name, input in deriver.inputs.items():
        mermaid += f"""
            {deriver.name.__hash__()}_{input.signal}["{input.signal}<br/>[{input.physicalUnit.symbol.replace(' ', '')}]"] --> {deriver_schema_DAG.name.__hash__()}_{input_name}
        """

    for output_name, output in deriver.outputs.items():
        mermaid += f"""
            {deriver_schema_DAG.name.__hash__()}_{output_name} --> {deriver.name.__hash__()}_{output_name}["{output_name}<br/>[{output.physicalUnit.symbol.replace(' ', '')}]"]
        """

    mermaid += """
end
```
"""

    display(Markdown(mermaid))


def run_deriver_locally(
    df: DataFrame,
    deriver: Deriver[
        InputType, OutputType, ConfigurationType, DeriverInputType, DeriverOutputType
    ],
    batch_size: int = 10000,
):
    deriver_schema = deriver.create_deriver_schema()

    if not isinstance(df.index, DatetimeIndex):
        raise ValueError("df must have a datetime index")

    df_timezone = df.index.tz
    df.index = df.index.tz_convert("UTC")

    def df_to_inputs(df: DataFrame):
        for input in df.reset_index().to_dict("records"):
            input_with_None = {k: (None if isna(v) else v) for k, v in input.items()}

            yield deriver_schema.inputs(**input_with_None)  # type: ignore

    source = TestingSource(ib=df_to_inputs(df), batch_size=batch_size)

    flow = Dataflow(deriver.name)

    stream = op.input("input", flow, source)

    input_model_fields = dict(deriver_schema.inputs.model_fields.items())

    def convert_input(inp):
        for input_name, input in deriver.inputs.items():
            if (
                input_name != "timestamp"
                and input_model_fields[input_name].json_schema_extra["physicalQuantity"]  # type: ignore
                is not None
            ):
                SIUnit: str = input_model_fields[input_name].json_schema_extra[  # type: ignore
                    "physicalQuantity"
                ]["SIUnitSymbol"]

                value = inp.__getattr__(input_name)
                if value is not None:
                    inp.__setattr__(
                        input_name,
                        Quantity(value, input.physicalUnit.symbol).to(SIUnit).magnitude,
                    )

        return inp

    converted_input_stream = op.map("convert_input", stream, convert_input)

    transformed_stream = deriver_schema.transform_stream(
        converted_input_stream, deriver.configurations
    )

    output_model_fields = dict(deriver_schema.outputs.model_fields.items())

    def convert_output(out):
        for output_name, output in deriver.outputs.items():
            if (
                output_name != "timestamp"
                and output_model_fields[output_name].json_schema_extra[  # type: ignore
                    "physicalQuantity"
                ]
                is not None
            ):
                SIUnit: str = output_model_fields[output_name].json_schema_extra[  # type: ignore
                    "physicalQuantity"
                ]["SIUnitSymbol"]

                value = out.__getattr__(output_name)
                if value is not None:
                    out.__setattr__(
                        output_name,
                        Quantity(value, SIUnit)
                        .to(output.physicalUnit.symbol)
                        .magnitude,
                    )

        return out

    converted_output_stream = op.map(
        "convert_output", transformed_stream, convert_output
    )

    output_list = []
    output_sink = TestingSink(output_list)

    op.output("out", converted_output_stream, output_sink)

    run_main(flow)

    return (
        DataFrame([output.model_dump() for output in output_list])
        .set_index("timestamp")
        .tz_convert(df_timezone)
    )
