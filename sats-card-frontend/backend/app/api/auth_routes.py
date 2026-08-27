"""
Authentication routes — register, login, refresh token, get current user.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Header
from pydantic import BaseModel, Field
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.database import get_db
from ..services.auth import AuthService, decode_token

router = APIRouter(prefix="/auth", tags=["auth"])


# ── Request/Response Models ─────────────────────────────────────────────


class RegisterRequest(BaseModel):
    phone: str = Field(..., description="E.164 phone number")
    pin: str = Field(..., min_length=4, max_length=4, description="4-digit PIN")
    name: str = Field(default="User", max_length=100)
    email: Optional[str] = None
    country: str = Field(default="UG", max_length=3)


class LoginRequest(BaseModel):
    phone: str
    pin: str = Field(..., min_length=4, max_length=4)


class RefreshRequest(BaseModel):
    refresh_token: str


class AuthResponse(BaseModel):
    user: dict
    tokens: dict


class UserResponse(BaseModel):
    id: str
    phone: str
    name: str
    email: Optional[str]
    country: str
    kyc_level: str
    is_verified: bool


# ── Routes ──────────────────────────────────────────────────────────────


@router.post("/register", response_model=AuthResponse)
async def register(req: RegisterRequest, db: AsyncSession = Depends(get_db)):
    """Register a new user with phone number + 4-digit PIN."""
    auth = AuthService(db)
    try:
        result = await auth.register(
            phone=req.phone,
            pin=req.pin,
            name=req.name,
            email=req.email,
            country=req.country,
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=AuthResponse)
async def login(req: LoginRequest, db: AsyncSession = Depends(get_db)):
    """Login with phone number + PIN."""
    auth = AuthService(db)
    try:
        result = await auth.login(phone=req.phone, pin=req.pin)
        return result
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.post("/refresh")
async def refresh(req: RefreshRequest, db: AsyncSession = Depends(get_db)):
    """Get new access token using refresh token."""
    auth = AuthService(db)
    try:
        tokens = await auth.refresh_token(req.refresh_token)
        return tokens.model_dump()
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


async def get_current_user(
    authorization: Optional[str] = Header(None),
    db: AsyncSession = Depends(get_db),
):
    """Dependency: extract and validate the current user from JWT."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid authorization header")

    token = authorization.replace("Bearer ", "")
    payload = decode_token(token, expected_type="access")
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    import uuid
    from sqlalchemy import select
    from ..models.user import User

    result = await db.execute(select(User).where(User.id == uuid.UUID(payload.sub)))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user


@router.get("/me", response_model=UserResponse)
async def get_me(user=Depends(get_current_user)):
    """Get current user profile."""
    return UserResponse(
        id=str(user.id),
        phone=user.phone_number,
        name=user.name,
        email=user.email,
        country=user.country,
        kyc_level=user.kyc_level,
        is_verified=user.is_verified,
    )
