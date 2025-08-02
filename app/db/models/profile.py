from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db.models.accessibility import Accessibility
from app.db.models.country import Country
from app.db.models.language import Language
from db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import List, Optional
from app.db.models.user import User


class Profile(Base):
    __tablename__ = "profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=True
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
    profile_languages: Mapped[List["ProfileLanguage"]] = relationship(
        back_populates="profile", cascade="all, delete-orphan"
    )
    profile_accessibilities: Mapped[List["ProfileAccessibility"]] = relationship(
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
    profile: Mapped["Profile"] = relationship(
        foreign_keys=[profile_id], back_populates="travel_companions"
    )
    # The companion profile
    companion_profile: Mapped["Profile"] = relationship(foreign_keys=[companion_id])


class ProfileNationality(Base):
    __tablename__ = "profile_nationalities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    profile_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("profiles.id"), nullable=False
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
    profile: Mapped["Profile"] = relationship(back_populates="profile_nationalities")
    country: Mapped["Country"] = relationship(back_populates="profile_nationalities")


class ProfileLanguage(Base):
    __tablename__ = "profile_languages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    profile_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("profiles.id"), nullable=False
    )
    language_id: Mapped[str] = mapped_column(
        String(2), ForeignKey("languages.id"), nullable=False
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
    profile: Mapped["Profile"] = relationship(back_populates="profile_languages")
    language: Mapped["Language"] = relationship(back_populates="profile_languages")


class ProfileAccessibility(Base):
    __tablename__ = "profile_accessibilities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    profile_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("profiles.id"), nullable=False
    )
    accessibility_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("accessibilities.id"), nullable=False
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
    profile: Mapped["Profile"] = relationship(back_populates="profile_accessibilities")
    accessibility: Mapped["Accessibility"] = relationship(
        back_populates="profile_accessibilities"
    )
