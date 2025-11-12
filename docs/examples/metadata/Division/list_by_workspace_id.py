from nortech import Nortech
from nortech.metadata.values.pagination import PaginationOptions

nortech = Nortech()

# List all divisions in a workspace
divisions = nortech.metadata.division.list_by_workspace_id(123)

# List with pagination
divisions = nortech.metadata.division.list_by_workspace_id(123, PaginationOptions(size=10, sortBy="name"))

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
