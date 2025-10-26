import base64
import datetime
import json
import os
from pathlib import Path
from typing import Any, Dict, Optional

import requests
from nacl.signing import SigningKey

try:
    from dotenv import load_dotenv  # type: ignore
    # Load .env from same directory as this file
    env_path = Path(__file__).parent / ".env"
    load_dotenv(env_path)
except Exception:
    # If python-dotenv isn't installed or file doesn't exist, use OS env vars
    pass

DEFAULT_BASE_URL = "https://trading.robinhood.com"


def _now_ts() -> int:
    return int(datetime.datetime.now(tz=datetime.timezone.utc).timestamp())


def generate_signature_base64(
    api_key: str,
    base64_private_key: str,
    timestamp: int,
    path: str,
    method: str,
    body: str = "",
) -> str:
    """
    Create base64-encoded Ed25519 signature for Robinhood Crypto API.
    Message format: f"{api_key}{timestamp}{path}{method}{body}"

    Notes:
    - For requests without a body (e.g., GET), body should be an empty string.
    - timestamp must be current within ~30 seconds when the request is received.
    """
    private_key_seed = base64.b64decode(base64_private_key)
    private_key = SigningKey(private_key_seed)
    message = f"{api_key}{timestamp}{path}{method}{body}"
    signed = private_key.sign(message.encode("utf-8"))
    return base64.b64encode(signed.signature).decode("utf-8")


class CryptoAPITrading:
    def __init__(
        self,
        api_key: Optional[str] = None,
        base64_private_key: Optional[str] = None,
        base_url: str = DEFAULT_BASE_URL,
        timeout: int = 10,
    ) -> None:
        self.api_key = api_key or os.getenv("API_KEY") or os.getenv("ROBINHOOD_API_KEY")
        self.base64_private_key = base64_private_key or os.getenv("BASE64_PRIVATE_KEY") or os.getenv("ROBINHOOD_BASE64_PRIVATE_KEY")
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

        if not self.api_key or not self.base64_private_key:
            # Allow construction for dry-run/testing (e.g., signature unit tests), but raise on network calls
            pass

    @staticmethod
    def get_query_params(key: str, *args: Optional[str]) -> str:
        if not args:
            return ""
        params = []
        for arg in args:
            if arg is None:
                continue
            params.append(f"{key}={arg}")
        return ("?" + "&".join(params)) if params else ""

    def _auth_headers(self, method: str, path: str, body: str) -> Dict[str, str]:
        if not self.api_key or not self.base64_private_key:
            raise RuntimeError("API_KEY and BASE64_PRIVATE_KEY are required. Set env vars or pass into CryptoAPITrading().")
        ts = _now_ts()
        signature = generate_signature_base64(self.api_key, self.base64_private_key, ts, path, method, body)
        return {
            "x-api-key": self.api_key,
            "x-signature": signature,
            "x-timestamp": str(ts),
            "Content-Type": "application/json; charset=utf-8",
        }

    def _request(self, method: str, path: str, body_obj: Optional[Dict[str, Any]] = None) -> Any:
        url = f"{self.base_url}{path}"
        body_str = json.dumps(body_obj) if body_obj is not None else ""
        headers = self._auth_headers(method, path, body_str)
        try:
            if method == "GET":
                resp = requests.get(url, headers=headers, timeout=self.timeout)
            elif method == "POST":
                payload = json.loads(body_str) if body_str else None
                resp = requests.post(url, headers=headers, json=payload, timeout=self.timeout)
            else:
                raise ValueError(f"Unsupported method: {method}")
            # Don't raise to allow callers to handle structured error responses
            return resp.json()
        except requests.RequestException as e:
            return {"type": "client_error", "errors": [{"attr": None, "detail": f"Request error: {e}"}]}

    # Accounts
    def get_account(self) -> Any:
        path = "/api/v1/crypto/trading/accounts/"
        return self._request("GET", path)

    # Market Data
    def get_best_bid_ask(self, *symbols: Optional[str]) -> Any:
        qp = self.get_query_params("symbol", *symbols)
        path = f"/api/v1/crypto/marketdata/best_bid_ask/{qp}"
        return self._request("GET", path)

    def get_estimated_price(self, symbol: str, side: str, quantity: str) -> Any:
        path = f"/api/v1/crypto/marketdata/estimated_price/?symbol={symbol}&side={side}&quantity={quantity}"
        return self._request("GET", path)

    # Trading
    def get_trading_pairs(self, *symbols: Optional[str], limit: Optional[int] = None, cursor: Optional[str] = None) -> Any:
        params = []
        for s in symbols or []:
            if s:
                params.append(("symbol", s))
        if limit is not None:
            params.append(("limit", str(limit)))
        if cursor is not None:
            params.append(("cursor", cursor))
        qp = ("?" + "&".join(f"{k}={v}" for k, v in params)) if params else ""
        path = f"/api/v1/crypto/trading/trading_pairs/{qp}"
        return self._request("GET", path)

    def get_holdings(self, *asset_codes: Optional[str], limit: Optional[int] = None, cursor: Optional[str] = None) -> Any:
        params = []
        for a in asset_codes or []:
            if a:
                params.append(("asset_code", a))
        if limit is not None:
            params.append(("limit", str(limit)))
        if cursor is not None:
            params.append(("cursor", cursor))
        qp = ("?" + "&".join(f"{k}={v}" for k, v in params)) if params else ""
        path = f"/api/v1/crypto/trading/holdings/{qp}"
        return self._request("GET", path)

    def get_orders(
        self,
        symbol: Optional[str] = None,
        side: Optional[str] = None,
        state: Optional[str] = None,
        type_: Optional[str] = None,
        created_at_start: Optional[str] = None,
        created_at_end: Optional[str] = None,
        updated_at_start: Optional[str] = None,
        updated_at_end: Optional[str] = None,
        limit: Optional[int] = None,
        cursor: Optional[str] = None,
    ) -> Any:
        params = []
        def add(k: str, v: Optional[str]):
            if v is not None:
                params.append((k, v))
        add("symbol", symbol)
        add("side", side)
        add("state", state)
        add("type", type_)
        add("created_at_start", created_at_start)
        add("created_at_end", created_at_end)
        add("updated_at_start", updated_at_start)
        add("updated_at_end", updated_at_end)
        if limit is not None:
            params.append(("limit", str(limit)))
        if cursor is not None:
            params.append(("cursor", cursor))
        qp = ("?" + "&".join(f"{k}={v}" for k, v in params)) if params else ""
        path = f"/api/v1/crypto/trading/orders/{qp}"
        return self._request("GET", path)

    def get_order(self, order_id: str) -> Any:
        path = f"/api/v1/crypto/trading/orders/{order_id}/"
        return self._request("GET", path)

    def cancel_order(self, order_id: str) -> Any:
        path = f"/api/v1/crypto/trading/orders/{order_id}/cancel/"
        return self._request("POST", path)

    def place_order(
        self,
        client_order_id: str,
        side: str,
        order_type: str,
        symbol: str,
        order_config: Dict[str, Any],
    ) -> Any:
        body = {
            "client_order_id": client_order_id,
            "side": side,
            "type": order_type,
            "symbol": symbol,
            f"{order_type}_order_config": order_config,
        }
        path = "/api/v1/crypto/trading/orders/"
        return self._request("POST", path, body)
