# Import all models so they are registered with SQLAlchemy Base metadata
# This is essential for Alembic autogeneration to work properly

from .user import User, Profile
from .accessibility import Accessibility
from .country import Country
from .language import Language

# Export all models for easy importing
__all__ = [
    "User",
    "Profile",
    "Accessibility",
    "Country",
    "Language",
]
