"""Module entry point for `python -m robinhood_trader`.

This forwards to the CLI in `robinhood_trader.cli`.
"""

from .cli import main


if __name__ == "__main__":
    main()
