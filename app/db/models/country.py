from sqlalchemy import String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import List, Optional

from app.db.base import Base
from app.db.models.profile import ProfileNationality


class Country(Base):
    __tablename__ = "countries"

    id: Mapped[str] = mapped_column(String(3), primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    continent: Mapped[str] = mapped_column(String(50), nullable=True)

    # Timestamp columns
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    deleted_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Relationships
    profile_nationalities: Mapped[List["ProfileNationality"]] = relationship(
        back_populates="country", cascade="all, delete-orphan"
    )
