"""
LND Lightning Network service.

Wraps the LND REST API to:
  - Create invoices (receive BTC)
  - Pay invoices (send BTC)
  - Check wallet balance
  - Get node info

Docs: https://lightning.engineering/lnd.html
API:  https://lightning.engineering/lnd-operating-guide-rest-api
"""

from __future__ import annotations

import hashlib
import logging
from datetime import datetime
from typing import Optional

import httpx
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


# ── Models ──────────────────────────────────────────────────────────────


class Invoice(BaseModel):
    """A Lightning invoice for receiving BTC."""

    payment_request: str = Field(..., description="BOLT11 invoice string")
    r_hash: str = Field(..., description="Payment hash (hex)")
    amount_sats: int = Field(..., gt=0)
    description: str = ""
    expires_at: datetime
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Payment(BaseModel):
    """Result of paying a Lightning invoice."""

    payment_hash: str
    payment_preimage: str
    amount_sats: int
    fee_sats: int
    status: str  # "SUCCEEDED" | "FAILED" | "IN_FLIGHT"
    destination: str = ""
    payment_request: str = ""


class WalletBalance(BaseModel):
    """Lightning node wallet balance."""

    balance_sats: int
    pending_balance_sats: int = 0
    reserved_balance_sats: int = 0


class NodeInfo(BaseModel):
    """Lightning node info."""

    pubkey: str
    alias: str
    num_channels: int
    num_peers: int
    synced: bool
    chain: str = "bitcoin"
    network: str = "mainnet"


# ── LND Service ─────────────────────────────────────────────────────────


class LNDService:
    """
    LND REST API client.

    Usage:
        lnd = LNDService(host="localhost", port=8080, macaroon="hex...")
        invoice = await lnd.create_invoice(amount_sats=10000, memo="Top-up")
        payment = await lnd.pay_invoice(invoice.payment_request)
        balance = await lnd.get_balance()
    """

    def __init__(
        self,
        host: str = "localhost",
        port: int = 8080,
        macaroon_hex: str = "",
        tls_cert_path: str = "",
        network: str = "mainnet",
    ):
        self.host = host
        self.port = port
        self.network = network
        self._base_url = f"https://{host}:{port}"
        self._headers = {
            "Grpc-Metadata-macaroon": macaroon_hex,
            "Content-Type": "application/json",
        }
        self._http = httpx.AsyncClient(
            timeout=30.0,
            verify=tls_cert_path if tls_cert_path else False,
        )

    # ── Create Invoice (Receive BTC) ─────────────────────────────────

    async def create_invoice(
        self,
        amount_sats: int,
        memo: str = "",
        expiry_seconds: int = 3600,
    ) -> Invoice:
        """
        Create a Lightning invoice to receive BTC.

        Args:
            amount_sats: Amount in satoshis
            memo: Description for the invoice
            expiry_seconds: How long the invoice is valid (default: 1 hour)
        """
        url = f"{self._base_url}/v1/invoices"
        payload = {
            "value": str(amount_sats),
            "memo": memo,
            "expiry": str(expiry_seconds),
        }

        resp = await self._http.post(url, json=payload, headers=self._headers)
        resp.raise_for_status()
        data = resp.json()

        # Decode r_hash from bytes to hex
        r_hash = data.get("r_hash", "")
        if isinstance(r_hash, str):
            r_hash_hex = r_hash
        else:
            r_hash_hex = hashlib.sha256(r_hash).hexdigest() if r_hash else ""

        from datetime import timedelta
        created = datetime.utcnow()
        expires = created + timedelta(seconds=expiry_seconds)

        logger.info("Created invoice: %d sats, memo=%s", amount_sats, memo)

        return Invoice(
            payment_request=data["payment_request"],
            r_hash=r_hash_hex,
            amount_sats=amount_sats,
            description=memo,
            expires_at=expires,
            created_at=created,
        )

    # ── Pay Invoice (Send BTC) ───────────────────────────────────────

    async def pay_invoice(self, payment_request: str, amount_sats: Optional[int] = None) -> Payment:
        """
        Pay a Lightning invoice.

        Args:
            payment_request: BOLT11 invoice string
            amount_sats: Optional amount (needed for zero-amount invoices)
        """
        url = f"{self._base_url}/v1/channels/transactions"
        payload = {"paymentRequest": payment_request}
        if amount_sats:
            payload["amt"] = str(amount_sats)

        resp = await self._http.post(url, json=payload, headers=self._headers)
        resp.raise_for_status()
        data = resp.json()

        logger.info("Paid invoice: hash=%s status=%s", data.get("payment_hash", "?"), data.get("status", "?"))

        return Payment(
            payment_hash=data.get("payment_hash", ""),
            payment_preimage=data.get("payment_preimage", ""),
            amount_sats=int(data.get("amount", amount_sats or 0)),
            fee_sats=int(data.get("fee", 0)),
            status=data.get("status", "FAILED"),
            destination=data.get("destination", ""),
            payment_request=payment_request,
        )

    # ── Wallet Balance ───────────────────────────────────────────────

    async def get_balance(self) -> WalletBalance:
        """Get the Lightning node's on-chain and channel balance."""
        url = f"{self._base_url}/v1/balance/blockchain"
        resp = await self._http.get(url, headers=self._headers)
        resp.raise_for_status()
        data = resp.json()

        confirmed = int(data.get("confirmed_balance", 0))
        unconfirmed = int(data.get("unconfirmed_balance", 0))

        # Also get channel balance
        channel_url = f"{self._base_url}/v1/balance/channels"
        try:
            ch_resp = await self._http.get(channel_url, headers=self._headers)
            ch_data = ch_resp.json() if ch_resp.status_code == 200 else {}
        except Exception:
            ch_data = {}

        channel_balance = int(ch_data.get("local_balance", {}).get("sat", 0))

        return WalletBalance(
            balance_sats=confirmed + channel_balance,
            pending_balance_sats=unconfirmed,
            reserved_balance_sats=0,
        )

    # ── Node Info ────────────────────────────────────────────────────

    async def get_node_info(self) -> NodeInfo:
        """Get Lightning node information."""
        url = f"{self._base_url}/v1/getinfo"
        resp = await self._http.get(url, headers=self._headers)
        resp.raise_for_status()
        data = resp.json()

        chains = data.get("chains", [])
        chain = chains[0].get("chain", "bitcoin") if chains else "bitcoin"
        network = chains[0].get("network", self.network) if chains else self.network

        return NodeInfo(
            pubkey=data.get("identity_pubkey", ""),
            alias=data.get("alias", ""),
            num_channels=data.get("num_pending_channels", 0) + data.get("num_active_channels", 0),
            num_peers=data.get("num_peers", 0),
            synced=data.get("synced_to_chain", False),
            chain=chain,
            network=network,
        )

    # ── List Invoices ────────────────────────────────────────────────

    async def list_invoices(self, limit: int = 50) -> list[dict]:
        """List recent invoices."""
        url = f"{self._base_url}/v1/invoices?num_max_invoices={limit}&reversed=true"
        resp = await self._http.get(url, headers=self._headers)
        resp.raise_for_status()
        data = resp.json()
        return data.get("invoices", [])

    # ── Cleanup ──────────────────────────────────────────────────────

    async def close(self):
        await self._http.aclose()
