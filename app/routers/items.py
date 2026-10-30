from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import ItemCreate, ItemResponse
from app.services.item_service import create_item, get_items, search_items

router = APIRouter(prefix="/items", tags=["Items"])


# Register a new lost item
@router.post("/", response_model=ItemResponse)
def register_item(item_data: ItemCreate, db: Session = Depends(get_db)):
    return create_item(db, item_data)


# Get all lost items or search by conditions
@router.get("/", response_model=list[ItemResponse])
def list_items(
    lost_number: int | None = None,
    item_name: str | None = None,
    status: str | None = None,
    db: Session = Depends(get_db),
):
    return search_items(db, lost_number=lost_number, item_name=item_name, status=status)
