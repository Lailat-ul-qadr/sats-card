"""
Safaricom MPESA (Daraja API) adapter.
=====================================
Implements the Safaricom Daraja API for M-Pesa payments.

Flow:
  1. Authenticate → get OAuth2 access token
  2. STK Push (Lipa Na M-Pesa) → push payment prompt to user's phone
  3. Callback → receive payment confirmation
  4. (Optional) Check Transaction Status

Docs: https://developer.safaricom.co.ke/APIs
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


class MPESAAdapter(MobileMoneyAdapter):
    """
    Safaricom MPESA adapter using Daraja API.

    Environments:
      - Sandbox: https://sandbox.safaricom.co.ke
      - Production: https://api.safaricom.co.ke

    Key endpoints:
      POST /oauth/v1/generate    - Get access token
      POST /mpesa/stkpush/v1/processrequest  - Initiate STK Push
      POST /mpesa/transactionstatus/v1/query  - Check transaction status
    """

    SANDBOX_BASE = "https://sandbox.safaricom.co.ke"
    PRODUCTION_BASE = "https://api.safaricom.co.ke"

    def __init__(
        self,
        consumer_key: str = "",
        consumer_secret: str = "",
        short_code: str = "",
        passkey: str = "",
        callback_url: str = "",
        environment: str = "sandbox",
    ):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.short_code = short_code
        self.passkey = passkey
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
        return "mpesa"

    # ── Authentication ───────────────────────────────────────────────

    async def authenticate(self) -> str:
        """Get OAuth2 token from Safaricom. Cached until expiry."""
        if self._token and self._token_expires and datetime.utcnow() < self._token_expires:
            return self._token

        url = f"{self._base_url}/oauth/v1/generate?grant_type=client_credentials"

        import base64
        credentials = base64.b64encode(
            f"{self.consumer_key}:{self.consumer_secret}".encode()
        ).decode()

        headers = {
            "Authorization": f"Basic {credentials}",
        }

        resp = await self._http.post(url, headers=headers)
        resp.raise_for_status()
        data = resp.json()

        self._token = data["access_token"]
        self._token_expires = datetime.utcnow() + timedelta(seconds=data.get("expires_in", 3600) - 60)
        logger.info("MPESA token refreshed, expires %s", self._token_expires)
        return self._token

    def _auth_headers(self, token: str) -> dict:
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

    def _generate_password(self) -> str:
        """Generate the password for STK Push."""
        import base64
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        data_to_encode = f"{self.short_code}{self.passkey}{timestamp}"
        return base64.b64encode(data_to_encode.encode()).decode()

    # ── STK Push (Request to Pay) ────────────────────────────────────

    async def collect(self, request: PaymentRequest) -> PaymentResponse:
        """
        Initiate STK Push — pushes a payment prompt to the user's phone.
        This is M-Pesa's "Lipa Na M-Pesa Online" (Pay with M-Pesa).
        """
        token = await self.authenticate()
        reference_id = str(uuid.uuid4())

        # Format phone number (remove + prefix, ensure 254 prefix)
        phone = request.phone_number.lstrip("+")
        if not phone.startswith("254"):
            phone = f"254{phone}"

        url = f"{self._base_url}/mpesa/stkpush/v1/processrequest"
        headers = self._auth_headers(token)

        payload = {
            "BusinessShortCode": self.short_code,
            "Password": self._generate_password(),
            "Timestamp": datetime.now().strftime("%Y%m%d%H%M%S"),
            "TransactionType": "CustomerBuyGoodsOnline",
            "Amount": str(int(request.amount)),
            "PartyA": phone,
            "PartyB": self.short_code,
            "PhoneNumber": phone,
            "CallBackURL": request.callback_url or self.callback_url,
            "AccountReference": request.reference,
            "TransactionDesc": request.description or "Mobibit Top-Up",
        }

        logger.info("MPESA collect: %s %s %s → ref=%s", request.amount, request.currency, request.phone_number, request.reference)

        try:
            resp = await self._http.post(url, json=payload, headers=headers)
            resp.raise_for_status()
            data = resp.json()

            return PaymentResponse(
                provider=self.provider_name,
                provider_txn_id=data.get("CheckoutRequestID", reference_id),
                reference=request.reference,
                status=PaymentStatus.PENDING,
                amount=request.amount,
                currency=request.currency,
                phone_number=request.phone_number,
                message=data.get("CustomerMessage", "STK Push sent to your phone"),
            )
        except httpx.HTTPStatusError as e:
            logger.error("MPESA collect failed: %s %s", e.response.status_code, e.response.text)
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
        """Check the status of an STK Push transaction."""
        token = await self.authenticate()

        url = f"{self._base_url}/mpesa/transactionstatus/v1/query"
        headers = self._auth_headers(token)

        payload = {
            "BusinessShortCode": self.short_code,
            "Password": self._generate_password(),
            "Timestamp": datetime.now().strftime("%Y%m%d%H%M%S"),
            "CheckoutRequestID": provider_txn_id,
        }

        resp = await self._http.post(url, json=payload, headers=headers)
        resp.raise_for_status()
        data = resp.json()

        # ResultCode: 0 = success, 1032 = cancelled, 1037 = timeout
        result_code = data.get("ResultCode", "")
        status_map = {
            "0": PaymentStatus.SUCCESSFUL,
            "1032": PaymentStatus.FAILED,
            "1037": PaymentStatus.TIMEOUT,
            "2001": PaymentStatus.FAILED,  # Wrong credentials
        }

        return PaymentResponse(
            provider=self.provider_name,
            provider_txn_id=provider_txn_id,
            reference=data.get("AccountReference", ""),
            status=status_map.get(str(result_code), PaymentStatus.PENDING),
            amount=0,  # Not returned in status check
            currency="KES",
            phone_number="",
            message=data.get("ResultDesc", ""),
        )

    # ── Validation ───────────────────────────────────────────────────

    async def validate_phone(self, phone_number: str) -> bool:
        """Validate that the phone number is an MPESA subscriber."""
        cleaned = phone_number.lstrip("+")
        # Kenya: +254 7XX, +254 1XX
        # Tanzania: +255 6XX, +255 7XX
        # Mozambique: +258 84, +258 85
        prefixes = [
            ("254", ["70", "71", "72", "73", "74", "75", "76", "77", "78", "79", "10", "11"]),
            ("255", ["60", "61", "62", "63", "64", "65", "66", "67", "68", "69",
                     "70", "71", "72", "73", "74", "75", "76", "77", "78", "79"]),
            ("258", ["84", "85"]),
        ]
        for country_code, pfxs in prefixes:
            if cleaned.startswith(country_code):
                local = cleaned[len(country_code):]
                return any(local.startswith(p) for p in pfxs)
        return False

    # ── Cleanup ──────────────────────────────────────────────────────

    async def close(self):
        await self._http.aclose()
