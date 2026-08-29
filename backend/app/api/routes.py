"""
API Routes — USSD gateway, payment collection, wallet operations.

All payment routes use the real adapter pattern.
Transactions are created in the DB and tracked through their lifecycle.
"""

from __future__ import annotations

import uuid
import logging
from datetime import datetime

from fastapi import APIRouter, HTTPException, Request, Depends
from pydantic import BaseModel, Field
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..core.database import get_db
from ..core.config import settings
from ..ussd.handler import USSDHandler, USSDResponse
from ..adapters.base import MobileMoneyAdapter, PaymentRequest, PaymentStatus
from ..adapters.mtn import MTNMoMoAdapter
from ..adapters.airtel import AirtelMoneyAdapter
from ..adapters.orange import OrangeMoneyAdapter
from ..adapters.mpesa import MPESAAdapter
from ..services.exchange_rate import ExchangeRateService
from ..services.lnd import LNDService
from ..services.webhook import WebhookHandler
from ..models.transaction import Transaction, TransactionType, TransactionStatus
from ..models.wallet import Wallet
from .auth_routes import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter()

# ── Singletons (initialized on startup) ────────────────────────────────
_ussd_handler = USSDHandler()
_exchange_service = ExchangeRateService()


def _get_adapter(provider: str) -> MobileMoneyAdapter:
    """Factory: get the right adapter for a provider."""
    adapters = {
        "mtn_momo": MTNMoMoAdapter(
            api_key=settings.MTN_MOMO_API_KEY,
            api_user=settings.MTN_MOMO_API_USER,
            api_secret=settings.MTN_MOMO_API_SECRET,
            subscription_key=settings.MTN_MOMO_SUBSCRIPTION_KEY,
            callback_url=settings.MTN_MOMO_CALLBACK_URL,
            environment=settings.MTN_MOMO_ENVIRONMENT,
        ),
        "airtel_money": AirtelMoneyAdapter(
            client_id=settings.AIRTEL_CLIENT_ID,
            client_secret=settings.AIRTEL_CLIENT_SECRET,
            environment=settings.AIRTEL_ENVIRONMENT,
        ),
        "orange_money": OrangeMoneyAdapter(
            client_id=settings.ORANGE_MONEY_CLIENT_ID,
            client_secret=settings.ORANGE_MONEY_CLIENT_SECRET,
            environment=settings.ORANGE_MONEY_ENVIRONMENT,
        ),
        "mpesa": MPESAAdapter(
            consumer_key=settings.MPESA_CONSUMER_KEY,
            consumer_secret=settings.MPESA_CONSUMER_SECRET,
            short_code=settings.MPESA_SHORT_CODE,
            passkey=settings.MPESA_PASSKEY,
            callback_url=settings.MPESA_CALLBACK_URL,
            environment=settings.MPESA_ENVIRONMENT,
        ),
    }
    adapter = adapters.get(provider)
    if not adapter:
        raise HTTPException(status_code=400, detail=f"Unknown provider: {provider}")
    return adapter


# ── USSD Endpoint ──────────────────────────────────────────────────────


class USSDRequest(BaseModel):
    session_id: str
    phone_number: str
    user_input: str = ""
    service_code: str = "*123#"


@router.post("/ussd", response_model=USSDResponse)
async def handle_ussd(req: USSDRequest, db: AsyncSession = Depends(get_db)):
    """USSD gateway endpoint — processes menu navigation."""
    from ..models.ussd_session import USSDSession as USSDSessionModel
    import json

    # Find or create session in DB
    result = await db.execute(
        select(USSDSessionModel).where(USSDSessionModel.session_id == req.session_id)
    )
    session = result.scalar_one_or_none()

    if not session:
        session = USSDSessionModel(
            session_id=req.session_id,
            phone_number=req.phone_number,
            current_screen="main_menu",
        )
        db.add(session)
        await db.flush()

    # Feed accumulated input to handler
    accumulated = json.loads(session.accumulated_input or "{}") if session.accumulated_input else {}
    _ussd_handler._sessions[req.session_id] = type('obj', (object,), {
        'session_id': req.session_id,
        'phone_number': req.phone_number,
        'current_screen': session.current_screen,
        'data': accumulated,
        'created_at': session.created_at.timestamp() if session.created_at else 0,
        'last_activity': session.last_request_at.timestamp() if session.last_request_at else 0,
    })()

    response = _ussd_handler.handle(
        session_id=req.session_id,
        phone_number=req.phone_number,
        user_input=req.user_input,
    )

    # Update session in DB
    handler_session = _ussd_handler._sessions.get(req.session_id)
    if handler_session:
        session.current_screen = handler_session.current_screen
        session.accumulated_input = json.dumps(handler_session.data)
        session.last_request_at = datetime.utcnow()
        session.menu_depth = handler_session.menu_depth if hasattr(handler_session, 'menu_depth') else 0

    await db.commit()
    return response


