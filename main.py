from typing import Any, Dict, Iterable, List
from robinhood.client import CryptoAPITrading
from utils.pricing import get_all_holdings_with_prices


def main() -> None:
    C = CryptoAPITrading()

    holdings = get_all_holdings_with_prices(C)
    print(holdings)

if __name__ == "__main__":
    main()
