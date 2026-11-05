from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.history_service import get_histories, get_all_histories

router = APIRouter(prefix="/history", tags=["History"])


# Get histories by lost number
@router.get("/{lost_number}")
def list_histories(lost_number: int, db: Session = Depends(get_db)):
    return get_histories(db, lost_number)


# Get all item histories
@router.get("/")
def list_all_histories(db: Session = Depends(get_db)):
    return get_all_histories(db)
