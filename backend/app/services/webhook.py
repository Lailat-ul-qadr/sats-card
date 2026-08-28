"""
Webhook handler service — processes payment confirmations from providers.

When MTN/Airtel/Orange confirms a payment, they POST to our webhook URL.
This service:
  1. Validates the webhook signature (if provided)
  2. Matches the payment to an existing transaction
  3. Updates the transaction status
  4. Credits the user's wallet
  5. Sends an SMS confirmation
"""

from __future__ import annotations

import hashlib
import hmac
import logging
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.transaction import Transaction, TransactionStatus
from ..models.wallet import Wallet
from ..services.transaction import TransactionService, TransactionError

logger = logging.getLogger(__name__)


class WebhookHandler:
    """
    Processes incoming webhook callbacks from mobile money providers.

    Usage:
        handler = WebhookHandler(db)
        result = await handler.process_mtn_webhook(payload)
    """

    def __init__(self, db: AsyncSession):
        self.db = db
        self.tx_service = TransactionService(db)

    # ── MTN MoMo Webhook ────────────────────────────────────────────

    async def process_mtn_webhook(self, payload: dict) -> dict:
        """
        Process MTN MoMo callback.

        MTN sends:
        {
            "externalId": "SC-A1B2C3D4E5F6",
            "amount": "5000",
            "currency": "UGX",
            "payer": {"partyIdType": "MSISDN", "partyId": "256771234567"},
            "status": "SUCCESSFUL",  // or FAILED, PENDING
            "reason": "...",
            "financialTransactionId": "...",
            "callbackMetadata": [...]
        }
        """
        reference = payload.get("externalId")
        status = payload.get("status", "").upper()
        provider_txn_id = payload.get("financialTransactionId", "")
        reason = payload.get("reason", "")

        logger.info("MTN webhook: ref=%s status=%s", reference, status)

        if not reference:
            logger.warning("MTN webhook missing externalId")
            return {"status": "ignored", "reason": "missing externalId"}

        # Process the status update
        result = await self.tx_service.process_webhook(
            provider="mtn_momo",
            provider_reference=reference,
            provider_status=status,
            raw_payload=payload,
        )

        if result:
            return {
                "status": "processed",
                "reference": reference,
                "transaction_status": result.status.value,
            }
        else:
            return {"status": "not_found", "reference": reference}

    # ── Airtel Money Webhook ────────────────────────────────────────

    async def process_airtel_webhook(self, payload: dict) -> dict:
        """
        Process Airtel Money callback.

        Airtel sends:
        {
            "transaction": {
                "id": "...",
                "status": "SUCCESS",
                "amount": "5000",
                "currency": "UGX",
                "customer": {"msisdn": "256771234567"}
            },
            "reference": "SC-A1B2C3D4E5F6"
        }
        """
        reference = payload.get("reference")
        transaction = payload.get("transaction", {})
        status = transaction.get("status", "").upper()

        logger.info("Airtel webhook: ref=%s status=%s", reference, status)

        if not reference:
            return {"status": "ignored", "reason": "missing reference"}

        result = await self.tx_service.process_webhook(
            provider="airtel_money",
            provider_reference=reference,
            provider_status=status,
            raw_payload=payload,
        )

        if result:
            return {
                "status": "processed",
                "reference": reference,
                "transaction_status": result.status.value,
            }
        else:
            return {"status": "not_found", "reference": reference}

    # ── Orange Money Webhook ────────────────────────────────────────

    async def process_orange_webhook(self, payload: dict) -> dict:
        """
        Process Orange Money callback.

        Orange sends:
        {
            "order_id": "SC-A1B2C3D4E5F6",
            "status": "SUCCESS",
            "amount": "5000",
            "currency": "XOF",
            "pay_token": "..."
        }
        """
        reference = payload.get("order_id")
        status = payload.get("status", "").upper()

        logger.info("Orange webhook: ref=%s status=%s", reference, status)

        if not reference:
            return {"status": "ignored", "reason": "missing order_id"}

        result = await self.tx_service.process_webhook(
            provider="orange_money",
            provider_reference=reference,
            provider_status=status,
            raw_payload=payload,
        )

        if result:
            return {
                "status": "processed",
                "reference": reference,
                "transaction_status": result.status.value,
            }
        else:
            return {"status": "not_found", "reference": reference}

    # ── Signature Verification ──────────────────────────────────────

    @staticmethod
    def verify_mtn_signature(
        payload: bytes,
        signature: str,
        secret: str,
    ) -> bool:
        """
        Verify MTN webhook signature (if configured).
        MTN may send an X-Callback-Signature header.
        """
        if not signature or not secret:
            return True  # Skip verification if not configured

        expected = hmac.new(
            secret.encode(),
            payload,
            hashlib.sha256,
        ).hexdigest()

        return hmac.compare_digest(expected, signature)

    # ── MPESA (Safaricom) Webhook ────────────────────────────────

    async def process_mpesa_webhook(self, payload: dict) -> dict:
        """
        Process MPESA (Safaricom) callback.

        MPESA sends:
        {
            "Body": {
                "stkCallback": {
                    "MerchantRequestID": "...",
                    "CheckoutRequestID": "...",
                    "ResultCode": 0,
                    "ResultDesc": "Success",
                    "CallbackMetadata": {
                        "Item": [
                            {"Name": "Amount", "Value": 5000},
                            {"Name": "MpesaReceiptNumber", "Value": "QHK31AA1ZZ"},
                            {"Name": "Balance"},
                            {"Name": "TransactionDate", "Value": 20240101120000},
                            {"Name": "PhoneNumber", "Value": 254712345678}
                        ]
                    }
                }
            }
        }
        """
        try:
            stk_callback = payload.get("Body", {}).get("stkCallback", {})
            result_code = stk_callback.get("ResultCode", -1)
            result_desc = stk_callback.get("ResultDesc", "")
            checkout_id = stk_callback.get("CheckoutRequestID", "")

            # Extract metadata
            callback_metadata = stk_callback.get("CallbackMetadata", {}).get("Item", [])
            metadata = {item.get("Name"): item.get("Value") for item in callback_metadata}

            receipt_number = metadata.get("MpesaReceiptNumber", "")
            amount = metadata.get("Amount", 0)
            phone = metadata.get("PhoneNumber", "")

            logger.info("MPESA webhook: checkout=%s code=%s receipt=%s", checkout_id, result_code, receipt_number)

            if not checkout_id and not receipt_number:
                logger.warning("MPESA webhook missing identifiers")
                return {"status": "ignored", "reason": "missing identifiers"}

            # Map result code to status
            status = "SUCCESSFUL" if result_code == 0 else "FAILED"

            # Use receipt number as reference if available
            reference = receipt_number or checkout_id

            result = await self.tx_service.process_webhook(
                provider="mpesa",
                provider_reference=reference,
                provider_status=status,
                raw_payload=payload,
            )

            if result:
                return {
                    "status": "processed",
                    "reference": reference,
                    "transaction_status": result.status.value,
                }
            else:
                return {"status": "not_found", "reference": reference}
        except Exception as e:
            logger.error("MPESA webhook error: %s", e)
            return {"status": "error", "error": str(e)}

    # ── Generic Webhook Router ──────────────────────────────────────

    async def route_webhook(self, provider: str, payload: dict) -> dict:
        """
        Route a webhook to the correct provider handler.

        Usage in routes:
            result = await webhook_handler.route_webhook("mtn", body)
        """
        handlers = {
            "mtn": self.process_mtn_webhook,
            "mtn_momo": self.process_mtn_webhook,
            "airtel": self.process_airtel_webhook,
            "airtel_money": self.process_airtel_webhook,
            "orange": self.process_orange_webhook,
            "orange_money": self.process_orange_webhook,
            "mpesa": self.process_mpesa_webhook,
        }

        handler = handlers.get(provider.lower())
        if not handler:
            logger.warning("Unknown webhook provider: %s", provider)
            return {"status": "unknown_provider", "provider": provider}

        return await handler(payload)
