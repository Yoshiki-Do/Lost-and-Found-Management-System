from datetime import date, datetime
from pydantic import BaseModel, ConfigDict

# Data required when registering a new item
class ItemCreate(BaseModel):
    item_name: str
    description: str | None = None
    found_location: str
    found_at: date
    storage_month: str
    storage_box: str


# Data returned when displaying an item
class ItemResponse(BaseModel):
    id: int
    lost_number: int
    item_name: str
    description: str | None
    found_location: str
    found_at: date
    registered_at: datetime
    storage_month: str
    storage_box: str
    status: str
    returned_at: datetime | None
    disposed_at: datetime | None

    model_config = ConfigDict(from_attributes=True)
