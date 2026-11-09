from sqlalchemy.orm import Session
from app.models import Item, ItemHistory
from app.schemas import ItemCreate, ItemUpdate
from app.services.number_service import get_next_lost_number
from app.services.history_service import create_history
from datetime import date, datetime


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

    create_history(
        db,
        lost_number=new_item.lost_number,
        action="REGISTERED",
        description="New item registered",
    )

    return new_item


def get_item_by_number(db: Session, lost_number: int) -> Item | None:
    return db.query(Item).filter(Item.lost_number == lost_number).first()


def update_item(db: Session, lost_number: int, item_data: ItemUpdate) -> Item | None:
    item = get_item_by_number(db, lost_number)

    if item is None or item.status != "REGISTERED":
        return None

    changed_fields = []

    # Check changed fields
    fields = {
        "item_name": "Item Name",
        "description": "Description",
        "found_location": "Found Location",
        "found_at": "Found Date",
        "storage_box": "Storage Box",
    }

    for field, label in fields.items():
        new_value = getattr(item_data, field)

        if getattr(item, field) != new_value:
            setattr(item, field, new_value)
            changed_fields.append(label)

    # Update storage month when found date changes
    if "Found Date" in changed_fields:
        item.storage_month = item.found_at.strftime("%Y-%m")

    # No changes
    if not changed_fields:
        return item

    # Create history record
    history = ItemHistory(
        lost_number=lost_number,
        action="UPDATED",
        description=f"Update fields: {', '.join(changed_fields)}",
    )

    db.add(history)

    # Save item and history together
    db.commit()
    db.refresh(item)

    return item


def get_items(db: Session) -> list[Item]:
    return db.query(Item).order_by(Item.lost_number.desc()).all()


def search_items(
    db: Session,
    lost_number: int | None = None,
    item_name: str | None = None,
    found_location: str | None = None,
    status: str | None = None,
    storage_month: str | None = None,
    found_date_from: date | None = None,
    found_date_to: date | None = None,
) -> list[Item]:
    query = db.query(Item)

    if lost_number is not None:
        query = query.filter(Item.lost_number == lost_number)

    if item_name:
        query = query.filter(Item.item_name.ilike(f"%{item_name}%"))

    if found_location:
        query = query.filter(Item.found_location.ilike(f"%{found_location}%"))

    if status:
        query = query.filter(Item.status == status)

    if storage_month:
        query = query.filter(Item.storage_month == storage_month)

    if found_date_from:
        query = query.filter(Item.found_at >= found_date_from)

    if found_date_to:
        query = query.filter(Item.found_at <= found_date_to)

    return query.order_by(Item.lost_number.desc()).all()


def return_item(db: Session, lost_number: int) -> Item | None:
    item = get_item_by_number(db, lost_number)

    if item is None:
        return None

    if item.status != "REGISTERED":
        return None

    item.status = "RETURNED"
    item.returned_at = datetime.now()

    db.commit()
    db.refresh(item)

    create_history(
        db,
        lost_number=lost_number,
        action="RETURNED",
        description="Item returned to owner",
    )

    return item


def dispose_item(db: Session, lost_number: int) -> Item | None:
    item = get_item_by_number(db, lost_number)

    if item is None:
        return None

    if item.status != "REGISTERED":
        return None

    item.status = "DISPOSED"
    item.disposed_at = datetime.now()

    db.commit()
    db.refresh(item)

    create_history(
        db, lost_number=lost_number, action="DISPOSED", description="Item disposed"
    )

    return item


def dispose_items_by_month(db: Session, storage_month: str) -> list[Item]:
    now = datetime.now()

    try:
        year, month = map(int, storage_month.split("-"))

        if month < 1 or month > 12:
            raise ValueError

        target_month_index = year * 12 + month
        current_month_index = now.year * 12 + now.month

    except ValueError:
        raise ValueError("Invalid storage month format")

    # Prevent disposal of items within latest 3 months
    if target_month_index >= current_month_index - 2:
        raise ValueError(
            "Items from the current month and previous two months cannot be disposed"
        )

    items = (
        db.query(Item)
        .filter(
            Item.storage_month == storage_month,
            Item.status == "REGISTERED",
        )
        .all()
    )

    if not items:
        return []

    for item in items:
        item.status = "DISPOSED"
        item.disposed_at = now

        history = ItemHistory(
            lost_number=item.lost_number,
            action="DISPOSED",
            description=f"Bulk disposal for {storage_month}",
        )

        db.add(history)

    db.commit()

    for item in items:
        db.refresh(item)

    return items
