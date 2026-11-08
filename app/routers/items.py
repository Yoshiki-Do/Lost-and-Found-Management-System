from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from datetime import date
from app.database import get_db
from app.schemas import ItemCreate, ItemResponse
from app.services.item_service import (
    create_item,
    get_item_by_number,
    get_items,
    return_item,
    dispose_item,
    dispose_items_by_month,
    search_items,
)
import csv
import io

router = APIRouter(prefix="/items", tags=["Items"])


# Register a new lost item
@router.post("/", response_model=ItemResponse)
def register_item(item_data: ItemCreate, db: Session = Depends(get_db)):
    return create_item(db, item_data)


# Export items as CSV
@router.get("/export/csv")
def export_items_csv(
    lost_number: int | None = None,
    item_name: str | None = None,
    status: str | None = None,
    found_location: str | None = None,
    storage_month: str | None = None,
    found_date_from: date | None = None,
    found_date_to: date | None = None,
    db: Session = Depends(get_db),
):
    items = search_items(
        db,
        lost_number=lost_number,
        item_name=item_name,
        found_location=found_location,
        status=status,
        storage_month=storage_month,
        found_date_from=found_date_from,
        found_date_to=found_date_to,
    )
    output = io.StringIO(newline="")
    writer = csv.writer(output)

    # CSV header
    writer.writerow(
        [
            "Lost Number",
            "Item Name",
            "Description",
            "Found Location",
            "Found Date",
            "Storage Month",
            "Storage Box",
            "Status",
        ]
    )

    # CSV data
    for item in items:
        writer.writerow(
            [
                item.lost_number,
                item.item_name,
                item.description,
                item.found_location,
                item.found_at,
                item.storage_month,
                item.storage_box,
                item.status,
            ]
        )

    csv_content = "\ufeff" + output.getvalue()

    return StreamingResponse(
        iter([csv_content]),
        media_type="text/csv; charset=utf-8",
        headers={
            "Content-Disposition": 'attachment; filename="lost_and_found_items.csv"'
        },
    )


# Get all lost items or search by conditions
@router.get("/", response_model=list[ItemResponse])
def list_items(
    lost_number: int | None = None,
    item_name: str | None = None,
    found_location: str | None = None,
    status: str | None = None,
    storage_month: str | None = None,
    found_date_from: date | None = None,
    found_date_to: date | None = None,
    db: Session = Depends(get_db),
):
    return search_items(
        db,
        lost_number=lost_number,
        item_name=item_name,
        found_location=found_location,
        status=status,
        storage_month=storage_month,
        found_date_from=found_date_from,
        found_date_to=found_date_to,
    )


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


# Bulk dispose items by storage month
@router.patch("/bulk-dispose/{storage_month}", response_model=list[ItemResponse])
def bulk_dispose_items(storage_month: str, db: Session = Depends(get_db)):
    try:
        return dispose_items_by_month(db, storage_month)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))
