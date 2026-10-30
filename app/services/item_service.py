from sqlalchemy.orm import Session
from app.models import Item
from app.schemas import ItemCreate
from app.services.number_service import get_next_lost_number


def create_item(db: Session, item_data: ItemCreate) -> Item:
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


def get_item_by_number(db: Session, lost_number: int) -> Item | None:
    return db.query(Item).filter(Item.lost_number == lost_number).first()


def get_items(db: Session) -> list[Item]:
    return db.query(Item).order_by(Item.lost_number.desc()).all()


def search_items(
    db: Session,
    lost_number: int | None = None,
    item_name: str | None = None,
    status: str | None = None,
) -> list[Item]:
    query = db.query(Item)

    if lost_number is not None:
        query = query.filter(Item.lost_number == lost_number)

    if item_name:
        query = query.filter(Item.item_name.ilike(f"%{item_name}%"))

    if status:
        query = query.filter(Item.status == status)

    return query.order_by(Item.lost_number.desc()).all()
