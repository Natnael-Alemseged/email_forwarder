from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Detect if using SQLite
is_sqlite = settings.DB_URI.startswith("sqlite")

# Create database engine
engine = create_engine(
    settings.DB_URI,
    connect_args={"check_same_thread": False} if is_sqlite else {}
)

# Session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Dependency for FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
