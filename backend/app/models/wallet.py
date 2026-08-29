"""
Wallet model — one per user, holds BTC balance in sats.

The wallet is the source of truth for the user's Bitcoin balance.
All operations (fund, send, spend) go through here with proper locking.
"""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import String, BigInteger, DateTime, ForeignKey, func, CheckConstraint, TypeDecorator
from sqlalchemy.orm import Mapped, mapped_column, relationship
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


class Wallet(Base):
    __tablename__ = "wallets"
    __table_args__ = (
        CheckConstraint("balance_sats >= 0", name="positive_balance"),
        CheckConstraint("reserved_sats >= 0", name="positive_reserved"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), unique=True, nullable=False
    )

    # ── Balances (in satoshis — the smallest Bitcoin unit) ───────────
    balance_sats: Mapped[int] = mapped_column(
        BigInteger, default=0,
        comment="Available BTC balance in satoshis"
    )
    reserved_sats: Mapped[int] = mapped_column(
        BigInteger, default=0,
        comment="Sats locked in pending transactions"
    )
    balance_usd: Mapped[float] = mapped_column(
        default=0.0,
        comment="Available USD balance"
    )
    reserved_usd: Mapped[float] = mapped_column(
        default=0.0,
        comment="USD locked in pending transactions"
    )

    # ── Lightning node info ─────────────────────────────────────────
    lnd_pubkey: Mapped[str | None] = mapped_column(
        String(66), nullable=True,
        comment="LND node public key"
    )
    lnd_address: Mapped[str | None] = mapped_column(
        String(255), nullable=True,
        comment="Lightning node address (pubkey@host)"
    )

    # ── Virtual Card ────────────────────────────────────────────────
    card_number: Mapped[str | None] = mapped_column(
        String(19), nullable=True,
        comment="Virtual card number (encrypted at rest)"
    )
    card_last4: Mapped[str | None] = mapped_column(String(4), nullable=True)
    card_expiry: Mapped[str | None] = mapped_column(String(5), nullable=True, comment="MM/YY")
    card_status: Mapped[str] = mapped_column(
        String(20), default="inactive",
        comment="inactive | active | frozen | closed"
    )

    # ── Limits ──────────────────────────────────────────────────────
    daily_spent_sats: Mapped[int] = mapped_column(BigInteger, default=0)
    daily_spent_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    monthly_spent_sats: Mapped[int] = mapped_column(BigInteger, default=0)
    monthly_spent_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    # ── Timestamps ──────────────────────────────────────────────────
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # ── Relationships ───────────────────────────────────────────────
    user: Mapped["User"] = relationship("User", back_populates="wallet")

    @property
    def balance_btc(self) -> float:
        """Balance in BTC (8 decimal places)."""
        return self.balance_sats / 100_000_000

    @property
    def available_sats(self) -> int:
        """Balance minus reserved (pending) amount."""
        return self.balance_sats - self.reserved_sats

    def __repr__(self) -> str:
        return f"<Wallet user={self.user_id} sats={self.balance_sats}>"
