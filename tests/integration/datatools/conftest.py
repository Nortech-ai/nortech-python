from datetime import datetime

import pytest

from nortech.metadata import MetadataOutput, SignalInput, SignalInputDict, SignalOutput


@pytest.fixture(scope="session", name="data_signal_input")
def data_signal_input_fixture() -> SignalInput:
    return SignalInput(
        workspace="test_workspace",
        asset="test_asset",
        division="test_division",
        unit="test_unit",
        signal="test_signal_1",
    )


@pytest.fixture(scope="session", name="data_signal_input_dict")
def data_signal_input_dict_fixture() -> SignalInputDict:
    return {
        "workspace": "test_workspace",
        "asset": "test_asset",
        "division": "test_division",
        "unit": "test_unit",
        "signal": "test_signal_2",
    }


@pytest.fixture(scope="session", name="data_signal_output")
def data_signal_output_fixture() -> SignalOutput:
    return SignalOutput(
        id=1,
        name="test_signal_3",
        description="test_description",
        physicalUnit="test_physical_unit",
        dataType="float",
        longDescription="test_long_description",
        workspace=MetadataOutput(id=1, name="test_workspace"),
        asset=MetadataOutput(id=1, name="test_asset"),
        division=MetadataOutput(id=1, name="test_division"),
        unit=MetadataOutput(id=1, name="test_unit"),
        device=MetadataOutput(id=1, name="test_device"),
        createdAt=datetime.now(),
        updatedAt=datetime.now(),
    )


@pytest.fixture(scope="session", name="data_signal_output_id_1")
def data_signal_output_id_1_fixture() -> SignalOutput:
    return SignalOutput(
        id=1,
        name="test_signal_4",
        description="test_description",
        physicalUnit="test_physical_unit",
        dataType="float",
        longDescription="test_long_description",
        workspace=MetadataOutput(id=1, name="test_workspace"),
        asset=MetadataOutput(id=1, name="test_asset"),
        division=MetadataOutput(id=1, name="test_division"),
        unit=MetadataOutput(id=1, name="test_unit"),
        device=MetadataOutput(id=1, name="test_device"),
        createdAt=datetime.now(),
        updatedAt=datetime.now(),
    )


@pytest.fixture(scope="session", name="data_signal_output_id_2")
def data_signal_output_id_2_fixture() -> SignalOutput:
    return SignalOutput(
        id=2,
        name="test_signal_3",
        description="test_description",
        physicalUnit="test_physical_unit",
        dataType="float",
        longDescription="test_long_description",
        workspace=MetadataOutput(id=1, name="test_workspace"),
        asset=MetadataOutput(id=1, name="test_asset"),
        division=MetadataOutput(id=1, name="test_division"),
        unit=MetadataOutput(id=1, name="test_unit"),
        device=MetadataOutput(id=1, name="test_device"),
        createdAt=datetime.now(),
        updatedAt=datetime.now(),
    )


@pytest.fixture(scope="session", name="data_signal_inputs")
def data_signal_inputs_fixture() -> list[SignalInput]:
    return [
        SignalInput(
            workspace="test_workspace",
            asset="test_asset",
            division="test_division",
            unit="test_unit",
            signal="test_signal_4",
        ),
        SignalInput(
            workspace="test_workspace",
            asset="test_asset",
            division="test_division",
            unit="test_unit",
            signal="test_signal_3",
        ),
        SignalInput(
            workspace="test_workspace",
            asset="test_asset",
            division="test_division",
            unit="test_unit",
            signal="test_signal_1",
        ),
        SignalInput(
            workspace="test_workspace",
            asset="test_asset",
            division="test_division",
            unit="test_unit",
            signal="test_signal_2",
        ),
    ]
