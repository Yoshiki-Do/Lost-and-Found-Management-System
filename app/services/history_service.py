from sqlalchemy.orm import Session
from app.models import ItemHistory


def create_history(
    db: Session, lost_number: int, action: str, description: str | None = None
) -> ItemHistory:
    history = ItemHistory(
        lost_number=lost_number, action=action, description=description
    )

    db.add(history)
    db.commit()
    db.refresh(history)

    return history


def get_histories(db: Session, lost_number: int) -> list[ItemHistory]:
    return (
        db.query(ItemHistory)
        .filter(ItemHistory.lost_number == lost_number)
        .order_by(ItemHistory.created_at.desc())
        .all()
    )


def get_all_histories(db: Session) -> list[ItemHistory]:
    return db.query(ItemHistory).order_by(ItemHistory.created_at.desc()).all()
