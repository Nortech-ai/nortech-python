from nortech import Nortech
from nortech.metadata.values.pagination import PaginationOptions

nortech = Nortech()

# List all units in an asset
units = nortech.metadata.unit.list_by_asset_id(123)

# List with pagination
units = nortech.metadata.unit.list_by_asset_id(123, PaginationOptions(size=10, sortBy="name"))

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
