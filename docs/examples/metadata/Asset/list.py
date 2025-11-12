from nortech import Nortech
from nortech.metadata.values.pagination import PaginationOptions
from nortech.metadata.values.workspace import WorkspaceInput

nortech = Nortech()

# List all assets in a workspace
assets = nortech.metadata.asset.list(123)  # using workspace ID

# List with pagination
assets = nortech.metadata.asset.list(
    "my-workspace",  # using workspace name
    PaginationOptions(size=10, sortBy="name"),
)

# Using WorkspaceInputDict dictionary
assets = nortech.metadata.asset.list({"workspace": "my-workspace"})

# Using WorkspaceInput pydantic object
assets = nortech.metadata.asset.list(WorkspaceInput(workspace="my-workspace"))

print(assets)
# PaginatedResponse(
#     size=2,
#     next=None,
#     data=[
#         AssetListOutput(
#             id=1,
#             name="my-asset",
#             description="my-description"
#         ),
#         AssetListOutput(
#             id=2,
#             name="another-asset",
#             description="another-description"
#         )
#     ]
# )
