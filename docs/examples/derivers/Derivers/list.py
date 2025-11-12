from nortech import Nortech
from nortech.derivers import Deriver


# Define Deriver
class MyDeriver(Deriver): ...


nortech = Nortech()

derivers = nortech.derivers.list()
print(derivers)
# PaginatedResponse(
#     size=1,
#     next=None,
#     data=[
#         DeployedDeriverList(
#             deriver=MyDeriver,
#             description="my-description",
#             start_at=None,
#         )
#     ],
# )
