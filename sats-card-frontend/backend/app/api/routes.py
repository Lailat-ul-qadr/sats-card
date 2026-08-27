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
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..core.database import get_db
from ..core.config import settings
from ..ussd.handler import USSDHandler, USSDResponse
from ..adapters.base import MobileMoneyAdapter, PaymentRequest, PaymentStatus
from ..adapters.mtn import MTNMoMoAdapter
from ..adapters.airtel import AirtelMoneyAdapter
from ..adapters.orange import OrangeMoneyAdapter
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
    description: str = "Sats Card Top-Up"


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
    memo: str = "Sats Card Top-Up"


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
    """Create a Lightning invoice to receive BTC."""
    return {
        "payment_request": f"lnbc{uuid.uuid4().hex[:50]}",
        "amount_sats": req.amount_sats,
        "description": req.memo,
        "expires_at": datetime.utcnow().isoformat(),
    }


@router.get("/wallet/balance")
async def get_wallet_balance(
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get wallet balance — BTC and USD."""
    result = await db.execute(
        select(Wallet).where(Wallet.user_id == user.id)
    )
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
