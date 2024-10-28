from pydantic import BaseModel, ConfigDict, Field


class PhysicalQuantity(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    name: str
    description: str
    si_unit: str = Field(alias="SIUnit")
    si_unit_symbol: str = Field(alias="SIUnitSymbol")


class PhysicalUnit(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    name: str
    description: str
    symbol: str
    physical_quantity: PhysicalQuantity = Field(alias="physicalQuantity")
