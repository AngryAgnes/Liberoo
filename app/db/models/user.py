import uuid
from sqlalchemy import Boolean, Enum, ForeignKey, Integer, String, DateTime, Uuid
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from app.db.base import Base
from app.db.models.enums import ChatSender

if TYPE_CHECKING:
    from app.db.models.geography import Country


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(128), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)

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
    profiles: Mapped[List["UserProfile"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )


class UserProfile(Base):
    __tablename__ = "profiles"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("users.id"), nullable=True
    )
    nickname: Mapped[str] = mapped_column(String(50), nullable=True)
    profile_picture: Mapped[str] = mapped_column(String(1000), nullable=True)
    surname: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    given_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    date_of_birth: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    sex: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    email: Mapped[Optional[str]] = mapped_column(
        String(100), unique=True, nullable=True
    )
    phone_number: Mapped[Optional[str]] = mapped_column(
        String(30), unique=True, nullable=True
    )
    driver_license_number: Mapped[Optional[str]] = mapped_column(
        String(100), unique=True, nullable=True
    )
    is_user: Mapped[bool] = mapped_column(default=True)
    email_verified: Mapped[bool] = mapped_column(default=False)
    phone_verified: Mapped[bool] = mapped_column(default=False)

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
    user: Mapped[Optional["User"]] = relationship(back_populates="profiles")

    profile_nationalities: Mapped[List["ProfileNationality"]] = relationship(
        back_populates="profile", cascade="all, delete-orphan"
    )
    travel_companions: Mapped[List["TravelCompanion"]] = relationship(
        foreign_keys="TravelCompanion.profile_id",
        back_populates="profile",
        cascade="all, delete-orphan",
    )


class TravelCompanion(Base):
    __tablename__ = "travel_companions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    profile_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("profiles.id"), nullable=False
    )
    companion_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("profiles.id"), nullable=False
    )

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
    # The main profile who added this companion
    profile: Mapped["UserProfile"] = relationship(
        foreign_keys=[profile_id], back_populates="travel_companions"
    )
    # The companion profile
    companion_profile: Mapped["UserProfile"] = relationship(foreign_keys=[companion_id])


class ProfileNationality(Base):
    __tablename__ = "profile_nationalities"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    profile_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("profiles.id"), nullable=False
    )
    country_id: Mapped[str] = mapped_column(
        String(3), ForeignKey("countries.id"), nullable=False
    )

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
    profile: Mapped["UserProfile"] = relationship(back_populates="profile_nationalities")
    country: Mapped["Country"] = relationship(back_populates="profile_nationalities")


class UserPreference(Base):
    __tablename__ = "user_preferences"

    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    currency: Mapped[Optional[str]] = mapped_column(String(10))
    notifications_enabled: Mapped[Optional[bool]] = mapped_column(Boolean)
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), default=func.now)

    user: Mapped["User"] = relationship(back_populates="preferences")


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE")
    )
    text_query: Mapped[Optional[str]] = mapped_column(String(300))
    sender: Mapped[Optional[ChatSender]] = mapped_column(
        Enum(ChatSender, name="chat_sender")
    )
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), default=func.now)

    user: Mapped[Optional["User"]] = relationship(back_populates="messages")