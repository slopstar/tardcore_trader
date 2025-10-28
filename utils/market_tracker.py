from datetime import datetime
import json
import os
from robinhood.client import CryptoAPITrading
from utils.pricing import get_all_holdings_with_prices


def log_to_file() -> None:
    holdings = get_all_holdings_with_prices(CryptoAPITrading())
    current_date: str = datetime.now().strftime("%Y-%m-%d")
    current_time: str = datetime.now().strftime("%H:%M:%S")

    if not os.path.exists("market_logs"):
        os.makedirs("market_logs")
    
    filepath: str = os.path.join("market_logs", f"{current_date}_market_prices.json")
    with open(filepath, "a") as f:
        json.dump(holdings, f)
        f.write(f"Timestamp: {current_time}\n")