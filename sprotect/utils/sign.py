"""Cross-signature and ring-chain signing utilities.

Provides HMAC-SHA256 single-file signing, verification, and
ring-chain multi-file signatures where each file's signature
depends on the next file's content hash, forming a closed loop.

Author: S-Protect Team
Version: 0.1.0
"""

from __future__ import annotations

import hmac as hmac_mod
import hashlib


def sign_file(file_path: str, key: bytes) -> str:
    """Compute an HMAC-SHA256 signature for the file content.

    Args:
        file_path: Path to the file to sign.
        key: The HMAC secret key.

    Returns:
        A 64-character lowercase hex HMAC-SHA256 digest.
    """
    with open(file_path, "rb") as f:
        data = f.read()
    return hmac_mod.new(key, data, hashlib.sha256).hexdigest()


def verify_file_signature(
    file_path: str, key: bytes, expected_sig: str
) -> bool:
    """Verify an HMAC-SHA256 signature against a file.

    Args:
        file_path: Path to the signed file.
        key: The HMAC secret key used during signing.
        expected_sig: The previously computed signature (hex string).

    Returns:
        True if the computed signature matches *expected_sig*.
    """
    actual = sign_file(file_path, key)
    return hmac_mod.compare_digest(actual, expected_sig)


def build_chain_signatures(
    files: list[str], chain_key: bytes
) -> dict[str, str]:
    """Build a ring-chain of interdependent signatures.

    File ``i`` gets an HMAC over its own content **plus** the SHA-256
    hash of file ``i+1`` (wrapping around so the last file depends on
    the first).  This creates a closed loop: tampering with any file
    breaks the chain.

    Args:
        files: Ordered list of file paths forming the chain ring.
        chain_key: HMAC key shared across all signatures.

    Returns:
        A dict mapping each file path to its 64-char hex signature.
    """
    n = len(files)
    file_hashes: list[bytes] = []
    for f in files:
        with open(f, "rb") as fh:
            file_hashes.append(hashlib.sha256(fh.read()).digest())

    signatures: dict[str, str] = {}
    for i, f in enumerate(files):
        next_hash = file_hashes[(i + 1) % n]
        with open(f, "rb") as fh:
            own_data = fh.read()
        combined = own_data + next_hash
        sig = hmac_mod.new(chain_key, combined, hashlib.sha256).hexdigest()
        signatures[f] = sig

    return signatures
