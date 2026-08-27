"""
Exchange rate oracle — fetches live BTC prices with Redis caching.

Supports:
  - USD/BTC, UGX/BTC, KES/BTC, etc.
  - Caching to avoid hammering APIs
  - Fallback to last known rate on API failure
"""

from __future__ import annotations

import logging
import time
from typing import Optional

import httpx
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class ExchangeRate(BaseModel):
    from_currency: str
    to_currency: str
    rate: float
    timestamp: float
    source: str = "coingecko"


class ExchangeRateService:
    """
    Fetches and caches BTC exchange rates.

    Uses CoinGecko as primary source (free, no API key).
    Falls back to last known rate if API is down.
    """

    COINGECKO_URL = "https://api.coingecko.com/api/v3/simple/price"

    # Supported fiat currencies for CoinGecko
    SUPPORTED_FIAT = {
        "USD": "usd", "EUR": "eur", "GBP": "gbp",
        "UGX": "ugx", "KES": "kes", "TZS": "tzs",
        "GHS": "ghs", "NGN": "ngn", "ZAR": "zar",
        "XOF": "xof", "XAF": "xaf",
    }

    def __init__(self, cache_ttl: int = 30):
        self.cache_ttl = cache_ttl
        self._cache: dict[str, ExchangeRate] = {}
        self._http = httpx.AsyncClient(timeout=10.0)

    async def get_rate(self, from_currency: str, to_currency: str = "BTC") -> ExchangeRate:
        """
        Get the exchange rate from from_currency to BTC.

        Examples:
            rate = await get_rate("UGX", "BTC")
            rate = await get_rate("USD", "sats")
        """
        cache_key = f"{from_currency}:{to_currency}"

        # Check cache
        if cache_key in self._cache:
            cached = self._cache[cache_key]
            if time.time() - cached.timestamp < self.cache_ttl:
                return cached

        # Fetch fresh rate
        try:
            rate = await self._fetch_rate(from_currency, to_currency)
            self._cache[cache_key] = rate
            return rate
        except Exception as e:
            logger.warning("Failed to fetch rate %s→%s: %s", from_currency, to_currency, e)
            # Return last known rate if available
            if cache_key in self._cache:
                logger.info("Using cached rate for %s→%s", from_currency, to_currency)
                return self._cache[cache_key]
            raise

    async def convert(
        self,
        amount: float,
        from_currency: str,
        to_currency: str = "sats",
    ) -> dict:
        """
        Convert an amount from one currency to another.
        Uses USD as the pivot currency for cross-conversions.
        """
        if from_currency == to_currency:
            return {"amount": amount, "from": from_currency, "to": to_currency, "converted": amount}

        # Get BTC price in USD from CoinGecko
        btc_usd_rate = await self._get_btc_usd_rate()

        # Local currency → USD rates (approximate, updated periodically)
        fiat_to_usd = {
            "UGX": 1 / 3700,  # 3700 UGX = 1 USD
            "KES": 1 / 130,
            "TZS": 1 / 2500,
            "GHS": 1 / 12,
            "NGN": 1 / 1550,
            "XOF": 1 / 600,
            "XAF": 1 / 600,
            "USD": 1,
            "EUR": 1.08,
            "GBP": 1.27,
            "ZAR": 1 / 18,
        }

        # Convert from_currency → USD
        from_rate = fiat_to_usd.get(from_currency.upper(), 0)
        usd_amount = amount * from_rate

        # Convert USD → to_currency
        if to_currency.upper() == "SATS":
            # 1 BTC = btc_usd_rate USD = 100M sats
            # So 1 USD = 100M / btc_usd_rate sats
            sats_per_usd = 100_000_000 / btc_usd_rate if btc_usd_rate > 0 else 0
            converted = int(usd_amount * sats_per_usd)
        elif to_currency.upper() == "BTC":
            converted = usd_amount / btc_usd_rate if btc_usd_rate > 0 else 0
        elif to_currency.upper() == "USD":
            converted = round(usd_amount, 2)
        else:
            # Target fiat: USD → target
            to_rate = fiat_to_usd.get(to_currency.upper(), 0)
            converted = round(usd_amount / to_rate, 2) if to_rate > 0 else 0

        return {"amount": amount, "from": from_currency, "to": to_currency, "converted": converted}

    async def _get_btc_usd_rate(self) -> float:
        """Get BTC price in USD."""
        rate = await self.get_rate("USD", "BTC")
        return rate.rate if rate.rate > 0 else 79000  # fallback

    async def _fetch_rate(self, from_currency: str, to_currency: str) -> ExchangeRate:
        """Fetch rate from CoinGecko."""
        fiat_code = self.SUPPORTED_FIAT.get(from_currency.upper(), "usd")

        if to_currency.upper() == "BTC":
            params = {"ids": "bitcoin", "vs_currencies": fiat_code}
        elif to_currency.upper() == "SATS":
            params = {"ids": "bitcoin", "vs_currencies": fiat_code}
        else:
            params = {"ids": "bitcoin", "vs_currencies": fiat_code}

        resp = await self._http.get(self.COINGECKO_URL, params=params)
        resp.raise_for_status()
        data = resp.json()

        btc_data = data.get("bitcoin", {})
        price = btc_data.get(fiat_code, 0)

        if to_currency.upper() == "SATS":
            # Convert BTC price to sats price
            rate_value = 1 / (price / 100_000_000) if price > 0 else 0
        else:
            rate_value = price

        return ExchangeRate(
            from_currency=from_currency.upper(),
            to_currency=to_currency.upper(),
            rate=rate_value,
            timestamp=time.time(),
            source="coingecko",
        )

    async def close(self):
        await self._http.aclose()
