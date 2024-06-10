from nortech.derivers.values.schema import DeriverSchemaDAG


def create_deriver_schema_subgraph(deriver_schema_DAG: DeriverSchemaDAG):
    mermaid = f"""
        subgraph "DeriverSchema ({deriver_schema_DAG.name})"
    """

    for input in deriver_schema_DAG.inputs:
        if input.name != "timestamp":
            if input.physicalQuantity:
                mermaid += f"""
                    {deriver_schema_DAG.name.__hash__()}_{input.name}["{input.name}<br/>[{input.physicalQuantity.SIUnitSymbol.replace(" ", "")}]"] --> transform_stream_{deriver_schema_DAG.name.__hash__()}["transform_stream"]
                """
            else:
                mermaid += f"""
                    {deriver_schema_DAG.name.__hash__()}_{input.name}["{input.name}"] --> transform_stream_{deriver_schema_DAG.name.__hash__()}["transform_stream"]
                """

    for output in deriver_schema_DAG.outputs:
        if output.name != "timestamp":
            if output.physicalQuantity:
                mermaid += f"""
                    transform_stream_{deriver_schema_DAG.name.__hash__()} --> {deriver_schema_DAG.name.__hash__()}_{output.name}["{output.name}<br/>[{output.physicalQuantity.SIUnitSymbol.replace(" ", "")}]"]
                """
            else:
                mermaid += f"""
                    transform_stream_{deriver_schema_DAG.name.__hash__()} --> {deriver_schema_DAG.name.__hash__()}_{output.name}["{output.name}"]
                """

    mermaid += """
        end
    """

    return mermaid


def create_deriver_schema_DAG_mermaid(
    mermaid: str, deriver_schema_DAG: DeriverSchemaDAG
):
    for input in deriver_schema_DAG.inputs:
        if input.name != "timestamp":
            for suggestedInput in input.suggestedInputsFromOtherDerivers:
                mermaid = create_deriver_schema_DAG_mermaid(
                    mermaid=mermaid,
                    deriver_schema_DAG=suggestedInput.deriverSchemaDAG,
                )

                mermaid += f"""
                    {suggestedInput.deriverSchemaDAG.name.__hash__()}_{suggestedInput.name} -.->|suggestedInput| {deriver_schema_DAG.name.__hash__()}_{input.name}
                """

    mermaid += create_deriver_schema_subgraph(deriver_schema_DAG=deriver_schema_DAG)

    return mermaid
