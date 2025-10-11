from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional, List
import uuid

from sqlalchemy import DateTime, Text, Integer, String, ForeignKey, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.db.models.geography import Hotel
    from app.db.models.trips import TripDay

class HotelStay(Base):
    __tablename__ = "hotel_stays"

    id: Mapped[str] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    hotel_id: Mapped[Optional[str]] = mapped_column(
        String(36), ForeignKey("hotels.id", ondelete="SET NULL")
    )
    trip_day_id: Mapped[Optional[str]] = mapped_column(
        String(36), ForeignKey("trip_days.id", ondelete="CASCADE")
    )
    hotel_name: Mapped[Optional[str]] = mapped_column(Text)
    room_type: Mapped[Optional[str]] = mapped_column(Text)
    room_number: Mapped[Optional[str]] = mapped_column(Text)
    price: Mapped[Optional[int]] = mapped_column(Integer)
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), default=func.now)

    hotel: Mapped[Optional["Hotel"]] = relationship(back_populates="stays")
    trip_day: Mapped[Optional["TripDay"]] = relationship(back_populates="hotel_stays")
