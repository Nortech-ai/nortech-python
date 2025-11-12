from nortech import Nortech
from nortech.metadata.values.unit import UnitInput

nortech = Nortech()

# Get by ID
unit = nortech.metadata.unit.get(123)

# Get by input dict
unit = nortech.metadata.unit.get(
    {"workspace": "my-workspace", "asset": "my-asset", "division": "my-division", "unit": "my-unit"}
)

# Get by UnitInput pydantic object
unit = nortech.metadata.unit.get(
    UnitInput(workspace="my-workspace", asset="my-asset", division="my-division", unit="my-unit")
)

print(unit)
# UnitOutput(
#     id=123,
#     name="my-unit",
#     created_at=datetime.datetime(2024, 1, 1, 0, 0, 0, 0),
#     updated_at=datetime.datetime(2024, 1, 1, 0, 0, 0, 0),
#     workspace=MetadataOutput(
#         id=123,
#         name="my-workspace"
#     ),
#     asset=MetadataOutput(
#         id=456,
#         name="my-asset"
#     ),
#     division=MetadataOutput(
#         id=789,
#         name="my-division"
#     )
# )
