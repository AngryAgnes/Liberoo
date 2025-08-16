from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from app.core.config import settings

# Create the SQLAlchemy engine
engine = create_engine(settings.database_url)

# Create sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """Base class for SQLAlchemy models."""

    pass


# Import all models so they are registered with the Base metadata
# This is crucial for Alembic autogeneration to detect schema changes
from app.db.models import *  # noqa: F401, F403


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
