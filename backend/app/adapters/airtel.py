"""
Airtel Money API adapter.

Implements the Airtel Africa Payment API (Collection / KYC).
Docs: https://developers.airtel.africa/documentation

Flow:
  1. Authenticate → get OAuth2 token
  2. Collection (CustomerPay) → push prompt to user
  3. Transaction Status → poll for result
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


class AirtelMoneyAdapter(MobileMoneyAdapter):
    """
    Airtel Africa Money adapter.

    Sandbox: https://openapi.airtel.africa
    Production: https://openapi.airtel.africa
    """

    BASE_URL = "https://openapi.airtel.africa"

    def __init__(
        self,
        client_id: str = "",
        client_secret: str = "",
        environment: str = "sandbox",
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.environment = environment
        self._token: Optional[str] = None
        self._token_expires: Optional[datetime] = None
        self._http = httpx.AsyncClient(timeout=30.0)

    @property
    def provider_name(self) -> str:
        return "airtel_money"

    # ── Authentication ───────────────────────────────────────────────

    async def authenticate(self) -> str:
        if self._token and self._token_expires and datetime.utcnow() < self._token_expires:
            return self._token

        url = f"{self.BASE_URL}/auth/oauth2/token"
        payload = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials",
        }

        resp = await self._http.post(url, json=payload)
        resp.raise_for_status()
        data = resp.json()

        self._token = data["access_token"]
        self._token_expires = datetime.utcnow() + timedelta(seconds=data.get("expires_in", 3600) - 60)
        logger.info("Airtel token refreshed")
        return self._token

    def _auth_headers(self, token: str) -> dict:
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "X-Country": "UG",  # Will be dynamic based on phone
            "X-Currency": "UGX",
        }

    # ── Collection ───────────────────────────────────────────────────

    async def collect(self, request: PaymentRequest) -> PaymentResponse:
        """Initiate CustomerPay — pushes a prompt to the user's phone."""
        token = await self.authenticate()
        reference_id = str(uuid.uuid4())

        # Determine country from phone prefix
        country = self._detect_country(request.phone_number)
        currency = self._currency_for_country(country)

        url = f"{self.BASE_URL}/airtelcash/v3/collections/"
        headers = {
            **self._auth_headers(token),
            "X-Country": country,
            "X-Currency": currency,
        }

        payload = {
            "reference": reference_id,
            "transaction": {
                "amount": str(request.amount),
                "country": country,
                "currency": currency,
                "customer": {
                    "msisdn": request.phone_number.lstrip("+"),
                },
            },
        }

        logger.info("Airtel collect: %s %s %s → ref=%s", request.amount, currency, request.phone_number, request.reference)

        try:
            resp = await self._http.post(url, json=payload, headers=headers)
            resp.raise_for_status()

            return PaymentResponse(
                provider=self.provider_name,
                provider_txn_id=reference_id,
                reference=request.reference,
                status=PaymentStatus.PENDING,
                amount=request.amount,
                currency=currency,
                phone_number=request.phone_number,
                message="Payment prompt sent to user's phone",
            )
        except httpx.HTTPStatusError as e:
            logger.error("Airtel collect failed: %s %s", e.response.status_code, e.response.text)
            return PaymentResponse(
                provider=self.provider_name,
                provider_txn_id=reference_id,
                reference=request.reference,
                status=PaymentStatus.FAILED,
                amount=request.amount,
                currency=currency,
                phone_number=request.phone_number,
                message=f"Provider error: {e.response.status_code}",
            )

    # ── Status Check ─────────────────────────────────────────────────

    async def check_status(self, provider_txn_id: str) -> PaymentResponse:
        token = await self.authenticate()

        url = f"{self.BASE_URL}/airtelcash/v3/collections/{provider_txn_id}"
        headers = self._auth_headers(token)

        resp = await self._http.get(url, headers=headers)
        resp.raise_for_status()
        data = resp.json()

        status_map = {
            "SUCCESS": PaymentStatus.SUCCESSFUL,
            "PENDING": PaymentStatus.PENDING,
            "FAILED": PaymentStatus.FAILED,
        }

        transaction = data.get("transaction", {})
        return PaymentResponse(
            provider=self.provider_name,
            provider_txn_id=provider_txn_id,
            reference=data.get("reference", ""),
            status=status_map.get(transaction.get("status", ""), PaymentStatus.PENDING),
            amount=float(transaction.get("amount", 0)),
            currency=transaction.get("currency", ""),
            phone_number=transaction.get("customer", {}).get("msisdn", ""),
            message=transaction.get("reason", ""),
        )

    # ── Validation ───────────────────────────────────────────────────

    async def validate_phone(self, phone_number: str) -> bool:
        """Validate Airtel subscriber numbers."""
        cleaned = phone_number.lstrip("+")
        prefixes = [
            ("256", ["70", "75"]),     # Uganda
            ("254", ["73", "74"]),     # Kenya
            ("255", ["68", "69"]),     # Tanzania
            ("176", ["70", "75"]),     # Rwanda
        ]
        for country_code, pfxs in prefixes:
            if cleaned.startswith(country_code):
                local = cleaned[len(country_code):]
                return any(local.startswith(p) for p in pfxs)
        return False

    # ── Helpers ──────────────────────────────────────────────────────

    @staticmethod
    def _detect_country(phone: str) -> str:
        cleaned = phone.lstrip("+")
        country_map = {
            "256": "UG", "254": "KE", "255": "TZ",
            "257": "BI", "250": "RW", "263": "ZW",
        }
        for code, country in country_map.items():
            if cleaned.startswith(code):
                return country
        return "UG"  # default

    @staticmethod
    def _currency_for_country(country: str) -> str:
        return {"UG": "UGX", "KE": "KES", "TZ": "TZS", "BI": "BIF", "RW": "RWF"}.get(country, "UGX")

    async def close(self):
        await self._http.aclose()
