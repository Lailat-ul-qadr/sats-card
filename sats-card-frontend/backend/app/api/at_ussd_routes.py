"""
Africa's Talking USSD Routes
=============================
Handles USSD callbacks from Africa's Talking gateway.

When a user dials your service code (e.g. *123#):
  1. AT POSTs to /api/at/ussd with sessionId, serviceCode, phoneNumber, text
  2. We process through our USSD handler
  3. Return CON (continue) or END (terminate) response

Setup:
  1. Register at africastalking.com
  2. Create a USSD app in the dashboard
  3. Set callback URL to: https://your-domain.com/api/at/ussd
  4. Register a service code (e.g. *123#)
  5. Add API key to backend/.env
"""

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
from typing import Optional
import logging

from ..adapters.africastalking import AfricasTalkingUSSD, ATUSSDRequest
from ..ussd.handler import USSDHandler, USSDResponse

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/at", tags=["africastalking"])

# Global handler instance (initialized on startup)
_ussd_handler = USSDHandler()


def get_ussd_handler() -> USSDHandler:
    return _ussd_handler


# ── Africa's Talking USSD Callback ──────────────────────────────────

@router.post("/ussd", response_class=PlainTextResponse)
async def at_ussd_callback(request: Request):
    """
    Africa's Talking USSD callback endpoint.

    AT sends POST with form-encoded data:
      - sessionId: unique session ID
      - serviceCode: USSD code dialed (e.g. *123#)
      - phoneNumber: user's phone (e.g. +256701234567)
      - text: accumulated input (e.g. "1*2*50000")

    We respond with plain text:
      - "CON menu text" to continue session
      - "END final text" to end session
    """
    try:
        # Parse form data from AT (supports both form and JSON)
        content_type = request.headers.get("content-type", "")
        if "json" in content_type:
            body = await request.json()
            session_id = body.get("sessionId", "")
            service_code = body.get("serviceCode", "")
            phone_number = body.get("phoneNumber", "")
            text = body.get("text", "")
        else:
            form = await request.form()
            session_id = form.get("sessionId", "")
            service_code = form.get("serviceCode", "")
            phone_number = form.get("phoneNumber", "")
            text = form.get("text", "")

        if not session_id or not phone_number:
            logger.error("Missing required fields from AT callback")
            return PlainTextResponse("END Invalid request. Please try again.")

        logger.info("AT USSD: session=%s phone=%s text=%s", session_id, phone_number, text)

        # Parse the accumulated text
        # AT sends: "1" for first input, "1*2" for second, "1*2*50000" for third
        adapter = AfricasTalkingUSSD(api_key="dummy")  # Just for parsing
        inputs = adapter.parse_input(text)

        # The last input is the current user input
        current_input = inputs[-1] if inputs else ""

        # Process through our USSD handler
        handler = get_ussd_handler()
        response = handler.handle(
            session_id=session_id,
            phone_number=phone_number,
            user_input=current_input,
        )

        # Format response for AT gateway
        return PlainTextResponse(adapter.format_response(response.text, response.continue_session))

    except Exception as e:
        logger.error("AT USSD callback error: %s", e)
        return PlainTextResponse("END An error occurred. Please try again later.")


# ── Alternative: JSON API for testing ──────────────────────────────

class ATUSSDTestRequest(BaseModel):
    """For testing the AT USSD flow via JSON API."""
    session_id: str
    phone_number: str
    text: str = ""
    service_code: str = "*123#"


@router.post("/ussd/test", response_class=PlainTextResponse)
async def at_ussd_test(req: ATUSSDTestRequest):
    """
    Test endpoint for AT USSD flow (JSON instead of form data).

    Use this to test without Africa's Talking gateway.
    """
    adapter = AfricasTalkingUSSD(api_key="dummy")
    inputs = adapter.parse_input(req.text)
    current_input = inputs[-1] if inputs else ""

    handler = get_ussd_handler()
    response = handler.handle(
        session_id=req.session_id,
        phone_number=req.phone_number,
        user_input=current_input,
    )

    return PlainTextResponse(adapter.format_response(response.text, response.continue_session))


# ── SMS Notification ────────────────────────────────────────────────

class SMSPayload(BaseModel):
    phone_number: str
    message: str


@router.post("/sms")
async def send_sms(payload: SMSPayload):
    """Send SMS notification via Africa's Talking."""
    import os
    api_key = os.getenv("AT_API_KEY", "")
    username = os.getenv("AT_USERNAME", "sandbox")

    if not api_key:
        return {"error": "AT_API_KEY not configured"}

    adapter = AfricasTalkingUSSD(api_key=api_key, username=username)
    result = await adapter.send_sms(payload.phone_number, payload.message)
    return result
