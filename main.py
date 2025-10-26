from typing import Any, Dict, Iterable, List
from robinhood.client import CryptoAPITrading


def main() -> None:
    C = CryptoAPITrading()

    print(C.get_holdings())

if __name__ == "__main__":
    main()
