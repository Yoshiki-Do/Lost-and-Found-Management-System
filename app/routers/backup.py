from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from app.services.backup_service import create_backup, restore_backup
from pathlib import Path

router = APIRouter(prefix="/backup", tags=["Backup"])


@router.post("/")
def backup_database():
    try:
        backup_path = create_backup()

        return FileResponse(
            path=backup_path,
            filename=backup_path.name,
            media_type="application/octet-stream",
        )

    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Backup failed: {str(error)}")


class RestoreRequest(BaseModel):
    filename: str


@router.get("/list")
def list_backups():
    backup_dir = Path("backups")

    backup_dir.mkdir(parents=True, exist_ok=True)

    backups = sorted(
        [
            file.name
            for file in backup_dir.glob("lost_and_found_*.db")
            if file.is_file()
        ],
        reverse=True,
    )

    return {"backups": backups}


@router.post("/restore")
def restore_database(request: RestoreRequest):
    try:
        restored_path = restore_backup(request.filename)

        return {
            "message": "Database restored successfully",
            "filename": restored_path.name,
        }

    except FileNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error))

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Restore failed: {str(error)}")
