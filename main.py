from dotenv import load_dotenv
from robinhood.client import CryptoAPITrading
from utils.pricing import get_all_holdings_with_prices

# Load environment variables from .env file
load_dotenv()


def main() -> None:
    client = CryptoAPITrading()

    holdings = get_all_holdings_with_prices(client)
    print(holdings)

if __name__ == "__main__":
    main()
