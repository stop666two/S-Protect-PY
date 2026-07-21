"""Decryption engine for S-Protect-PY.

Decrypts JSON payloads produced by the encryption engine, verifying
the source hash for integrity.

Author: S-Protect Team
Version: 0.1.0
"""

from __future__ import annotations

import json

from sprotect.utils.crypto import aes_decrypt, sha256_hash


def decrypt_file(encrypted_data: bytes) -> tuple[str, str]:
    """Decrypt an encrypted JSON payload back to source code.

    Parses the JSON payload, extracts the AES key and ciphertext,
    decrypts using AES-256-GCM, and verifies the source hash.

    Args:
        encrypted_data: JSON-encoded bytes (from encrypt_file output).

    Returns:
        A tuple of (decrypted_source_code, original_file_hash).

    Raises:
        ValueError: If the payload format is invalid or hash mismatch.
        InvalidTag: If decryption fails (wrong key or corrupted data).
    """
    payload = json.loads(encrypted_data.decode("utf-8"))

    if payload.get("type") != "encrypted_python":
        raise ValueError(f"Unknown payload type: {payload.get('type')}")
    if payload.get("algorithm") != "aes-256-gcm":
        raise ValueError(f"Unsupported algorithm: {payload.get('algorithm')}")

    aes_key = bytes.fromhex(payload["aes_key"])
    encrypted = bytes.fromhex(payload["data"])
    expected_hash = payload["source_hash"]

    decrypted = aes_decrypt(encrypted, aes_key)
    actual_hash = sha256_hash(decrypted)

    if actual_hash != expected_hash:
        raise ValueError(
            f"Source hash mismatch: expected {expected_hash}, got {actual_hash}"
        )

    return decrypted.decode("utf-8"), expected_hash
