"""
Africa's Talking USSD Gateway Adapter
=====================================
Handles USSD sessions via Africa's Talking API.

AT sends POST to your callback URL with:
  - sessionId: unique session identifier
  - serviceCode: the USSD code dialed (e.g. *123#)
  - phoneNumber: user's phone number
  - text: accumulated user input (colon-separated)

Your response must start with:
  - "CON " to keep the session alive (show more menus)
  - "END " to terminate the session (show final message)
"""

import httpx
import logging
from typing import Optional
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class ATUSSDRequest(BaseModel):
    """Incoming request from Africa's Talking USSD gateway."""
    sessionId: str
    serviceCode: str
    phoneNumber: str
    text: str = ""


class ATUSSDResponse(BaseModel):
    """Response to send back to Africa's Talking."""
    text: str  # Must start with CON or END


class AfricasTalkingUSSD:
    """
    Africa's Talking USSD adapter.

    Flow:
      1. User dials *123# (your registered service code)
      2. AT POSTs to your callback URL with session params
      3. You return CON/menu text or END/final text
      4. AT shows the text on the user's phone
      5. User replies, AT POSTs again with accumulated text
      6. Repeat until you return END
    """

    def __init__(self, api_key: str, username: str = "sandbox"):
        self.api_key = api_key
        self.username = username
        self.base_url = "https://api.africastalking.com"
        self.headers = {
            "apiKey": api_key,
            "Accept": "application/json",
        }

    def parse_input(self, text: str) -> list[str]:
        """
        Parse accumulated text from AT.
        Format: "1*2*3" -> ["1", "2", "3"]
        First item is the first user input, subsequent items are follow-ups.
        """
        if not text:
            return []
        return text.split("*")

    def format_response(self, text: str, continue_session: bool = True) -> str:
        """
        Format response for AT gateway.
        CON = continue session, END = terminate session.
        """
        prefix = "CON " if continue_session else "END "
        return prefix + text

    async def send_airtime(self, phone_number: str, amount: float, currency: str = "UGX") -> dict:
        """
        Send airtime to a phone number (used for cashback/rewards).
        POST https://api.africastalking.com/version1/airtime
        """
        url = f"{self.base_url}/version1/airtime"
        payload = {
            "username": self.username,
            "recipients": [
                {
                    "phoneNumber": phone_number,
                    "amount": amount,
                    "currencyCode": currency,
                }
            ],
        }
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                resp = await client.post(url, json=payload, headers=self.headers)
                resp.raise_for_status()
                return resp.json()
        except Exception as e:
            logger.error("Airtime send failed: %s", e)
            return {"error": str(e)}

    async def send_sms(self, phone_number: str, message: str) -> dict:
        """
        Send SMS notification.
        POST https://api.africastalking.com/version1/messaging
        """
        url = f"{self.base_url}/version1/messaging"
        payload = {
            "username": self.username,
            "recipients": [phone_number],
            "message": message,
        }
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                resp = await client.post(url, json=payload, headers=self.headers)
                resp.raise_for_status()
                return resp.json()
        except Exception as e:
            logger.error("SMS send failed: %s", e)
            return {"error": str(e)}
