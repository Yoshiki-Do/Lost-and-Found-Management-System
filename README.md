# Lost and Found Management System

A local desktop application for managing lost and found items in hotels.

Built with **Python, FastAPI, SQLite, and PyWebView**.

## Overview

The Lost and Found Management System helps hotel housekeeping staff manage items found on hotel premises.

The application runs locally on a Windows PC and stores its data in an SQLite database. No cloud services or external database servers are required.

## Features

- **Dashboard** – View an overview of registered lost and found items.
- **Item Registration** – Register found items with details such as item name, location, and date found.
- **Item Management** – Search, view, and edit registered items.
- **Status Management** – Track items through registration, return, and disposal.
- **History Tracking** – Keep a record of item updates and status changes.
- **Bulk Disposal** – Dispose of eligible items in batches.
- **Excel Export** – Export item records to an Excel file.
- **Backup and Restore** – Create database backups and restore data when needed.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| FastAPI | Backend web framework |
| SQLite | Local database |
| SQLAlchemy | Database ORM |
| Jinja2 | HTML templating |
| HTML / CSS / JavaScript | User interface |
| openpyxl | Excel export |
| PyWebView | Desktop application window |
| PyInstaller | Windows executable packaging |

## Project Structure

```text
Lost-and-Found-Management-System/
├── app/
│   ├── routers/
│   ├── services/
│   ├── static/
│   ├── templates/
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   └── paths.py
├── desktop.py
├── LostAndFound.spec
├── requirements.txt
└── .gitignore
```

## Running the Application

### Development Mode

1. Clone the repository.
2. Create and activate a Python virtual environment.
3. Install the required packages.
4. Start the desktop application.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python desktop.py
```

### Building a Windows Executable

Install PyInstaller if it is not already included in the environment.

```powershell
pip install pyinstaller
pyinstaller --clean --noconfirm LostAndFound.spec
```

The executable will be generated in the `dist` directory.

**Note:** Build the executable on a Windows environment matching the target PC architecture (x64 or ARM64).

## Data Storage

When running as a packaged executable, application data is stored locally under:

```text
%LOCALAPPDATA%\LostAndFound\
```

The directory contains:

- `data/` – SQLite database
- `backups/` – Database backup files

## Deployment

Designed for local use on a Windows PC in a hotel housekeeping office.

No cloud hosting or external database server is required.

## License

No license has been specified yet.