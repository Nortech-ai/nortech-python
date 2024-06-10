from pydantic import BaseModel, Field


class PhysicalQuantity(BaseModel):
    name: str = Field()
    description: str = Field()
    SIUnit: str = Field()
    SIUnitSymbol: str = Field()


class PhysicalUnit(BaseModel):
    name: str = Field()
    description: str = Field()
    symbol: str = Field()
    physicalQuantity: PhysicalQuantity = Field()
