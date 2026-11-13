import sqlite3
from datetime import datetime
from app.database import engine
from app.paths import DATABASE_PATH, BACKUP_DIR


def create_backup():
    # Database file path
    database_path = DATABASE_PATH

    # Create backup directory
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    # Generate backup filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = BACKUP_DIR / f"lost_and_found_{timestamp}.db"

    # Create SQLite backup
    with sqlite3.connect(database_path) as source:
        with sqlite3.connect(backup_path) as destination:
            source.backup(destination)

    return backup_path


def restore_backup(backup_filename: str):
    # Get backup directory
    backup_dir = BACKUP_DIR.resolve()

    # Validate backup filename
    from pathlib import Path

    if Path(backup_filename).name != backup_filename:
        raise ValueError("Invalid backup filename")

    if not backup_filename.startswith(
        "lost_and_found_"
    ) or not backup_filename.endswith(".db"):
        raise ValueError("Invalid backup file")

    backup_path = (backup_dir / backup_filename).resolve()

    if backup_path.parent != backup_dir or not backup_path.is_file():
        raise FileNotFoundError("Backup file not found")

    # Check backup database integrity
    with sqlite3.connect(backup_path) as source:
        result = source.execute("PRAGMA integrity_check").fetchone()

        if result[0] != "ok":
            raise ValueError("Backup database is corrupted")

    # Create automatic backup before restoration
    create_backup()

    # Dispose SQLAlchemy connections
    engine.dispose()

    # Restore database
    with sqlite3.connect(backup_path) as source:
        with sqlite3.connect(DATABASE_PATH) as destination:
            source.backup(destination)

    return backup_path
