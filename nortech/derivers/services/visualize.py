from hashlib import sha256

from nortech.derivers.values.schema import DeriverSchemaDAG


def create_deriver_schema_subgraph(deriver_schema_dag: DeriverSchemaDAG):
    mermaid = f"""
        subgraph "DeriverSchema ({deriver_schema_dag.name})"
    """

    for deriver_input in deriver_schema_dag.inputs:
        if deriver_input.name != "timestamp":
            node_id = sha256(deriver_schema_dag.name.encode()).hexdigest()[:8]

            if deriver_input.physical_quantity:
                mermaid += f"""
                    {node_id}_{deriver_input.name}["{deriver_input.name}<br/>[{deriver_input.physical_quantity.si_unit_symbol.replace(" ", "")}]"] --> transform_stream_{node_id}["transform_stream"]
                """
            else:
                mermaid += f"""
                    {node_id}_{deriver_input.name}["{deriver_input.name}"] --> transform_stream_{node_id}["transform_stream"]
                """

    for deriver_output in deriver_schema_dag.outputs:
        if deriver_output.name != "timestamp":
            node_id = sha256(deriver_schema_dag.name.encode()).hexdigest()[:8]

            if deriver_output.physical_quantity:
                mermaid += f"""
                    transform_stream_{node_id} --> {node_id}_{deriver_output.name}["{deriver_output.name}<br/>[{deriver_output.physical_quantity.si_unit_symbol.replace(" ", "")}]"]
                """
            else:
                mermaid += f"""
                    transform_stream_{node_id} --> {node_id}_{deriver_output.name}["{deriver_output.name}"]
                """

    mermaid += """
        end
    """

    return mermaid


def create_deriver_schema_dag_mermaid(mermaid: str, deriver_schema_dag: DeriverSchemaDAG):
    for deriver_input in deriver_schema_dag.inputs:
        if deriver_input.name != "timestamp":
            for suggested_input in deriver_input.suggested_inputs_from_other_derivers:
                mermaid = create_deriver_schema_dag_mermaid(
                    mermaid=mermaid,
                    deriver_schema_dag=suggested_input.deriver_schema_dag,
                )

                source_id = sha256(suggested_input.deriver_schema_dag.name.encode()).hexdigest()[:8]
                target_id = sha256(deriver_schema_dag.name.encode()).hexdigest()[:8]

                mermaid += f"""
                    {source_id}_{suggested_input.name} -.->|suggestedInput| {target_id}_{deriver_input.name}
                """

    mermaid += create_deriver_schema_subgraph(deriver_schema_dag=deriver_schema_dag)

    return mermaid
