from nortech import Nortech
from nortech.metadata.values.asset import AssetInput

nortech = Nortech()

# Get by ID
asset = nortech.metadata.asset.get(123)

# Get by input dict
asset = nortech.metadata.asset.get({"workspace": "my-workspace", "asset": "my-asset"})

# Get by AssetInput pydantic object
asset = nortech.metadata.asset.get(AssetInput(workspace="my-workspace", asset="my-asset"))

print(asset)
# AssetOutput(
#     id=123,
#     name="my-asset",
#     description="my-description",
#     created_at=datetime.datetime(2024, 1, 1, 0, 0, 0, 0),
#     updated_at=datetime.datetime(2024, 1, 1, 0, 0, 0, 0),
#     workspace=MetadataOutput(
#         id=123,
#         name="my-workspace",
#     )
# )
