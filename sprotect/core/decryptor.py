"""Decryption engine for S-Protect-PY (testing/verification only).

Matches the HMAC-SHA256 stream cipher used by the build pipeline.
"""

from __future__ import annotations

import hmac
import hashlib
import json


def _xor_stream(key: bytes, data: bytes) -> bytes:
    out = bytearray(len(data))
    for i in range(0, len(data), 32):
        ctr = (i // 32).to_bytes(8, "big")
        stream = hmac.new(key, ctr, "sha256").digest()
        chunk = data[i:i+32]
        for j in range(len(chunk)):
            out[i+j] = chunk[j] ^ stream[j]
    return bytes(out)


def decrypt_file(encrypted_data: bytes) -> tuple[str, str]:
    """Decrypt an encrypted payload.

    Args:
        encrypted_data: JSON bytes from encrypt_file().

    Returns:
        Tuple of (source_code, source_hash).

    Raises:
        ValueError: If HMAC integrity check fails.
    """
    payload = json.loads(encrypted_data.decode("utf-8"))
    key = bytes.fromhex(payload["key"])
    ct = bytes.fromhex(payload["data"])
    sig = payload.get("hmac", "")
    expected = hmac.new(key, ct, "sha256").hexdigest()
    if sig and not hmac.compare_digest(sig, expected):
        raise ValueError("HMAC integrity check failed")
    plain = _xor_stream(key, ct)
    return plain.decode("utf-8"), payload.get("source_hash", "")
