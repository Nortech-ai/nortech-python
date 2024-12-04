#

### Nortech

Main class for interacting with the Nortech SDK.

**Attributes**:

- `metadata` _Metadata_ - Client for interacting with the Nortech Metadata API.
- `datatools` _Datatools_ - Client for interacting with the Nortech Datatools API.
- `derivers` _Derivers_ - Client for interacting with the Nortech Derivers API.

#### constructor

```python
def __init__(url: str = "https://api.apps.nor.tech",
             api_key: str | None = None,
             ignore_pagination: bool | None = None,
             user_agent: str | None = None,
             experimental_features: bool | None = None,
             timeout: float | Timeout | None = None,
             retry: int | Retry | None = None)
```

Initialize the Nortech class.

**Arguments**:

- `url` _str_ - The URL of the Nortech API. Defaults to "https://api.apps.nor.tech".
- `api_key` _str | None_ - The API key for the Nortech API.
- `ignore_pagination` _bool | None_ - Whether to ignore pagination.
- `user_agent` _str | None_ - The user agent for the Nortech API.
- `experimental_features` _bool | None_ - Whether to enable experimental features.
- `timeout` _float | Timeout | None_ - The timeout setting for the API request. From [urllib3](https://urllib3.readthedocs.io/en/stable/reference/urllib3.util.html#urllib3.util.Timeout) package.
- `retry` _int | Retry | None_ - The retry setting for the API request. From [urllib3](https://urllib3.readthedocs.io/en/stable/reference/urllib3.util.html#urllib3.util.Retry) package.
  

**Example**:

```python
from urllib3 import Retry, Timeout

from nortech import Nortech

nortech = Nortech()  # Uses environment variables for configs

nortech = Nortech(api_key="my_api_key")  # Sets the API key

nortech = Nortech(ignore_pagination=False)  # Use pagination

nortech = Nortech(user_agent="my_user_agent")  # Sets the user agent

nortech = Nortech(timeout=Timeout(connect=10, read=60))  # Sets the timeout

nortech = Nortech(
    retry=Retry(
        total=5,
        backoff_factor=1,
        status_forcelist=[502, 503, 504],
        allowed_methods=["GET", "POST"],
        raise_on_status=False,
    )
)  # Sets the retry configuration

```



## metadata

### Metadata

Client for interacting with the Nortech Metadata API.

**Attributes**:

- `workspace` _Workspace_ - Client for interacting with the Nortech Metadata Workspace API.
- `asset` _Asset_ - Client for interacting with the Nortech Metadata Asset API.
- `division` _Division_ - Client for interacting with the Nortech Metadata Division API.
- `unit` _Unit_ - Client for interacting with the Nortech Metadata Unit API.
- `device` _Device_ - Client for interacting with the Nortech Metadata Device API.
- `signal` _Signal_ - Client for interacting with the Nortech Metadata Signal API.

### Workspace

Workspace.

#### get

```python
def get(
    workspace: int | str | WorkspaceInputDict | WorkspaceInput
    | WorkspaceOutput | WorkspaceListOutput
) -> WorkspaceOutput
```

Get a workspace by ID or name.

**Arguments**:

- `workspace` _int | str | WorkspaceInputDict | WorkspaceInput | WorkspaceOutput | WorkspaceListOutput_ - The workspace identifier, which can be:
  - *int*: The workspace "ID".
  - *str*: The workspace "name".
  - [WorkspaceInputDict](#workspaceinputdict): A dictionary representation of a workspace input.
  - [WorkspaceInput](#workspaceinput): A pydantic model representing a workspace input.
  - [WorkspaceOutput](#workspaceoutput): A pydantic model representing a workspace output. Obtained from requesting a workspace metadata.
  - [WorkspaceListOutput](#workspacelistoutput): A pydantic model representing a listed workspace output. Obtained from requesting workspaces metadata.
  

**Returns**:

- `WorkspaceOutput` - The workspace details.
  

**Example**:

```python
from nortech import Nortech
from nortech.core.values.workspace import WorkspaceInput

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

```

#### list

```python
def list(
    pagination_options: PaginationOptions[Literal["id", "name", "description"]]
    | None = None
) -> PaginatedResponse[WorkspaceListOutput]
```

List all workspaces.

**Arguments**:

- `pagination_options` _PaginationOptions, optional_ - Pagination settings.
  

**Returns**:

- `PaginatedResponse[WorkspaceListOutput]` - A paginated list of workspaces.
  

**Example**:

```python
from nortech import Nortech
from nortech.gateways.nortech_api import PaginationOptions

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

```

### Asset

#### get

```python
def get(
    asset: int | AssetInputDict | AssetInput | AssetOutput | AssetListOutput
) -> AssetOutput
```

Get an asset by ID or input.

**Arguments**:

- `asset` _int | AssetInputDict | AssetInput | AssetOutput | AssetListOutput_ - The asset identifier, which can be:
  - *int*: The asset "ID".
  - [AssetInputDict](#assetinputdict): A dictionary representation of an asset input.
  - [AssetInput](#assetinput): A pydantic model representing an asset input.
  - [AssetOutput](#assetoutput): A pydantic model representing an asset output. Obtained from requesting an asset metadata.
  - [AssetListOutput](#assetlistoutput): A pydantic model representing a listed asset output. Obtained from requesting assets metadata.
  

**Returns**:

- `AssetOutput` - The asset details.
  

**Example**:

```python
from nortech import Nortech
from nortech.core.values.asset import AssetInput

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

```

#### list

```python
def list(
    workspace: int | str | WorkspaceInputDict | WorkspaceInput
    | WorkspaceOutput | WorkspaceListOutput,
    pagination_options: PaginationOptions[Literal["id", "name", "description"]]
    | None = None
) -> PaginatedResponse[AssetListOutput]
```

List all assets in a workspace.

**Arguments**:

- `workspace` _int | str | WorkspaceInputDict | WorkspaceInput | WorkspaceOutput | WorkspaceListOutput_ - The workspace identifier, which can be:
  - *int*: The workspace "ID".
  - *str*: The workspace "name".
  - [WorkspaceInputDict](#workspaceinputdict): A dictionary representation of a workspace input.
  - [WorkspaceInput](#workspaceinput): A pydantic model representing a workspace input.
  - [WorkspaceOutput](#workspaceoutput): A pydantic model representing a workspace output.
  - [WorkspaceListOutput](#workspacelistoutput): A pydantic model representing a listed workspace output.
- `pagination_options` _PaginationOptions, optional_ - Pagination settings.
  

**Returns**:

- `PaginatedResponse[AssetListOutput]` - A paginated list of assets.
  

**Example**:

```python
from nortech import Nortech
from nortech.gateways.nortech_api import PaginationOptions
from nortech.core.values.workspace import WorkspaceInput

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

```

### Division

#### get

```python
def get(
    division: int | DivisionInputDict | DivisionInput | DivisionOutput
    | DivisionListOutput
) -> DivisionOutput
```

Get a division by ID or input.

**Arguments**:

- `division` _int | DivisionInputDict | DivisionInput | DivisionOutput | DivisionListOutput_ - The division identifier, which can be:
  - *int*: The division "ID".
  - [DivisionInputDict](#divisioninputdict): A dictionary representation of a division input.
  - [DivisionInput](#divisioninput): A pydantic model representing a division input.
  - [DivisionOutput](#divisionoutput): A pydantic model representing a division output. Obtained from requesting a division metadata.
  - [DivisionListOutput](#divisionlistoutput): A pydantic model representing a listed division output. Obtained from requesting divisions metadata.
  

**Returns**:

- `DivisionOutput` - The division details.
  

**Example**:

```python
from nortech import Nortech
from nortech.core.values.division import DivisionInput

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

```

#### list

```python
def list(
    asset: int | AssetInputDict | AssetInput | AssetOutput | AssetListOutput,
    pagination_options: PaginationOptions[Literal["id", "name", "description"]]
    | None = None
) -> PaginatedResponse[DivisionListOutput]
```

List all divisions in an asset.

**Arguments**:

- `asset` _int | AssetInputDict | AssetInput | AssetOutput | AssetListOutput_ - The asset identifier, which can be:
  - *int*: The asset "ID".
  - [AssetInputDict](#assetinputdict): A dictionary representation of an asset input.
  - [AssetInput](#assetinput): A pydantic model representing an asset input.
  - [AssetOutput](#assetoutput): A pydantic model representing an asset output.
  - [AssetListOutput](#assetlistoutput): A pydantic model representing a listed asset output.
- `pagination_options` _PaginationOptions, optional_ - Pagination settings.
  

**Returns**:

- `PaginatedResponse[DivisionListOutput]` - A paginated list of divisions.
  

**Example**:

```python
from nortech import Nortech
from nortech.gateways.nortech_api import PaginationOptions
from nortech.core.values.asset import AssetInput

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

```

#### list\_by\_workspace\_id

```python
def list_by_workspace_id(
    workspace_id: int,
    pagination_options: PaginationOptions[Literal["id", "name", "description"]]
    | None = None
) -> PaginatedResponse[DivisionListOutput]
```

List all divisions in a workspace.

**Arguments**:

- `workspace_id` _int_ - The workspace ID.
- `pagination_options` _PaginationOptions, optional_ - Pagination settings.
  

**Returns**:

- `PaginatedResponse[DivisionListOutput]` - A paginated list of divisions.
  

**Example**:

```python
from nortech import Nortech
from nortech.gateways.nortech_api import PaginationOptions

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

```

### Unit

#### get

```python
def get(
    unit: int | UnitInputDict | UnitInput | UnitOutput | UnitListOutput
) -> UnitOutput
```

Get a unit by ID or input.

**Arguments**:

- `unit` _int | UnitInputDict | UnitInput | UnitOutput | UnitListOutput_ - The unit identifier, which can be:
  - *int*: The unit "ID".
  - [UnitInputDict](#unitinputdict): A dictionary representation of a unit input.
  - [UnitInput](#unitinput): A pydantic model representing a unit input.
  - [UnitOutput](#unitoutput): A pydantic model representing a unit output. Obtained from requesting a unit metadata.
  - [UnitListOutput](#unitlistoutput): A pydantic model representing a listed unit output. Obtained from requesting units metadata.
  

**Returns**:

- `UnitOutput` - The unit details.
  

**Example**:

```python
from nortech import Nortech
from nortech.core.values.unit import UnitInput

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

```

#### list

```python
def list(
    division: int | DivisionInputDict | DivisionInput | DivisionOutput
    | DivisionListOutput,
    pagination_options: PaginationOptions[Literal["id", "name"]] | None = None
) -> PaginatedResponse[UnitListOutput]
```

List all units in a division.

**Arguments**:

- `division` _int | DivisionInputDict | DivisionInput | DivisionOutput | DivisionListOutput_ - The division identifier, which can be:
  - *int*: The division "ID".
  - [DivisionInputDict](#divisioninputdict): A dictionary representation of a division input.
  - [DivisionInput](#divisioninput): A pydantic model representing a division input.
  - [DivisionOutput](#divisionoutput): A pydantic model representing a division output.
  - [DivisionListOutput](#divisionlistoutput): A pydantic model representing a listed division output.
- `pagination_options` _PaginationOptions, optional_ - Pagination settings.
  

**Returns**:

- `PaginatedResponse[UnitListOutput]` - A paginated list of units.
  

**Example**:

```python
from nortech import Nortech
from nortech.gateways.nortech_api import PaginationOptions
from nortech.core.values.division import DivisionInput

nortech = Nortech()

# List all units in a division
units = nortech.metadata.unit.list(123)  # using division ID

# List with pagination
units = nortech.metadata.unit.list(
    {"workspace": "my-workspace", "asset": "my-asset", "division": "my-division"},  # using DivisionInputDict
    PaginationOptions(size=10, sortBy="name"),
)

# Using DivisionInput pydantic object
units = nortech.metadata.unit.list(DivisionInput(workspace="my-workspace", asset="my-asset", division="my-division"))

print(units)
# PaginatedResponse(
#     size=2,
#     next=None,
#     data=[
#         UnitListOutput(
#             id=1,
#             name="my-unit"
#         ),
#         UnitListOutput(
#             id=2,
#             name="another-unit"
#         )
#     ]
# )

```

#### list\_by\_workspace\_id

```python
def list_by_workspace_id(
    workspace_id: int,
    pagination_options: PaginationOptions[Literal["id", "name"]] | None = None
) -> PaginatedResponse[UnitListOutput]
```

List all units in a workspace.

**Arguments**:

- `workspace_id` _int_ - The workspace ID.
- `pagination_options` _PaginationOptions, optional_ - Pagination settings.
  

**Returns**:

- `PaginatedResponse[UnitListOutput]` - A paginated list of units.
  

**Example**:

```python
from nortech import Nortech
from nortech.gateways.nortech_api import PaginationOptions

nortech = Nortech()

# List all units in a workspace
units = nortech.metadata.unit.list_by_workspace_id(123)

# List with pagination
units = nortech.metadata.unit.list_by_workspace_id(123, PaginationOptions(size=10, sortBy="name"))

print(units)
# PaginatedResponse(
#     size=2,
#     next=None,
#     data=[
#         UnitListOutput(
#             id=1,
#             name="my-unit"
#         ),
#         UnitListOutput(
#             id=2,
#             name="another-unit"
#         )
#     ]
# )

```

#### list\_by\_asset\_id

```python
def list_by_asset_id(
    asset_id: int,
    pagination_options: PaginationOptions[Literal["id", "name"]] | None = None
) -> PaginatedResponse[UnitListOutput]
```

List all units in an asset.

**Arguments**:

- `asset_id` _int_ - The asset ID.
- `pagination_options` _PaginationOptions, optional_ - Pagination settings.
  

**Returns**:

- `PaginatedResponse[UnitListOutput]` - A paginated list of units.
  

**Example**:

```python
from nortech import Nortech
from nortech.gateways.nortech_api import PaginationOptions

nortech = Nortech()

# List all units in an asset
units = nortech.metadata.unit.list_by_asset_id(123)

# List with pagination
units = nortech.metadata.unit.list_by_asset_id(123, PaginationOptions(size=10, sortBy="name"))

print(units)
# PaginatedResponse(
#     size=2,
#     next=None,
#     data=[
#         UnitListOutput(
#             id=1,
#             name="my-unit"
#         ),
#         UnitListOutput(
#             id=2,
#             name="another-unit"
#         )
#     ]
# )
```

### Device

#### get

```python
def get(
    device: int | DeviceInputDict | DeviceInput | DeviceOutput
    | DeviceListOutput
) -> DeviceOutput
```

Get a device by ID or input.

**Arguments**:

- `device` _int | DeviceInputDict | DeviceInput | DeviceOutput | DeviceListOutput_ - The device identifier, which can be:
  - *int*: The device "ID".
  - [DeviceInputDict](#deviceinputdict): A dictionary representation of a device input.
  - [DeviceInput](#deviceinput): A pydantic model representing a device input.
  - [DeviceOutput](#deviceoutput): A pydantic model representing a device output. Obtained from requesting a device metadata.
  - [DeviceListOutput](#devicelistoutput): A pydantic model representing a listed device output. Obtained from requesting devices metadata.
  

**Returns**:

- `DeviceOutput` - The device details.
  

**Example**:

```python
from nortech import Nortech
from nortech.core.values.device import DeviceInput

nortech = Nortech()

# Get by ID
device = nortech.metadata.device.get(123)

# Get by input dict
device = nortech.metadata.device.get(
    {"workspace": "my-workspace", "asset": "my-asset", "division": "my-division", "device": "my-device"}
)

# Get by DeviceInput pydantic object
device = nortech.metadata.device.get(
    DeviceInput(workspace="my-workspace", asset="my-asset", division="my-division", device="my-device")
)

print(device)
# DeviceOutput(
#     id=123,
#     name="my-device",
#     type="my-type",
#     onboarded=True,
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

```

#### list

```python
def list(
    division: int | DivisionInputDict | DivisionInput | DivisionOutput
    | DivisionListOutput,
    pagination_options: PaginationOptions[Literal["id", "name", "type",
                                                  "onboarded"]] | None = None
) -> PaginatedResponse[DeviceListOutput]
```

List all devices in a division.

**Arguments**:

- `division` _int | DivisionInputDict | DivisionInput | DivisionOutput | DivisionListOutput_ - The division identifier, which can be:
  - *int*: The division "ID".
  - [DivisionInputDict](#divisioninputdict): A dictionary representation of a division input.
  - [DivisionInput](#divisioninput): A pydantic model representing a division input.
  - [DivisionOutput](#divisionoutput): A pydantic model representing a division output.
  - [DivisionListOutput](#divisionlistoutput): A pydantic model representing a listed division output.
- `pagination_options` _PaginationOptions, optional_ - Pagination settings.
  

**Returns**:

- `PaginatedResponse[DeviceListOutput]` - A paginated list of devices.
  

**Example**:

```python
from nortech import Nortech
from nortech.gateways.nortech_api import PaginationOptions
from nortech.core.values.division import DivisionInput

nortech = Nortech()

# List all devices in a division
devices = nortech.metadata.device.list(123)  # using division ID

# List with pagination
devices = nortech.metadata.device.list(
    {"workspace": "my-workspace", "asset": "my-asset", "division": "my-division"},  # using DivisionInputDict
    PaginationOptions(size=10, sortBy="name"),
)

# Using DivisionInput pydantic object
devices = nortech.metadata.device.list(
    DivisionInput(workspace="my-workspace", asset="my-asset", division="my-division")
)

print(devices)
# PaginatedResponse(
#     size=2,
#     next=None,
#     data=[
#         DeviceListOutput(
#             id=1,
#             name="my-device",
#             type="my-type",
#             onboarded=True
#         ),
#         DeviceListOutput(
#             id=2,
#             name="another-device",
#             type="another-type",
#             onboarded=False
#         )
#     ]
# )

```

#### list\_by\_workspace\_id

```python
def list_by_workspace_id(
    workspace_id: int,
    pagination_options: PaginationOptions[Literal["id", "name", "type",
                                                  "onboarded"]] | None = None
) -> PaginatedResponse[DeviceListOutput]
```

List all devices in a workspace.

**Arguments**:

- `workspace_id` _int_ - The workspace ID.
- `pagination_options` _PaginationOptions, optional_ - Pagination settings.
  

**Returns**:

- `PaginatedResponse[DeviceListOutput]` - A paginated list of devices.
  

**Example**:

```python
from nortech import Nortech
from nortech.gateways.nortech_api import PaginationOptions

nortech = Nortech()

# List all devices in a workspace
devices = nortech.metadata.device.list_by_workspace_id(123)

# List with pagination
devices = nortech.metadata.device.list_by_workspace_id(123, PaginationOptions(size=10, sortBy="name"))

print(devices)
# PaginatedResponse(
#     size=2,
#     next=None,
#     data=[
#         DeviceListOutput(
#             id=1,
#             name="my-device",
#             type="my-type",
#             onboarded=True
#         ),
#         DeviceListOutput(
#             id=2,
#             name="another-device",
#             type="another-type",
#             onboarded=False
#         )
#     ]
# )

```

#### list\_by\_asset\_id

```python
def list_by_asset_id(
    asset_id: int,
    pagination_options: PaginationOptions[Literal["id", "name", "type",
                                                  "onboarded"]] | None = None
) -> PaginatedResponse[DeviceListOutput]
```

List all devices in an asset.

**Arguments**:

- `asset_id` _int_ - The asset ID.
- `pagination_options` _PaginationOptions, optional_ - Pagination settings.
  

**Returns**:

- `PaginatedResponse[DeviceListOutput]` - A paginated list of devices.
  

**Example**:

```python
from nortech import Nortech
from nortech.gateways.nortech_api import PaginationOptions

nortech = Nortech()

# List all devices in an asset
devices = nortech.metadata.device.list_by_asset_id(123)

# List with pagination
devices = nortech.metadata.device.list_by_asset_id(123, PaginationOptions(size=10, sortBy="name"))

print(devices)
# PaginatedResponse(
#     size=2,
#     next=None,
#     data=[
#         DeviceListOutput(
#             id=1,
#             name="my-device",
#             type="my-type",
#             onboarded=True
#         ),
#         DeviceListOutput(
#             id=2,
#             name="another-device",
#             type="another-type",
#             onboarded=False
#         )
#     ]
# )

```

### Signal

#### get

```python
def get(
    signal: int
    | SignalInputDict
    | SignalInput
    | SignalOutput
    | SignalListOutput
    | SignalDeviceInputDict
    | SignalDeviceInput
) -> SignalOutput
```

Get a signal by ID or input.

**Arguments**:

- `signal` _int | SignalInputDict | SignalInput | SignalOutput | SignalListOutput | SignalDeviceInputDict | SignalDeviceInput_ - The signal identifier, which can be:
  - *int*: The signal "ID".
  - [SignalInputDict](#signalinputdict): A dictionary representation of a signal input.
  - [SignalInput](#signalinput): A pydantic model representing a signal input.
  - [SignalOutput](#signaloutput): A pydantic model representing a signal output. Obtained from requesting a signal metadata.
  - [SignalListOutput](#signallistoutput): A pydantic model representing a listed signal output. Obtained from requesting signals metadata.
  - [SignalDeviceInputDict](#signaldeviceinputdict): A dictionary representation of a device signal input.
  - [SignalDeviceInput](#signaldeviceinput): A pydantic model representing a device signal input.
  

**Returns**:

- `SignalOutput` - The signal details.
  

**Example**:

```python
from nortech import Nortech
from nortech.core.values.signal import SignalDeviceInput, SignalInput

nortech = Nortech()

# Get by ID
signal = nortech.metadata.signal.get(123)

# Get unit signal by input dict
signal = nortech.metadata.signal.get(
    {
        "workspace": "my-workspace",
        "asset": "my-asset",
        "division": "my-division",
        "unit": "my-unit",
        "signal": "my-signal",
    }
)

# Get device signal by input dict
signal = nortech.metadata.signal.get(
    {
        "workspace": "my-workspace",
        "asset": "my-asset",
        "division": "my-division",
        "device": "my-device",
        "signal": "my-signal",
    }
)

# Get by SignalInput pydantic object
signal = nortech.metadata.signal.get(
    SignalInput(
        workspace="my-workspace", asset="my-asset", division="my-division", unit="my-unit", signal="my-signal"
    )
)

# Get by SignalDeviceInput pydantic object
signal = nortech.metadata.signal.get(
SignalDeviceInput(
        workspace="my-workspace", asset="my-asset", division="my-division", device="my-device", signal="my-signal"
    )
)

print(signal)
# SignalOutput(
#     id=123,
#     name="my-signal",
#     physical_unit="°C",
#     data_type="float64",
#     description="Temperature sensor",
#     long_description="Main temperature sensor for the unit",
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
#     ),
#     unit=MetadataOutput(
#         id=101,
#         name="my-unit"
#     )
#     device=MetadataOutput(
#         id=101,
#         name="my-device"
#     )
# )

```

#### list

```python
def list(
    unit_or_device: int | UnitInputDict | UnitInput | UnitOutput
    | DeviceInputDict | DeviceInput | DeviceOutput,
    pagination_options: PaginationOptions[Literal["id", "name",
                                                  "physical_unit", "data_type",
                                                  "description",
                                                  "long_description"]]
    | None = None
) -> PaginatedResponse[SignalListOutput]
```

List all signals in a unit or device.

**Arguments**:

- `unit_or_device` _int | UnitInputDict | UnitInput | UnitOutput | DeviceInputDict | DeviceInput | DeviceOutput_ - The unit or device identifier, which can be:
  - *int*: The unit/device "ID".
  - [UnitInputDict](#unitinputdict): A dictionary representation of a unit input.
  - [UnitInput](#unitinput): A pydantic model representing a unit input.
  - [UnitOutput](#unitoutput): A pydantic model representing a unit output.
  - [DeviceInputDict](#deviceinputdict): A dictionary representation of a device input.
  - [DeviceInput](#deviceinput): A pydantic model representing a device input.
  - [DeviceOutput](#deviceoutput): A pydantic model representing a device output.
- `pagination_options` _PaginationOptions, optional_ - Pagination settings.
  

**Returns**:

- `PaginatedResponse[SignalListOutput]` - A paginated list of signals.
  

**Example**:

```python
from nortech import Nortech
from nortech.gateways.nortech_api import PaginationOptions
from nortech.core.values.device import DeviceInput
from nortech.core.values.unit import UnitInput

nortech = Nortech()

# List all signals in a unit
signals = nortech.metadata.signal.list(123)  # using unit ID

# List unit signals with pagination
signals = nortech.metadata.signal.list(
    {"workspace": "my-workspace", "asset": "my-asset", "division": "my-division", "unit": "my-unit"},
    PaginationOptions(size=10, sortBy="name"),
)

# List device signals with pagination
signals = nortech.metadata.signal.list(
    {"workspace": "my-workspace", "asset": "my-asset", "division": "my-division", "device": "my-device"},
    PaginationOptions(size=10, sortBy="name"),
)

# Using UnitInput pydantic object
signals = nortech.metadata.signal.list(
    UnitInput(workspace="my-workspace", asset="my-asset", division="my-division", unit="my-unit")
)

# Using DeviceInput pydantic object
signals = nortech.metadata.signal.list(
    DeviceInput(workspace="my-workspace", asset="my-asset", division="my-division", device="my-device")
)

print(signals)
# PaginatedResponse(
#     size=2,
#     next=None,
#     data=[
#         SignalListOutput(
#             id=1,
#             name="my-signal",
#             physical_unit="°C",
#             data_type="float64",
#             description="Temperature sensor",
#             long_description="Main temperature sensor for the unit"
#         ),
#         SignalListOutput(
#             id=2,
#             name="another-signal",
#             physical_unit="bar",
#             data_type="float64",
#             description="Pressure sensor",
#             long_description="Main pressure sensor for the unit"
#         )
#     ]
# )

```

#### list\_by\_workspace\_id

```python
def list_by_workspace_id(
    workspace_id: int,
    pagination_options: PaginationOptions[Literal["id", "name",
                                                  "physical_unit", "data_type",
                                                  "description",
                                                  "long_description"]]
    | None = None
) -> PaginatedResponse[SignalListOutput]
```

List all signals in a workspace.

**Arguments**:

- `workspace_id` _int_ - The workspace ID.
- `pagination_options` _PaginationOptions, optional_ - Pagination settings.
  

**Returns**:

- `PaginatedResponse[SignalListOutput]` - A paginated list of signals.
  

**Example**:

```python
from nortech import Nortech
from nortech.gateways.nortech_api import PaginationOptions

nortech = Nortech()

# List all signals in a workspace
signals = nortech.metadata.signal.list_by_workspace_id(123)

# List with pagination
signals = nortech.metadata.signal.list_by_workspace_id(123, PaginationOptions(size=10, sortBy="name"))

print(signals)
# PaginatedResponse(
#     size=2,
#     next=None,
#     data=[
#         SignalListOutput(
#             id=1,
#             name="my-signal",
#             physical_unit="°C",
#             data_type="float64",
#             description="Temperature sensor",
#             long_description="Main temperature sensor for the unit"
#         ),
#         SignalListOutput(
#             id=2,
#             name="another-signal",
#             physical_unit="bar",
#             data_type="float64",
#             description="Pressure sensor",
#             long_description="Main pressure sensor for the unit"
#         )
#     ]
# )

```

#### list\_by\_asset\_id

```python
def list_by_asset_id(
    asset_id: int,
    pagination_options: PaginationOptions[Literal["id", "name",
                                                  "physical_unit", "data_type",
                                                  "description",
                                                  "long_description"]]
    | None = None
) -> PaginatedResponse[SignalListOutput]
```

List all signals in an asset.

**Arguments**:

- `asset_id` _int_ - The asset ID.
- `pagination_options` _PaginationOptions, optional_ - Pagination settings.
  

**Returns**:

- `PaginatedResponse[SignalListOutput]` - A paginated list of signals.
  

**Example**:

```python
from nortech import Nortech
from nortech.gateways.nortech_api import PaginationOptions

nortech = Nortech()

# List all signals in an asset
signals = nortech.metadata.signal.list_by_asset_id(123)

# List with pagination
signals = nortech.metadata.signal.list_by_asset_id(123, PaginationOptions(size=10, sortBy="name"))

print(signals)
# PaginatedResponse(
#     size=2,
#     next=None,
#     data=[
#         SignalListOutput(
#             id=1,
#             name="my-signal",
#             physical_unit="°C",
#             data_type="float64",
#             description="Temperature sensor",
#             long_description="Main temperature sensor for the unit"
#         ),
#         SignalListOutput(
#             id=2,
#             name="another-signal",
#             physical_unit="bar",
#             data_type="float64",
#             description="Pressure sensor",
#             long_description="Main pressure sensor for the unit"
#         )
#     ]
# )


```

#### list\_by\_division\_id

```python
def list_by_division_id(
    division_id: int,
    pagination_options: PaginationOptions[Literal["id", "name",
                                                  "physical_unit", "data_type",
                                                  "description",
                                                  "long_description"]]
    | None = None
) -> PaginatedResponse[SignalListOutput]
```

List all signals in a division.

**Arguments**:

- `division_id` _int_ - The division ID.
- `pagination_options` _PaginationOptions, optional_ - Pagination settings.
  

**Returns**:

- `PaginatedResponse[SignalListOutput]` - A paginated list of signals.
  

**Example**:

```python
from nortech import Nortech
from nortech.gateways.nortech_api import PaginationOptions

nortech = Nortech()

# List all signals in a division
signals = nortech.metadata.signal.list_by_division_id(123)

# List with pagination
signals = nortech.metadata.signal.list_by_division_id(123, PaginationOptions(size=10, sortBy="name"))

print(signals)
# PaginatedResponse(
#     size=2,
#     next=None,
#     data=[
#         SignalListOutput(
#             id=1,
#             name="my-signal",
#             physical_unit="°C",
#             data_type="float64",
#             description="Temperature sensor",
#             long_description="Main temperature sensor for the unit"
#         ),
#         SignalListOutput(
#             id=2,
#             name="another-signal",
#             physical_unit="bar",
#             data_type="float64",
#             description="Pressure sensor",
#             long_description="Main pressure sensor for the unit"
#         )
#     ]
# )


```



## datatools

### Download

#### download\_data

```python
def download_data(signals: Sequence[int | SignalInput | SignalInputDict
                                    | SignalOutput | SignalListOutput],
                  time_window: TimeWindow, output_path: str,
                  file_format: Format)
```

Download data for the specified signals within the given time window. If experimental features are enabled, live data will also be downloaded.

**Arguments**:

- `signals` _Sequence[int | SignalInput | SignalInputDict | SignalOutput | SignalListOutput]_ - A list of signals to download, which can be of the following types:
  - int: The signal "ID".
  - [SignalInputDict](#signalinputdict): A dictionary representation of a signal input.
  - [SignalInput](#signalinput): A pydantic model representing a signal input.
  - [SignalOutput](#signaloutput): A pydantic model representing a signal output. Obtained from requesting a signal metadata.
  - [SignalListOutput](#signallistoutput): A pydantic model representing a listed signal output. Obtained from requesting signals metadata.
- `time_window` _TimeWindow_ - The time window for which data should be downloaded.
- `output_path` _str_ - The file path where the downloaded data will be saved.
- `file_format` _Format_ - The format of the output file. Can be "parquet", "csv", or "json".
  

**Raises**:

- `NotImplementedError` - If the time window corresponds to hot storage, which is not yet supported.
  

**Example**:

```python
from datetime import datetime

from nortech import Nortech
from nortech.core.values.signal import SignalInput, SignalInputDict
from nortech.datatools.values.windowing import TimeWindow

# Initialize the Nortech client
nortech = Nortech()

# Define signals to download
signal1: SignalInputDict = {
    "workspace": "workspace1",
    "asset": "asset1",
    "division": "division1",
    "unit": "unit1",
    "signal": "signal1",
}
signal2 = 789  # Signal ID
signal3 = SignalInput(workspace="workspace2", asset="asset2", division="division2", unit="unit2", signal="signal2")

fetched_signals = nortech.metadata.signal.list(  # Fetched signals
    {"workspace": "workspace3", "asset": "asset3", "division": "division3", "unit": "unit3"}
).data

# Define the time window for data download
my_time_window = TimeWindow(start=datetime(2023, 1, 1), end=datetime(2023, 1, 31))

# Specify the output path and file format
output_path = "path/to/output"
file_format = "parquet"

# Call the download_data function with manually defined signals or fetched signals
nortech.datatools.download.download_data(
    signals=[signal1, signal2, signal3] + fetched_signals,
    time_window=my_time_window,
    output_path=output_path,
    file_format=file_format,
)

```

### Pandas

#### get\_df

```python
def get_df(signals: Sequence[int | SignalInput | SignalInputDict | SignalOutput
                             | SignalListOutput],
           time_window: TimeWindow) -> DataFrame
```

Retrieve a pandas DataFrame for the specified signals within the given time window. If experimental features are enabled, live data will also be retrieved.

**Arguments**:

- `signals` _Sequence[int | SignalInput | SignalInputDict | SignalOutput | SignalListOutput]_ - A list of signals to download, which can be of the following types:
  - *int*: The signal "ID".
  - [SignalInputDict](#signalinputdict): A dictionary representation of a signal input.
  - [SignalInput](#signalinput): A pydantic model representing a signal input.
  - [SignalOutput](#signaloutput): A pydantic model representing a signal output. Obtained from requesting a signal metadata.
  - [SignalListOutput](#signallistoutput): A pydantic model representing a listed signal output. Obtained from requesting signals metadata.
- `time_window` _TimeWindow_ - The time window for which data should be retrieved.
  

**Returns**:

- `DataFrame` - A pandas DataFrame containing the data.
  

**Raises**:

- `NoSignalsRequestedError` - Raised when no signals are requested.
- `InvalidTimeWindow` - Raised when the start date is after the end date.
  

**Example**:

```python
from datetime import datetime

from nortech import Nortech
from nortech.core.values.signal import SignalInput, SignalInputDict
from nortech.datatools.values.windowing import TimeWindow

# Initialize the Nortech client
nortech = Nortech()

# Define signals to download
signal1: SignalInputDict = {
    "workspace": "workspace1",
    "asset": "asset1",
    "division": "division1",
    "unit": "unit1",
    "signal": "signal1",
}
signal2 = 789  # Signal ID
signal3 = SignalInput(workspace="workspace2", asset="asset2", division="division2", unit="unit2", signal="signal2")

fetched_signals = nortech.metadata.signal.list(  # Fetched signals
    {"workspace": "workspace3", "asset": "asset3", "division": "division3", "unit": "unit3"}
).data

# Define the time window for data download
my_time_window = TimeWindow(start=datetime(2023, 1, 1), end=datetime(2023, 1, 31))

# Call the get_df function with manually defined signals or fetched signals
df = nortech.datatools.pandas.get_df(
    signals=[signal1, signal2, signal3] + fetched_signals,
    time_window=my_time_window,
)

print(df.columns)
# [
#     "timestamp",
#     "workspace_1/asset_1/division_1/unit_1/signal_1",
#     "workspace_1/asset_1/division_1/unit_1/signal_2",
#     "workspace_2/asset_2/division_2/unit_2/signal_3",
#     "workspace_3/asset_3/division_3/unit_3/signal_4",
#     "workspace_3/asset_3/division_3/unit_3/signal_5",
# ]

```

### Polars

#### get\_lazy\_df

```python
def get_lazy_df(signals: Sequence[int | SignalInput | SignalInputDict
                                  | SignalOutput | SignalListOutput],
                time_window: TimeWindow) -> LazyFrame
```

Retrieve a polars LazyFrame for the specified signals within the given time window. If experimental features are enabled, live data will also be retrieved.

**Arguments**:

- `signals` _Sequence[int | SignalInput | SignalInputDict | SignalOutput | SignalListOutput]_ - A list of signals to download, which can be of the following types:
  - *int*: The signal "ID".
  - [SignalInputDict](#signalinputdict): A dictionary representation of a signal input.
  - [SignalInput](#signalinput): A pydantic model representing a signal input.
  - [SignalOutput](#signaloutput): A pydantic model representing a signal output. Obtained from requesting a signal metadata.
  - [SignalListOutput](#signallistoutput): A pydantic model representing a listed signal output. Obtained from requesting signals metadata.
- `time_window` _TimeWindow_ - The time window for which data should be retrieved.
  

**Returns**:

- `LazyFrame` - A polars LazyFrame containing the data.
  

**Raises**:

- `NoSignalsRequestedError` - Raised when no signals are requested.
- `InvalidTimeWindow` - Raised when the start date is after the end date.
  

**Example**:

```python
from datetime import datetime

from nortech import Nortech
from nortech.core.values.signal import SignalInput, SignalInputDict
from nortech.datatools.values.windowing import TimeWindow

# Initialize the Nortech client
nortech = Nortech()

# Define signals to download
signal1: SignalInputDict = {
    "workspace": "workspace1",
    "asset": "asset1",
    "division": "division1",
    "unit": "unit1",
    "signal": "signal1",
}
signal2 = 789  # Signal ID
signal3 = SignalInput(workspace="workspace2", asset="asset2", division="division2", unit="unit2", signal="signal2")

fetched_signals = nortech.metadata.signal.list(  # Fetched signals
    {"workspace": "workspace3", "asset": "asset3", "division": "division3", "unit": "unit3"}
).data

# Define the time window for data download
my_time_window = TimeWindow(start=datetime(2023, 1, 1), end=datetime(2023, 1, 31))

# Call the get_df function with manually defined signals or fetched signals
df = nortech.datatools.polars.get_lazy_df(
    signals=[signal1, signal2, signal3] + fetched_signals,
    time_window=my_time_window,
)

print(df.columns)
# [
#     "timestamp",
#     "workspace_1/asset_1/division_1/unit_1/signal_1",
#     "workspace_1/asset_1/division_1/unit_1/signal_2",
#     "workspace_2/asset_2/division_2/unit_2/signal_3",
#     "workspace_3/asset_3/division_3/unit_3/signal_4",
#     "workspace_3/asset_3/division_3/unit_3/signal_5",
# ]

```

#### get\_df

```python
def get_df(signals: Sequence[int | SignalInput | SignalInputDict | SignalOutput
                             | SignalListOutput],
           time_window: TimeWindow) -> PolarsDataFrame
```

Retrieve a polars DataFrame for the specified signals within the given time window. If experimental features are enabled, live data will also be retrieved.

**Arguments**:

- `signals` _Sequence[int | SignalInput | SignalInputDict | SignalOutput | SignalListOutput]_ - A list of signals to download, which can be of the following types:
  - *int*: The signal "ID".
  - [SignalInputDict](#signalinputdict): A dictionary representation of a signal input.
  - [SignalInput](#signalinput): A pydantic model representing a signal input.
  - [SignalOutput](#signaloutput): A pydantic model representing a signal output. Obtained from requesting a signal metadata.
  - [SignalListOutput](#signallistoutput): A pydantic model representing a listed signal output. Obtained from requesting signals metadata.
- `time_window` _TimeWindow_ - The time window for which data should be retrieved.
  

**Returns**:

- `DataFrame` - A polars DataFrame containing the data.
  

**Raises**:

- `NoSignalsRequestedError` - Raised when no signals are requested.
- `InvalidTimeWindow` - Raised when the start date is after the end date.
  

**Example**:

```python
from datetime import datetime

from nortech import Nortech
from nortech.core.values.signal import SignalInput, SignalInputDict
from nortech.datatools.values.windowing import TimeWindow

# Initialize the Nortech client
nortech = Nortech()

# Define signals to download
signal1: SignalInputDict = {
    "workspace": "workspace1",
    "asset": "asset1",
    "division": "division1",
    "unit": "unit1",
    "signal": "signal1",
}
signal2 = 789  # Signal ID
signal3 = SignalInput(workspace="workspace2", asset="asset2", division="division2", unit="unit2", signal="signal2")

fetched_signals = nortech.metadata.signal.list(  # Fetched signals
    {"workspace": "workspace3", "asset": "asset3", "division": "division3", "unit": "unit3"}
).data

# Define the time window for data download
my_time_window = TimeWindow(start=datetime(2023, 1, 1), end=datetime(2023, 1, 31))

# Call the get_df function with manually defined signals or fetched signals
df = nortech.datatools.polars.get_df(
    signals=[signal1, signal2, signal3] + fetched_signals,
    time_window=my_time_window,
)

print(df.columns)
# [
#     "timestamp",
#     "workspace_1/asset_1/division_1/unit_1/signal_1",
#     "workspace_1/asset_1/division_1/unit_1/signal_2",
#     "workspace_2/asset_2/division_2/unit_2/signal_3",
#     "workspace_3/asset_3/division_3/unit_3/signal_4",
#     "workspace_3/asset_3/division_3/unit_3/signal_5",
# ]

```



## derivers

### Derivers

Client for interacting with the Nortech Derivers API.

**Attributes**:

- `nortech_api` _NortechAPI_ - The Nortech API client.

#### deploy\_deriver

```python
def deploy_deriver(deriver: Deriver,
                   workspace: str | None = None,
                   dry_run: bool = True) -> DeriverDiffs
```

Deploy a deriver to a workspace.

**Arguments**:

- `deriver` _Deriver_ - The deriver to deploy.
- `workspace` _str, optional_ - The workspace to deploy to. Defaults to None.
- `dry_run` _bool, optional_ - Whether to perform a dry run. Defaults to True.
  

**Returns**:

- `DeriverDiffs` - The deriver diffs.
  

**Example**:

```python
from datetime import datetime

from pydantic import Field

from nortech import Nortech
from nortech.derivers import (
    Deriver,
    DeriverInput,
    DeriverOutput,
    physical_units,
)


def create_test_schema():
    import bytewax.operators as op
    from bytewax.dataflow import Stream
    from pydantic import BaseModel

    from nortech.derivers import (
        DeriverInputSchema,
        DeriverOutputSchema,
        DeriverSchema,
        InputField,
        OutputField,
        physical_units,
    )

    class Input(DeriverInputSchema):
        input_signal: float | None = InputField(
            description="Input signal description",
            physical_quantity=physical_units.temperature,
        )

    class Output(DeriverOutputSchema):
        output_signal: float | None = OutputField(
            description="Output signal description",
            physical_quantity=physical_units.temperature,
            create_deriver_schema=create_test_schema,
        )

    class Configurations(BaseModel):
        configuration_value: float = Field(
            description="Configuration value description",
        )

    def transform_stream(
        stream: Stream[Input],
        config: Configurations,
    ) -> Stream[Output]:
        output_stream = op.map(
            step_id="map_output",
            up=stream,
            mapper=lambda input_message: Output(
                timestamp=input_message.timestamp,
                output_signal=input_message.input_signal * config.configuration_value
                if input_message.input_signal is not None
                else None,
            ),
        )

        return output_stream

    return DeriverSchema(
        name="Test Schema",
        description="Test Schema description",
        inputs=Input,
        outputs=Output,
        configurations=Configurations,
        transform_stream=transform_stream,
    )


deriver_schema = create_test_schema()

inputs = {
    deriver_schema.inputs.input_signal: DeriverInput(
        workspace="Workspace",
        asset="Asset",
        division="Division",
        unit="Unit",
        signal="Signal",
        physicalUnit=physical_units.celsius,
    )
}

outputs = {
    deriver_schema.outputs.output_signal: DeriverOutput(
        workspace="Workspace",
        asset="Asset",
        division="Division",
        unit="Unit",
        signal="Signal",
        physicalUnit=physical_units.celsius,
    )
}

configurations = deriver_schema.configurations(
    configuration_value=2.0,
)

deriver = Deriver(
    name="Test Deriver",
    description="Test Deriver description",
    inputs=inputs,
    outputs=outputs,
    configurations=configurations,
    start_at=datetime(2022, 1, 1, 0, 0, 0),
    create_deriver_schema=create_test_schema,
)

nortech = Nortech()

diffs = nortech.derivers.deploy_deriver(deriver)

print(diffs)
# DeriverDiffs(
#     deriver_schemas={
#         "Test Schema": SchemaDiff(
#             old=Schema(
#                 id=1,
#                 hash="hash",
#                 history_id=1,
#                 created_at=datetime(2022, 1, 1, 0, 0, 0),
#                 updated_at=datetime(2022, 1, 1, 0, 0, 0),
#             ),
#             new=Schema(
#                 id=1,
#                 hash="hash",
#                 history_id=1,
#                 created_at=datetime(2022, 1, 1, 0, 0, 0),
#                 updated_at=datetime(2022, 1, 1, 0, 0, 0),
#             ),
#         )
#     },
#     derivers={
#         "Test Deriver": SchemaDiff(
#             old=Schema(
#                 id=1,
#                 hash="hash",
#                 history_id=1,
#                 created_at=datetime(2022, 1, 1, 0, 0, 0),
#                 updated_at=datetime(2022, 1, 1, 0, 0, 0),
#             ),
#             new=Schema(
#                 id=1,
#                 hash="hash",
#                 history_id=1,
#                 created_at=datetime(2022, 1, 1, 0, 0, 0),
#                 updated_at=datetime(2022, 1, 1, 0, 0, 0),
#             ),
#         )
#     },
# )
```

#### visualize\_deriver\_schema

```python
def visualize_deriver_schema(
        create_deriver_schema: Callable[[], DeriverSchema]) -> None
```

Visualize a deriver schema as a mermaid diagram rendered as markdown in all frontends.

By default all representations will be computed and sent to the frontends.
Frontends can decide which representation is used and how.

In terminal IPython this will be similar to using :func:`print`, for use in richer
frontends see Jupyter notebook examples with rich display logic.

**Arguments**:

- `create_deriver_schema` _Callable[[], DeriverSchema]_ - A function that creates a deriver schema.
  

**Example**:

```python
from nortech import Nortech

nortech = Nortech()

# Define a function that creates a Deriver Schema
def create_test_schema():
    ...
    return DeriverSchema(...)

# Visualize the schema
nortech.derivers.visualize_deriver_schema(create_test_schema)
```

#### visualize\_deriver

```python
def visualize_deriver(deriver: Deriver) -> None
```

Visualize a deriver as a mermaid diagram rendered as markdown in all frontends.

By default all representations will be computed and sent to the frontends.
Frontends can decide which representation is used and how.

In terminal IPython this will be similar to using :func:`print`, for use in richer
frontends see Jupyter notebook examples with rich display logic.

**Arguments**:

- `deriver` _Deriver_ - The deriver to visualize.
  

**Example**:

```python
from nortech import Nortech

nortech = Nortech()

# Create Deriver
deriver = ...

# Visualize the deriver
nortech.derivers.visualize_deriver(deriver)
```

#### run\_deriver\_locally

```python
def run_deriver_locally(df: DataFrame,
                        deriver: Deriver[InputType, OutputType,
                                         ConfigurationType, DeriverInputType,
                                         DeriverOutputType],
                        batch_size: int = 10000) -> DataFrame
```

Run a deriver locally on a DataFrame.

**Arguments**:

- `df` _DataFrame_ - The input DataFrame.
- `deriver` _Deriver_ - The deriver to run.
- `batch_size` _int, optional_ - The batch size for processing. Defaults to 10000.
  

**Returns**:

- `DataFrame` - The processed DataFrame with derived signals.
  

**Example**:

```python
from datetime import timezone

import pandas as pd

from nortech import Nortech

nortech = Nortech()

# Create Deriver
deriver = ...

# Create input DataFrame or use nortech.datatools to get data
df = pd.DataFrame(
    {
        "timestamp": pd.date_range(start="2023-01-01", periods=100, freq="s", tz=timezone.utc),
        "input_signal": [float(i) for i in range(100)],
    }
).set_index("timestamp")

# Run the deriver locally
result_df = nortech.derivers.run_deriver_locally(df, deriver, batch_size=5000)

print(result_df)
#                            output_signal
# timestamp
# 2023-01-01 00:00:00+00:00            0.0
# 2023-01-01 00:00:01+00:00            2.0
# 2023-01-01 00:00:02+00:00            4.0
# 2023-01-01 00:00:03+00:00            6.0
# 2023-01-01 00:00:04+00:00            8.0
# ...                                  ...
# 2023-01-01 00:01:35+00:00          190.0
# 2023-01-01 00:01:36+00:00          192.0
# 2023-01-01 00:01:37+00:00          194.0
# 2023-01-01 00:01:38+00:00          196.0
# 2023-01-01 00:01:39+00:00          198.0
```



## metadata.values.time\_window

### TimeWindow

Time window model.

**Attributes**:

- `start` _datetime_ - Start time.
- `end` _datetime_ - End time.



## metadata.values.pagination

### PaginationOptions

Pagination options for list endpoints.

**Attributes**:

- `size` _int | None, default=100, le=100_ - The number of items to return.
- `sort_by` _str | None_ - The field to sort by.
- `sort_order` _"asc" | "desc", default="asc"_ - The order to sort by.
- `next_token` _str | None_ - The next token to use for pagination.

### PaginatedResponse

Paginated response from list endpoints.

**Attributes**:

- `size` _int_ - The number of items returned.
- `data` _list[obj]_ - The list of items.
- `next.token` _str | None_ - The next token to use for pagination. If None, there are no more pages.



## metadata.values.workspace

Module containing all schemas related with Workspaces.

### WorkspaceInputDict

Dictionary representation of Workspace input data.

**Attributes**:

- `workspace` _str_ - The name of the Workspace.

### WorkspaceInput

Pydantic model for Workspace input data.

**Attributes**:

- `workspace` _str_ - The name of the Workspace.

### WorkspaceListOutput

Output model for workspace list entries.

**Attributes**:

- `id` _int_ - Id of the Workspace.
- `name` _str_ - Name of the Workspace.
- `description` _str_ - A description of the Workspace.

### WorkspaceOutput

Detailed output model for a single workspace.

**Attributes**:

- `id` _int_ - Id of the Workspace.
- `name` _str_ - Name of the Workspace.
- `description` _str_ - A description of the Workspace.
- `created_at` _datetime_ - Timestamp of when the Workspace was created.
- `updated_at` _datetime_ - Timestamp of when the Workspace was last updated.



## metadata.values.asset

Module containing all schemas related with Assets.

### AssetInputDict

Dictionary representation of Asset input data.

**Attributes**:

- `workspace` _str_ - The name of the Workspace.
- `asset` _str_ - The name of the Asset.

### AssetInput

Pydantic model for asset input data.

**Attributes**:

- `workspace` _str_ - The name of the Workspace.
- `asset` _str_ - The name of the Asset.

### AssetListOutput

Output model for asset list entries.

**Attributes**:

- `id` _int_ - Id of the Asset.
- `name` _str_ - Name of the Asset.
- `description` _str_ - A description of the Asset.

### AssetOutput

Detailed output model for a single asset.

**Attributes**:

- `id` _int_ - Id of the Asset.
- `name` _str_ - Name of the Asset.
- `description` _str_ - A description of the Asset.
- `created_at` _datetime_ - Timestamp of when the Asset was created.
- `updated_at` _datetime_ - Timestamp of when the Asset was last updated.
- `workspace` - Metadata about the Workspace containing the Asset.
  - id (int): Id of the Workspace.
  - name (str): Name of the Workspace.



## metadata.values.division

Module containing all schemas related with Divisions.

### DivisionInputDict

Dictionary representation of Division input data.

**Attributes**:

- `workspace` _str_ - The name of the Workspace.
- `asset` _str_ - The name of the Asset.
- `division` _str_ - The name of the Division.

### DivisionInput

Pydantic model for Division input data.

**Attributes**:

- `workspace` _str_ - The name of the Workspace.
- `asset` _str_ - The name of the Asset.
- `division` _str_ - The name of the Division.

### DivisionListOutput

Output model for division list entries.

**Attributes**:

- `id` _int_ - Id of the Division.
- `name` _str_ - Name of the Division.
- `description` _str_ - A description of the division.

### DivisionOutput

Detailed output model for a single division.

**Attributes**:

- `id` _int_ - Id of the Division.
- `name` _str_ - Name of the Division.
- `description` _str_ - A description of the division.
- `created_at` _datetime_ - Timestamp of when the Division was created.
- `updated_at` _datetime_ - Timestamp of when the Division was last updated.
- `workspace` - Metadata about the Workspace containing the Division.
  - id (int): Id of the Workspace.
  - name (str): Name of the Workspace.
- `asset` - Metadata about the Asset containing the Division.
  - id (int): Id of the Asset.
  - name (str): Name of the Asset.



## metadata.values.unit

Module containing all schemas related with Units.

### UnitInputDict

Dictionary representation of Unit input data.

**Attributes**:

- `workspace` _str_ - The name of the Workspace.
- `asset` _str_ - The name of the Asset.
- `division` _str_ - The name of the Division.
- `unit` _str_ - The name of the Unit.

### UnitInput

Pydantic model for Unit input data.

**Attributes**:

- `workspace` _str_ - The name of the Workspace.
- `asset` _str_ - The name of the Asset.
- `division` _str_ - The name of the Division.
- `unit` _str_ - The name of the Unit.

### UnitListOutput

Output model for unit list entries.

**Attributes**:

- `id` _int_ - Id of the Unit.
- `name` _str_ - Name of the Unit.

### UnitDivision

Output model for unit division entries.

**Attributes**:

- `id` _int_ - Id of the Division.
- `name` _str_ - Name of the Division.

### UnitOutput

Detailed output model for a single unit.

**Attributes**:

- `id` _int_ - Id of the Unit.
- `name` _str_ - Name of the Unit.
- `created_at` _datetime_ - Timestamp of when the Unit was created.
- `updated_at` _datetime_ - Timestamp of when the Unit was last updated.
- `workspace` - Metadata about the Workspace containing the Unit.
  - id (int): Id of the Workspace.
  - name (str): Name of the Workspace.
- `asset` - Metadata about the Asset containing the Unit.
  - id (int): Id of the Asset.
  - name (str): Name of the Asset.
- `division` - Metadata about the Division containing the Unit.
  - id (int): Id of the Division.
  - name (str): Name of the Division.



## metadata.values.device

Module containing all schemas related with Devices.

### DeviceInputDict

Dictionary representation of Device input data.

**Attributes**:

- `workspace` _str_ - The name of the Workspace.
- `asset` _str_ - The name of the Asset.
- `division` _str_ - The name of the Division.
- `device` _str_ - The name of the Device.

### DeviceInput

Pydantic model for Device input data.

**Attributes**:

- `workspace` _str_ - The name of the Workspace.
- `asset` _str_ - The name of the Asset.
- `division` _str_ - The name of the Division.
- `device` _str_ - The name of the Device.

### DeviceListOutput

Output model for device list entries.

**Attributes**:

- `id` _int_ - Id of the Device.
- `name` _str_ - Name of the Device.
- `type` _str_ - The type of the Device.
- `onboarded` _bool_ - Whether the Device is onboarded.

### DeviceOutput

Detailed output model for a single device.

**Attributes**:

- `id` _int_ - Id of the Device.
- `name` _str_ - Name of the Device.
- `type` _str_ - The type of the Device.
- `onboarded` _bool_ - Whether the Device is onboarded.
- `created_at` _datetime_ - Timestamp of when the Device was created.
- `updated_at` _datetime_ - Timestamp of when the Device was last updated.
- `workspace` - Metadata about the Workspace containing the Device.
  - id (int): Id of the Workspace.
  - name (str): Name of the Workspace.
- `asset` - Metadata about the Asset containing the Device.
  - id (int): Id of the Asset.
  - name (str): Name of the Asset.
- `division` - Metadata about the Division containing the Device.
  - id (int): Id of the Division.
  - name (str): Name of the Division.



## metadata.values.signal

Module containing all schemas related with Signals.

### SignalInputDict

Dictionary representation of Signal input data.

**Attributes**:

- `workspace` _str_ - The name of the Workspace.
- `asset` _str_ - The name of the Asset.
- `division` _str_ - The name of the Division.
- `unit` _str_ - The name of the Unit.
- `signal` _str_ - The name of the Signal.

### SignalInput

Pydantic model for Signal input data.

**Attributes**:

- `workspace` _str_ - The name of the Workspace.
- `asset` _str_ - The name of the Asset.
- `division` _str_ - The name of the Division.
- `unit` _str_ - The name of the Unit.
- `signal` _str_ - The name of the Signal.

### SignalDeviceInputDict

Dictionary representation of SignalDevice input data.

**Attributes**:

- `workspace` _str_ - The name of the Workspace.
- `asset` _str_ - The name of the Asset.
- `division` _str_ - The name of the Division.
- `device` _str_ - The name of the Device.
- `signal` _str_ - The name of the Signal.

### SignalDeviceInput

Pydantic model for SignalDevice input data.

**Attributes**:

- `workspace` _str_ - The name of the Workspace.
- `asset` _str_ - The name of the Asset.
- `division` _str_ - The name of the Division.
- `device` _str_ - The name of the Device.
- `signal` _str_ - The name of the Signal.

### SignalListOutput

Output model for signal list entries.

**Attributes**:

- `id` _int_ - Id of the Signal.
- `name` _str_ - Name of the Signal.
- `physical_unit` _str_ - The physical unit of the Signal.
- `data_type` _Literal["float", "boolean", "string", "json"]_ - The data type of the Signal.
- `description` _str_ - A description of the Signal.
- `long_description` _str_ - A long description of the Signal.

### SignalOutput

Detailed output model for a single signal.

**Attributes**:

- `id` _int_ - Id of the Signal.
- `name` _str_ - Name of the Signal.
- `created_at` _datetime_ - Timestamp of when the Signal was created.
- `updated_at` _datetime_ - Timestamp of when the Signal was last updated.
- `workspace` - Metadata about the Workspace containing the Signal.
  - id (int): Id of the Workspace.
  - name (str): Name of the Workspace.
- `asset` - Metadata about the Asset containing the Signal.
  - id (int): Id of the Asset.
  - name (str): Name of the Asset.
- `division` - Metadata about the Division containing the Signal.
  - id (int): Id of the Division.
  - name (str): Name of the Division.
- `unit` - Metadata about the Unit containing the Signal.
  - id (int): Id of the Unit.
  - name (str): Name of the Unit.
- `device` - Metadata about the Device containing the Signal.
  - id (int): Id of the Device.
  - name (str): Name of the Device.



## derivers.values.schema

### DataTypeEnum

Enumeration of supported data types.

**Attributes**:

- `float` - Floating point number type
- `boolean` - Boolean type
- `string` - String type
- `json` - JSON type

### DeriverSchemaConfiguration

Pydantic model for deriver schema configuration data.

**Attributes**:

- `name` _str_ - The name of the configuration parameter.
- `description` _str_ - A description of the configuration parameter.
- `data_type` _DataTypeEnum_ - The data type of the configuration parameter.

### DeriverSchemaOutput

Pydantic model for deriver schema output data.

**Attributes**:

- `name` _str_ - The name of the output.
- `description` _str_ - A description of the output.
- `data_type` _DataTypeEnum_ - The data type of the output.
- `physical_quantity` _PhysicalQuantity | None_ - The physical quantity of the output, if applicable.

### SuggestedInput

Pydantic model for suggested input data.

**Attributes**:

- `name` _str_ - The name of the suggested input.
- `description` _str_ - A description of the suggested input.
- `data_type` _DataTypeEnum_ - The data type of the suggested input.
- `physical_quantity` _PhysicalQuantity | None_ - The physical quantity of the suggested input, if applicable.
- `create_deriver_schema` _Callable[[], DeriverSchema]_ - Function that creates the deriver schema for this input.

#### InputField

```python
def InputField(description: str,
               physical_quantity: PhysicalQuantity | None,
               suggested_inputs: list[Any] | None = None)
```

Create an input field with metadata.

**Arguments**:

- `description` _str_ - Description of the input field.
- `physical_quantity` _PhysicalQuantity | None_ - Physical quantity of the input field.
- `suggested_inputs` _list[Any] | None, optional_ - List of suggested inputs. Defaults to None.
  

**Returns**:

- `Field` - A pydantic Field with the specified metadata.

### DeriverInputSchema

Pydantic model for deriver schema input data.

**Attributes**:

- `timestamp` _datetime_ - The timestamp for the input.

### DeriverOutputSchema

Pydantic model for deriver schema output data.

**Attributes**:

- `timestamp` _datetime_ - The timestamp for the output.

### DeriverSchema

Pydantic model for a deriver schema.

**Attributes**:

- `name` _str_ - The name of the deriver.
- `description` _str_ - A description of the deriver.
- `inputs` _Type[InputType]_ - The input schema type.
- `outputs` _Type[OutputType]_ - The output schema type.
- `configurations` _Type[ConfigurationType]_ - The configuration schema type.
- `transform_stream` _Callable_ - Function that transforms input stream to output stream given a configuration.

#### OutputField

```python
def OutputField(description: str, physical_quantity: PhysicalQuantity | None,
                create_deriver_schema: Callable[[], DeriverSchema])
```

Create an output field with metadata.

**Arguments**:

- `description` _str_ - Description of the output field.
- `physical_quantity` _PhysicalQuantity | None_ - Physical quantity of the output field.
- `create_deriver_schema` _Callable[[], DeriverSchema]_ - Function that creates the deriver schema.
  

**Returns**:

- `Field` - A pydantic Field with the specified metadata.

### DeriverSchemaOutputWithDAG

Pydantic model for deriver schema output with DAG information.

**Attributes**:

- `name` _str_ - The name of the output.
- `description` _str_ - A description of the output.
- `data_type` _DataTypeEnum_ - The data type of the output.
- `physical_quantity` _PhysicalQuantity | None_ - The physical quantity of the output, if applicable.
- `deriver_schema_dag` _DeriverSchemaDAG_ - The DAG associated with this output.

### DeriverSchemaInput

Pydantic model for deriver schema input with suggested inputs.

**Attributes**:

- `name` _str_ - The name of the input.
- `description` _str_ - A description of the input.
- `data_type` _DataTypeEnum_ - The data type of the input.
- `physical_quantity` _PhysicalQuantity | None_ - The physical quantity of the input.
- `suggested_inputs_from_other_derivers` _list[DeriverSchemaOutputWithDAG]_ - List of suggested inputs.

### DeriverSchemaDAG

Pydantic model for a deriver schema DAG.

**Attributes**:

- `name` _str_ - The name of the deriver schema.
- `description` _str_ - A description of the deriver schema.
- `inputs` _list[DeriverSchemaInput]_ - List of inputs in the deriver schema.
- `outputs` _list[DeriverSchemaOutput]_ - List of outputs in the deriver schema.
- `configurations` _list[DeriverSchemaConfiguration]_ - List of configurations in the deriver schema.
- `script` _str_ - The script associated with this deriver schema.



## derivers.values.instance

### DeriverInput

Pydantic model for deriver input data.

**Attributes**:

- `workspace` _str_ - The name of the Workspace.
- `asset` _str_ - The name of the Asset.
- `division` _str_ - The name of the Division.
- `unit` _str_ - The name of the Unit.
- `signal` _str_ - The name of the Signal.
- `physical_unit` _PhysicalUnit_ - The physical unit of the input signal.

### DeriverOutput

Pydantic model for deriver output data.

**Attributes**:

- `workspace` _str_ - The name of the Workspace.
- `asset` _str_ - The name of the Asset.
- `division` _str_ - The name of the Division.
- `unit` _str_ - The name of the Unit.
- `signal` _str_ - The name of the Signal.
- `physical_unit` _PhysicalUnit_ - The physical unit of the output signal.

### Deriver

Pydantic model for a deriver.

**Attributes**:

- `name` _str_ - The name of the deriver.
- `description` _str_ - A description of the deriver.
- `inputs` _dict[Any, DeriverInputType]_ - Dictionary mapping deriver schema inputs to their input signals.
- `outputs` _dict[Any, DeriverOutputType]_ - Dictionary mapping deriver schema outputs to their output signals.
- `configurations` _ConfigurationType_ - Configuration parameters for the deriver.
- `start_at` _datetime_ - Start time for the deriver.
- `create_deriver_schema` _Callable[[], DeriverSchema[InputType, OutputType, ConfigurationType]]_ - Function that creates the deriver schema.



## derivers.values.physical\_units\_schema

### PhysicalQuantity

Pydantic model for physical quantity data.

**Attributes**:

- `name` _str_ - The name of the physical quantity.
- `description` _str_ - A description of the physical quantity.
- `si_unit` _str_ - The SI unit for this physical quantity.
- `si_unit_symbol` _str_ - The symbol for the SI unit.

### PhysicalUnit

Pydantic model for physical unit data.

**Attributes**:

- `name` _str_ - The name of the physical unit.
- `description` _str_ - A description of the physical unit.
- `symbol` _str_ - The symbol for this physical unit.
- `physical_quantity` _PhysicalQuantity_ - The physical quantity this unit measures.

