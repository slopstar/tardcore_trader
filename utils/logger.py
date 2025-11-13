import os
import json
import datetime
from typing import Any, Dict, List, Tuple

from robinhood.client import CryptoAPITrading
from utils.pricing import get_all_holdings
from utils.coinmarketcap import get_latest_quote, get_top_listings, CoinMarketCapError


def _utc_now() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc)


def _date_parts(dt: datetime.datetime) -> Tuple[str, str, str]:
    return f"{dt.year:04d}", f"{dt.month:02d}", f"{dt.day:02d}"


def _ensure_daily_path(base_dir: str = "logs") -> Tuple[str, str]:
    now = _utc_now()
    year, month, day = _date_parts(now)
    dir_path = os.path.join(base_dir, year, month)
    os.makedirs(dir_path, exist_ok=True)
    file_path = os.path.join(dir_path, f"{day}.json")
    return file_path, now


def _fetch_holdings_quotes(client: CryptoAPITrading) -> Tuple[List[Dict[str, Any]], float]:
    holdings = []
    total_value = 0.0

    try:
        rh_holdings = get_all_holdings(client)
    except Exception as e:  # Missing Robinhood creds or network issues
        print(f"Error fetching holdings from Robinhood: {e}")
        return holdings, total_value

    for asset, qty_str in rh_holdings:
        symbol = (asset or "").upper()
        try:
            qty = float(qty_str)
        except (TypeError, ValueError):
            qty = 0.0

        row: Dict[str, Any] = {"symbol": symbol, "quantity": qty}

        try:
            quote = get_latest_quote(symbol)
            usd = (quote.get("data", {}).get(symbol, {}).get("quote", {}) or {}).get("USD")
            if usd:
                price = float(usd.get("price") or 0)
                value = qty * price
                row.update(
                    {
                        "price_usd": price,
                        "value_usd": value,
                        "usd_quote": usd,
                    }
                )
                total_value += value
            else:
                row.update({"price_usd": None, "value_usd": None, "usd_quote": None})
        except CoinMarketCapError as e:
            row.update({"error": str(e)})

        holdings.append(row)

    return holdings, total_value


def _fetch_top_coins(limit: int = 50) -> List[Dict[str, Any]]:
    try:
        data = get_top_listings(limit=limit, convert="USD")
    except CoinMarketCapError:
        return []

    results: List[Dict[str, Any]] = []
    for item in data.get("data", [])[:limit]:
        usd = (item.get("quote") or {}).get("USD") or {}
        results.append(
            {
                "rank": item.get("cmc_rank"),
                "symbol": item.get("symbol"),
                "name": item.get("name"),
                "price_usd": usd.get("price"),
                "market_cap_usd": usd.get("market_cap"),
                "percent_change_24h": usd.get("percent_change_24h"),
                "usd_quote": usd,
            }
        )
    return results


def write_daily_snapshot(
    client: CryptoAPITrading,
    logs_dir: str = "logs",
    top_limit: int = 50,
    overwrite: bool = False,
    ) -> str:
    """
    Write a daily snapshot JSON containing holdings quotes and top coins.

    File path: logs/YYYY/MM/DD.json (UTC date)
    Returns the absolute or relative file path written (or existing path if skipped).
    """
    file_path, now = _ensure_daily_path(logs_dir)

    if os.path.exists(file_path) and not overwrite:
        return file_path

    holdings, total_value = _fetch_holdings_quotes(client)
    top_coins = _fetch_top_coins(limit=top_limit)

    year, month, day = _date_parts(now)
    payload: Dict[str, Any] = {
        "date": f"{year}-{month}-{day}",
        "generated_at_iso": now.replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "holdings": holdings,
        "top_coins": top_coins,
        "summary": {
            "portfolio_value_usd": total_value,
            "num_holdings": len(holdings),
            "top_count": len(top_coins),
        },
    }

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    return file_path

def pull_log_data(
    log_path: str,
    ) -> Dict[str, Any]:
    """
    Pull and deserialize log data from a given log file path.

    Args:
        log_path: Path to the log JSON file.

    Returns:
        Deserialized log data as a dictionary.
    """
    if not os.path.exists(log_path):
        raise FileNotFoundError(f"Log file not found: {log_path}")

    with open(log_path, "r", encoding="utf-8") as f:
        return json.load(f)