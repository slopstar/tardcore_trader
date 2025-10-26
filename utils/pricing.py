from __future__ import annotations

from typing import Any

from robinhood.client import CryptoAPITrading


class PricingError(Exception):
    """Raised when price data cannot be parsed from API response."""


def get_price(client: CryptoAPITrading, symbol: str) -> float:
    """Return the current price for the given symbol using the observed payload shape.

    Expects: { 'results': [ { 'price': '<number-as-string>', ... } ] }
    """
    payload: Any = client.get_best_bid_ask(symbol)

    # Surface client error early if present
    if isinstance(payload, dict) and payload.get("type") == "client_error":
        raise PricingError(str(payload))

    try:
        return float(payload["results"][0]["price"])  # type: ignore[index]
    except Exception as e:
        raise PricingError(f"Could not parse price for {symbol}. Payload: {payload}") from e
