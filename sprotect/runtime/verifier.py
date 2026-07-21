"""Runtime integrity verification for checksum rings and cross-signature chains.

Verifies that the protected project's files have not been tampered with
by checking checksum ring integrity and cross-file HMAC signature chains.

Author: S-Protect Team
Version: 0.1.0
"""

from __future__ import annotations

import hashlib
import hmac as hmac_mod
import os


class IntegrityVerifier:
    """Verifies file integrity using checksum rings and cross-signature chains.

    Checksum ring: each file's hash is stored in another file, forming a
    closed ring. The verifier reads each file, computes its hash, and
    checks that it matches the expected value.

    Cross-signature chain: files are ordered in a chain where each file's
    HMAC-SHA256 signature is derived from its content. The verifier
    recomputes the HMAC for each file and compares against expected values.
    """

    def __init__(self, runtime_dir: str) -> None:
        """Initialize the verifier with the runtime directory path.

        Args:
            runtime_dir: Path to the directory containing files to verify.
        """
        self.runtime_dir = runtime_dir

    def verify_checksum_ring(self, ring_data: dict[str, str]) -> bool:
        """Verify a checksum ring for the given files.

        ``ring_data`` maps each relative file path to its expected
        SHA-256 hex digest.  The method reads each file, computes its
        actual SHA-256 hash, and compares it to the expected value.
        Returns ``True`` only if every file matches.

        Args:
            ring_data: Mapping of relative file path to expected
                       SHA-256 hex digest.

        Returns:
            True if all file hashes match their expected values.
        """
        for rel_path, expected_hex in ring_data.items():
            full_path = os.path.join(self.runtime_dir, rel_path)
            if not os.path.isfile(full_path):
                return False
            with open(full_path, "rb") as f:
                actual_hex = hashlib.sha256(f.read()).hexdigest()
            if actual_hex != expected_hex:
                return False
        return True

    def verify_cross_signature_chain(
        self,
        files: list[str],
        chain_key: bytes,
        signatures: dict[str, str],
    ) -> bool:
        """Verify an HMAC-SHA256 cross-signature chain.

        ``files`` is the ordered list of relative file paths in the
        chain.  ``chain_key`` is the HMAC key.  ``signatures`` maps
        each relative file path to its expected HMAC-SHA256 hex digest.

        The method recomputes the HMAC-SHA256 of each file's content
        and compares it with the expected signature.  Returns ``True``
        only if every signature is valid.

        Args:
            files: Ordered list of relative file paths in the chain.
            chain_key: HMAC key used for signing.
            signatures: Mapping of relative file path to expected
                        HMAC-SHA256 hex digest.

        Returns:
            True if all file signatures are valid.
        """
        for rel_path in files:
            if rel_path not in signatures:
                return False
            full_path = os.path.join(self.runtime_dir, rel_path)
            if not os.path.isfile(full_path):
                return False
            with open(full_path, "rb") as f:
                content = f.read()
            expected = signatures[rel_path]
            computed = hmac_mod.new(
                chain_key, content, hashlib.sha256
            ).hexdigest()
            if not hmac_mod.compare_digest(computed, expected):
                return False
        return True
