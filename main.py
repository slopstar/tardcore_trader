from dotenv import load_dotenv
from robinhood.client import CryptoAPITrading
from utils.pricing import get_all_holdings_with_prices
import os
import json
from pprint import pprint

# Load environment variables from .env file
load_dotenv()


def main() -> None:
    client = CryptoAPITrading()

    holdings = get_all_holdings_with_prices(client)
    # Pretty-print holdings for readability
    print("Holdings:")
    pprint(holdings)

    # Optional: if user has set CMC_API_KEY in .env, fetch latest quote for first holding
    from utils.coinmarketcap import get_latest_quote, CoinMarketCapError

    api_key = os.getenv("CMC_API_KEY")
    if api_key and len(holdings) > 0:
        first_asset = holdings[0][0]  # asset code like 'BTC'
        try:
            quote = get_latest_quote(first_asset)
            # Print a concise USD quote if present (pretty JSON)
            data = quote.get("data", {}).get(first_asset.upper(), {})
            usd = data.get("quote", {}).get("USD")
            if usd:
                print(f"CMC latest quote for {first_asset}:")
                print(json.dumps(usd, indent=2))
            else:
                print("CMC returned no USD quote for", first_asset)
                print("Full CMC response:")
                print(json.dumps(quote, indent=2))
        except CoinMarketCapError as e:
            print("CoinMarketCap error:", e)


if __name__ == "__main__":
    main()
