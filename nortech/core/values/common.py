from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class MetadataOutput(BaseModel):
    id: int
    name: str


class MetadataTimestamps(MetadataOutput):
    model_config = ConfigDict(populate_by_name=True)

    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
