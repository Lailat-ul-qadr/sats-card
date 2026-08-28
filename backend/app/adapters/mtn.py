"""
MTN Mobile Money (MoMo) API adapter.

Implements the MTN MoMo Collection API v2.0.
Docs: https://momodeveloper.mtn.com/api-documentation

Flow:
  1. Authenticate → get OAuth2 access token
  2. Request to Pay → push prompt to user's phone
  3. Poll Check Status → get final result
  4. (Optional) Receive callback webhook
"""

from __future__ import annotations

import uuid
import logging
from datetime import datetime, timedelta
from typing import Optional

import httpx

from .base import (
    MobileMoneyAdapter,
    PaymentRequest,
    PaymentResponse,
    PaymentStatus,
    BalanceResponse,
)

logger = logging.getLogger(__name__)


class MTNMoMoAdapter(MobileMoneyAdapter):
    """
    MTN MoMo Collection API adapter.

    Environment URLs (country-specific):
      Rwanda Sandbox:      https://sandbox.momodeveloper.mtn.co.rw
      Rwanda Production:   https://momoapi.mtn.co.rw
      Uganda Sandbox:      https://sandbox.momodeveloper.mtn.com
      Uganda Production:   https://proxy.momoapi.mtn.com
      Generic Sandbox:     https://sandbox.momodeveloper.mtn.com
      Generic Production:  https://proxy.momoapi.mtn.com
    """

    # Country-specific base URLs
    COUNTRY_URLS = {
        "rw": {"sandbox": "https://sandbox.momodeveloper.mtn.co.rw", "production": "https://momoapi.mtn.co.rw"},
        "ug": {"sandbox": "https://sandbox.momodeveloper.mtn.com", "production": "https://proxy.momoapi.mtn.com"},
        "gh": {"sandbox": "https://sandbox.momodeveloper.mtn.com", "production": "https://proxy.momoapi.mtn.com"},
        "cm": {"sandbox": "https://sandbox.momodeveloper.mtn.com", "production": "https://proxy.momoapi.mtn.com"},
    }

    SANDBOX_BASE = "https://sandbox.momodeveloper.mtn.co.rw"
    PRODUCTION_BASE = "https://momoapi.mtn.co.rw"

    def __init__(
        self,
        api_key: str = "",
        api_user: str = "",
        api_secret: str = "",
        subscription_key: str = "",
        callback_url: str = "",
        environment: str = "sandbox",
    ):
        self.api_key = api_key
        self.api_user = api_user
        self.api_secret = api_secret
        self.subscription_key = subscription_key
        self.callback_url = callback_url
        self.environment = environment

        self._base_url = (
            self.PRODUCTION_BASE if environment == "production" else self.SANDBOX_BASE
        )
        self._token: Optional[str] = None
        self._token_expires: Optional[datetime] = None
        self._http = httpx.AsyncClient(timeout=30.0)

    @property
    def provider_name(self) -> str:
        return "mtn_momo"

    # ── Authentication ───────────────────────────────────────────────

    async def authenticate(self) -> str:
        """Get OAuth2 token from MTN. Cached until expiry."""
        if self._token and self._token_expires and datetime.utcnow() < self._token_expires:
            return self._token

        url = f"{self._base_url}/collection/token/"
        headers = {
            "Authorization": f"Basic {self._encode_credentials()}",
            "Ocp-Apim-Subscription-Key": self.subscription_key,
        }

        resp = await self._http.post(url, headers=headers)
        resp.raise_for_status()
        data = resp.json()

        self._token = data["access_token"]
        self._token_expires = datetime.utcnow() + timedelta(seconds=data.get("expires_in", 3600) - 60)
        logger.info("MTN MoMo token refreshed, expires %s", self._token_expires)
        return self._token

    def _encode_credentials(self) -> str:
        """Base64-encode api_user:api_secret."""
        import base64
        return base64.b64encode(f"{self.api_user}:{self.api_secret}".encode()).decode()

    def _auth_headers(self, token: str) -> dict:
        return {
            "Authorization": f"Bearer {token}",
            "X-Reference-Id": str(uuid.uuid4()),
            "X-Target-Environment": self.environment,
            "Ocp-Apim-Subscription-Key": self.subscription_key,
            "Content-Type": "application/json",
        }

    # ── Collection (Request to Pay) ──────────────────────────────────

    async def collect(self, request: PaymentRequest) -> PaymentResponse:
        """
        Initiate a Request to Pay — pushes a payment prompt to the user's phone.
        """
        token = await self.authenticate()
        reference_id = str(uuid.uuid4())

        url = f"{self._base_url}/collection/v1_0/requesttopay/{reference_id}"
        headers = {
            "Authorization": f"Bearer {token}",
            "X-Reference-Id": reference_id,
            "X-Target-Environment": self.environment,
            "Ocp-Apim-Subscription-Key": self.subscription_key,
            "Content-Type": "application/json",
        }

        payload = {
            "amount": str(request.amount),
            "currency": request.currency,
            "externalId": request.reference,
            "payer": {
                "partyIdType": "MSISDN",
                "partyId": request.phone_number.lstrip("+"),
            },
            "payerMessage": request.description or "Mobibit Top-Up",
            "payeeNote": f"Ref: {request.reference}",
        }

        if request.callback_url:
            payload["payeeNote"] = request.callback_url

        logger.info("MTN collect: %s %s %s → ref=%s", request.amount, request.currency, request.phone_number, request.reference)

        try:
            resp = await self._http.post(url, json=payload, headers=headers)
            resp.raise_for_status()

            return PaymentResponse(
                provider=self.provider_name,
                provider_txn_id=reference_id,
                reference=request.reference,
                status=PaymentStatus.PENDING,
                amount=request.amount,
                currency=request.currency,
                phone_number=request.phone_number,
                message="Payment prompt sent to user's phone",
            )
        except httpx.HTTPStatusError as e:
            logger.error("MTN collect failed: %s %s", e.response.status_code, e.response.text)
            return PaymentResponse(
                provider=self.provider_name,
                provider_txn_id=reference_id,
                reference=request.reference,
                status=PaymentStatus.FAILED,
                amount=request.amount,
                currency=request.currency,
                phone_number=request.phone_number,
                message=f"Provider error: {e.response.status_code}",
            )

    # ── Status Check ─────────────────────────────────────────────────

    async def check_status(self, provider_txn_id: str) -> PaymentResponse:
        """Poll the status of a Request to Pay."""
        token = await self.authenticate()

        url = f"{self._base_url}/collection/v1_0/requesttopay/{provider_txn_id}"
        headers = {
            "Authorization": f"Bearer {token}",
            "X-Target-Environment": self.environment,
            "Ocp-Apim-Subscription-Key": self.subscription_key,
        }

        resp = await self._http.get(url, headers=headers)
        resp.raise_for_status()
        data = resp.json()

        status_map = {
            "PENDING": PaymentStatus.PENDING,
            "PROCESSING": PaymentStatus.PROCESSING,
            "SUCCESSFUL": PaymentStatus.SUCCESSFUL,
            "FAILED": PaymentStatus.FAILED,
        }

        return PaymentResponse(
            provider=self.provider_name,
            provider_txn_id=provider_txn_id,
            reference=data.get("externalId", ""),
            status=status_map.get(data.get("status", ""), PaymentStatus.PENDING),
            amount=float(data.get("amount", 0)),
            currency=data.get("currency", ""),
            phone_number=data.get("payer", {}).get("partyId", ""),
            fee=float(data.get("fee", 0)),
            message=data.get("reason", ""),
        )

    # ── Validation ───────────────────────────────────────────────────

    async def validate_phone(self, phone_number: str) -> bool:
        """Validate that the phone number is an MTN subscriber."""
        # MTN numbers: +2567xx, +23324x, +23325x, +23320x
        cleaned = phone_number.lstrip("+")
        # Uganda: 256 70x-78x
        # Ghana: 233 24x, 25x, 20x
        # Cameroon: 237 67x, 65x, 68x
        prefixes = [
            ("256", ["70", "71", "72", "73", "74", "75", "76", "77", "78"]),
            ("233", ["24", "25", "20"]),
            ("237", ["67", "65", "68"]),
        ]
        for country_code, pfxs in prefixes:
            if cleaned.startswith(country_code):
                local = cleaned[len(country_code):]
                return any(local.startswith(p) for p in pfxs)
        return False

    # ── Cleanup ──────────────────────────────────────────────────────

    async def close(self):
        await self._http.aclose()
