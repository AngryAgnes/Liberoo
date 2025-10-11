from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, List, Optional
import uuid

from sqlalchemy import DateTime, String, Text, SmallInteger, ForeignKey, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.db.models.trips import TripDay
    from app.db.models.geography import Airport


class FlightItinerary(Base):
    __tablename__ = "flight_itineraries"

    id: Mapped[str] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    trip_day_id: Mapped[Optional[str]] = mapped_column(
        String(36), ForeignKey("trip_days.id", ondelete="CASCADE")
    )
    departure_airport: Mapped[Optional[str]] = mapped_column(
        String(3), ForeignKey("airports.code", ondelete="RESTRICT")
    )
    arrival_airport: Mapped[Optional[str]] = mapped_column(
        String(3), ForeignKey("airports.code", ondelete="RESTRICT")
    )
    departure_time: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    arrival_time: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), default=func.now)

    trip_day: Mapped[Optional["TripDay"]] = relationship(back_populates="flight_itineraries")

    departure_airport_obj: Mapped[Optional["Airport"]] = relationship(
        foreign_keys=[departure_airport], back_populates="departing_itineraries"
    )
    arrival_airport_obj: Mapped[Optional["Airport"]] = relationship(
        foreign_keys=[arrival_airport], back_populates="arriving_itineraries"
    )

    segments: Mapped[List["FlightSegment"]] = relationship(
        back_populates="itinerary", cascade="all, delete-orphan"
    )


class FlightSegment(Base):
    __tablename__ = "flight_segments"

    id: Mapped[str] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    itinerary_id: Mapped[Optional[str]] = mapped_column(
        String(36), ForeignKey("flight_itineraries.id", ondelete="CASCADE")
    )
    segment_number: Mapped[Optional[int]] = mapped_column(SmallInteger)
    departure_airport: Mapped[Optional[str]] = mapped_column(
        String(3), ForeignKey("airports.code", ondelete="RESTRICT")
    )
    arrival_airport: Mapped[Optional[str]] = mapped_column(
        String(3), ForeignKey("airports.code", ondelete="RESTRICT")
    )
    departure_time: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    arrival_time: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    airline_name: Mapped[Optional[str]] = mapped_column(Text)
    seat_type: Mapped[Optional[str]] = mapped_column(String(20))
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), default=func.now)

    itinerary: Mapped[Optional["FlightItinerary"]] = relationship(back_populates="segments")

    departure_airport_obj: Mapped[Optional["Airport"]] = relationship(
        foreign_keys=[departure_airport], back_populates="departing_segments"
    )
    arrival_airport_obj: Mapped[Optional["Airport"]] = relationship(
        foreign_keys=[arrival_airport], back_populates="arriving_segments"
    )
