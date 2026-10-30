from datetime import datetime
from pydantic import BaseModel, ConfigDict

# Data required when registering a new item
class ItemCreate(BaseModel):
    item_name: str
    description: str | None = None
    found_location: str
    found_at: datetime
    storage_month: str
    storage_box: str


# Data returned when displaying an item
class ItemResponse(BaseModel):
    id: int
    lost_number: int
    item_name: str
    description: str | None
    found_location: str
    found_at: datetime
    registered_at: datetime
    storage_month: str
    storage_box: str
    status: str
    retention_start_at: datetime | None
    retention_due_at: datetime | None
    returned_at: datetime | None
    disposed_at: datetime | None

    model_config = ConfigDict(from_attributes=True)
