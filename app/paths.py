import sys
import os
from pathlib import Path

# Database application data directory
if getattr(sys, "frozen", False):
    APP_DATA_DIR = Path(os.environ.get("LOCALAPPDATA", Path.home())) / "LostAndFound"
else:
    APP_DATA_DIR = Path(__file__).resolve().parent.parent

# Data directories
DATA_DIR = APP_DATA_DIR / "data"
BACKUP_DIR = APP_DATA_DIR / "backups"

# Create directories if they do not exist
DATA_DIR.mkdir(parents=True, exist_ok=True)
BACKUP_DIR.mkdir(parents=True, exist_ok=True)

# SQLite database file
DATABASE_PATH = DATA_DIR / "lost_and_found.db"
