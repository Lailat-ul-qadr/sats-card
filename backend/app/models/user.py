"""
User model — phone-number-first auth for emerging markets.

In East Africa, phone numbers ARE identity. No email needed.
"""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import String, Boolean, DateTime, Text, func, TypeDecorator
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import TypeDecorator

from .base import Base


class UUID(TypeDecorator):
    """Portable UUID type for SQLite + PostgreSQL."""
    impl = String(36)
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is not None:
            return str(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            return uuid.UUID(value)
        return value


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(), primary_key=True, default=uuid.uuid4
    )
    phone_number: Mapped[str] = mapped_column(
        String(20), unique=True, index=True, nullable=False,
        comment="E.164 format, e.g. +256701234567"
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False, default="User")
    email: Mapped[str | None] = mapped_column(String(255), unique=True, nullable=True)

    # ── Auth ────────────────────────────────────────────────────────
    pin_hash: Mapped[str] = mapped_column(
        String(128), nullable=False,
        comment="BCrypt hash of 4-digit USSD PIN"
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)

    # ── KYC ─────────────────────────────────────────────────────────
    kyc_level: Mapped[str] = mapped_column(
        String(20), default="none",
        comment="none | tier1 | tier2"
    )
    kyc_verified_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    # ── Preferences ─────────────────────────────────────────────────
    preferred_currency: Mapped[str] = mapped_column(String(3), default="UGX")
    preferred_language: Mapped[str] = mapped_column(String(5), default="en")
    daily_limit_usd: Mapped[float] = mapped_column(default=500.0)
    monthly_limit_usd: Mapped[float] = mapped_column(default=5000.0)

    # ── Metadata ────────────────────────────────────────────────────
    country: Mapped[str] = mapped_column(String(3), default="UG")
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    last_ussd_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # ── Relationships ───────────────────────────────────────────────
    wallet: Mapped["Wallet"] = relationship("Wallet", back_populates="user", uselist=False)
    transactions: Mapped[list["Transaction"]] = relationship("Transaction", back_populates="user")
    ussd_sessions: Mapped[list["USSDSession"]] = relationship("USSDSession", back_populates="user")

    def __repr__(self) -> str:
        return f"<User {self.phone_number} name={self.name}>"
