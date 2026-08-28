"""
Bitcoin Lightning Network Routes
=================================
API endpoints for Bitcoin Lightning payments.

Supports:
  - LND direct (regtest via Polar) — default when STRIKE_API_KEY is empty
  - Strike API (sandbox/production) — when STRIKE_API_KEY is set

Endpoints:
  POST /api/lightning/invoice     - Create invoice (receive BTC)
  GET  /api/lightning/invoice/:id - Check invoice status
  POST /api/lightning/pay         - Send BTC via Lightning
  GET  /api/lightning/rate        - Get BTC exchange rate
  POST /api/lightning/webhook     - Strike webhook callback
"""

from fastapi import APIRouter, HTTPException, Depends, Header, Request
from pydantic import BaseModel, Field
from typing import Optional
import logging
import os
import hashlib
import hmac

from ..core.config import settings
from ..services.lnd import LNDService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/lightning", tags=["lightning"])


# ── Helper: get LND service ─────────────────────────────────────────

def get_lnd() -> LNDService:
    """Get LND service client from config."""
    return LNDService(
        host=settings.LND_HOST,
        port=settings.LND_REST_PORT,
        macaroon_hex=settings.LND_MACAROON_HEX,
        tls_cert_path=settings.LND_TLS_CERT_PATH,
        network=settings.LND_NETWORK,
    )


# ── Create Invoice (Receive BTC) ───────────────────────────────────

class CreateInvoiceRequest(BaseModel):
    amount: float = Field(..., gt=0, description="Amount in sats")
    currency: str = Field("sats", description="Currency: sats or USD")
    description: str = "Mobibit Top-Up"
    correlation_id: Optional[str] = Field(None, description="Your unique reference")


class CreateInvoiceResponse(BaseModel):
    invoice_id: str
    bolt11: str
    amount_sats: int
    description: str
    state: str
    message: str


@router.post("/invoice", response_model=CreateInvoiceResponse)
async def create_invoice(req: CreateInvoiceRequest):
    """
    Create a Lightning invoice to receive BTC.

    For regtest (LND):
      1. Create invoice in sats via LND
      2. Return BOLT11 for scanning/paying
    """
    try:
        lnd = get_lnd()

        # Convert amount to sats
        amount_sats = int(req.amount) if req.currency == "sats" else int(req.amount * 100_000_000)

        invoice = await lnd.create_invoice(
            amount_sats=amount_sats,
            memo=req.description,
            expiry_seconds=3600,
        )

        return CreateInvoiceResponse(
            invoice_id=invoice.r_hash,
            bolt11=invoice.payment_request,
            amount_sats=amount_sats,
            description=req.description,
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
        lnd = get_lnd()

        # List invoices and find by payment hash
        invoices = await lnd.list_invoices(limit=50)
        for inv in invoices:
            r_hash = inv.get("r_hash", "")
            # r_hash may be base64 or hex depending on LND version
            if isinstance(r_hash, str) and (r_hash == invoice_id or inv.get("payment_request", "")[:20] == invoice_id[:20]):
                state = inv.get("state", "OPEN")
                return {
                    "invoice_id": invoice_id,
                    "state": state,  # OPEN, ACCEPTED, CANCELED, SETTLED
                    "amount_sats": int(inv.get("value", 0)),
                    "payment_request": inv.get("payment_request", ""),
                }

        # Not found — return OPEN
        return {
            "invoice_id": invoice_id,
            "state": "OPEN",
            "amount_sats": 0,
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Check invoice failed: %s", e)
        raise HTTPException(status_code=500, detail=str(e))


# ── Send BTC Payment ───────────────────────────────────────────────

class SendPaymentRequest(BaseModel):
    bolt11_invoice: str = Field(..., description="BOLT11 Lightning invoice to pay")
    description: str = "Mobibit BTC Transfer"
    amount_sats: Optional[int] = Field(None, description="Amount in sats (for zero-amount invoices)")


class SendPaymentResponse(BaseModel):
    payment_hash: str
    status: str
    fee_sats: int
    message: str


@router.post("/pay", response_model=SendPaymentResponse)
async def send_payment(req: SendPaymentRequest):
    """
    Send BTC via Lightning Network.

    Flow:
      1. User provides a Lightning invoice
      2. LND pays the invoice
      3. Deduct from user's BTC balance
    """
    try:
        lnd = get_lnd()

        payment = await lnd.pay_invoice(
            payment_request=req.bolt11_invoice,
            amount_sats=req.amount_sats,
        )

        return SendPaymentResponse(
            payment_hash=payment.payment_hash,
            status=payment.status,
            fee_sats=payment.fee_sats,
            message="Payment sent successfully" if payment.status == "SUCCEEDED" else f"Payment {payment.status}",
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Send payment failed: %s", e)
        raise HTTPException(status_code=500, detail=str(e))


# ── Exchange Rate ──────────────────────────────────────────────────

@router.get("/rate")
async def get_btc_rate(currency: str = "USD"):
    """Get current BTC exchange rate (uses CoinGecko for regtest)."""
    try:
        import httpx

        # For regtest, use a fixed test rate
        if settings.LND_NETWORK == "regtest":
            return {
                "currency": currency,
                "rate": 60000.00 if currency == "USD" else 0,
                "source": "regtest-fixed",
                "network": "regtest",
            }

        # For mainnet, use CoinGecko
        url = f"https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies={currency.lower()}"
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            data = resp.json()
            rate = data.get("bitcoin", {}).get(currency.lower(), 0)

        return {
            "currency": currency,
            "rate": rate,
            "source": "coingecko",
        }
    except Exception as e:
        logger.error("Get rate failed: %s", e)
        # Fallback rate for regtest
        if settings.LND_NETWORK == "regtest":
            return {"currency": currency, "rate": 60000.00, "source": "regtest-fallback"}
        raise HTTPException(status_code=500, detail=str(e))


# ── Node Info ──────────────────────────────────────────────────────

@router.get("/info")
async def get_node_info():
    """Get Lightning node info (pubkey, alias, chain, sync status)."""
    try:
        lnd = get_lnd()
        info = await lnd.get_node_info()
        return info.model_dump()
    except Exception as e:
        logger.error("Get node info failed: %s", e)
        raise HTTPException(status_code=500, detail=str(e))


# ── Wallet Balance ─────────────────────────────────────────────────

@router.get("/balance")
async def get_wallet_balance():
    """Get Lightning wallet balance."""
    try:
        lnd = get_lnd()
        balance = await lnd.get_balance()
        return balance.model_dump()
    except Exception as e:
        logger.error("Get wallet balance failed: %s", e)
        raise HTTPException(status_code=500, detail=str(e))


# ── Strike Webhook (legacy) ───────────────────────────────────────

@router.post("/webhook")
async def strike_webhook(request: Request):
    """
    Strike webhook callback for payment confirmations.
    Used when Strike API is configured.
    """
    try:
        body = await request.json()
        event_type = body.get("eventType", "")
        logger.info("Strike webhook: %s", event_type)
        return {"status": "ok"}
    except Exception as e:
        logger.error("Strike webhook error: %s", e)
        return {"status": "error", "message": str(e)}
