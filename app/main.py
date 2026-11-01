from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.database import Base, engine
from app.models import Item, ItemHistory
from app.routers import items, history, dashboard

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Lost and Found Management System")

templates = Jinja2Templates(directory="app/templates")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Register routers
app.include_router(items.router)
app.include_router(history.router)
app.include_router(dashboard.router)


@app.get("/")
def read_root():
    return {"message": "Lost and Found API is running"}


@app.get("/dashboard")
def dashboard_page(request: Request):
    return templates.TemplateResponse(request=request, name="dashboard.html")


@app.get("/items")
def items_page(request: Request):
    return templates.TemplateResponse(request=request, name="items.html")
