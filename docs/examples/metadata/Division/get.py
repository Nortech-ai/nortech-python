from nortech import Nortech
from nortech.metadata.values.division import DivisionInput

nortech = Nortech()

# Get by ID
division = nortech.metadata.division.get(123)

# Get by input dict
division = nortech.metadata.division.get({"workspace": "my-workspace", "asset": "my-asset", "division": "my-division"})

# Get by DivisionInput pydantic object
division = nortech.metadata.division.get(
    DivisionInput(workspace="my-workspace", asset="my-asset", division="my-division")
)

print(division)
# DivisionOutput(
#     id=123,
#     name="my-division",
#     description="my-description",
#     created_at=datetime.datetime(2024, 1, 1, 0, 0, 0, 0),
#     updated_at=datetime.datetime(2024, 1, 1, 0, 0, 0, 0),
#     workspace=MetadataOutput(
#         id=123,
#         name="my-workspace"
#     ),
#     asset=MetadataOutput(
#         id=456,
#         name="my-asset"
#     )
# )