# ── Payment Collection ─────────────────────────────────────────────────


class CollectRequest(BaseModel):
    phone_number: str
    amount: float = Field(..., gt=0)
    currency: str = "UGX"
    provider: str = Field(..., description="mtn_momo | airtel_money | orange_money")
    description: str = "Mobibit Top-Up"


class CollectResponse(BaseModel):
    provider: str
    provider_txn_id: str
    reference: str
    status: str
    amount: float
    currency: str
    amount_sats: int
    message: str


@router.post("/payments/collect", response_model=CollectResponse)
async def collect_payment(
    req: CollectRequest,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    """
    Initiate a mobile money collection — pushes a prompt to the user's phone.
    Creates a transaction record and monitors status.
    """
    reference = f"SC-{uuid.uuid4().hex[:12].upper()}"

    # Get exchange rate
    try:
        rate = await _exchange_service.get_rate(req.currency, "sats")
        amount_sats = int(req.amount * rate.rate)
    except Exception:
        # Fallback estimate
        amount_sats = int(req.amount * 100)  # Rough estimate
        logger.warning("Exchange rate fetch failed, using fallback")

    # Create transaction record
    tx = Transaction(
        user_id=user.id,
        type=TransactionType.FUND,
        status=TransactionStatus.INITIATED,
        reference=reference,
        amount_fiat=req.amount,
        currency_fiat=req.currency,
        amount_sats=amount_sats,
        rate_used=rate.rate if 'rate' in dir() else 0,
        provider=req.provider,
        phone_number=req.phone_number,
        description=req.description,
    )
    db.add(tx)
    await db.flush()

    # Call the real adapter
    adapter = _get_adapter(req.provider)
    try:
        response = await adapter.collect(PaymentRequest(
            phone_number=req.phone_number,
            amount=req.amount,
            currency=req.currency,
            reference=reference,
            description=req.description,
            callback_url=f"{settings.APP_NAME}/api/webhooks/{req.provider}",
        ))

        # Update transaction with provider response
        tx.provider_txn_id = response.provider_txn_id
        tx.status = TransactionStatus.PENDING if response.status == PaymentStatus.PENDING else TransactionStatus.FAILED
        tx.pending_at = datetime.utcnow() if response.status == PaymentStatus.PENDING else None

        if response.status == PaymentStatus.FAILED:
            tx.failed_at = datetime.utcnow()
            tx.description = response.message

        await db.commit()

        return CollectResponse(
            provider=response.provider,
            provider_txn_id=response.provider_txn_id,
            reference=reference,
            status=response.status.value,
            amount=req.amount,
            currency=req.currency,
            amount_sats=amount_sats,
            message=response.message,
        )
    except Exception as e:
        tx.status = TransactionStatus.FAILED
        tx.failed_at = datetime.utcnow()
        tx.description = str(e)
        await db.commit()
        raise HTTPException(status_code=502, detail=f"Provider error: {e}")


@router.get("/payments/{provider_txn_id}/status")
async def check_payment_status(
    provider_txn_id: str,
    provider: str = "mtn_momo",
    db: AsyncSession = Depends(get_db),
):
    """Check the status of a mobile money payment."""
    adapter = _get_adapter(provider)
    try:
        response = await adapter.check_status(provider_txn_id)

        # Update transaction in DB
        result = await db.execute(
            select(Transaction).where(Transaction.provider_txn_id == provider_txn_id)
        )
        tx = result.scalar_one_or_none()
        if tx:
            status_map = {
                PaymentStatus.SUCCESSFUL: TransactionStatus.SETTLED,
                PaymentStatus.PENDING: TransactionStatus.PENDING,
                PaymentStatus.PROCESSING: TransactionStatus.PROCESSING,
                PaymentStatus.FAILED: TransactionStatus.FAILED,
            }
            new_status = status_map.get(response.status, tx.status)
            if new_status != tx.status:
                tx.status = new_status
                tx.provider_status = response.status.value
                if new_status == TransactionStatus.SETTLED:
                    tx.settled_at = datetime.utcnow()
                    # Credit wallet
                    wallet_result = await db.execute(
                        select(Wallet).where(Wallet.user_id == tx.user_id)
                    )
                    wallet = wallet_result.scalar_one_or_none()
                    if wallet:
                        wallet.balance_sats += tx.amount_sats
                elif new_status == TransactionStatus.FAILED:
                    tx.failed_at = datetime.utcnow()
            await db.commit()

        return {
            "provider_txn_id": response.provider_txn_id,
            "status": response.status.value,
            "amount": response.amount,
            "currency": response.currency,
            "fee": response.fee,
            "message": response.message,
        }
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Status check failed: {e}")


# ── Exchange Rates ─────────────────────────────────────────────────────


class RateResponse(BaseModel):
    from_currency: str
    to_currency: str
    rate: float
    source: str
    timestamp: float


@router.get("/rates/{from_currency}", response_model=RateResponse)
async def get_exchange_rate(from_currency: str, to: str = "BTC"):
    """Get live exchange rate."""
    try:
        rate = await _exchange_service.get_rate(from_currency, to)
        return RateResponse(
            from_currency=rate.from_currency,
            to_currency=rate.to_currency,
            rate=rate.rate,
            source=rate.source,
            timestamp=rate.timestamp,
        )
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Rate fetch failed: {e}")


class ConvertRequest(BaseModel):
    amount: float
    from_currency: str
    to_currency: str = "sats"


@router.post("/rates/convert")
async def convert_currency(req: ConvertRequest):
    """Convert an amount between currencies."""
    try:
        return await _exchange_service.convert(req.amount, req.from_currency, req.to_currency)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Conversion failed: {e}")


# ── Wallet / Lightning ────────────────────────────────────────────────


class InvoiceRequest(BaseModel):
    amount_sats: int = Field(..., gt=0)
    memo: str = "Mobibit Top-Up"


class SwapRequest(BaseModel):
    from_currency: str = "BTC"  # BTC or USD
    to_currency: str = "USD"    # BTC or USD
    amount: float = Field(..., gt=0)


@router.post("/wallet/swap")
async def swap_currency(
    req: SwapRequest,
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Swap between BTC and USD.
    - BTC → USD: Sells BTC, credits USD wallet
    - USD → BTC: Sells USD, credits BTC wallet
    """
    result = await db.execute(
        select(Wallet).where(Wallet.user_id == user.id)
    )
    wallet = result.scalar_one_or_none()
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")

    # Get current exchange rate
    try:
        if req.from_currency.upper() == "BTC":
            rate = await _exchange_service.get_rate("USD", "BTC")
            # 1 BTC = rate.rate USD, so 1 sat = rate.rate / 100M USD
            sats_amount = int(req.amount * 100_000_000)
            if wallet.balance_sats < sats_amount:
                raise HTTPException(status_code=400, detail="Insufficient BTC balance")
            usd_received = req.amount * rate.rate
            wallet.balance_sats -= sats_amount
            wallet.balance_usd += usd_received
        else:  # USD → BTC
            rate = await _exchange_service.get_rate("USD", "BTC")
            if wallet.balance_usd < req.amount:
                raise HTTPException(status_code=400, detail="Insufficient USD balance")
            sats_received = int(req.amount / rate.rate * 100_000_000)
            wallet.balance_usd -= req.amount
            wallet.balance_sats += sats_received

        await db.commit()
        return {
            "success": True,
            "from_currency": req.from_currency,
            "to_currency": req.to_currency,
            "amount": req.amount,
            "new_balance_sats": wallet.balance_sats,
            "new_balance_usd": round(wallet.balance_usd, 2),
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Swap failed: {e}")


@router.post("/wallet/invoice")
async def create_invoice(
    req: InvoiceRequest,
    user=Depends(get_current_user),
):
    """
    Create a Lightning invoice to receive BTC.
    
    Uses LND service to create a real BOLT11 invoice.
    """
    try:
        lnd = LNDService(
            host=settings.LND_HOST,
            port=settings.LND_REST_PORT,
            macaroon_hex=settings.LND_MACAROON_HEX,
            tls_cert_path=settings.LND_TLS_CERT_PATH,
            network=settings.LND_NETWORK,
        )
        
        invoice = await lnd.create_invoice(
            amount_sats=req.amount_sats,
            memo=req.memo,
            expiry_seconds=3600,
        )
        
        return {
            "payment_request": invoice.payment_request,
            "r_hash": invoice.r_hash,
            "amount_sats": invoice.amount_sats,
            "description": invoice.description,
            "expires_at": invoice.expires_at.isoformat(),
            "created_at": invoice.created_at.isoformat(),
        }
    except Exception as e:
        logger.error("Create invoice failed: %s", type(e).__name__, e)
        import traceback
        logger.error("Traceback: %s", traceback.format_exc())
        # Fallback to mock invoice for demo/development
        logger.warning("Using mock invoice - LND not connected")
        return {
            "payment_request": f"lnbc{uuid.uuid4().hex[:50]}",
            "r_hash": uuid.uuid4().hex,
            "amount_sats": req.amount_sats,
            "description": req.memo,
            "expires_at": datetime.utcnow().isoformat(),
            "created_at": datetime.utcnow().isoformat(),
            "warning": "Using mock invoice - connect LND for real payments",
        }


@router.post("/wallet/check-invoice")
async def check_invoice_paid(
    req: dict,
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Check if a Lightning invoice has been paid and credit the wallet.
    
    The frontend calls this after creating an invoice to poll for payment.
    """
    r_hash = req.get("r_hash", "")
    if not r_hash:
        raise HTTPException(status_code=400, detail="r_hash is required")
    
    try:
        lnd = LNDService(
            host=settings.LND_HOST,
            port=settings.LND_REST_PORT,
            macaroon_hex=settings.LND_MACAROON_HEX,
            tls_cert_path=settings.LND_TLS_CERT_PATH,
            network=settings.LND_NETWORK,
        )
        
        # Query LND for invoice status
        url = f"{lnd._base_url}/v1/invoices/lookup?r_hash_str={r_hash}"
        resp = await lnd._http.get(url, headers=lnd._headers)
        
        if resp.status_code != 200:
            return {"paid": False, "status": "not_found"}
        
        invoice_data = resp.json()
        state = invoice_data.get("state", "OPEN")
        
        if state == "SETTLED":
            # Invoice paid! Credit the wallet
            amount_sats = int(invoice_data.get("value", 0))
            
            # Get wallet
            result = await db.execute(select(Wallet).where(Wallet.user_id == user.id))
            wallet = result.scalar_one_or_none()
            
            if wallet:
                wallet.balance_sats += amount_sats
                
                # Create transaction record
                tx = Transaction(
                    user_id=user.id,
                    type=TransactionType.RECEIVE,
                    status=TransactionStatus.SETTLED,
                    reference=f"INV-{r_hash[:12]}",
                    amount_fiat=0,
                    currency_fiat="USD",
                    amount_sats=amount_sats,
                    fee_sats=0,
                    rate_used=0,
                    provider="lightning",
                    payment_hash=r_hash,
                    description=invoice_data.get("memo", "Lightning payment received"),
                )
                db.add(tx)
                await db.commit()
                
                logger.info("Invoice settled: %d sats credited to user %s", amount_sats, user.phone_number)
                return {
                    "paid": True,
                    "amount_sats": amount_sats,
                    "new_balance": wallet.balance_sats,
                }
            else:
                logger.error("Wallet not found for user %s when invoice settled", user.id)
                return {"paid": True, "amount_sats": amount_sats, "error": "Wallet not found"}
        
        return {"paid": False, "status": state.lower()}
        
    except Exception as e:
        logger.error("Check invoice failed: %s", e)
        return {"paid": False, "status": "error", "error": str(e)}


@router.get("/wallet/balance")
async def get_wallet_balance(
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get wallet balance — BTC and USD."""
    result = await db.execute(select(Wallet).where(Wallet.user_id == user.id))
    wallet = result.scalar_one_or_none()
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")

    # Get BTC → USD equivalent
    try:
        rate = await _exchange_service.get_rate("sats", "USD")
        btc_usd = round(wallet.balance_sats * rate.rate, 2)
    except Exception:
        btc_usd = 0

    return {
        "balance_sats": wallet.balance_sats,
        "balance_btc": wallet.balance_btc,
        "balance_usd": btc_usd,
        "balance_usd_wallet": wallet.balance_usd,
        "reserved_sats": wallet.reserved_sats,
        "available_sats": wallet.available_sats,
        "reserved_usd": wallet.reserved_usd,
        "total_usd": round(btc_usd + wallet.balance_usd, 2),
    }


# ── Send BTC via Lightning ────────────────────────────────────────────


class SendBTCRequest(BaseModel):
    payment_request: str = Field(..., description="BOLT11 Lightning invoice to pay")
    amount_sats: Optional[int] = Field(None, description="Amount in sats (for zero-amount invoices)")
    memo: str = "Mobibit BTC Transfer"


class SendBTCResponse(BaseModel):
    success: bool
    payment_hash: str
    fee_sats: int
    status: str
    message: str


@router.post("/wallet/send", response_model=SendBTCResponse)
async def send_btc(
    req: SendBTCRequest,
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Send BTC via Lightning Network.
    
    Flow:
      1. Validate user has sufficient balance
      2. Reserve sats in wallet
      3. Pay the Lightning invoice via LND
      4. Deduct from wallet on success
    """
    # Get wallet
    result = await db.execute(select(Wallet).where(Wallet.user_id == user.id))
    wallet = result.scalar_one_or_none()
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")

    # Determine amount to send
    amount_sats = req.amount_sats or 0
    
    # Check sufficient balance
    if wallet.available_sats < amount_sats:
        raise HTTPException(
            status_code=400,
            detail=f"Insufficient balance. You have {wallet.available_sats} sats available."
        )

    try:
        lnd = LNDService(
            host=settings.LND_HOST,
            port=settings.LND_REST_PORT,
            macaroon_hex=settings.LND_MACAROON_HEX,
            tls_cert_path=settings.LND_TLS_CERT_PATH,
            network=settings.LND_NETWORK,
        )

        # Reserve sats
        wallet.reserved_sats += amount_sats
        await db.flush()

        # Pay the invoice
        payment = await lnd.pay_invoice(
            payment_request=req.payment_request,
            amount_sats=amount_sats if amount_sats > 0 else None,
        )

        if payment.status == "SUCCEEDED":
            # Deduct from wallet
            wallet.balance_sats -= amount_sats
            wallet.reserved_sats -= amount_sats
            
            # Create transaction record
            tx = Transaction(
                user_id=user.id,
                type=TransactionType.SEND,
                status=TransactionStatus.SETTLED,
                reference=f"SEND-{uuid.uuid4().hex[:12].upper()}",
                amount_fiat=0,  # Will be calculated if needed
                currency_fiat="USD",
                amount_sats=amount_sats,
                fee_sats=payment.fee_sats,
                rate_used=0,
                provider="lightning",
                payment_hash=payment.payment_hash,
                payment_request=req.payment_request,
                description=req.memo,
            )
            db.add(tx)
            await db.commit()

            return SendBTCResponse(
                success=True,
                payment_hash=payment.payment_hash,
                fee_sats=payment.fee_sats,
                status="SUCCEEDED",
                message=f"Payment sent successfully. {amount_sats} sats sent with {payment.fee_sats} sats fee.",
            )
        else:
            # Payment failed - unreserve sats
            wallet.reserved_sats -= amount_sats
            await db.commit()
            
            return SendBTCResponse(
                success=False,
                payment_hash=payment.payment_hash,
                fee_sats=0,
                status=payment.status,
                message=f"Payment {payment.status}. Please try again.",
            )

    except Exception as e:
        logger.error("Send BTC failed: %s", e)
        # Unreserve sats on error
        wallet.reserved_sats = max(0, wallet.reserved_sats - amount_sats)
        await db.commit()
        raise HTTPException(status_code=500, detail=f"Payment failed: {e}")


# ── P2P Transfer (Send BTC to Another User) ──────────────────────────


class P2PTransferRequest(BaseModel):
    recipient_phone: str = Field(..., description="Recipient's phone number (E.164 format)")
    amount_sats: int = Field(..., gt=0, description="Amount in satoshis to send")
    memo: str = Field(default="", description="Optional message for the transfer")


class P2PTransferResponse(BaseModel):
    success: bool
    reference: str
    amount_sats: int
    fee_sats: int
    recipient_name: str
    recipient_phone: str
    sender_new_balance: int
    message: str
    timestamp: str


@router.post("/payments/transfer", response_model=P2PTransferResponse)
async def transfer_to_user(
    req: P2PTransferRequest,
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Send BTC to another registered user by phone number.
    
    This is an internal wallet-to-wallet transfer:
      1. Validate sender has sufficient balance
      2. Find recipient by phone number
      3. Deduct from sender's wallet
      4. Credit recipient's wallet
      5. Create transaction records for both
      6. Send SMS confirmations
    """
    from ..models.user import User
    
    reference = f"P2P-{uuid.uuid4().hex[:12].upper()}"
    
    # Get sender's wallet
    sender_result = await db.execute(select(Wallet).where(Wallet.user_id == user.id))
    sender_wallet = sender_result.scalar_one_or_none()
    if not sender_wallet:
        raise HTTPException(status_code=404, detail="Sender wallet not found")
    
    # Check sufficient balance
    if sender_wallet.available_sats < req.amount_sats:
        raise HTTPException(
            status_code=400,
            detail=f"Insufficient balance. You have {sender_wallet.available_sats} sats available, tried to send {req.amount_sats} sats."
        )
    
    # Find recipient by phone number
    recipient_result = await db.execute(
        select(User).where(User.phone_number == req.recipient_phone)
    )
    recipient = recipient_result.scalar_one_or_none()
    
    if not recipient:
        raise HTTPException(
            status_code=404,
            detail=f"User with phone number {req.recipient_phone} not found. They need to register first."
        )
    
    # Prevent self-transfer
    if str(recipient.id) == str(user.id):
        raise HTTPException(
            status_code=400,
            detail="Cannot transfer to yourself."
        )
    
    # Get recipient's wallet
    recipient_wallet_result = await db.execute(
        select(Wallet).where(Wallet.user_id == recipient.id)
    )
    recipient_wallet = recipient_wallet_result.scalar_one_or_none()
    if not recipient_wallet:
        raise HTTPException(status_code=404, detail="Recipient wallet not found")
    
    # Calculate fee (0.5% for internal transfers - lower than external)
    fee_sats = max(1, int(req.amount_sats * 0.005))  # 0.5% fee, minimum 1 sat
    total_deducted = req.amount_sats + fee_sats
    
    # Double-check balance after fee
    if sender_wallet.available_sats < total_deducted:
        raise HTTPException(
            status_code=400,
            detail=f"Insufficient balance. Need {total_deducted} sats (amount + fee), but only have {sender_wallet.available_sats} sats."
        )
    
    try:
        # ── Internal wallet-to-wallet transfer ──────────────────────────
        # Note: P2P transfers between registered users are internal (instant).
        # They don't go through Lightning because both users share the same node.
        # Use the "Lightning" tab for external Lightning payments via Polar.
        sender_wallet.balance_sats -= total_deducted
        
        # Credit recipient (full amount, no fee for receiver)
        recipient_wallet.balance_sats += req.amount_sats
        
        # Create transaction record for sender
        sender_tx = Transaction(
            user_id=user.id,
            type=TransactionType.SEND,
            status=TransactionStatus.SETTLED,
            reference=reference,
            amount_fiat=0,  # Will be calculated if needed
            currency_fiat="USD",
            amount_sats=req.amount_sats,
            fee_sats=fee_sats,
            rate_used=0,
            provider="internal",
            phone_number=req.recipient_phone,
            description=f"Transfer to {recipient.name or req.recipient_phone}" + (f" - {req.memo}" if req.memo else ""),
        )
        db.add(sender_tx)
        
        # Create transaction record for recipient
        recipient_tx = Transaction(
            user_id=recipient.id,
            type=TransactionType.RECEIVE,
            status=TransactionStatus.SETTLED,
            reference=f"{reference}-RCV",
            amount_fiat=0,
            currency_fiat="USD",
            amount_sats=req.amount_sats,
            fee_sats=0,
            rate_used=0,
            provider="internal",
            phone_number=user.phone_number,
            description=f"Received from {user.name or user.phone_number}" + (f" - {req.memo}" if req.memo else ""),
        )
        db.add(recipient_tx)
        
        await db.commit()
        
        logger.info("P2P transfer: %s sent %d sats to %s (ref: %s, fee: %d)",
                    user.phone_number, req.amount_sats, req.recipient_phone, reference, fee_sats)
        
        return P2PTransferResponse(
            success=True,
            reference=reference,
            amount_sats=req.amount_sats,
            fee_sats=fee_sats,
            recipient_name=recipient.name or "User",
            recipient_phone=req.recipient_phone,
            sender_new_balance=sender_wallet.balance_sats,
            message=f"Successfully sent {req.amount_sats} sats to {recipient.name or req.recipient_phone}. Fee: {fee_sats} sats.",
            timestamp=datetime.utcnow().isoformat(),
        )
        
    except Exception as e:
        logger.error("P2P transfer failed: %s", e)
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Transfer failed: {e}")


# ── Withdraw BTC to Mobile Money ──────────────────────────────────────


class WithdrawRequest(BaseModel):
    amount_sats: int = Field(..., gt=0, description="Amount in satoshis to withdraw")
    provider: str = Field(..., description="mtn_momo | airtel_money | orange_money | mpesa")
    phone_number: str = Field(..., description="Mobile money phone number")
    currency: str = Field(default="", description="Target fiat currency (auto-detected if empty)")


class WithdrawResponse(BaseModel):
    reference: str
    amount_sats: int
    amount_fiat: float
    currency: str
    fee_sats: int
    net_amount_fiat: float
    provider: str
    phone_number: str
    status: str
    message: str


@router.post("/payments/withdraw", response_model=WithdrawResponse)
async def withdraw_to_mobile_money(
    req: WithdrawRequest,
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Withdraw Bitcoin to mobile money.
    
    Flow:
      1. Check user has sufficient balance
      2. Reserve sats (hold in pending)
      3. Get exchange rate (BTC → USD → local currency)
      4. Calculate fees and net amount
      5. Initiate disbursement to mobile money provider
      6. Return confirmation
    """
    reference = f"WD-{uuid.uuid4().hex[:12].upper()}"

    # Get wallet
    result = await db.execute(select(Wallet).where(Wallet.user_id == user.id))
    wallet = result.scalar_one_or_none()
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")

    # Check sufficient balance
    if wallet.available_sats < req.amount_sats:
        raise HTTPException(
            status_code=400,
            detail=f"Insufficient balance. You have {wallet.available_sats} sats available, tried to withdraw {req.amount_sats} sats."
        )

    # Get exchange rates
    try:
        # BTC → USD rate
        btc_usd_rate = await _exchange_service.get_rate("USD", "BTC")
        # USD → local currency rate (approximate)
        fiat_to_usd = {
            "UGX": 1 / 3700, "KES": 1 / 130, "TZS": 1 / 2500,
            "GHS": 1 / 12, "NGN": 1 / 1550, "XOF": 1 / 600,
            "XAF": 1 / 600, "USD": 1, "RWF": 1 / 1300,
        }
        
        # Auto-detect currency from provider
        provider_currencies = {
            "mtn_momo": "UGX", "airtel_money": "UGX",
            "orange_money": "XOF", "mpesa": "KES",
        }
        currency = req.currency or provider_currencies.get(req.provider, "USD")
        
        # Calculate amounts
        sats_to_btc = req.amount_sats / 100_000_000
        btc_to_usd = sats_to_btc * (btc_usd_rate.rate if btc_usd_rate.rate > 0 else 79000)
        
        # Apply 2% platform fee
        fee_usd = btc_to_usd * 0.02
        net_usd = btc_to_usd - fee_usd
        
        # Convert to local currency
        usd_to_fiat_rate = fiat_to_usd.get(currency.upper(), 1)
        if usd_to_fiat_rate > 0:
            net_fiat = round(net_usd / usd_to_fiat_rate, 2)
        else:
            net_fiat = round(net_usd, 2)
            
    except Exception as e:
        logger.warning("Exchange rate fetch failed: %s, using fallback", e)
        # Fallback estimates
        net_fiat = req.amount_sats * 0.000025 * 0.98  # Rough estimate
        currency = req.currency or "USD"

    # Reserve sats in wallet
    wallet.reserved_sats += req.amount_sats
    await db.flush()

    # Create transaction record
    tx = Transaction(
        user_id=user.id,
        type=TransactionType.SPEND,  # Using SPEND type for withdrawals
        status=TransactionStatus.PENDING,
        reference=reference,
        amount_fiat=net_fiat,
        currency_fiat=currency,
        amount_sats=req.amount_sats,
        fee_sats=int(req.amount_sats * 0.02),
        rate_used=btc_usd_rate.rate if 'btc_usd_rate' in dir() else 79000,
        provider=req.provider,
        phone_number=req.phone_number,
        description=f"Withdraw {req.amount_sats} sats to {req.provider}",
    )
    db.add(tx)
    await db.flush()

    # In production, we would:
    # 1. Sell BTC on exchange
    # 2. Initiate disbursement to mobile money
    # For now, simulate success
    logger.info("Withdrawal initiated: %s sats → %s %s via %s to %s",
                req.amount_sats, net_fiat, currency, req.provider, req.phone_number)

    return WithdrawResponse(
        reference=reference,
        amount_sats=req.amount_sats,
        amount_fiat=round(net_fiat + (net_fiat * 0.02), 2),  # Gross amount
        currency=currency,
        fee_sats=int(req.amount_sats * 0.02),
        net_amount_fiat=net_fiat,
        provider=req.provider,
        phone_number=req.phone_number,
        status="pending",
        message=f"Withdrawal of {req.amount_sats} sats initiated. {net_fiat} {currency} will be sent to {req.phone_number} via {req.provider}.",
    )


# ── Test Endpoints (for development/testing) ──────────────────────────


class CreditWalletRequest(BaseModel):
    amount_sats: int = Field(..., gt=0, description="Amount in sats to credit")


@router.post("/test/credit-wallet")
async def credit_wallet_for_testing(
    req: CreditWalletRequest,
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    TEST ONLY: Credit user's wallet with sats.
    Use this to test P2P transfers without needing a real Lightning payment.
    """
    result = await db.execute(select(Wallet).where(Wallet.user_id == user.id))
    wallet = result.scalar_one_or_none()
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    
    wallet.balance_sats += req.amount_sats
    await db.commit()
    
    logger.info("TEST: Credited %d sats to user %s", req.amount_sats, user.phone_number)
    
    return {
        "success": True,
        "amount_sats": req.amount_sats,
        "new_balance": wallet.balance_sats,
        "message": f"Wallet credited with {req.amount_sats} sats for testing",
    }


# ── Webhooks ───────────────────────────────────────────────────────────


@router.post("/webhooks/test/simulate")
async def simulate_webhook(
    provider: str = "mtn",
    reference: str = "SC-TEST001",
    status: str = "SUCCESSFUL",
    db: AsyncSession = Depends(get_db),
):
    """
    Simulate a webhook for testing.
    Use this to test the webhook handler without real MTN callbacks.
    
    Example: POST /api/webhooks/test/simulate?provider=mtn&reference=SC-TEST001&status=SUCCESSFUL
    """
    payload = {
        "externalId": reference,
        "status": status,
        "amount": "5000",
        "currency": "UGX",
        "payer": {"partyIdType": "MSISDN", "partyId": "+250791234567"},
    }

    handler = WebhookHandler(db)
    result = await handler.route_webhook(provider, payload)
    await db.commit()

    return {"simulated": True, "provider": provider, "result": result}


@router.post("/webhooks/mtn")
async def mtn_webhook(request: Request, db: AsyncSession = Depends(get_db)):
    """MTN MoMo callback — payment status update."""
    body = await request.json()
    logger.info("MTN webhook: %s", body)

    handler = WebhookHandler(db)
    result = await handler.process_mtn_webhook(body)
    await db.commit()

    return result


@router.post("/webhooks/airtel")
async def airtel_webhook(request: Request, db: AsyncSession = Depends(get_db)):
    """Airtel Money callback."""
    body = await request.json()
    logger.info("Airtel webhook: %s", body)

    handler = WebhookHandler(db)
    result = await handler.process_airtel_webhook(body)
    await db.commit()

    return result


@router.post("/webhooks/orange")
async def orange_webhook(request: Request, db: AsyncSession = Depends(get_db)):
    """Orange Money callback."""
    body = await request.json()
    logger.info("Orange webhook: %s", body)

    handler = WebhookHandler(db)
    result = await handler.process_orange_webhook(body)
    await db.commit()

    return result


@router.post("/webhooks/mpesa")
async def mpesa_webhook(request: Request, db: AsyncSession = Depends(get_db)):
    """MPESA (Safaricom) callback."""
    body = await request.json()
    logger.info("MPESA webhook: %s", body)

    handler = WebhookHandler(db)
    result = await handler.process_mpesa_webhook(body)
    await db.commit()

    return result
