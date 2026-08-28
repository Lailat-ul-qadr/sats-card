"""
Orange Money API adapter.

Implements the Orange Money Web Payment API.
Docs: https://developer.orange.com/apis/om-webpay

Flow:
  1. Authenticate → get OAuth2 token
  2. Init Payment → redirect or push to user
  3. Check Status → poll for result
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
)

logger = logging.getLogger(__name__)


class OrangeMoneyAdapter(MobileMoneyAdapter):
    """
    Orange Money adapter for West Africa.
    """

    SANDBOX_BASE = "https://api.orange.com/orange-money-webpay/dev/v1"
    PRODUCTION_BASE = "https://api.orange.com/orange-money-webpay/v1"

    def __init__(
        self,
        client_id: str = "",
        client_secret: str = "",
        environment: str = "sandbox",
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.environment = environment
        self._base_url = (
            self.PRODUCTION_BASE if environment == "production" else self.SANDBOX_BASE
        )
        self._token: Optional[str] = None
        self._token_expires: Optional[datetime] = None
        self._http = httpx.AsyncClient(timeout=30.0)

    @property
    def provider_name(self) -> str:
        return "orange_money"

    # ── Authentication ───────────────────────────────────────────────

    async def authenticate(self) -> str:
        if self._token and self._token_expires and datetime.utcnow() < self._token_expires:
            return self._token

        url = "https://api.orange.com/oauth/v3/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }

        resp = await self._http.post(url, data=data, headers=headers)
        resp.raise_for_status()
        result = resp.json()

        self._token = result["access_token"]
        self._token_expires = datetime.utcnow() + timedelta(seconds=result.get("expires_in", 3600) - 60)
        logger.info("Orange Money token refreshed")
        return self._token

    def _auth_headers(self, token: str) -> dict:
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

    # ── Payment Initiation ───────────────────────────────────────────

    async def collect(self, request: PaymentRequest) -> PaymentResponse:
        """Initiate a payment via Orange Money."""
        token = await self.authenticate()
        reference_id = str(uuid.uuid4())

        url = f"{self._base_url}/webpayment"
        headers = self._auth_headers(token)

        payload = {
            "merchant_key": self.client_id,
            "currency": self._orange_currency(request.currency),
            "order_id": request.reference,
            "amount": request.amount,
            "return_url": request.callback_url or "https://yourdomain.com/payment/return",
            "cancel_url": request.callback_url or "https://yourdomain.com/payment/cancel",
            "notif_url": request.callback_url or "",
            "lang": "en",
        }

        logger.info("Orange collect: %s %s %s → ref=%s", request.amount, request.currency, request.phone_number, request.reference)

        try:
            resp = await self._http.post(url, json=payload, headers=headers)
            resp.raise_for_status()
            data = resp.json()

            pay_token = data.get("pay_token", reference_id)
            payment_url = data.get("payment_url", "")

            return PaymentResponse(
                provider=self.provider_name,
                provider_txn_id=pay_token,
                reference=request.reference,
                status=PaymentStatus.PENDING,
                amount=request.amount,
                currency=request.currency,
                phone_number=request.phone_number,
                message=f"Payment URL: {payment_url}" if payment_url else "Payment initiated",
            )
        except httpx.HTTPStatusError as e:
            logger.error("Orange collect failed: %s %s", e.response.status_code, e.response.text)
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
        token = await self.authenticate()

        url = f"{self._base_url}/webpayment/{provider_txn_id}"
        headers = self._auth_headers(token)

        resp = await self._http.get(url, headers=headers)
        resp.raise_for_status()
        data = resp.json()

        status_map = {
            "SUCCESS": PaymentStatus.SUCCESSFUL,
            "PENDING": PaymentStatus.PENDING,
            "FAILED": PaymentStatus.FAILED,
            "EXPIRED": PaymentStatus.TIMEOUT,
        }

        return PaymentResponse(
            provider=self.provider_name,
            provider_txn_id=provider_txn_id,
            reference=data.get("order_id", ""),
            status=status_map.get(data.get("status", ""), PaymentStatus.PENDING),
            amount=float(data.get("amount", 0)),
            currency=data.get("currency", ""),
            phone_number="",
            message=data.get("msg", ""),
        )

    # ── Validation ───────────────────────────────────────────────────

    async def validate_phone(self, phone_number: str) -> bool:
        """Validate Orange subscriber numbers."""
        cleaned = phone_number.lstrip("+")
        prefixes = [
            ("225", ["01", "05", "07", "08"]),   # Côte d'Ivoire
            ("221", ["70", "71", "72", "73", "74", "75", "76", "77", "78"]),  # Senegal
            ("223", ["70", "71", "72", "73", "74", "75", "76", "77", "78"]),  # Mali
            ("226", ["60", "61", "62", "63", "64", "65", "66", "67", "68"]),  # Burkina Faso
            ("227", ["90", "91", "92", "93", "94", "95", "96", "97", "98"]),  # Niger
            ("228", ["90", "91", "92", "93", "94", "95", "96", "97", "98"]),  # Togo
        ]
        for country_code, pfxs in prefixes:
            if cleaned.startswith(country_code):
                local = cleaned[len(country_code):]
                return any(local.startswith(p) for p in pfxs)
        return False

    @staticmethod
    def _orange_currency(code: str) -> str:
        """Map ISO currency codes to Orange Money currency format."""
        return {
            "XOF": "XOF", "CFA": "XOF",
            "UGX": "UGX", "KES": "KES",
            "XAF": "XAF",
        }.get(code.upper(), "XOF")

    async def close(self):
        await self._http.aclose()
