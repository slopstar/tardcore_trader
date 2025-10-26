"""
Key generation utilities for Robinhood Crypto API (Ed25519).

Exposes `generate_keypair()` which returns a tuple of base64-encoded
(private_key, public_key) matching the format expected by Robinhood.
"""

from __future__ import annotations

import base64
from typing import Tuple

import nacl.signing


def generate_keypair() -> Tuple[str, str]:
    """Generate an Ed25519 key pair and return as base64 strings.

    Returns:
        (private_key_base64, public_key_base64)
    """
    # Generate an Ed25519 keypair
    private_key = nacl.signing.SigningKey.generate()
    public_key = private_key.verify_key

    # Convert to base64 strings (format Robinhood expects)
    private_key_base64 = base64.b64encode(private_key.encode()).decode()
    public_key_base64 = base64.b64encode(public_key.encode()).decode()

    return private_key_base64, public_key_base64
