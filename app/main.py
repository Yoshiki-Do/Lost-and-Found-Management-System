import sys
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.database import Base, engine
from app.models import Item, ItemHistory
from app.routers import items, history, dashboard, backup

# Determine application resource directory
if getattr(sys, "frozen", False):
    APP_DIR = Path(sys._MEIPASS) / "app"
else:
    APP_DIR = Path(__file__).resolve().parent


# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Lost and Found Management System")

templates = Jinja2Templates(directory=str(APP_DIR / "templates"))

app.mount("/static", StaticFiles(directory=str(APP_DIR / "static")), name="static")


# Register routers
app.include_router(items.router)
app.include_router(history.router)
app.include_router(dashboard.router)
app.include_router(backup.router)


@app.get("/")
def read_root():
    return {"message": "Lost and Found API is running"}


@app.get("/dashboard")
def dashboard_page(request: Request):
    return templates.TemplateResponse(request=request, name="dashboard.html")


@app.get("/items")
def items_page(request: Request):
    return templates.TemplateResponse(request=request, name="items.html")


@app.get("/register")
def register_page(request: Request):
    return templates.TemplateResponse(request=request, name="register.html")


@app.get("/details/{lost_number}")
def details_page(lost_number: int, request: Request):
    return templates.TemplateResponse(request=request, name="details.html")


@app.get("/edit/{lost_number}")
def edit_page(lost_number: int, request: Request):
    return templates.TemplateResponse(request=request, name="edit.html")


@app.get("/disposal")
def disposal_page(request: Request):
    return templates.TemplateResponse(request=request, name="disposal.html")


@app.get("/history-page")
def history_page(request: Request):
    return templates.TemplateResponse(request=request, name="history.html")


@app.get("/backup-page")
def backup_page(request: Request):
    return templates.TemplateResponse(request=request, name="backup.html")
