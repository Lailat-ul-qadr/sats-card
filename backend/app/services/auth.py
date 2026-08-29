"""
Authentication service — phone-number + PIN auth.

In East Africa, USSD PINs (4 digits) are the standard auth method.
We also support email/password for the web app.

Flow:
  1. User registers with phone number → gets a 4-digit PIN
  2. User logs in with phone + PIN → gets JWT token
  3. Frontend sends JWT in Authorization header
  4. Backend validates JWT on every request
"""

from __future__ import annotations

import uuid
import logging
from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.config import settings
from ..models.user import User

logger = logging.getLogger(__name__)

# ── Password Hashing ────────────────────────────────────────────────────

pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")


def hash_pin(pin: str) -> str:
    """Hash a 4-digit PIN."""
    return pwd_context.hash(pin)


def verify_pin(plain_pin: str, hashed_pin: str) -> bool:
    """Verify a PIN against its hash."""
    return pwd_context.verify(plain_pin, hashed_pin)


# ── JWT Token ───────────────────────────────────────────────────────────

ALGORITHM = "HS256"


class TokenPair(BaseModel):
    """Access + refresh token pair."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = Field(description="Seconds until access token expires")


class TokenPayload(BaseModel):
    """JWT payload."""

    sub: str  # User ID
    phone: str
    exp: datetime
    iat: datetime
    type: str = "access"  # access | refresh


def create_tokens(user_id: str, phone: str) -> TokenPair:
    """Create access + refresh token pair."""
    now = datetime.utcnow()

    access_payload = {
        "sub": user_id,
        "phone": phone,
        "type": "access",
        "iat": now,
        "exp": now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    }

    refresh_payload = {
        "sub": user_id,
        "phone": phone,
        "type": "refresh",
        "iat": now,
        "exp": now + timedelta(days=30),
    }

    access_token = jwt.encode(access_payload, settings.SECRET_KEY, algorithm=ALGORITHM)
    refresh_token = jwt.encode(refresh_payload, settings.SECRET_KEY, algorithm=ALGORITHM)

    return TokenPair(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )


def decode_token(token: str, expected_type: str = "access") -> Optional[TokenPayload]:
    """Decode and validate a JWT token."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        token_type = payload.get("type", "access")

        if token_type != expected_type:
            logger.warning("Token type mismatch: expected=%s got=%s", expected_type, token_type)
            return None

        return TokenPayload(
            sub=payload["sub"],
            phone=payload["phone"],
            exp=datetime.fromtimestamp(payload["exp"]),
            iat=datetime.fromtimestamp(payload["iat"]),
            type=token_type,
        )
    except JWTError as e:
        logger.warning("JWT decode failed: %s", e)
        return None


# ── Auth Service ────────────────────────────────────────────────────────


class AuthService:
    """
    Handles user registration, login, and token management.

    Usage:
        auth = AuthService(db)
        user = await auth.register(phone="+256701234567", pin="1234", name="John")
        tokens = await auth.login(phone="+256701234567", pin="1234")
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    async def register(
        self,
        phone: str,
        pin: str,
        name: str = "User",
        email: Optional[str] = None,
        country: str = "UG",
    ) -> dict:
        """
        Register a new user with phone + PIN.

        Returns user dict + tokens.
        Raises ValueError if phone already registered.
        """
        # Check if phone already exists
        existing = await self.db.execute(
            select(User).where(User.phone_number == phone)
        )
        if existing.scalar_one_or_none():
            raise ValueError(f"Phone number {phone} already registered")

        # Create user
        user = User(
            phone_number=phone,
            name=name,
            email=email,
            pin_hash=hash_pin(pin),
            country=country,
            is_verified=True,  # Phone verified via USSD
            kyc_level="tier1",
        )
        self.db.add(user)
        await self.db.flush()  # Get the user ID

        # Create wallet with sign-up bonus
        from ..models.wallet import Wallet
        from ..core.config import settings
        wallet = Wallet(
            user_id=user.id,
            balance_sats=settings.SIGNUP_BONUS_SATS,  # Give new users a bonus!
        )
        self.db.add(wallet)
        await self.db.commit()

        tokens = create_tokens(str(user.id), phone)
        logger.info("Registered new user: %s with %d sats bonus", phone, settings.SIGNUP_BONUS_SATS)

        return {
            "user": {
                "id": str(user.id),
                "phone": user.phone_number,
                "name": user.name,
                "email": user.email,
            },
            "tokens": tokens.model_dump(),
        }

    async def login(self, phone: str, pin: str) -> dict:
        """
        Login with phone + PIN.

        Returns tokens on success.
        Raises ValueError on invalid credentials.
        """
        result = await self.db.execute(
            select(User).where(User.phone_number == phone)
        )
        user = result.scalar_one_or_none()

        if not user or not verify_pin(pin, user.pin_hash):
            raise ValueError("Invalid phone number or PIN")

        if not user.is_active:
            raise ValueError("Account is deactivated")

        # Update last login
        user.last_login_at = datetime.utcnow()
        await self.db.commit()

        tokens = create_tokens(str(user.id), phone)
        logger.info("User logged in: %s", phone)

        return {
            "user": {
                "id": str(user.id),
                "phone": user.phone_number,
                "name": user.name,
            },
            "tokens": tokens.model_dump(),
        }

    async def refresh_token(self, refresh_token: str) -> TokenPair:
        """Get new access token using refresh token."""
        payload = decode_token(refresh_token, expected_type="refresh")
        if not payload:
            raise ValueError("Invalid or expired refresh token")

        return create_tokens(payload.sub, payload.phone)

    async def get_user_by_token(self, token: str) -> Optional[User]:
        """Get user from access token."""
        payload = decode_token(token, expected_type="access")
        if not payload:
            return None

        result = await self.db.execute(
            select(User).where(User.id == uuid.UUID(payload.sub))
        )
        return result.scalar_one_or_none()
