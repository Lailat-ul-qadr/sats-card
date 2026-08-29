"""
Mobibit Africa API — FastAPI application entry point.

Run with:
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
"""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.config import settings
from .core.database import create_tables
from .api.routes import router as api_router
from .api.auth_routes import router as auth_router
from .api.at_ussd_routes import router as at_router
from .api.lightning_routes import router as lightning_router

logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup/shutdown lifecycle."""
    logger.info("🚀 Starting %s v%s", settings.APP_NAME, settings.APP_VERSION)
    logger.info("   Network: %s", settings.LND_NETWORK)
    logger.info("   MTN env: %s | Airtel env: %s | Orange env: %s | MPESA env: %s",
                settings.MTN_MOMO_ENVIRONMENT, settings.AIRTEL_ENVIRONMENT,
                settings.ORANGE_MONEY_ENVIRONMENT, settings.MPESA_ENVIRONMENT)
    await create_tables()
    logger.info("✅ Database tables ready")
    yield
    logger.info("Shutting down...")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── CORS ────────────────────────────────────────────────────────────────

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174", "http://localhost:5175", "http://localhost:5173", "http://localhost:3000", "https://mobibitafrica.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routes ──────────────────────────────────────────────────────────────

app.include_router(api_router, prefix="/api")
app.include_router(auth_router, prefix="/api")
app.include_router(at_router, prefix="/api")
app.include_router(lightning_router, prefix="/api")


@app.get("/")
async def root():
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "status": "running",
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}
