from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.history_service import get_histories

router = APIRouter(prefix="/history", tags=["History"])


@router.get("/{lost_number}")
def list_histories(lost_number: int, db: Session = Depends(get_db)):
    return get_histories(db, lost_number)
