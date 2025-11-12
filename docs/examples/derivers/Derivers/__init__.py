# To define a deriver, you need to create a class that inherits from the Deriver class.
# The class must have two inner classes: Inputs and Outputs.
# The Inputs class must inherit from DeriverInputs and the Outputs class must inherit from DeriverOutputs.
# The Inputs class must define the inputs of the deriver.
# The Outputs class must define the outputs of the deriver.
# The run method must be defined and return a bytewax stream.

from __future__ import annotations

import bytewax.operators as op

from nortech.derivers import Deriver, DeriverInput, DeriverInputs, DeriverOutput, DeriverOutputs


class MyDeriver(Deriver):
    class Inputs(DeriverInputs):
        input_1: float | None = DeriverInput(
            workspace="workspace1", asset="asset1", division="division1", unit="unit1", signal="signal1"
        )
        input_2: float | None = DeriverInput(
            workspace="workspace2", asset="asset2", division="division2", unit="unit2", signal="signal2"
        )

    class Outputs(DeriverOutputs):
        output_1: float = DeriverOutput(
            workspace="workspace1",
            asset="asset1",
            division="division1",
            unit="unit1",
            signal="new_signal1",
            description="output_1",
            long_description="output_1_long_description",
            physical_unit="m/s",
        )
        output_2: str = DeriverOutput(
            workspace="workspace2",
            asset="asset2",
            division="division2",
            unit="unit2",
            signal="new_signal2",
            description="output_2",
            long_description="output_2_long_description",
            physical_unit="m/s",
        )

    def run(self, inputs: op.Stream[Inputs]) -> op.Stream[Outputs]:
        return op.map(
            "",
            inputs,
            lambda _input: self.Outputs(
                timestamp=_input.timestamp,
                output_1=_input.input_1 or 0,
                output_2=str(_input.input_2),
            ),
        )
