from __future__ import annotations

from datetime import date, datetime, time
from typing import TYPE_CHECKING, List, Optional
import uuid

from sqlalchemy import DateTime, SmallInteger, Date, Time, String, ForeignKey, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.models.geography import Attraction, Food

if TYPE_CHECKING:
    from app.db.models.user import User
    from app.db.models.geography import Country, City, Hotel
    from app.db.models.flights import FlightItinerary
    from app.db.models.lodging import HotelStay
    from app.db.models.associations import TimeblockFood, TimeblockAttraction


class Trip(Base):
    __tablename__ = "trips"

    id: Mapped[str] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[Optional[str]] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE")
    )
    start_date: Mapped[Optional[Date]] = mapped_column(Date)
    end_date: Mapped[Optional[Date]] = mapped_column(Date)
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), default=func.now)

    user: Mapped[Optional["User"]] = relationship(back_populates="trips")
    days: Mapped[List["TripDay"]] = relationship(
        back_populates="trip", cascade="all, delete-orphan"
    )


class TripDay(Base):
    __tablename__ = "trip_days"

    id: Mapped[str] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    trip_id: Mapped[Optional[str]] = mapped_column(
        String(36), ForeignKey("trips.id", ondelete="CASCADE")
    )
    day_number: Mapped[Optional[int]] = mapped_column(SmallInteger)
    date: Mapped[Optional[Date]] = mapped_column(Date)
    country_id: Mapped[Optional[str]] = mapped_column(
        String(36), ForeignKey("countries.id", ondelete="SET NULL")
    )
    hotel_id: Mapped[Optional[str]] = mapped_column(
        String(36), ForeignKey("hotels.id", ondelete="SET NULL")
    )
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), default=func.now)

    trip: Mapped[Optional["Trip"]] = relationship(back_populates="days")
    country: Mapped[Optional["Country"]] = relationship(back_populates="trip_days")
    hotel: Mapped[Optional["Hotel"]] = relationship(back_populates="as_default_on_trip_days")

    time_blocks: Mapped[List["DayTimeBlock"]] = relationship(
        back_populates="trip_day", cascade="all, delete-orphan"
    )
    flight_itineraries: Mapped[List["FlightItinerary"]] = relationship(
        back_populates="trip_day", cascade="all, delete-orphan"
    )
    hotel_stays: Mapped[List["HotelStay"]] = relationship(
        back_populates="trip_day", cascade="all, delete-orphan"
    )


class DayTimeBlock(Base):
    __tablename__ = "day_time_blocks"

    id: Mapped[str] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    trip_day_id: Mapped[Optional[str]] = mapped_column(
        String(36), ForeignKey("trip_days.id", ondelete="CASCADE")
    )
    start_time: Mapped[Optional[Time]] = mapped_column(Time)
    end_time: Mapped[Optional[Time]] = mapped_column(Time)
    city_id: Mapped[Optional[str]] = mapped_column(
        String(36), ForeignKey("cities.id", ondelete="SET NULL")
    )
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), default=func.now)

    trip_day: Mapped[Optional["TripDay"]] = relationship(back_populates="time_blocks")
    city: Mapped[Optional["City"]] = relationship(back_populates="time_blocks")

    foods: Mapped[List["Food"]] = relationship(
        secondary="timeblock_foods", back_populates="time_blocks"
    )
    attractions: Mapped[List["Attraction"]] = relationship(
        secondary="timeblock_attractions", back_populates="time_blocks"
    )

    food_links: Mapped[List["TimeblockFood"]] = relationship(
        back_populates="time_block", cascade="all, delete-orphan"
    )
    attraction_links: Mapped[List["TimeblockAttraction"]] = relationship(
        back_populates="time_block", cascade="all, delete-orphan"
    )
