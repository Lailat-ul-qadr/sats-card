"""
SMS notification service — sends transaction confirmations via Africa's Talking.

Supports:
  - Transaction confirmations (fund, send, receive, spend)
  - Balance alerts
  - OTP verification codes
  - Fallback to console logging in sandbox mode

Docs: https://africastalking.com/docs
"""

from __future__ import annotations

import logging
from typing import Optional
from datetime import datetime

import httpx
from pydantic import BaseModel

from ..core.config import settings

logger = logging.getLogger(__name__)


# ── Message Templates ──────────────────────────────────────────────────


class SMSMessage(BaseModel):
    to: str
    message: str
    sender_id: str = ""


def fund_confirmation(phone: str, amount_fiat: float, currency: str, sats: int, ref: str) -> SMSMessage:
    """Mobile money → BTC confirmation."""
    return SMSMessage(
        to=phone,
        message=(
            f"✅ Mobibit Africa: {amount_fiat:,.0f} {currency} received!\n"
            f"Balance credited: {sats:,} sats\n"
            f"Ref: {ref}\n"
            f"View: mobibitafrica.com/dashboard"
        ),
    )


def send_confirmation(phone: str, sats: int, recipient: str, fee: int, ref: str) -> SMSMessage:
    """BTC sent via Lightning confirmation."""
    return SMSMessage(
        to=phone,
        message=(
            f"⚡ Mobibit Africa: {sats:,} sats sent!\n"
            f"To: {recipient}\n"
            f"Fee: {fee} sats\n"
            f"Ref: {ref}"
        ),
    )


def receive_confirmation(phone: str, sats: int, ref: str) -> SMSMessage:
    """BTC received via Lightning confirmation."""
    return SMSMessage(
        to=phone,
        message=(
            f"📥 Mobibit Africa: {sats:,} sats received!\n"
            f"Balance updated.\n"
            f"Ref: {ref}"
        ),
    )


def spend_confirmation(phone: str, amount_fiat: float, currency: str, sats: int, merchant: str, ref: str) -> SMSMessage:
    """Card spend confirmation."""
    return SMSMessage(
        to=phone,
        message=(
            f"💳 Mobibit Africa: {amount_fiat:,.2f} {currency} spent\n"
            f"At: {merchant}\n"
            f"Sats deducted: {sats:,}\n"
            f"Ref: {ref}"
        ),
    )


def balance_alert(phone: str, sats: int, btc: float, usd: float) -> SMSMessage:
    """Low balance alert."""
    return SMSMessage(
        to=phone,
        message=(
            f"⚠️ Mobibit Africa: Low balance!\n"
            f"Balance: {sats:,} sats ({btc:.8f} BTC)\n"
            f"≈ ${usd:.2f} USD\n"
            f"Top up: mobibitafrica.com/fund"
        ),
    )


def otp_message(phone: str, code: str) -> SMSMessage:
    """OTP verification code."""
    return SMSMessage(
        to=phone,
        message=f"Your Mobibit Africa verification code is: {code}\nValid for 5 minutes.",
    )


# ── SMS Service ────────────────────────────────────────────────────────


class SMSService:
    """
    Sends SMS messages via Africa's Talking API.

    In sandbox mode, messages are logged to console instead.

    Usage:
        sms = SMSService()
        await sms.send(fund_confirmation("+256701234567", 5000, "UGX", 85000, "SC-ABC123"))
    """

    AFRICASTALKING_URL = "https://api.africastalking.com/version1/messaging"
    TWILIO_URL = "https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json"

    def __init__(self):
        self.provider = settings.SMS_PROVIDER
        self.sender_id = settings.SMS_SENDER_ID
        self.api_key = settings.SMS_API_KEY
        self._http = httpx.AsyncClient(timeout=10.0)

    async def send(self, message: SMSMessage) -> dict:
        """
        Send an SMS message.

        Returns:
            {"success": bool, "message_id": str, "cost": str}
        """
        message.sender_id = message.sender_id or self.sender_id

        # Sandbox mode — log instead of sending
        if settings.DEBUG or not self.api_key:
            logger.info("📱 SMS [%s → %s]: %s", self.sender_id, message.to, message.message)
            return {
                "success": True,
                "message_id": f"sandbox_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
                "cost": "0",
                "mode": "sandbox",
            }

        try:
            if self.provider == "africastalking":
                return await self._send_africastalking(message)
            elif self.provider == "twilio":
                return await self._send_twilio(message)
            else:
                logger.warning("Unknown SMS provider: %s", self.provider)
                return {"success": False, "message_id": "", "cost": "0", "error": "Unknown provider"}
        except Exception as e:
            logger.error("SMS send failed: %s", e)
            return {"success": False, "message_id": "", "cost": "0", "error": str(e)}

    async def send_bulk(self, messages: list[SMSMessage]) -> list[dict]:
        """Send multiple SMS messages."""
        results = []
        for msg in messages:
            result = await self.send(msg)
            results.append(result)
        return results

    async def _send_africastalking(self, message: SMSMessage) -> dict:
        """Send via Africa's Talking API."""
        headers = {
            "apiKey": self.api_key,
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }
        data = {
            "username": "mobibit",  # Africa's Talking username
            "to": message.to,
            "message": message.message,
            "from": message.sender_id,
        }

        resp = await self._http.post(self.AFRICASTALKING_URL, data=data, headers=headers)
        resp.raise_for_status()
        result = resp.json()

        sms_data = result.get("SMSMessageData", {})
        recipients = sms_data.get("Recipients", [])
        first = recipients[0] if recipients else {}

        return {
            "success": first.get("status") == "Success",
            "message_id": first.get("messageId", ""),
            "cost": first.get("cost", "0"),
        }

    async def _send_twilio(self, message: SMSMessage) -> dict:
        """Send via Twilio API."""
        # Twilio requires account_sid and auth_token
        # For now, return sandbox
        logger.info("Twilio SMS not configured, logging: %s", message.message)
        return {"success": True, "message_id": "twilio_mock", "cost": "0", "mode": "sandbox"}

    async def close(self):
        await self._http.aclose()
