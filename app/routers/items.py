from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import ItemCreate, ItemResponse
from app.services.item_service import (
    create_item,
    get_item_by_number,
    get_items,
    return_item,
    dispose_item,
    search_items,
)

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


# Get a lost item by a lost number
@router.get("/{lost_number}", response_model=ItemResponse)
def get_item(lost_number: int, db: Session = Depends(get_db)):
    item = get_item_by_number(db, lost_number)

    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return item


# Return a lost item
@router.patch("/{lost_number}/return", response_model=ItemResponse)
def return_lost_item(lost_number: int, db: Session = Depends(get_db)):
    item = return_item(db, lost_number)

    if item is None:
        raise HTTPException(
            status_code=404, detail="Item not found or item cannot be returned"
        )

    return item


# Dispose a lost item
@router.patch("/{lost_number}/dispose", response_model=ItemResponse)
def dispose_lost_item(lost_number: int, db: Session = Depends(get_db)):
    item = dispose_item(db, lost_number)

    if item is None:
        raise HTTPException(
            status_code=404, detail="Item not found or item cannot be disposed"
        )

    return item
