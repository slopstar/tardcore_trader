from robinhood.client import CryptoAPITrading
from utils.coinmarketcap import get_latest_quote, CoinMarketCapError
import json
import os


def get_all_holdings(client: CryptoAPITrading) -> list:
    """Get all holdings from Robinhood - returns list of (asset_code, quantity) tuples."""
    holdings: dict = client.get_holdings()
    results: list = []

    for holding in holdings.get("results", []):
        asset: str = holding.get("asset_code")
        quantity: str = holding.get("quantity_available_for_trading")
        results.append((asset, quantity))

    return results


def fetch_cmc_quotes_for_holdings(holdings: list) -> None:
    """Fetch and print CoinMarketCap quotes with pricing for all holdings."""
    
    cmc_api_key = os.getenv("CMC_API_KEY")
    if not cmc_api_key:
        return

    if len(holdings) == 0:
        return

    for holding in holdings:
        asset = holding[0]  # asset code like 'BTC'
        quantity = float(holding[1])  # quantity held
        
        try:
            quote = get_latest_quote(asset)
            # Print a concise USD quote if present (pretty JSON)
            data = quote.get("data", {}).get(asset.upper(), {})
            usd = data.get("quote", {}).get("USD")
            if usd:
                price = usd.get("price", 0)
                total_value = quantity * price
                print(f"\n{asset}: {quantity} @ ${price:.2f} = ${total_value:.2f}")
                print("CMC data:")
                print(json.dumps(usd, indent=2))
            else:
                print(f"\nCMC returned no USD quote for {asset}")
                print("Full CMC response:")
                print(json.dumps(quote, indent=2))
        except CoinMarketCapError as e:
            print(f"\nCoinMarketCap error for {asset}:", e)


def display_portfolio(client: CryptoAPITrading) -> None:
    """Get holdings from Robinhood and display with CoinMarketCap pricing."""
    holdings = get_all_holdings(client)
    fetch_cmc_quotes_for_holdings(holdings)