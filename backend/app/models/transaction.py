"""
Transaction model — tracks every money movement.

Lifecycle:
  initiated → pending → processing → settled | failed | reversed

Each transaction records:
  - Who (user)
  - What type (fund, send, receive, spend)
  - How much (fiat + sats)
  - Which provider (MTN, Airtel, Orange, Lightning)
  - Status and timestamps for each state change
"""

from __future__ import annotations

import uuid
import enum
from datetime import datetime

from sqlalchemy import (
    String, BigInteger, Float, DateTime, ForeignKey,
    Text, Enum, func, Index, TypeDecorator,
)
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


class TransactionType(str, enum.Enum):
    """What kind of transaction this is."""

    FUND = "fund"           # Mobile money → BTC (user tops up)
    SEND = "send"           # BTC → Lightning invoice (user sends)
    RECEIVE = "receive"     # Lightning invoice → BTC (user receives)
    SPEND = "spend"         # BTC → virtual card payment
    SWAP = "swap"           # Internal conversion (e.g. BTC ↔ USD)


class TransactionStatus(str, enum.Enum):
    """Lifecycle status — every transaction goes through these states."""

    INITIATED = "initiated"     # Created, waiting for provider
    PENDING = "pending"         # Provider acknowledged, waiting for user action
    PROCESSING = "processing"   # User approved, being processed
    SETTLED = "settled"         # Confirmed on Lightning/blockchain
    FAILED = "failed"           # Provider or network error
    REVERSED = "reversed"       # Refund / chargeback


class Transaction(Base):
    __tablename__ = "transactions"
    __table_args__ = (
        Index("idx_tx_user_created", "user_id", "created_at"),
        Index("idx_tx_status", "status"),
        Index("idx_tx_reference", "reference", unique=True),
        Index("idx_tx_provider_txn", "provider_txn_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )

    # ── Transaction Details ─────────────────────────────────────────
    type: Mapped[TransactionType] = mapped_column(
        Enum(TransactionType), nullable=False
    )
    status: Mapped[TransactionStatus] = mapped_column(
        Enum(TransactionStatus), default=TransactionStatus.INITIATED
    )
    reference: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False,
        comment="Our internal reference (e.g. SC-A1B2C3D4E5F6)"
    )

    # ── Amounts ─────────────────────────────────────────────────────
    amount_fiat: Mapped[float] = mapped_column(Float, nullable=False, comment="Amount in local currency")
    currency_fiat: Mapped[str] = mapped_column(String(3), nullable=False, comment="ISO 4217, e.g. UGX")
    amount_sats: Mapped[int] = mapped_column(BigInteger, nullable=False, comment="Amount in satoshis")
    fee_sats: Mapped[int] = mapped_column(BigInteger, default=0, comment="Lightning network fee")

    # ── Exchange Rate at Time of Transaction ────────────────────────
    rate_used: Mapped[float] = mapped_column(Float, nullable=False, comment="sats per unit of fiat")
    rate_source: Mapped[str] = mapped_column(String(20), default="coingecko")

    # ── Provider Info ───────────────────────────────────────────────
    provider: Mapped[str] = mapped_column(
        String(30), nullable=False,
        comment="mtn_momo | airtel_money | orange_money | lightning"
    )
    provider_txn_id: Mapped[str | None] = mapped_column(
        String(100), nullable=True,
        comment="Provider's own transaction ID"
    )
    provider_status: Mapped[str | None] = mapped_column(
        String(30), nullable=True,
        comment="Raw status from provider"
    )

    # ── Lightning Details ───────────────────────────────────────────
    payment_hash: Mapped[str | None] = mapped_column(
        String(64), nullable=True,
        comment="Lightning payment hash (for send/receive)"
    )
    payment_request: Mapped[str | None] = mapped_column(
        Text, nullable=True,
        comment="BOLT11 invoice string"
    )
    destination_pubkey: Mapped[str | None] = mapped_column(
        String(66), nullable=True,
        comment="Lightning node pubkey (for send)"
    )

    # ── Mobile Money Details ────────────────────────────────────────
    phone_number: Mapped[str | None] = mapped_column(
        String(20), nullable=True,
        comment="Phone number used for mobile money"
    )
    merchant_name: Mapped[str | None] = mapped_column(
        String(100), nullable=True,
        comment="Merchant name (for card spend)"
    )

    # ── Description & Metadata ──────────────────────────────────────
    description: Mapped[str] = mapped_column(Text, default="")
    metadata_json: Mapped[str | None] = mapped_column(
        Text, nullable=True,
        comment="Additional data as JSON string"
    )

    # ── Timestamps ──────────────────────────────────────────────────
    initiated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    pending_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    processing_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    settled_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    failed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # ── Relationships ───────────────────────────────────────────────
    user: Mapped["User"] = relationship("User", back_populates="transactions")

    def __repr__(self) -> str:
        return f"<Transaction {self.reference} type={self.type.value} status={self.status.value}>"
