"""
Transaction lifecycle service.

Manages the full lifecycle of a transaction:
  initiated → pending → processing → settled | failed | reversed

Handles:
  - Status transitions with validation
  - Wallet crediting on settlement
  - Webhook callback processing
  - Background polling for pending transactions
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Optional

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.transaction import Transaction, TransactionStatus, TransactionType
from ..models.wallet import Wallet

logger = logging.getLogger(__name__)


class TransactionError(Exception):
    """Raised when a transaction operation fails."""
    pass


class TransactionService:
    """
    Manages transaction state transitions and wallet operations.

    Usage:
        svc = TransactionService(db)
        tx = await svc.create_fund_transaction(user_id, amount, currency, provider, phone)
        await svc.settle_transaction(tx.reference)
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    # ── Status Transitions ───────────────────────────────────────────

    # Valid transitions: from_status → [allowed_to_status]
    VALID_TRANSITIONS = {
        TransactionStatus.INITIATED: [TransactionStatus.PENDING, TransactionStatus.FAILED],
        TransactionStatus.PENDING: [TransactionStatus.PROCESSING, TransactionStatus.SETTLED, TransactionStatus.FAILED],
        TransactionStatus.PROCESSING: [TransactionStatus.SETTLED, TransactionStatus.FAILED, TransactionStatus.REVERSED],
        TransactionStatus.SETTLED: [],  # Terminal state
        TransactionStatus.FAILED: [TransactionStatus.INITIATED],  # Can retry
        TransactionStatus.REVERSED: [],  # Terminal state
    }

    def _validate_transition(self, tx: Transaction, new_status: TransactionStatus) -> None:
        """Validate that the status transition is allowed."""
        allowed = self.VALID_TRANSITIONS.get(tx.status, [])
        if new_status not in allowed:
            raise TransactionError(
                f"Invalid transition: {tx.status.value} → {new_status.value}. "
                f"Allowed: {[s.value for s in allowed]}"
            )

    async def _transition(
        self,
        tx: Transaction,
        new_status: TransactionStatus,
        provider_status: Optional[str] = None,
        provider_txn_id: Optional[str] = None,
    ) -> Transaction:
        """Perform a status transition with timestamp update."""
        self._validate_transition(tx, new_status)

        tx.status = new_status
        now = datetime.utcnow()

        # Update timestamp for the new status
        timestamp_map = {
            TransactionStatus.PENDING: 'pending_at',
            TransactionStatus.PROCESSING: 'processing_at',
            TransactionStatus.SETTLED: 'settled_at',
            TransactionStatus.FAILED: 'failed_at',
        }
        attr = timestamp_map.get(new_status)
        if attr:
            setattr(tx, attr, now)

        if provider_status:
            tx.provider_status = provider_status
        if provider_txn_id:
            tx.provider_txn_id = provider_txn_id

        await self.db.flush()
        logger.info("Transaction %s: %s → %s", tx.reference, tx.status.value, new_status.value)
        return tx

    # ── Create Transactions ──────────────────────────────────────────

    async def create_fund_transaction(
        self,
        user_id,
        reference: str,
        amount_fiat: float,
        currency_fiat: str,
        amount_sats: int,
        rate_used: float,
        provider: str,
        phone_number: str,
        description: str = "",
    ) -> Transaction:
        """Create a new fund (mobile money → BTC) transaction."""
        tx = Transaction(
            user_id=user_id,
            type=TransactionType.FUND,
            status=TransactionStatus.INITIATED,
            reference=reference,
            amount_fiat=amount_fiat,
            currency_fiat=currency_fiat,
            amount_sats=amount_sats,
            rate_used=rate_used,
            provider=provider,
            phone_number=phone_number,
            description=description or f"Mobile money top-up via {provider}",
        )
        self.db.add(tx)
        await self.db.flush()
        logger.info("Created fund transaction: %s (%s %s)", reference, amount_fiat, currency_fiat)
        return tx

    async def create_send_transaction(
        self,
        user_id,
        reference: str,
        amount_sats: int,
        payment_request: str,
        payment_hash: str,
        destination: str,
        fee_sats: int = 0,
    ) -> Transaction:
        """Create a new send (BTC → Lightning) transaction."""
        # Deduct from wallet first (reserve the sats)
        wallet = await self._get_wallet(user_id)
        if not wallet:
            raise TransactionError("Wallet not found")
        if wallet.available_sats < amount_sats + fee_sats:
            raise TransactionError(f"Insufficient balance: {wallet.available_sats} sats available")

        wallet.reserved_sats += amount_sats + fee_sats
        await self.db.flush()

        tx = Transaction(
            user_id=user_id,
            type=TransactionType.SEND,
            status=TransactionStatus.INITIATED,
            reference=reference,
            amount_fiat=0,  # No fiat involved
            currency_fiat="BTC",
            amount_sats=amount_sats,
            fee_sats=fee_sats,
            rate_used=0,
            provider="lightning",
            payment_request=payment_request,
            payment_hash=payment_hash,
            destination_pubkey=destination,
            description=f"Lightning payment to {destination[:16]}...",
        )
        self.db.add(tx)
        await self.db.flush()
        logger.info("Created send transaction: %s (%d sats)", reference, amount_sats)
        return tx

    async def create_receive_transaction(
        self,
        user_id,
        reference: str,
        amount_sats: int,
        payment_hash: str,
        payment_request: str,
        description: str = "",
    ) -> Transaction:
        """Create a new receive (Lightning → BTC) transaction."""
        tx = Transaction(
            user_id=user_id,
            type=TransactionType.RECEIVE,
            status=TransactionStatus.PENDING,
            reference=reference,
            amount_fiat=0,
            currency_fiat="BTC",
            amount_sats=amount_sats,
            rate_used=0,
            provider="lightning",
            payment_hash=payment_hash,
            payment_request=payment_request,
            description=description or "Lightning invoice",
        )
        self.db.add(tx)
        await self.db.flush()
        logger.info("Created receive transaction: %s (%d sats)", reference, amount_sats)
        return tx

    async def create_spend_transaction(
        self,
        user_id,
        reference: str,
        amount_fiat: float,
        currency_fiat: str,
        amount_sats: int,
        rate_used: float,
        merchant_name: str,
        card_last4: str,
    ) -> Transaction:
        """Create a new spend (card payment) transaction."""
        wallet = await self._get_wallet(user_id)
        if not wallet:
            raise TransactionError("Wallet not found")
        if wallet.available_sats < amount_sats:
            raise TransactionError(f"Insufficient balance: {wallet.available_sats} sats available")

        wallet.reserved_sats += amount_sats
        await self.db.flush()

        tx = Transaction(
            user_id=user_id,
            type=TransactionType.SPEND,
            status=TransactionStatus.INITIATED,
            reference=reference,
            amount_fiat=amount_fiat,
            currency_fiat=currency_fiat,
            amount_sats=amount_sats,
            rate_used=rate_used,
            provider="virtual_card",
            merchant_name=merchant_name,
            description=f"Card spend at {merchant_name}",
        )
        self.db.add(tx)
        await self.db.flush()
        logger.info("Created spend transaction: %s (%s %s at %s)", reference, amount_fiat, currency_fiat, merchant_name)
        return tx

    # ── Status Updates ───────────────────────────────────────────────

    async def mark_pending(self, reference: str, provider_txn_id: str) -> Transaction:
        """Mark transaction as pending (provider acknowledged)."""
        tx = await self._get_transaction(reference)
        return await self._transition(tx, TransactionStatus.PENDING, provider_txn_id=provider_txn_id)

    async def mark_processing(self, reference: str) -> Transaction:
        """Mark transaction as processing (user approved)."""
        tx = await self._get_transaction(reference)
        return await self._transition(tx, TransactionStatus.PROCESSING)

    async def settle_transaction(self, reference: str, fee_sats: int = 0) -> Transaction:
        """
        Settle a transaction — credit the wallet and mark as settled.

        This is called when:
          - Mobile money webhook confirms payment
          - Lightning payment is confirmed
          - Card spend is approved
        """
        tx = await self._get_transaction(reference)
        tx = await self._transition(tx, TransactionStatus.SETTLED)
        tx.fee_sats = fee_sats

        # Credit wallet for fund/receive transactions
        if tx.type in (TransactionType.FUND, TransactionType.RECEIVE):
            wallet = await self._get_wallet(tx.user_id)
            if wallet:
                wallet.balance_sats += tx.amount_sats
                logger.info("Credited %d sats to wallet for %s", tx.amount_sats, reference)

        # Release reserved sats for send/spend transactions
        elif tx.type in (TransactionType.SEND, TransactionType.SPEND):
            wallet = await self._get_wallet(tx.user_id)
            if wallet:
                wallet.reserved_sats = max(0, wallet.reserved_sats - tx.amount_sats - tx.fee_sats)
                wallet.balance_sats -= tx.amount_sats + tx.fee_sats
                logger.info("Debited %d sats from wallet for %s (fee: %d)", tx.amount_sats, reference, tx.fee_sats)

        await self.db.flush()
        return tx

    async def fail_transaction(self, reference: str, reason: str = "") -> Transaction:
        """Mark a transaction as failed."""
        tx = await self._get_transaction(reference)
        tx = await self._transition(tx, TransactionStatus.FAILED)
        tx.description = reason or tx.description

        # Release reserved sats for send/spend
        if tx.type in (TransactionType.SEND, TransactionType.SPEND):
            wallet = await self._get_wallet(tx.user_id)
            if wallet:
                wallet.reserved_sats = max(0, wallet.reserved_sats - tx.amount_sats - tx.fee_sats)
                logger.info("Released reserved %d sats for failed %s", tx.amount_sats, reference)

        await self.db.flush()
        return tx

    async def reverse_transaction(self, reference: str, reason: str = "") -> Transaction:
        """Reverse a settled transaction (refund)."""
        tx = await self._get_transaction(reference)
        tx = await self._transition(tx, TransactionStatus.REVERSED)
        tx.description = reason or tx.description

        # Reverse wallet credit/debit
        wallet = await self._get_wallet(tx.user_id)
        if wallet:
            if tx.type in (TransactionType.FUND, TransactionType.RECEIVE):
                wallet.balance_sats -= tx.amount_sats
            elif tx.type in (TransactionType.SEND, TransactionType.SPEND):
                wallet.balance_sats += tx.amount_sats + tx.fee_sats

        await self.db.flush()
        return tx

    # ── Webhook Processing ───────────────────────────────────────────

    async def process_webhook(
        self,
        provider: str,
        provider_reference: str,
        provider_status: str,
        raw_payload: dict,
    ) -> Optional[Transaction]:
        """
        Process a payment provider webhook.

        Called by the webhook endpoints when MTN/Airtel/Orange
        sends a status update.
        """
        result = await self.db.execute(
            select(Transaction).where(
                and_(
                    Transaction.provider == provider,
                    Transaction.reference == provider_reference,
                )
            )
        )
        tx = result.scalar_one_or_none()
        if not tx:
            # Try by provider_txn_id
            result = await self.db.execute(
                select(Transaction).where(Transaction.provider_txn_id == provider_reference)
            )
            tx = result.scalar_one_or_none()

        if not tx:
            logger.warning("Webhook for unknown transaction: %s %s", provider, provider_reference)
            return None

        # Map provider status to our status
        status_map = {
            "SUCCESSFUL": TransactionStatus.SETTLED,
            "SUCCESS": TransactionStatus.SETTLED,
            "COMPLETED": TransactionStatus.SETTLED,
            "PENDING": TransactionStatus.PENDING,
            "PROCESSING": TransactionStatus.PROCESSING,
            "FAILED": TransactionStatus.FAILED,
            "REJECTED": TransactionStatus.FAILED,
            "EXPIRED": TransactionStatus.FAILED,
            "TIMEOUT": TransactionStatus.FAILED,
            "REVERSED": TransactionStatus.REVERSED,
        }

        target_status = status_map.get(provider_status.upper())
        if not target_status:
            logger.warning("Unknown provider status: %s", provider_status)
            return tx

        # Perform the transition
        try:
            if target_status == TransactionStatus.SETTLED:
                tx = await self.settle_transaction(tx.reference)
            elif target_status == TransactionStatus.FAILED:
                tx = await self.fail_transaction(tx.reference, f"Provider: {provider_status}")
            elif target_status == TransactionStatus.PENDING:
                tx = await self._transition(tx, TransactionStatus.PENDING, provider_status=provider_status)
            elif target_status == TransactionStatus.PROCESSING:
                tx = await self._transition(tx, TransactionStatus.PROCESSING, provider_status=provider_status)
            elif target_status == TransactionStatus.REVERSED:
                tx = await self.reverse_transaction(tx.reference, f"Provider: {provider_status}")

            await self.db.commit()
            return tx
        except TransactionError as e:
            logger.error("Webhook transition failed: %s", e)
            return tx

    # ── Queries ──────────────────────────────────────────────────────

    async def get_user_transactions(
        self,
        user_id,
        tx_type: Optional[TransactionType] = None,
        status: Optional[TransactionStatus] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[Transaction]:
        """Get user's transactions with optional filters."""
        query = select(Transaction).where(Transaction.user_id == user_id)

        if tx_type:
            query = query.where(Transaction.type == tx_type)
        if status:
            query = query.where(Transaction.status == status)

        query = query.order_by(Transaction.created_at.desc()).limit(limit).offset(offset)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_pending_transactions(self, limit: int = 100) -> list[Transaction]:
        """Get all pending transactions for background polling."""
        result = await self.db.execute(
            select(Transaction)
            .where(Transaction.status.in_([
                TransactionStatus.PENDING,
                TransactionStatus.PROCESSING,
            ]))
            .order_by(Transaction.created_at.asc())
            .limit(limit)
        )
        return list(result.scalars().all())

    # ── Helpers ──────────────────────────────────────────────────────

    async def _get_transaction(self, reference: str) -> Transaction:
        result = await self.db.execute(
            select(Transaction).where(Transaction.reference == reference)
        )
        tx = result.scalar_one_or_none()
        if not tx:
            raise TransactionError(f"Transaction not found: {reference}")
        return tx

    async def _get_wallet(self, user_id) -> Optional[Wallet]:
        result = await self.db.execute(
            select(Wallet).where(Wallet.user_id == user_id)
        )
        return result.scalar_one_or_none()
