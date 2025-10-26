from robinhood.client import CryptoAPITrading


def get_current_market_price(client: CryptoAPITrading, symbol: str) -> float:
    """Get current market price for a trading pair symbol (e.g., 'BTC-USD')."""
    price_data = client.get_best_bid_ask(symbol)

    # Extract the ask price from the first result
    if "results" in price_data and len(price_data["results"]) > 0:
        result = price_data["results"][0]
        # Use ask price (what you'd pay to buy) - it's already a string price
        if "ask_inclusive_of_buy_spread" in result:
            return float(result["ask_inclusive_of_buy_spread"])

    # Handle error case
    return 0.0


def calculate_holding_value(quantity: str, price: float) -> float:
    """Calculate total value of a holding given quantity and price."""
    return float(quantity) * price


def get_all_holdings_with_prices(client: CryptoAPITrading) -> list:
    holdings: dict = client.get_holdings()
    results: list = []

    for holding in holdings.get("results", []):
        asset: str = holding.get("asset_code")
        quantity: str = holding.get("quantity_available_for_trading")
        # Convert asset code to trading pair symbol (e.g., BTC -> BTC-USD)
        symbol = f"{asset}-USD"
        price: float = get_current_market_price(client, symbol)
        approximate_dollar_value: float = calculate_holding_value(quantity, price)
        results.append((asset, quantity, price, approximate_dollar_value))

    return results