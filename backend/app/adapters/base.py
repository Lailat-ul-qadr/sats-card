"""
Abstract adapter for mobile money providers.

Every provider (MTN, Airtel, Orange) implements this interface.
The rest of the app only talks to MobileMoneyAdapter — never to
provider-specific code directly. This makes adding new providers
a one-file job.
"""

from __future__ import annotations

import abc
from enum import Enum
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


# ── Data Models ─────────────────────────────────────────────────────────


class PaymentStatus(str, Enum):
    """Lifecycle states for a mobile money payment."""

    INITIATED = "initiated"
    PENDING = "pending"
    PROCESSING = "processing"
    SUCCESSFUL = "successful"
    FAILED = "failed"
    TIMEOUT = "timeout"
    REVERSED = "reversed"


class PaymentRequest(BaseModel):
    """Incoming request to collect mobile money from a user."""

    phone_number: str = Field(..., description="E.164 phone number, e.g. +256701234567")
    amount: float = Field(..., gt=0, description="Amount in local fiat currency")
    currency: str = Field(..., min_length=3, max_length=3, description="ISO 4217 currency code, e.g. UGX")
    reference: str = Field(..., description="Unique internal reference / invoice ID")
    description: str = Field(default="", description="Human-readable description")
    callback_url: Optional[str] = Field(
        default=None,
        description="Webhook URL for async status updates",
    )


class PaymentResponse(BaseModel):
    """Response from the provider after initiating a collection."""

    provider: str = Field(..., description="Provider identifier, e.g. mtn_momo")
    provider_txn_id: str = Field(..., description="Provider's own transaction ID")
    reference: str = Field(..., description="Our internal reference echoed back")
    status: PaymentStatus
    amount: float
    currency: str
    phone_number: str
    fee: float = Field(default=0.0, description="Provider fee in local currency")
    message: str = Field(default="")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class BalanceResponse(BaseModel):
    """Balance check result from a provider."""

    provider: str
    balance: float
    currency: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# ── Abstract Adapter ────────────────────────────────────────────────────


class MobileMoneyAdapter(abc.ABC):
    """
    Every mobile money provider must implement these four methods.

    Usage:
        adapter = MTNMoMoAdapter()
        resp = await adapter.collect(payment_request)
        status = await adapter.check_status(provider_txn_id)
    """

    @property
    @abc.abstractmethod
    def provider_name(self) -> str:
        """Short identifier, e.g. 'mtn_momo'."""

    @abc.abstractmethod
    async def authenticate(self) -> str:
        """
        Obtain or refresh an access token.
        Returns the token string. Implementations should cache it
        and only re-authenticate when expired.
        """

    @abc.abstractmethod
    async def collect(self, request: PaymentRequest) -> PaymentResponse:
        """
        Initiate a mobile money collection (push to user's phone).
        The user will receive a prompt on their phone to approve.
        """

    @abc.abstractmethod
    async def check_status(self, provider_txn_id: str) -> PaymentResponse:
        """
        Check the status of a previously initiated collection.
        Returns updated status (may still be PENDING).
        """

    @abc.abstractmethod
    async def validate_phone(self, phone_number: str) -> bool:
        """
        Validate that a phone number is registered with this provider.
        Returns True if valid and registered.
        """

    async def get_balance(self) -> BalanceResponse:
        """
        Check the merchant/collection account balance.
        Optional — not all providers support this.
        """
        raise NotImplementedError(f"{self.provider_name} does not support balance checks")
