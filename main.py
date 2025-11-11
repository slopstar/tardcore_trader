from dotenv import load_dotenv
from robinhood.client import CryptoAPITrading
from utils.pricing import display_portfolio

# Load environment variables from .env file
load_dotenv()


def main() -> None:
    client = CryptoAPITrading()

    display_portfolio(client)


if __name__ == "__main__":
    main()
