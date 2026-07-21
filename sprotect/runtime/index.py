"""Runtime index decryption and signature verification.

Loads the encrypted index file, decrypts it using AES-256-GCM,
and verifies its HMAC-SHA256 integrity signature before the
reconstructor uses the shard metadata.

Author: S-Protect Team
Version: 0.1.0
"""

from __future__ import annotations

import hashlib
import hmac as hmac_mod
import json
from typing import Any

from sprotect.utils.crypto import aes_decrypt


def decrypt_index(encrypted_index: bytes, index_key: bytes) -> dict[str, Any]:
    """Decrypt an encrypted index payload.

    The encrypted index is expected to be an AES-256-GCM ciphertext
    (12-byte nonce + ciphertext + tag) whose plaintext is a JSON
    object.

    Args:
        encrypted_index: The raw encrypted index bytes.
        index_key: A 32-byte AES-256 key.

    Returns:
        The deserialized index dict.
    """
    plaintext = aes_decrypt(encrypted_index, index_key)
    return json.loads(plaintext.decode("utf-8"))


def verify_index_signature(index: dict[str, Any], signing_key: bytes) -> bool:
    """Verify the HMAC-SHA256 signature embedded in the index.

    The index dict must contain a ``signature`` field whose value is
    the 64-char hex HMAC-SHA256 of the canonical JSON representation
    (sorted keys, no extra whitespace) of the **rest** of the dict.

    Args:
        index: The deserialized index dict.
        signing_key: The HMAC key used to sign the index.

    Returns:
        True if the signature is valid.
    """
    expected_sig = index.get("signature", "")
    if not expected_sig:
        return False

    payload = {k: v for k, v in index.items() if k != "signature"}
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    computed = hmac_mod.new(
        signing_key, canonical.encode("utf-8"), hashlib.sha256
    ).hexdigest()
    return hmac_mod.compare_digest(computed, expected_sig)
