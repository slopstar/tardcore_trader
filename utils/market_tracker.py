from datetime import datetime
import json
import os
from robinhood.client import CryptoAPITrading
from utils.pricing import get_all_holdings_with_prices


def log_to_file(client: CryptoAPITrading) -> None:
    holdings = get_all_holdings_with_prices(client)
    current_time: str = datetime.now().isoformat()

    if not os.path.exists("market_logs"):
        os.makedirs("market_logs")
    
    current_date: str = datetime.now().strftime("%Y-%m-%d")
    filepath: str = os.path.join("market_logs", f"{current_date}_market_prices.jsonl")
    
    log_entry = {
        "timestamp": current_time,
        "holdings": holdings
    }
    
    with open(filepath, "a") as f:
        json.dump(log_entry, f)
        f.write("\n")