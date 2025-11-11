from dotenv import load_dotenv
from robinhood.client import CryptoAPITrading
from utils.pricing import display_portfolio
from utils.logger import write_daily_snapshot

# Load environment variables from .env file
load_dotenv()


def main() -> None:
    client = CryptoAPITrading()

    # Existing portfolio display (stdout)
    display_portfolio(client)

    # Daily snapshot JSON (idempotent: skips if file exists)
    path = write_daily_snapshot(client)
    print(f"Daily snapshot written/skipped at: {path}")


if __name__ == "__main__":
    main()
