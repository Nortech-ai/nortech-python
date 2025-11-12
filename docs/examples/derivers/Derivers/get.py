from nortech import Nortech
from nortech.derivers import Deriver


# Define Deriver
class MyDeriver(Deriver): ...


nortech = Nortech()

# Get deriver by class or class name
derivers = nortech.derivers.get(MyDeriver)
derivers = nortech.derivers.get("MyDeriver")

print(derivers)
# DeployedDeriver(
#     deriver=MyDeriver,
#     description="my-description",
#     start_at="2025-01-01T12:00:00Z",
#     inputs=[
#         SignalOutput(
#             id=1,
#             name="input_1",
#             description="input_1",
#             long_description="input_1_long_description",
#             data_type="float",
#             physical_unit="m/s",
#             created_at="2025-01-01T12:00:00Z",
#             updated_at="2025-01-01T12:00:00Z",
#             workspace=MetadataOutput(
#                 id=1,
#                 name="workspace1",
#             ),
#             asset=MetadataOutput(
#                 id=1,
#                 name="asset1",
#             ),
#             division=MetadataOutput(
#                 id=1,
#                 name="division1",
#             ),
#             unit=MetadataOutput(
#                 id=1,
#                 name="unit1",
#             ),
#         ),
#     ],
#     outputs=[
#         SignalOutput(
#             id=2,
#             name="output_1",
#             description="output_1",
#             long_description="output_1_long_description",
#             data_type="float",
#             physical_unit="m/s",
#             created_at="2025-01-01T12:00:00Z",
#             updated_at="2025-01-01T12:00:00Z",
#             workspace=MetadataOutput(
#                 id=1,
#                 name="workspace1",
#             ),
#             asset=MetadataOutput(
#                 id=1,
#                 name="asset1",
#             ),
#             division=MetadataOutput(
#                 id=1,
#                 name="division1",
#             ),
#             unit=MetadataOutput(
#                 id=1,
#                 name="unit1",
#             ),
#         ),
#     ]
# )
