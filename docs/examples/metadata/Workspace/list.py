from nortech import Nortech
from nortech.metadata.values.pagination import PaginationOptions

nortech = Nortech()

# List all workspaces
workspaces = nortech.metadata.workspace.list()

# List with pagination
workspaces = nortech.metadata.workspace.list(PaginationOptions(size=10, sortBy="name"))

print(workspaces)
# PaginatedResponse(
#     size=2,
#     next=None,
#     data=[
#         WorkspaceListOutput(
#             id=1,
#             name="my-workspace",
#             description="my-description"
#         ),
#         WorkspaceListOutput(
#             id=2,
#             name="my-workspace",
#             description="my-description"
#         )
#     ]
# )
