from nortech import Nortech
from nortech.metadata.values.signal import SignalInput

nortech = Nortech()

# Get by ID
signal = nortech.metadata.signal.get(123)

# Get unit signal by input dict
signal = nortech.metadata.signal.get(
    {
        "workspace": "my-workspace",
        "asset": "my-asset",
        "division": "my-division",
        "unit": "my-unit",
        "signal": "my-signal",
    }
)


# Get by SignalInput pydantic object
signal = nortech.metadata.signal.get(
    SignalInput(workspace="my-workspace", asset="my-asset", division="my-division", unit="my-unit", signal="my-signal")
)

print(signal)
# SignalOutput(
#     id=123,
#     name="my-signal",
#     physical_unit="°C",
#     data_type="float64",
#     description="Temperature sensor",
#     long_description="Main temperature sensor for the unit",
#     created_at=datetime.datetime(2024, 1, 1, 0, 0, 0, 0),
#     updated_at=datetime.datetime(2024, 1, 1, 0, 0, 0, 0),
#     workspace=MetadataOutput(
#         id=123,
#         name="my-workspace"
#     ),
#     asset=MetadataOutput(
#         id=456,
#         name="my-asset"
#     ),
#     division=MetadataOutput(
#         id=789,
#         name="my-division"
#     ),
#     unit=MetadataOutput(
#         id=101,
#         name="my-unit"
#     )
# )
