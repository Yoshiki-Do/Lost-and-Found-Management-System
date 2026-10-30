from sqlalchemy.orm import Session
from app.models import Item
from app.schemas import ItemCreate
from app.services.number_service import get_next_lost_number


def create_item(db: Session, item_data: ItemCreate) -> item:
    new_item = Item(
        lost_number=get_next_lost_number(db),
        item_name=item_data.item_name,
        description=item_data.description,
        found_location=item_data.found_location,
        found_at=item_data.found_at,
        storage_month=item_data.storage_month,
        storage_box=item_data.storage_box,
        status="REGISTERED",
    )

    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    
    return new_item
