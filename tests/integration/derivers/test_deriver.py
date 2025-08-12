from __future__ import annotations

from datetime import timezone

import bytewax.operators as op
import pandas as pd
import pytest

from nortech import Nortech
from nortech.derivers import (
    Deriver,
    DeriverInput,
    DeriverInputs,
    DeriverOutput,
    DeriverOutputs,
    run_deriver_locally_with_df,
)
from nortech.derivers.values.deriver import InvalidDeriverError, validate_deriver


def test_validate_deriver_not_subclass():
    class NotDeriverSubclass:
        pass

    with pytest.raises(InvalidDeriverError) as exc_info:
        validate_deriver(NotDeriverSubclass)
    assert str(exc_info.value) == "Deriver must be a subclass of Deriver."


def test_validate_deriver_no_inputs():
    class NoInputsDeriver(Deriver):
        pass

    with pytest.raises(InvalidDeriverError) as exc_info:
        validate_deriver(NoInputsDeriver)
    assert str(exc_info.value) == "Deriver must have at least one input."


def test_validate_deriver_no_outputs():
    class NoOutputsDeriver(Deriver):
        class Inputs(DeriverInputs):
            input_signal: float | None = DeriverInput(
                workspace="Workspace",
                asset="Asset",
                division="Division",
                unit="Unit",
                signal="Signal",
            )

    with pytest.raises(InvalidDeriverError) as exc_info:
        validate_deriver(NoOutputsDeriver)
    assert str(exc_info.value) == "Deriver must have at least one output."


def test_validate_deriver_invalid_output_type():
    class InvalidOutputTypeDeriver(Deriver):
        class Inputs(DeriverInputs):
            input_signal: float | None = DeriverInput(
                workspace="Workspace",
                asset="Asset",
                division="Division",
                unit="Unit",
                signal="Signal",
            )

        class Outputs(DeriverOutputs):
            output_signal: int | None = DeriverOutput(
                workspace="Workspace",
                asset="Asset",
                division="Division",
                unit="Unit",
                signal="Signal",
            )

    with pytest.raises(InvalidDeriverError) as exc_info:
        validate_deriver(InvalidOutputTypeDeriver)
    assert (
        str(exc_info.value)
        == "Deriver output 'output_signal' has type 'int', which is not allowed. Allowed types: float, str, bool, dict, list."
    )


def test_validate_deriver_no_run_method():
    class NoRunMethodDeriver(Deriver):
        class Inputs(DeriverInputs):
            input_signal: float | None = DeriverInput(
                workspace="Workspace",
                asset="Asset",
                division="Division",
                unit="Unit",
                signal="Signal",
            )

        class Outputs(DeriverOutputs):
            output_signal: float | None = DeriverOutput(
                workspace="Workspace",
                asset="Asset",
                division="Division",
                unit="Unit",
                signal="Signal",
            )

    with pytest.raises(InvalidDeriverError) as exc_info:
        validate_deriver(NoRunMethodDeriver)
    assert str(exc_info.value) == "Deriver must implement the run method."


class TestDeriver(Deriver):
    class Inputs(DeriverInputs):
        input_signal: float | None = DeriverInput(
            workspace="Workspace",
            asset="Asset",
            division="Division",
            unit="Unit",
            signal="Signal",
        )

    class Outputs(DeriverOutputs):
        output_signal: float | None = DeriverOutput(
            workspace="Workspace",
            asset="Asset",
            division="Division",
            unit="Unit",
            signal="Signal",
            description="Output signal",
            long_description="Output signal long description",
            physical_unit="m/s",
        )

    def run(
        self,
        stream: op.Stream[Inputs],
    ) -> op.Stream[Outputs]:
        output_stream = op.map(
            step_id="map_output",
            up=stream,
            mapper=lambda input_message: self.Outputs(
                timestamp=input_message.timestamp,
                output_signal=input_message.input_signal,
            ),
        )

        return output_stream


def test_validate_deriver():
    validate_deriver(TestDeriver)

    with pytest.raises(InvalidDeriverError):
        validate_deriver(int)


def test_deriver_run_locally(nortech: Nortech):
    size = 100
    df = pd.DataFrame(
        {
            "timestamp": pd.date_range(start="2023-01-01", periods=size, freq="s", tz=timezone.utc),
            "input_signal": [float(i) for i in range(size)],
        }
    ).set_index("timestamp")

    output_deriver = run_deriver_locally_with_df(deriver=TestDeriver, df=df)

    renamed_df = df.rename(columns={"input_signal": "output_signal"})
    print(output_deriver)
    print(renamed_df)

    assert output_deriver.equals(renamed_df)
