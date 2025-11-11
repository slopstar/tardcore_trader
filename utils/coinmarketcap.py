import os
import time
from typing import Any, Dict, Optional

import requests

API_BASE = "https://pro-api.coinmarketcap.com/v1"


class CoinMarketCapError(Exception):
    pass


def _cmc_get(path: str, params: Optional[Dict[str, str]] = None, timeout: int = 10) -> Any:
    """
    Internal helper to call CoinMarketCap Pro API.
    Reads API key from the `CMC_API_KEY` environment variable.
    """
    api_key = os.getenv("CMC_API_KEY")
    if not api_key:
        raise CoinMarketCapError("CMC_API_KEY not set in environment")

    headers = {"X-CMC_PRO_API_KEY": api_key}
    url = f"{API_BASE}{path}"

    try:
        resp = requests.get(url, headers=headers, params=params or {}, timeout=timeout)
        resp.raise_for_status()
        data = resp.json()
        # CoinMarketCap returns a 'status' object with error info when something went wrong
        if isinstance(data, dict) and "status" in data and data["status"].get("error_code", 0) != 0:
            raise CoinMarketCapError(data["status"].get("error_message") or "CMC API error")
        return data
    except requests.RequestException as e:
        raise CoinMarketCapError(f"Request failed: {e}")


def get_latest_quote(symbol: str) -> Dict[str, Any]:
    """
    Get the latest quote for a symbol (e.g., 'BTC', 'ETH').
    Returns the JSON response from `/cryptocurrency/quotes/latest`.
    """
    path = "/cryptocurrency/quotes/latest"
    params = {"symbol": symbol.upper()}
    return _cmc_get(path, params=params)


def get_historical_ohlcv(
    symbol: str,
    time_start: Optional[str] = None,
    time_end: Optional[str] = None,
    interval: str = "daily",
) -> Dict[str, Any]:
    """
    Get historical OHLCV data from CMC.

    - `symbol`: symbol like 'BTC' or 'ETH'
    - `time_start` / `time_end`: RFC3339 or `YYYY-MM-DD` strings accepted by CMC
    - `interval`: 'daily', 'hourly', etc. (availability depends on plan)

    Returns the JSON response from `/cryptocurrency/ohlcv/historical`.
    This function retries a few times on transient failures.
    """
    path = "/cryptocurrency/ohlcv/historical"
    params: Dict[str, str] = {"symbol": symbol.upper(), "interval": interval}
    if time_start:
        params["time_start"] = time_start
    if time_end:
        params["time_end"] = time_end

    for attempt in range(3):
        try:
            return _cmc_get(path, params=params)
        except CoinMarketCapError:
            # simple backoff
            if attempt < 2:
                time.sleep(1 + attempt * 2)
                continue
            raise


def get_top_listings(limit: int = 50, convert: str = "USD") -> Dict[str, Any]:
    """
    Get top cryptocurrencies by market cap.

    Returns the JSON response from `/cryptocurrency/listings/latest`.
    - `limit`: number of assets to return (default 50)
    - `convert`: fiat or crypto symbol to convert prices to (default 'USD')
    """
    path = "/cryptocurrency/listings/latest"
    params = {
        "start": "1",
        "limit": str(limit),
        "convert": convert,
    }
    return _cmc_get(path, params=params)
