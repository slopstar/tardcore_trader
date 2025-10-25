# tardcore_trader

A minimal Robinhood Crypto API helper project with a neat, package-first layout.

## Project layout

- `robinhood_trader/` — Python package with the trading client, utilities, and CLI
  - `client.py` — `CryptoAPITrading` HTTP client and signing helper
  - `utils/` — small reusable helpers
    - `keys.py` — `generate_keypair()` for Ed25519 keys
  - `cli.py` — command-line interface (subcommands)
  - `__main__.py` — enables `python -m robinhood_trader ...`
- `requirements.txt` — dependencies

## Setup

1) Create and activate a virtual environment (example):

```powershell
# Windows PowerShell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
```

2) Install dependencies:

```powershell
pip install -r requirements.txt
```

3) Create a `.env` file with your credentials (after generating keys):

```
API_KEY=rh-api-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
BASE64_PRIVATE_KEY=base64-of-your-private-key
```

## CLI usage

All previous scripts are now consolidated into a single CLI. Run the package as a module and select a subcommand:

```powershell
# Generate a new Ed25519 keypair (base64)
python -m robinhood_trader generate-keys

# Call get_account() to validate credentials
python -m robinhood_trader test-connection

# View holdings (optionally filter by asset code)
python -m robinhood_trader view-holdings           # all holdings
python -m robinhood_trader view-holdings BTC ETH   # filtered
```

This prints both public and private keys for `generate-keys`. Paste the PUBLIC key into the Robinhood portal. Add the PRIVATE key (base64) to your `.env`.

## Notes

- Secrets are ignored by `.gitignore` (`.env`, keys, etc.).
- The package exposes `CryptoAPITrading` and `generate_signature_base64` directly:

```python
from robinhood_trader import CryptoAPITrading, generate_signature_base64
```
