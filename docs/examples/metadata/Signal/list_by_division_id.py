from nortech import Nortech
from nortech.metadata.values.pagination import PaginationOptions

nortech = Nortech()

# List all signals in a division
signals = nortech.metadata.signal.list_by_division_id(123)

# List with pagination
signals = nortech.metadata.signal.list_by_division_id(123, PaginationOptions(size=10, sortBy="name"))

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
