"""
Bitcoin Lightning Network Routes
=================================
API endpoints for Bitcoin Lightning payments via Strike API.

Endpoints:
  POST /api/lightning/invoice     - Create invoice (receive BTC)
  GET  /api/lightning/invoice/:id - Check invoice status
  POST /api/lightning/pay         - Send BTC via Lightning
  GET  /api/lightning/rate        - Get BTC exchange rate
  POST /api/lightning/webhook     - Strike webhook callback
"""

from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel, Field
from typing import Optional
import logging
import os
import hashlib
import hmac

from ..adapters.lightning import StrikeLightning, LightningInvoice

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/lightning", tags=["lightning"])


def get_strike() -> StrikeLightning:
    """Get Strike API client from environment."""
    api_key = os.getenv("STRIKE_API_KEY", "")
    env = os.getenv("STRIKE_ENVIRONMENT", "sandbox")
    if not api_key:
        raise HTTPException(status_code=503, detail="STRIKE_API_KEY not configured")
    return StrikeLightning(api_key=api_key, environment=env)


# ── Create Invoice (Receive BTC) ───────────────────────────────────

class CreateInvoiceRequest(BaseModel):
    amount: float = Field(..., gt=0, description="Amount in fiat currency")
    currency: str = Field("USD", description="Currency code: USD, UGX, etc.")
    description: str = "Sats Card Top-Up"
    correlation_id: Optional[str] = Field(None, description="Your unique reference")


class CreateInvoiceResponse(BaseModel):
    invoice_id: str
    bolt11: str
    amount_fiat: float
    currency: str
    state: str
    message: str


@router.post("/invoice", response_model=CreateInvoiceResponse)
async def create_invoice(req: CreateInvoiceRequest):
    """
    Create a Lightning invoice to receive BTC payment.

    Flow:
      1. Create invoice in fiat amount
      2. Generate quote -> get BOLT11 invoice
      3. Return BOLT11 to show as QR code
      4. User scans QR with Lightning wallet
      5. Payment arrives -> webhook confirms -> credit user
    """
    try:
        strike = get_strike()

        # Create invoice
        invoice = await strike.create_invoice(
            amount=req.amount,
            currency=req.currency,
            description=req.description,
            correlation_id=req.correlation_id,
        )

        # Generate quote to get BOLT11
        bolt11 = await strike.generate_quote(invoice.invoice_id)

        return CreateInvoiceResponse(
            invoice_id=invoice.invoice_id,
            bolt11=bolt11,
            amount_fiat=req.amount,
            currency=req.currency,
            state="UNPAID",
            message="Scan this Lightning invoice with your wallet to pay",
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Create invoice failed: %s", e)
        raise HTTPException(status_code=500, detail=str(e))


# ── Check Invoice Status ───────────────────────────────────────────

@router.get("/invoice/{invoice_id}")
async def check_invoice(invoice_id: str):
    """Check if a Lightning invoice has been paid."""
    try:
        strike = get_strike()
        status = await strike.get_invoice_status(invoice_id)
        return status
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Check invoice failed: %s", e)
        raise HTTPException(status_code=500, detail=str(e))


# ── Send BTC Payment ───────────────────────────────────────────────

class SendPaymentRequest(BaseModel):
    bolt11_invoice: str = Field(..., description="BOLT11 Lightning invoice to pay")
    description: str = "Sats Card BTC Transfer"


class SendPaymentResponse(BaseModel):
    payment_id: str
    state: str
    message: str


@router.post("/pay", response_model=SendPaymentResponse)
async def send_payment(req: SendPaymentRequest):
    """
    Send BTC via Lightning Network.

    Flow:
      1. User provides a Lightning invoice (from their wallet)
      2. We create a quote for the amount
      3. Execute the payment
      4. Deduct from user's BTC balance
    """
    try:
        strike = get_strike()
        payment = await strike.send_payment(
            bolt11_invoice=req.bolt11_invoice,
            description=req.description,
        )

        return SendPaymentResponse(
            payment_id=payment.payment_id,
            state=payment.state,
            message="Payment initiated" if payment.state == "CREATED" else f"Payment {payment.state}",
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Send payment failed: %s", e)
        raise HTTPException(status_code=500, detail=str(e))


# ── Exchange Rate ──────────────────────────────────────────────────

@router.get("/rate")
async def get_btc_rate(currency: str = "USD"):
    """Get current BTC exchange rate from Strike."""
    try:
        strike = get_strike()
        rate = await strike.get_btc_rate(currency)
        return {
            "currency": currency,
            "rate": rate,
            "source": "strike",
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Get rate failed: %s", e)
        raise HTTPException(status_code=500, detail=str(e))


# ── Strike Webhook ─────────────────────────────────────────────────

@router.post("/webhook")
async def strike_webhook(request: Request):
    """
    Strike webhook callback for payment confirmations.

    Strike sends POST when:
      - Invoice is paid
      - Payment is completed
      - Quote expires

    Verify the webhook signature before processing.
    """
    try:
        body = await request.json()
        event_type = body.get("eventType", "")
        logger.info("Strike webhook: %s", event_type)

        if event_type == "invoice.paid":
            invoice_id = body.get("data", {}).get("invoiceId", "")
            logger.info("Invoice paid: %s", invoice_id)
            # TODO: Credit user's BTC balance in database

        elif event_type == "payment.completed":
            payment_id = body.get("data", {}).get("paymentId", "")
            logger.info("Payment completed: %s", payment_id)
            # TODO: Update transaction status in database

        return {"status": "ok"}
    except Exception as e:
        logger.error("Strike webhook error: %s", e)
        return {"status": "error", "message": str(e)}
