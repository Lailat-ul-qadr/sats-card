"""
Bitcoin Lightning Network Adapter (Strike API)
===============================================
Uses Strike API to create invoices, generate Lightning payment requests,
and send/receive bitcoin over the Lightning Network.

Flow for receiving BTC (user buys bitcoin):
  1. Create invoice in USD/UGX amount
  2. Generate quote -> returns Lightning invoice (BOLT11)
  3. Show invoice/QR to user
  4. User pays via Lightning wallet
  5. Webhook confirms payment -> credit user's BTC balance

Flow for sending BTC (user sends bitcoin):
  1. User provides Lightning invoice or destination
  2. Create quote for the amount
  3. Execute payment
  4. Confirm delivery
"""

import httpx
import logging
from typing import Optional
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class LightningInvoice(BaseModel):
    """A Lightning invoice for receiving payment."""
    invoice_id: str
    bolt11: str  # The Lightning invoice string
    amount_fiat: float
    currency: str
    amount_sats: int
    state: str  # UNPAID, PAID, etc.
    qr_code_url: Optional[str] = None


class LightningPayment(BaseModel):
    """Result of sending a Lightning payment."""
    payment_id: str
    amount_sats: int
    amount_fiat: float
    currency: str
    state: str  # CREATED, COMPLETED, FAILED
    preimage: Optional[str] = None


class StrikeLightning:
    """
    Strike API adapter for Bitcoin Lightning Network.

    Environments:
      - Sandbox: https://api-strike.me (test with test API key)
      - Production: https://api.strike.me

    Key endpoints:
      POST /v1/invoices          - Create invoice
      POST /v1/invoices/{id}/quotes  - Generate quote (get BOLT11)
      POST /v1/payments          - Send payment
      GET  /v1/invoices/{id}     - Check invoice status
    """

    def __init__(self, api_key: str, environment: str = "sandbox"):
        self.api_key = api_key
        if environment == "sandbox":
            self.base_url = "https://api-strike.me"
        else:
            self.base_url = "https://api.strike.me"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    # ── Create Invoice ──────────────────────────────────────────────

    async def create_invoice(
        self,
        amount: float,
        currency: str = "USD",
        description: str = "Sats Card Top-Up",
        correlation_id: Optional[str] = None,
    ) -> LightningInvoice:
        """
        Create a Lightning invoice for receiving payment.

        Args:
            amount: Amount in fiat (e.g. 10.00 for $10)
            currency: Fiat currency code (USD, UGX, etc.)
            description: Invoice description
            correlation_id: Your unique reference ID

        Returns:
            LightningInvoice with BOLT11 string and details
        """
        url = f"{self.base_url}/v1/invoices"
        payload = {
            "amount": {
                "amount": f"{amount:.2f}",
                "currency": currency,
            },
            "description": description,
        }
        if correlation_id:
            payload["correlationId"] = correlation_id

        try:
            async with httpx.AsyncClient(timeout=30) as client:
                resp = await client.post(url, json=payload, headers=self.headers)
                resp.raise_for_status()
                data = resp.json()

            invoice_id = data.get("invoiceId", "")
            return LightningInvoice(
                invoice_id=invoice_id,
                bolt11="",  # Need to generate quote to get BOLT11
                amount_fiat=amount,
                currency=currency,
                amount_sats=0,
                state=data.get("state", "UNPAID"),
            )
        except Exception as e:
            logger.error("Create invoice failed: %s", e)
            raise

    # ── Generate Quote (get BOLT11) ────────────────────────────────

    async def generate_quote(self, invoice_id: str, amount_sats: int = 0) -> str:
        """
        Generate a quote for an invoice, which produces the BOLT11 Lightning invoice string.

        The quote locks in an exchange rate for ~30 seconds.
        After that, you need to generate a new quote.

        Args:
            invoice_id: The invoice ID from create_invoice()
            amount_sats: Optional amount in sats (for USD-denominated invoices)

        Returns:
            BOLT11 Lightning invoice string
        """
        url = f"{self.base_url}/v1/invoices/{invoice_id}/quotes"
        payload = {}
        if amount_sats > 0:
            payload["amount"] = {
                "amount": str(amount_sats),
                "currency": "BTC",
            }

        try:
            async with httpx.AsyncClient(timeout=30) as client:
                resp = await client.post(url, json=payload, headers=self.headers)
                resp.raise_for_status()
                data = resp.json()

            bolt11 = data.get("bolt11", "")
            logger.info("Generated quote for invoice %s: %s...", invoice_id, bolt11[:20])
            return bolt11
        except Exception as e:
            logger.error("Generate quote failed: %s", e)
            raise

    # ── Send Payment ───────────────────────────────────────────────

    async def send_payment(
        self,
        bolt11_invoice: str,
        description: str = "Sats Card BTC Transfer",
    ) -> LightningPayment:
        """
        Send a Lightning payment to a BOLT11 invoice.

        Args:
            bolt11_invoice: The BOLT11 Lightning invoice to pay
            description: Payment description

        Returns:
            LightningPayment with status and details
        """
        url = f"{self.base_url}/v1/payments"
        payload = {
            "invoice": bolt11_invoice,
            "description": description,
        }

        try:
            async with httpx.AsyncClient(timeout=60) as client:
                resp = await client.post(url, json=payload, headers=self.headers)
                resp.raise_for_status()
                data = resp.json()

            return LightningPayment(
                payment_id=data.get("paymentId", ""),
                amount_sats=0,  # Extract from response
                amount_fiat=0,
                currency="BTC",
                state=data.get("state", "CREATED"),
                preimage=data.get("preimage"),
            )
        except Exception as e:
            logger.error("Send payment failed: %s", e)
            raise

    # ── Check Invoice Status ───────────────────────────────────────

    async def get_invoice_status(self, invoice_id: str) -> dict:
        """
        Check if an invoice has been paid.

        Returns:
            dict with state: UNPAID, PAID, etc.
        """
        url = f"{self.base_url}/v1/invoices/{invoice_id}"

        try:
            async with httpx.AsyncClient(timeout=15) as client:
                resp = await client.get(url, headers=self.headers)
                resp.raise_for_status()
                return resp.json()
        except Exception as e:
            logger.error("Get invoice status failed: %s", e)
            return {"state": "UNKNOWN", "error": str(e)}

    # ── Get Exchange Rate ──────────────────────────────────────────

    async def get_btc_rate(self, currency: str = "USD") -> float:
        """
        Get current BTC exchange rate from Strike.

        Returns:
            BTC price in the specified currency
        """
        url = f"{self.base_url}/v1/tickers"

        try:
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.get(url, headers=self.headers)
                resp.raise_for_status()
                data = resp.json()

            # Find the rate for the requested currency
            for ticker in data if isinstance(data, list) else []:
                if ticker.get("currency") == currency:
                    return float(ticker.get("price", 0))
            return 0
        except Exception as e:
            logger.error("Get BTC rate failed: %s", e)
            return 0
