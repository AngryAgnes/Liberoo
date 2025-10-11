# Import all models so they are registered with SQLAlchemy Base metadata
# This is essential for Alembic autogeneration to work properly

from app.db.base import Base
from .enums import ChatSender, Sex
from .user import User, UserProfile, UserPreference, ChatMessage
from .geography import Country, City, Place, Hotel, Food, Attraction, Airport
from .lodging import HotelStay
from .trips import Trip, TripDay, DayTimeBlock
from .flights import FlightItinerary, FlightSegment
from .associations import TimeblockFood, TimeblockAttraction

# Export all models for easy importing
__all__ = [
    "Base",
    "ChatSender",
    "Sex",
    "User",
    "UserProfile",
    "UserPreference",
    "ChatMessage",
    "Country",
    "City",
    "Place",
    "Hotel",
    "Food",
    "Attraction",
    "Airport",
    "Trip",
    "TripDay",
    "DayTimeBlock",
    "FlightItinerary",
    "FlightSegment",
    "HotelStay",
    "TimeblockFood",
    "TimeblockAttraction",
]
