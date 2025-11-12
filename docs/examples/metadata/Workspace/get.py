from nortech import Nortech
from nortech.metadata.values.workspace import WorkspaceInput

nortech = Nortech()

# Get by ID
workspace = nortech.metadata.workspace.get(123)

# Get by name
workspace = nortech.metadata.workspace.get("my-workspace")

# Get by input dict
workspace = nortech.metadata.workspace.get({"workspace": "my-workspace"})

# Get by WorkspaceInput pydantic object
workspace = nortech.metadata.workspace.get(WorkspaceInput(workspace="my-workspace"))

print(workspace)
# WorkspaceOutput(
#     id=123,
#     name="my-workspace",
#     description="my-description",
#     created_at=datetime.datetime(2024, 1, 1, 0, 0, 0, 0),
#     updated_at=datetime.datetime(2024, 1, 1, 0, 0, 0, 0)
# )
