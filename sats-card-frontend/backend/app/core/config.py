"""
Application configuration — loaded from environment variables or .env file.
All secrets live here; never hardcode credentials.
"""

from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # ── App ──────────────────────────────────────────────────────────
    APP_NAME: str = "Sats Card API"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = Field(default=False)
    SECRET_KEY: str = Field(..., description="JWT signing secret")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # ── Database ─────────────────────────────────────────────────────
    DATABASE_URL: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/satscard",
        description="Async PostgreSQL connection string",
    )

    # ── Redis ────────────────────────────────────────────────────────
    REDIS_URL: str = "redis://localhost:6379/0"

    # ── LND (Lightning Network Daemon) ──────────────────────────────
    LND_HOST: str = "localhost"
    LND_PORT: int = 10009
    LND_REST_PORT: int = 8080
    LND_MACAROON_HEX: str = Field(
        default="",
        description="Hex-encoded macaroon for LND authentication",
    )
    LND_TLS_CERT_PATH: str = Field(
        default="",
        description="Path to LND TLS certificate",
    )
    LND_NETWORK: str = "mainnet"  # mainnet | testnet | simnet

    # ── MTN Mobile Money (MoMo API) ────────────────────────────────
    MTN_MOMO_API_KEY: str = Field(default="", description="MTN MoMo API key (from developer portal)")
    MTN_MOMO_API_USER: str = Field(default="", description="MTN MoMo API user UUID")
    MTN_MOMO_API_SECRET: str = Field(default="", description="MTN MoMo API secret")
    MTN_MOMO_ENVIRONMENT: str = "sandbox"  # sandbox | production
    MTN_MOMO_SUBSCRIPTION_KEY: str = Field(default="", description="Subscription key from developer portal profile")
    MTN_MOMO_CALLBACK_URL: str = "https://yourdomain.com/api/webhooks/mtn"
    MTN_MOMO_COUNTRY: str = "rw"  # rw | ug | gh | cm

    # ── Airtel Money API ────────────────────────────────────────────
    AIRTEL_CLIENT_ID: str = Field(default="", description="Airtel API client ID")
    AIRTEL_CLIENT_SECRET: str = Field(default="", description="Airtel API client secret")
    AIRTEL_ENVIRONMENT: str = "sandbox"  # sandbox | production
    AIRTEL_BASE_URL: str = "https://openapi.airtel.africa"

    # ── Orange Money API ────────────────────────────────────────────
    ORANGE_MONEY_CLIENT_ID: str = Field(default="")
    ORANGE_MONEY_CLIENT_SECRET: str = Field(default="")
    ORANGE_MONEY_ENVIRONMENT: str = "sandbox"
    ORANGE_MONEY_BASE_URL: str = "https://api.orange.com/orange-money-webpay/dev/v1"

    # ── Exchange Rate ───────────────────────────────────────────────
    BTC_PRICE_FEED_URL: str = "https://api.coingecko.com/api/v3/simple/price"
    PRICE_CACHE_TTL_SECONDS: int = 30

    # ── Africa's Talking (USSD + SMS) ──────────────────────────────
    AT_API_KEY: str = Field(default="", description="Africa's Talking API key")
    AT_USERNAME: str = Field(default="sandbox", description="AT username (sandbox or production)")
    AT_ENVIRONMENT: str = "sandbox"  # sandbox | production

    # ── Strike (Bitcoin Lightning) ──────────────────────────────────
    STRIKE_API_KEY: str = Field(default="", description="Strike API key for Lightning payments")
    STRIKE_ENVIRONMENT: str = "sandbox"  # sandbox | production

    # ── SMS Gateway ─────────────────────────────────────────────────
    SMS_PROVIDER: str = "africastalking"  # africastalking | twilio
    SMS_API_KEY: str = Field(default="")
    SMS_SENDER_ID: str = "SATSCARD"

    # ── USSD ────────────────────────────────────────────────────────
    USSD_SESSION_TIMEOUT_SECONDS: int = 180  # 3 minutes
    USSD_SHORT_CODE: str = "*123#"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
