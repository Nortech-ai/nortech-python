from nortech import Nortech
from nortech.metadata.values.asset import AssetInput
from nortech.metadata.values.pagination import PaginationOptions

nortech = Nortech()

# List all divisions in an asset
divisions = nortech.metadata.division.list(123)  # using asset ID

# List with pagination
divisions = nortech.metadata.division.list(
    {"workspace": "my-workspace", "asset": "my-asset"},  # using AssetInputDict
    PaginationOptions(size=10, sortBy="name"),
)

# Using AssetInput pydantic object
divisions = nortech.metadata.division.list(AssetInput(workspace="my-workspace", asset="my-asset"))

print(divisions)
# PaginatedResponse(
#     size=2,
#     next=None,
#     data=[
#         DivisionListOutput(
#             id=1,
#             name="my-division",
#             description="my-description"
#         ),
#         DivisionListOutput(
#             id=2,
#             name="another-division",
#             description="another-description"
#         )
#     ]
# )
