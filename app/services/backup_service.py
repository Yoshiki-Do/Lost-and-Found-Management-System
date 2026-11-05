import sqlite3
from pathlib import Path
from datetime import datetime
from app.database import engine


def create_backup() -> Path:
    # Get database file path
    database_path = Path(engine.url.database).resolve()

    # Create backup directory
    backup_dir = Path("backups")
    backup_dir.mkdir(parents=True, exist_ok=True)

    # Generate backup filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = backup_dir / f"lost_and_found_{timestamp}.db"

    # Create SQLite backup
    with sqlite3.connect(database_path) as source:
        with sqlite3.connect(backup_path) as destination:
            source.backup(destination)

    return backup_path


def restore_backup(backup_filename: str) -> Path:
    # Get backup directory
    backup_dir = Path("backups").resolve()

    # Validate backup filename
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
    database_path = Path(engine.url.database).resolve()

    with sqlite3.connect(backup_path) as source:
        with sqlite3.connect(database_path) as destination:
            source.backup(destination)

    return backup_path
