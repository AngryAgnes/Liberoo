from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, List, Optional, Dict, Any
import uuid

from sqlalchemy import DateTime, String, Text, Integer, JSON, ForeignKey, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.db.models.trips import TripDay
    from app.db.models.lodging import HotelStay
    from app.db.models.flights import FlightItinerary, FlightSegment
    from app.db.models.trips import DayTimeBlock
    from app.db.models.associations import (
        TimeblockFood,
        TimeblockAttraction,
    )

class Country(Base):
    __tablename__ = "countries"

    id: Mapped[str] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    country_code: Mapped[Optional[str]] = mapped_column(String(3))
    continent: Mapped[Optional[str]] = mapped_column(String(16))

    cities: Mapped[List["City"]] = relationship(back_populates="country")
    places: Mapped[List["Place"]] = relationship(back_populates="country")
    trip_days: Mapped[List["TripDay"]] = relationship(back_populates="country")


class City(Base):
    __tablename__ = "cities"

    id: Mapped[str] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    country_id: Mapped[Optional[str]] = mapped_column(
        String(36), ForeignKey("countries.id", ondelete="RESTRICT")
    )
    name: Mapped[Optional[str]] = mapped_column(String(64))

    country: Mapped[Optional["Country"]] = relationship(back_populates="cities")
    places: Mapped[List["Place"]] = relationship(back_populates="city")
    airports: Mapped[List["Airport"]] = relationship(back_populates="city")
    time_blocks: Mapped[List["DayTimeBlock"]] = relationship(back_populates="city")


class Place(Base):
    __tablename__ = "places"

    id: Mapped[str] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    country_id: Mapped[Optional[str]] = mapped_column(
        String(36), ForeignKey("countries.id", ondelete="RESTRICT")
    )
    city_id: Mapped[Optional[str]] = mapped_column(
        String(36), ForeignKey("cities.id", ondelete="SET NULL")
    )
    address: Mapped[Optional[str]] = mapped_column(Text)
    # Portable stand-in for POINT: {"lat": ..., "lon": ...}
    geolocation: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON)
    detail: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), default=func.now)

    country: Mapped[Optional["Country"]] = relationship(back_populates="places")
    city: Mapped[Optional["City"]] = relationship(back_populates="places")

    hotels: Mapped[List["Hotel"]] = relationship(back_populates="place")
    foods: Mapped[List["Food"]] = relationship(back_populates="place")
    attractions: Mapped[List["Attraction"]] = relationship(back_populates="place")
    airports: Mapped[List["Airport"]] = relationship(back_populates="place")


class Hotel(Base):
    __tablename__ = "hotels"

    id: Mapped[str] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    place_id: Mapped[Optional[str]] = mapped_column(
        String(36), ForeignKey("places.id", ondelete="CASCADE")
    )
    name: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), default=func.now)

    place: Mapped[Optional["Place"]] = relationship(back_populates="hotels")
    stays: Mapped[List["HotelStay"]] = relationship(back_populates="hotel")
    as_default_on_trip_days: Mapped[List["TripDay"]] = relationship(
        back_populates="hotel"
    )


class Food(Base):
    __tablename__ = "foods"

    id: Mapped[str] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    place_id: Mapped[Optional[str]] = mapped_column(
        String(36), ForeignKey("places.id", ondelete="CASCADE")
    )
    name: Mapped[Optional[str]] = mapped_column(Text)
    price: Mapped[Optional[int]] = mapped_column(Integer)
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), default=func.now)

    place: Mapped[Optional["Place"]] = relationship(back_populates="foods")
    time_links: Mapped[List["TimeblockFood"]] = relationship(
        back_populates="food", cascade="all, delete-orphan"
    )
    time_blocks: Mapped[List["DayTimeBlock"]] = relationship(
        secondary="timeblock_foods", back_populates="foods"
    )


class Attraction(Base):
    __tablename__ = "attractions"

    id: Mapped[str] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    place_id: Mapped[Optional[str]] = mapped_column(
        String(36), ForeignKey("places.id", ondelete="CASCADE")
    )
    name: Mapped[Optional[str]] = mapped_column(Text)
    price: Mapped[Optional[int]] = mapped_column(Integer)
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), default=func.now)

    place: Mapped[Optional["Place"]] = relationship(back_populates="attractions")
    time_links: Mapped[List["TimeblockAttraction"]] = relationship(
        back_populates="attraction", cascade="all, delete-orphan"
    )
    time_blocks: Mapped[List["DayTimeBlock"]] = relationship(
        secondary="timeblock_attractions", back_populates="attractions"
    )


class Airport(Base):
    __tablename__ = "airports"

    code: Mapped[str] = mapped_column(String(3), primary_key=True)  # IATA
    city_id: Mapped[Optional[str]] = mapped_column(
        String(36), ForeignKey("cities.id", ondelete="SET NULL")
    )
    place_id: Mapped[Optional[str]] = mapped_column(
        String(36), ForeignKey("places.id", ondelete="SET NULL")
    )

    city: Mapped[Optional["City"]] = relationship(back_populates="airports")
    place: Mapped[Optional["Place"]] = relationship(back_populates="airports")

    departing_itineraries: Mapped[List["FlightItinerary"]] = relationship(
        back_populates="departure_airport_obj",
        foreign_keys="FlightItinerary.departure_airport",
    )
    arriving_itineraries: Mapped[List["FlightItinerary"]] = relationship(
        back_populates="arrival_airport_obj",
        foreign_keys="FlightItinerary.arrival_airport",
    )
    departing_segments: Mapped[List["FlightSegment"]] = relationship(
        back_populates="departure_airport_obj",
        foreign_keys="FlightSegment.departure_airport",
    )
    arriving_segments: Mapped[List["FlightSegment"]] = relationship(
        back_populates="arrival_airport_obj",
        foreign_keys="FlightSegment.arrival_airport",
    )
