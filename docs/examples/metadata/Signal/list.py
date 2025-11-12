from nortech import Nortech
from nortech.metadata.values.pagination import PaginationOptions
from nortech.metadata.values.unit import UnitInput

nortech = Nortech()

# List all signals in a unit
signals = nortech.metadata.signal.list(123)  # using unit ID

# List unit signals with pagination
signals = nortech.metadata.signal.list(
    {"workspace": "my-workspace", "asset": "my-asset", "division": "my-division", "unit": "my-unit"},
    PaginationOptions(size=10, sortBy="name"),
)

# Using UnitInput pydantic object
signals = nortech.metadata.signal.list(
    UnitInput(workspace="my-workspace", asset="my-asset", division="my-division", unit="my-unit")
)

print(signals)
# PaginatedResponse(
#     size=2,
#     next=None,
#     data=[
#         SignalListOutput(
#             id=1,
#             name="my-signal",
#             physical_unit="°C",
#             data_type="float64",
#             description="Temperature sensor",
#             long_description="Main temperature sensor for the unit"
#         ),
#         SignalListOutput(
#             id=2,
#             name="another-signal",
#             physical_unit="bar",
#             data_type="float64",
#             description="Pressure sensor",
#             long_description="Main pressure sensor for the unit"
#         )
#     ]
# )
