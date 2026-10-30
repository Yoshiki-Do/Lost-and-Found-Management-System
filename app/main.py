from fastapi import FastAPI
from app.database import Base, engine
from app.models import Item
from app.routers import items

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Lost and Found Management System")

# Register routers
app.include_router(items.router)


@app.get("/")
def read_root():
    return {"message": "Lost and Found API is running"}
