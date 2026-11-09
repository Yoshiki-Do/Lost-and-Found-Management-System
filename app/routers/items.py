from datetime import date
from io import BytesIO

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import ItemCreate, ItemUpdate, ItemResponse
from app.services.item_service import (
    create_item,
    get_item_by_number,
    return_item,
    dispose_item,
    dispose_items_by_month,
    search_items,
    update_item,
)

router = APIRouter(prefix="/items", tags=["Items"])


# Register a new lost item
@router.post("/", response_model=ItemResponse)
def register_item(item_data: ItemCreate, db: Session = Depends(get_db)):
    return create_item(db, item_data)


# Update an existing lost item
@router.put("/{lost_number}", response_model=ItemResponse)
def update_lost_item(
    lost_number: int, item_data: ItemUpdate, db: Session = Depends(get_db)
):
    item = update_item(db, lost_number, item_data)

    if item is None:
        raise HTTPException(
            status_code=404, detail="Item not found or item cannot be updated"
        )

    return item


# Export items as Excel
@router.get("/export/excel")
def export_items_excel(
    lost_number: int | None = None,
    item_name: str | None = None,
    found_location: str | None = None,
    status: str | None = None,
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

    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "Items"

    headers = [
        "Lost Number",
        "Item Name",
        "Description",
        "Found Location",
        "Found Date",
        "Storage Month",
        "Storage Box",
        "Status",
    ]

    worksheet.append(headers)

    # Header style
    for cell in worksheet[1]:
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill(fill_type="solid", fgColor="1F4E78")
        cell.alignment = Alignment(
            horizontal="center", vertical="center", wrap_text=True
        )

    # Add item data
    for item in items:
        worksheet.append(
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

    # Adjust column widths
    max_widths = [14, 30, 50, 30, 15, 16, 20, 16]

    for column_index, max_width in enumerate(max_widths, start=1):
        column_letter = get_column_letter(column_index)

        longest_length = max(
            len(str(cell.value or "")) for cell in worksheet[column_letter]
        )

        worksheet.column_dimensions[column_letter].width = min(
            max(longest_length + 2, 12), max_width
        )

    # Data cell formatting
    for row in worksheet.iter_rows(min_row=2):
        status_value = row[7].value

        for cell in row:
            cell.alignment = Alignment(vertical="top", wrap_text=True)

        # Found Date format
        row[4].number_format = "yyyy-mm-dd"

        # Status colors
        if status_value == "DISPOSED":
            for cell in row:
                cell.fill = PatternFill(fill_type="solid", fgColor="E0E0E0")
        elif status_value == "RETURNED":
            for cell in row:
                cell.font = Font(color="0000FF")

    # Freeze header row
    worksheet.freeze_panes = "A2"

    # Add filter buttons
    worksheet.auto_filter.ref = worksheet.dimensions

    # Create Excel file
    output = BytesIO()
    workbook.save(output)
    output.seek(0)

    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": 'attachment; filename="lost_and_found_items.xlsx"'
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
