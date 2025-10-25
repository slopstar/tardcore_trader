"""Command-line interface for robinhood_trader.

Usage examples:
    python -m robinhood_trader generate-keys
    python -m robinhood_trader test-connection
    python -m robinhood_trader view-holdings BTC ETH
"""

from __future__ import annotations

import argparse
from pprint import pprint

from . import CryptoAPITrading
from .utils import generate_keypair


def cmd_generate_keys(_args: argparse.Namespace) -> None:
    print("=" * 70)
    print("Robinhood Crypto API Key Pair Generator")
    print("=" * 70)
    print()

    private_b64, public_b64 = generate_keypair()

    print("✅ Keys generated successfully!")
    print()
    print("-" * 70)
    print("PUBLIC KEY (paste this into Robinhood credential portal):")
    print("-" * 70)
    print(public_b64)
    print()
    print("-" * 70)
    print("PRIVATE KEY (⚠️  KEEP SECRET - add to your .env file):")
    print("-" * 70)
    print(private_b64)
    print()
    print("=" * 70)
    print("NEXT STEPS:")
    print("=" * 70)
    print("1. Go to: https://robinhood.com/account/crypto (desktop browser)")
    print("2. Create a new API credential")
    print("3. Paste your PUBLIC KEY when prompted")
    print("4. Copy the API_KEY that Robinhood gives you")
    print("5. Add to your .env file:")
    print()
    print("   API_KEY=rh-api-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx")
    print(f"   BASE64_PRIVATE_KEY={private_b64}")
    print()
    print("⚠️  Security reminder:")
    print("   - Never commit .env to git")
    print("   - Never share your PRIVATE KEY")
    print("   - Robinhood will NEVER ask for your private key")
    print("=" * 70)


def cmd_test_connection(_args: argparse.Namespace) -> None:
    client = CryptoAPITrading()
    resp = client.get_account()
    print("Response from get_account():")
    pprint(resp)


def cmd_view_holdings(args: argparse.Namespace) -> None:
    symbols = args.symbols or []
    client = CryptoAPITrading()
    resp = client.get_holdings(*symbols)
    pprint(resp)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="robinhood_trader",
        description="CLI for the Robinhood Crypto API helper package",
    )
    sub = parser.add_subparsers(dest="command")

    # generate-keys
    p_keys = sub.add_parser("generate-keys", help="Generate and print an Ed25519 keypair (base64)")
    p_keys.set_defaults(func=cmd_generate_keys)

    # test-connection
    p_test = sub.add_parser("test-connection", help="Call get_account() to validate credentials")
    p_test.set_defaults(func=cmd_test_connection)

    # view-holdings
    p_hold = sub.add_parser("view-holdings", help="Print holdings; optionally filter by asset codes (e.g., BTC ETH)")
    p_hold.add_argument("symbols", nargs="*", help="Asset codes to filter (optional)")
    p_hold.set_defaults(func=cmd_view_holdings)

    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


__all__ = ["main", "build_parser"]
