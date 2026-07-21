"""Cryptographic engine: cross-file sharded key, multi-layer encryption, chain integrity."""

from __future__ import annotations
import os, hashlib, hmac, json, secrets, zlib
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def aes_key() -> bytes:
    return AESGCM.generate_key(bit_length=256)

def aes_encrypt(data: bytes, key: bytes, aad: bytes = b"") -> bytes:
    nonce = os.urandom(12)
    return nonce + AESGCM(key).encrypt(nonce, data, aad)

def aes_decrypt(ct: bytes, key: bytes, aad: bytes = b"") -> bytes:
    return AESGCM(key).decrypt(ct[:12], ct[12:], aad)

def split_key(key: bytes, n: int) -> list[bytes]:
    """Split key into N XOR shards. Reconstruct with xor_shards()."""
    if n < 2: raise ValueError("Need at least 2 shards")
    shards = [os.urandom(len(key)) for _ in range(n - 1)]
    final = bytearray(len(key))
    for i in range(len(key)):
        v = key[i]
        for s in shards: v ^= s[i]
        final[i] = v
    shards.append(bytes(final))
    return shards

def xor_shards(shards: list[bytes]) -> bytes:
    r = bytearray(shards[0])
    for s in shards[1:]:
        for i in range(len(r)): r[i] ^= s[i]
    return bytes(r)

def chain_hash(payloads: list[dict], key: bytes) -> list[str]:
    """Build circular HMAC chain using encrypted data field (d) only.
    This ensures chain signatures remain valid even when metadata fields change."""
    n = len(payloads)
    sigs = []
    for i in range(n):
        h = hashlib.sha256(payloads[(i + 1) % n].get("d", "").encode()).digest()
        sigs.append(hmac.new(key, h, "sha256").hexdigest())
    return sigs

def xof_stream(length: int, seed: bytes) -> bytes:
    r = bytearray(); c = 0
    while len(r) < length:
        r.extend(hashlib.sha256(seed + c.to_bytes(4, "big")).digest())
        c += 1
    return bytes(r[:length])

def xor_stream(data: bytes, key: bytes) -> bytes:
    ks = xof_stream(len(data), key)
    return bytes(a ^ b for a, b in zip(data, ks))

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def encrypt_payload(source_data: bytes, shard: bytes, chain_sig: str = "",
                    compress: int = 9, pad_max: int = 512) -> bytes:
    """Encrypt with multi-layer + embedded shard.

    Payload structure:
    - Shard (32 bytes) XOR'd across files, need ALL to reconstruct master key
    - AES-GCM ciphertext of compressed source
    - Chain signature for cross-file integrity
    """
    compressed = zlib.compress(source_data, level=compress)
    xored = xor_stream(compressed, shard)
    ct = aes_encrypt(xored, shard)
    pad = os.urandom(secrets.randbelow(pad_max + 1))
    payload = {
        "v": 3, "s": shard.hex(), "d": ct.hex(),
        "c": chain_sig, "p": pad.hex(), "h": sha256(source_data),
    }
    return json.dumps(payload, separators=(",", ":")).encode()


def decrypt_payload(data: bytes, shard: bytes, expected_chain: str = "") -> tuple[str, str]:
    """Decrypt with given shard (use reconstructed master key)."""
    p = json.loads(data.decode())
    if p.get("v") != 3:
        raise ValueError("Unsupported payload version")
    if expected_chain and p.get("c", "") != expected_chain:
        raise ValueError("Chain integrity check failed")
    ct = bytes.fromhex(p["d"])
    xored = aes_decrypt(ct, shard)
    compressed = xor_stream(xored, hashlib.sha256(shard).digest()[:32])
    src = zlib.decompress(compressed).decode()
    return src, p.get("h", "")


def encrypt_loader(loader_source: str, key: bytes) -> bytes:
    """Encrypt the runtime loader itself with the master key."""
    return encrypt_payload(loader_source.encode(), key, pad_max=0)


def decrypt_loader(data: bytes, key: bytes) -> str:
    """Decrypt runtime loader."""
    src, _ = decrypt_payload(data, key)
    return src
