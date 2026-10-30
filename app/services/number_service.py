from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import Item


def get_next_lost_number(db: Session) -> int:
    """
    Get the next continuous lost number.
    """
    current_max = db.query(func.max(Item.lost_number)).scalar()

    if current_max is None:
        return 1

    return current_max + 1
