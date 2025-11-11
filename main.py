from dotenv import load_dotenv
from robinhood.client import CryptoAPITrading
from utils.pricing import display_portfolio, get_all_holdings, fetch_cmc_quotes_for_holdings
from pprint import pprint

# Load environment variables from .env file
load_dotenv()


def main() -> None:
    client = CryptoAPITrading()

    display_portfolio(client)


if __name__ == "__main__":
    main()
