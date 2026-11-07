from datetime import datetime
from sqlalchemy import Column, Date, DateTime, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class Item(Base):
    __tablename__ = "items"

    # Internal database ID
    id = Column(Integer, primary_key=True, index=True)

    # Lost and Found management number
    lost_number = Column(Integer, unique=True, nullable=False, index=True)

    # Item information
    item_name = Column(String(200), nullable=False)
    description = Column(String(200), nullable=True)

    # Found information
    found_location = Column(String(200), nullable=False)
    found_at = Column(Date, nullable=False)

    # Registration information
    registered_at = Column(DateTime, default=datetime.now, nullable=False)

    # Storage information
    storage_month = Column(String(7), nullable=False)
    storage_box = Column(String(50), nullable=False)

    # Status: REGISTERED, RETURNED, DISPOSED, CANCELLED
    status = Column(String(20), default="REGISTERED", nullable=False)

    # Return information
    returned_at = Column(DateTime, nullable=True)

    # Disposal information
    disposed_at = Column(DateTime, nullable=True)


class ItemHistory(Base):
    __tablename__ = "item_histories"

    id = Column(Integer, primary_key=True, index=True)
    lost_number = Column(Integer, nullable=False, index=True)
    action = Column(String(20), nullable=False)
    description = Column(String(200), nullable=True)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
