"""Cryptographic engine: multi-layer AES-256-GCM, RSA key wrapping, polymorphic padding."""

from __future__ import annotations
import os, hashlib, hmac, json, secrets, struct, zlib
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization


def aes_key() -> bytes:
    return AESGCM.generate_key(bit_length=256)

def aes_encrypt(data: bytes, key: bytes, aad: bytes = b"") -> bytes:
    nonce = os.urandom(12)
    return nonce + AESGCM(key).encrypt(nonce, data, aad)

def aes_decrypt(ct: bytes, key: bytes, aad: bytes = b"") -> bytes:
    return AESGCM(key).decrypt(ct[:12], ct[12:], aad)

def xof_stream(length: int, seed: bytes) -> bytes:
    """Extendable-output function: generates arbitrary-length keystream from seed."""
    result = bytearray()
    ctr = 0
    while len(result) < length:
        result.extend(hashlib.sha256(seed + ctr.to_bytes(4, "big")).digest())
        ctr += 1
    return bytes(result[:length])

def xor_stream(data: bytes, key: bytes) -> bytes:
    ks = xof_stream(len(data), key)
    return bytes(a ^ b for a, b in zip(data, ks))

def hmac_sign(data: bytes, key: bytes) -> str:
    return hmac.new(key, data, "sha256").hexdigest()

def rsa_keypair() -> tuple[bytes, bytes]:
    pk = rsa.generate_private_key(65537, 4096)
    return (pk.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8, serialization.NoEncryption()),
            pk.public_key().public_bytes(serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo))

def rsa_encrypt(data: bytes, pub: bytes) -> bytes:
    return serialization.load_pem_public_key(pub).encrypt(
        data, padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=None))

def rsa_decrypt(data: bytes, priv: bytes) -> bytes:
    return serialization.load_pem_private_key(priv, None).decrypt(
        data, padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=None))

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def encrypt_payload(source_data: bytes, algorithm: str = "aes-256-gcm") -> bytes:
    """Multi-layer encryption with polymorphic padding.

    Encryption layers:
    1. Compress source with zlib (obfuscates plaintext patterns)
    2. XOR with a random stream (pre-layer obfuscation)
    3. AES-256-GCM primary encryption
    4. Random padding appended (polymorphic output size)
    """
    # Layer 1: compress
    compressed = zlib.compress(source_data, level=9)
    # Layer 2: XOR obfuscation
    xor_key = os.urandom(32)
    xored = xor_stream(compressed, xor_key)
    # Layer 3: AES-256-GCM with AAD
    aes_k = aes_key()
    ct = aes_encrypt(xored, aes_k, aad=b"S-Protect-v2")
    # Polymorphic padding (random size 0-256 bytes)
    pad = os.urandom(secrets.randbelow(256))
    # Build payload
    payload = {
        "v": 2, "a": "aes",
        "k": aes_k.hex(),              # AES key
        "x": xor_key.hex(),            # XOR key (pre-layer)
        "d": ct.hex(),                 # ciphertext
        "h": sha256(source_data),      # source hash
        "p": pad.hex(),                # polymorphic padding
        "s": hmac_sign(ct, aes_k),     # HMAC of ciphertext
    }
    return json.dumps(payload, separators=(",", ":")).encode()


def decrypt_payload(data: bytes) -> tuple[str, str]:
    """Decrypt a multi-layer encrypted payload."""
    p = json.loads(data.decode())
    if p.get("v") != 2:
        raise ValueError("Unsupported payload version")
    aes_k = bytes.fromhex(p["k"])
    ct = bytes.fromhex(p["d"])
    # Verify HMAC
    expected = p.get("s", "")
    if expected and not hmac.compare_digest(expected, hmac_sign(ct, aes_k)):
        raise ValueError("HMAC integrity check failed")
    # Layer 3: AES decrypt
    xored = aes_decrypt(ct, aes_k, aad=b"S-Protect-v2")
    # Layer 2: XOR decrypt
    xor_k = bytes.fromhex(p["x"])
    compressed = xor_stream(xored, xor_k)
    # Layer 1: decompress
    src = zlib.decompress(compressed).decode()
    return src, p.get("h", "")
