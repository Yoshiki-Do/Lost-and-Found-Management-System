from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQL database file
DATABASE_URL = "sqlite:///./data/lost_and_found.db"

# Create database engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for database models
Base = declarative_base()
