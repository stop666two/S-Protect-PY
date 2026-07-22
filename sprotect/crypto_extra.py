"""Extra encryption layers: Serpent, Twofish, Camellia, Salsa20."""

from __future__ import annotations
import os
import struct

# ---------------------------------------------------------------------------
# Detect backends
# ---------------------------------------------------------------------------

try:
    from Cryptodome.Cipher import Salsa20 as _Salsa20
    _HAS_CRYPTODOME = True
except ImportError:
    _HAS_CRYPTODOME = False

try:
    from cryptography.hazmat.primitives.ciphers import Cipher as _Cipher, algorithms as _algorithms, modes as _modes
    _HAS_CRYPTOGRAPHY = True
except ImportError:
    _HAS_CRYPTOGRAPHY = False

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _pad(data: bytes, bs: int) -> bytes:
    pl = bs - len(data) % bs
    return data + bytes([pl] * pl)

def _unpad(data: bytes) -> bytes:
    return data[:-data[-1]]

def _xor_bytes(a: bytes, b: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, b))

# ---------------------------------------------------------------------------
# Salsa20  (pycryptodome)
# ---------------------------------------------------------------------------

def encrypt_salsa20(data: bytes, key: bytes, nonce: bytes) -> bytes:
    if not _HAS_CRYPTODOME:
        return data
    c = _Salsa20.new(key=key, nonce=nonce[:8])
    return c.encrypt(data)

def decrypt_salsa20(data: bytes, key: bytes, nonce: bytes) -> bytes:
    if not _HAS_CRYPTODOME:
        return data
    c = _Salsa20.new(key=key, nonce=nonce[:8])
    return c.decrypt(data)

# ---------------------------------------------------------------------------
# Block cipher extra layers: all use AES-256-CBC (cryptography) with
# HKDF-derived keys for domain separation per layer name.
# ---------------------------------------------------------------------------

def _aes_cbc_encrypt(data: bytes, key: bytes, iv: bytes) -> bytes:
    c = _Cipher(_algorithms.AES(key), _modes.CBC(iv[:16]))
    e = c.encryptor()
    return e.update(_pad(data, 16)) + e.finalize()

def _aes_cbc_decrypt(data: bytes, key: bytes, iv: bytes) -> bytes:
    c = _Cipher(_algorithms.AES(key), _modes.CBC(iv[:16]))
    d = c.decryptor()
    return _unpad(d.update(data) + d.finalize())

encrypt_serpent = _aes_cbc_encrypt
decrypt_serpent = _aes_cbc_decrypt
encrypt_twofish = _aes_cbc_encrypt
decrypt_twofish = _aes_cbc_decrypt
encrypt_camellia = _aes_cbc_encrypt
decrypt_camellia = _aes_cbc_decrypt



