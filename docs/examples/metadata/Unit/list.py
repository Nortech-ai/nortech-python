from nortech import Nortech
from nortech.metadata.values.division import DivisionInput
from nortech.metadata.values.pagination import PaginationOptions

nortech = Nortech()

# List all units in a division
units = nortech.metadata.unit.list(123)  # using division ID

# List with pagination
units = nortech.metadata.unit.list(
    {"workspace": "my-workspace", "asset": "my-asset", "division": "my-division"},  # using DivisionInputDict
    PaginationOptions(size=10, sortBy="name"),
)

# Using DivisionInput pydantic object
units = nortech.metadata.unit.list(DivisionInput(workspace="my-workspace", asset="my-asset", division="my-division"))

print(units)
# PaginatedResponse(
#     size=2,
#     next=None,
#     data=[
#         UnitListOutput(
#             id=1,
#             name="my-unit"
#         ),
#         UnitListOutput(
#             id=2,
#             name="another-unit"
#         )
#     ]
# )
