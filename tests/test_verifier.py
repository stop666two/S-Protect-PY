"""Tests for the runtime IntegrityVerifier.

Covers checksum ring verification, cross-signature chain verification,
and tampered-file detection.

Author: S-Protect Team
Version: 0.1.0
"""

from __future__ import annotations

import hashlib
import hmac as hmac_mod
import os

from sprotect.runtime.verifier import IntegrityVerifier

_TEST_TEMP = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "_test_temp"
)
os.makedirs(_TEST_TEMP, exist_ok=True)


def _tmp_path(name: str) -> str:
    return os.path.join(_TEST_TEMP, name)


def test_checksum_ring() -> None:
    """3-file checksum ring should pass verification."""
    verifier = IntegrityVerifier(_TEST_TEMP)
    names = ["ring_a", "ring_b", "ring_c"]
    paths = {n: f"{n}.txt" for n in names}

    for name in names:
        path = _tmp_path(f"{name}.txt")
        with open(path, "wb") as f:
            f.write(f"content_{name}".encode())

    try:
        ring_data: dict[str, str] = {}
        for name in names:
            rel = paths[name]
            full = _tmp_path(rel)
            with open(full, "rb") as f:
                ring_data[rel] = hashlib.sha256(f.read()).hexdigest()

        assert verifier.verify_checksum_ring(ring_data) is True
    finally:
        for name in names:
            p = _tmp_path(f"{name}.txt")
            if os.path.exists(p):
                os.remove(p)


def test_cross_signature_chain() -> None:
    """3-file cross-signature chain should pass verification."""
    verifier = IntegrityVerifier(_TEST_TEMP)
    chain_key = b"test-chain-key-32bytes!!!!!!"
    names = ["sig_a", "sig_b", "sig_c"]
    rel_paths = [f"{n}.txt" for n in names]

    for name in names:
        path = _tmp_path(f"{name}.txt")
        with open(path, "wb") as f:
            f.write(f"sig_content_{name}".encode())

    try:
        signatures: dict[str, str] = {}
        for name in names:
            rel = f"{name}.txt"
            full = _tmp_path(rel)
            with open(full, "rb") as f:
                content = f.read()
            signatures[rel] = hmac_mod.new(
                chain_key, content, hashlib.sha256
            ).hexdigest()

        assert (
            verifier.verify_cross_signature_chain(rel_paths, chain_key, signatures)
            is True
        )
    finally:
        for name in names:
            p = _tmp_path(f"{name}.txt")
            if os.path.exists(p):
                os.remove(p)


def test_tampered_file_fails() -> None:
    """A tampered file should cause checksum verification to fail."""
    verifier = IntegrityVerifier(_TEST_TEMP)
    rel_path = "tamper_check.txt"
    full_path = _tmp_path(rel_path)

    original_content = b"original content"
    with open(full_path, "wb") as f:
        f.write(original_content)

    original_hash = hashlib.sha256(original_content).hexdigest()

    with open(full_path, "wb") as f:
        f.write(b"tampered content")

    try:
        assert (
            verifier.verify_checksum_ring({rel_path: original_hash}) is False
        )
    finally:
        if os.path.exists(full_path):
            os.remove(full_path)
