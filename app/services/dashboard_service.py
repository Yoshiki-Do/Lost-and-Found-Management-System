from sqlalchemy.orm import Session
from app.models import Item


def get_dashboard_summary(db: Session) -> dict:
    total_items = db.query(Item).count()

    registered_items = db.query(Item).filter(Item.status == "REGISTERED").count()

    returned_items = db.query(Item).filter(Item.status == "RETURNED").count()

    disposed_items = db.query(Item).filter(Item.status == "DISPOSED").count()

    return {
        "total_items": total_items,
        "registered_items": registered_items,
        "returned_items": returned_items,
        "disposed_items": disposed_items,
    }
