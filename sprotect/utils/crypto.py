"""Cryptographic utility functions for S-Protect-PY.

Provides AES-256-GCM symmetric encryption, RSA OAEP asymmetric
encryption, SHA-256 hashing, and HMAC-SHA256 signing using the
cryptography library.

Author: S-Protect Team
Version: 0.1.0
"""

from __future__ import annotations

import hashlib
import hmac as hmac_mod
import os

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def generate_aes_key() -> bytes:
    """Generate a random AES-256 key (32 bytes).

    Returns:
        A 32-byte random AES key suitable for AES-256-GCM.
    """
    return AESGCM.generate_key(bit_length=256)


def aes_encrypt(data: bytes, key: bytes) -> bytes:
    """Encrypt data using AES-256-GCM.

    The ciphertext is prefixed with the 12-byte nonce used for
    encryption, enabling deterministic decryption without separate
    nonce management.

    Args:
        data: The plaintext bytes to encrypt.
        key: A 32-byte AES-256 key (from generate_aes_key).

    Returns:
        Concatenated nonce (12 bytes) + ciphertext bytes.
    """
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, data, None)
    return nonce + ciphertext


def aes_decrypt(ciphertext: bytes, key: bytes) -> bytes:
    """Decrypt AES-256-GCM encrypted data.

    Expects the first 12 bytes to be the nonce used during encryption,
    followed by the ciphertext + GCM authentication tag.

    Args:
        ciphertext: Nonce (12 bytes) + ciphertext bytes.
        key: A 32-byte AES-256 key matching the encryption key.

    Returns:
        The decrypted plaintext bytes.

    Raises:
        InvalidTag: If the key is wrong or data is corrupted.
    """
    nonce = ciphertext[:12]
    ct = ciphertext[12:]
    aesgcm = AESGCM(key)
    return aesgcm.decrypt(nonce, ct, None)


def generate_rsa_keypair() -> tuple[bytes, bytes]:
    """Generate an RSA-2048 key pair.

    Returns:
        A tuple of (private_key_pem, public_key_pem) as bytes.
    """
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    public_pem = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    return private_pem, public_pem


def rsa_encrypt(data: bytes, public_key_pem: bytes) -> bytes:
    """Encrypt data using RSA OAEP with SHA-256.

    Args:
        data: The plaintext bytes to encrypt (max 190 bytes for RSA-2048).
        public_key_pem: The PEM-encoded public key.

    Returns:
        The encrypted ciphertext bytes.
    """
    public_key = serialization.load_pem_public_key(public_key_pem)
    assert hasattr(public_key, "encrypt")
    return public_key.encrypt(  # type: ignore[union-attr]
        data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )


def rsa_decrypt(ciphertext: bytes, private_key_pem: bytes) -> bytes:
    """Decrypt RSA OAEP encrypted data.

    Args:
        ciphertext: The ciphertext bytes to decrypt.
        private_key_pem: The PEM-encoded private key.

    Returns:
        The decrypted plaintext bytes.
    """
    private_key = serialization.load_pem_private_key(
        private_key_pem,
        password=None,
    )
    assert hasattr(private_key, "decrypt")
    return private_key.decrypt(  # type: ignore[union-attr]
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )


def sha256_hash(data: bytes) -> str:
    """Compute the SHA-256 hex digest of the given data.

    Args:
        data: The input bytes to hash.

    Returns:
        A 64-character lowercase hex string of the SHA-256 hash.
    """
    return hashlib.sha256(data).hexdigest()


def hmac_sign(data: bytes, key: bytes) -> str:
    """Create an HMAC-SHA256 signature for the given data.

    Args:
        data: The input bytes to sign.
        key: The HMAC secret key bytes.

    Returns:
        A 64-character lowercase hex string of the HMAC-SHA256 signature.
    """
    return hmac_mod.new(key, data, hashlib.sha256).hexdigest()
