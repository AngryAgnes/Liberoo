from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.db.models.geography import Attraction, Food
    from app.db.models.trips import DayTimeBlock


class TimeblockFood(Base):
    __tablename__ = "timeblock_foods"

    food_id: Mapped[str] = mapped_column(
        String(36), primary_key=True
    )
    time_block_id: Mapped[str] = mapped_column(
        String(36), primary_key=True
    )
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), default=func.now)

    # Foreign keys live on target tables to avoid circular imports in this file
    food: Mapped["Food"] = relationship(back_populates="time_links")
    time_block: Mapped["DayTimeBlock"] = relationship(back_populates="food_links")


class TimeblockAttraction(Base):
    __tablename__ = "timeblock_attractions"

    attraction_id: Mapped[str] = mapped_column(
        String(36), primary_key=True
    )
    time_block_id: Mapped[str] = mapped_column(
        String(36), primary_key=True
    )
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), default=func.now)

    attraction: Mapped["Attraction"] = relationship(back_populates="time_links")
    time_block: Mapped["DayTimeBlock"] = relationship(back_populates="attraction_links")
