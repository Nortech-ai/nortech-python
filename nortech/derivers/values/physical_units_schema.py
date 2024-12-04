from pydantic import BaseModel, ConfigDict, Field


class PhysicalQuantity(BaseModel):
    """Pydantic model for physical quantity data.

    Attributes:
        name (str): The name of the physical quantity.
        description (str): A description of the physical quantity.
        si_unit (str): The SI unit for this physical quantity.
        si_unit_symbol (str): The symbol for the SI unit.

    """

    model_config = ConfigDict(populate_by_name=True)

    name: str
    description: str
    si_unit: str = Field(alias="SIUnit")
    si_unit_symbol: str = Field(alias="SIUnitSymbol")


class PhysicalUnit(BaseModel):
    """Pydantic model for physical unit data.

    Attributes:
        name (str): The name of the physical unit.
        description (str): A description of the physical unit.
        symbol (str): The symbol for this physical unit.
        physical_quantity (PhysicalQuantity): The physical quantity this unit measures.

    """

    model_config = ConfigDict(populate_by_name=True)

    name: str
    description: str
    symbol: str
    physical_quantity: PhysicalQuantity = Field(alias="physicalQuantity")
