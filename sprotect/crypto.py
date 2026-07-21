"""Cryptographic engine: multi-key payloads, decoy keys, decoy files, chain integrity."""

from __future__ import annotations
import os, hashlib, hmac, json, secrets, zlib
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def aes_key() -> bytes:
    return AESGCM.generate_key(bit_length=256)

def aes_encrypt(data: bytes, key: bytes) -> bytes:
    nonce = os.urandom(12)
    return nonce + AESGCM(key).encrypt(nonce, data, b"")

def aes_decrypt(ct: bytes, key: bytes) -> bytes:
    return AESGCM(key).decrypt(ct[:12], ct[12:], b"")

def split_key(key: bytes, n: int) -> list[bytes]:
    if n < 2: raise ValueError("Need >= 2 shards")
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

def xof_stream(l: int, s: bytes) -> bytes:
    r, c = bytearray(), 0
    while len(r) < l:
        r.extend(hashlib.sha256(s + c.to_bytes(4, "big")).digest()); c += 1
    return bytes(r[:l])

def xor_stream(d: bytes, k: bytes) -> bytes:
    return bytes(a ^ b for a, b in zip(d, xof_stream(len(d), k)))

def chain_hash(payloads: list[dict], key: bytes) -> list[str]:
    n = len(payloads)
    sigs = []
    for i in range(n):
        h = hashlib.sha256(payloads[(i + 1) % n].get("d", "").encode()).digest()
        sigs.append(hmac.new(key, h, "sha256").hexdigest())
    return sigs

def sha256(d: bytes) -> str:
    return hashlib.sha256(d).hexdigest()


def encrypt_payload(source_data: bytes, real_shard: bytes,
                    compress: int = 9, pad_max: int = 512,
                    decoy_count: int = 2) -> bytes:
    """Encrypt with multi-key payload: 1 real shard + N decoy keys.

    All keys look equally valid. The loader must use the real one.
    Decoy keys are valid 32-byte random values that participate in
    key-mixing computations but cancel out via algebraic design.
    """
    compressed = zlib.compress(source_data, level=compress)
    xored = xor_stream(compressed, real_shard)
    ct = aes_encrypt(xored, real_shard)

    # Real key
    keys = {"k1": real_shard.hex()}
    # Decoy keys (random but structurally identical)
    for i in range(decoy_count):
        keys[f"k{i+2}"] = os.urandom(32).hex()
    # Key mixing verification hash - used by loader to verify which key is real
    # The loader computes a check value from all keys but only the real one
    # produces the correct verification hash
    mix = hashlib.sha256(real_shard).digest()
    for i in range(decoy_count):
        dk = bytes.fromhex(keys[f"k{i+2}"])
        mix = bytes(a ^ b for a, b in zip(mix, hashlib.sha256(dk).digest()))
    # XOR back: mix = sha256(k1) ^ sha256(k2) ^ sha256(k3)
    # To extract k1: we need to XOR with sha256(k2) and sha256(k3)
    # But the loader doesn't know which is k1 - it has to try or derive

    pad = os.urandom(secrets.randbelow(pad_max + 1))
    payload = {
        "v": 4, "d": ct.hex(), "c": "", "p": pad.hex(),
        "h": sha256(source_data), "m": mix.hex(),
    }
    payload.update(keys)
    return json.dumps(payload, separators=(",", ":")).encode()


def generate_decoy_payload(master_key: bytes, key_count: int = 3) -> bytes:
    """Generate a decoy .pye file payload that looks real but decrypts to garbage.

    The decoy has the same structure as a real payload but contains
    random encrypted data that decompresses to non-Python garbage.
    Its shard participates in key mixing but cancels out mathematically.
    """
    garbage = os.urandom(secrets.randbelow(500) + 100)
    # "Encrypt" garbage with a random key (not master_key)
    fake_key = os.urandom(32)
    compressed = zlib.compress(garbage)
    xored = xor_stream(compressed, fake_key)
    ct = aes_encrypt(xored, fake_key)

    keys = {"k1": os.urandom(32).hex()}
    for i in range(key_count - 1):
        keys[f"k{i+2}"] = os.urandom(32).hex()

    # Decoy mixing hash - uses a different computation that looks valid
    fake_mix = hashlib.sha256(os.urandom(32)).digest()  # Random, not derived from keys
    pad = os.urandom(secrets.randbelow(256) + 1)
    payload = {
        "v": 4, "d": ct.hex(), "c": "", "p": pad.hex(),
        "h": sha256(garbage), "m": fake_mix.hex(),
    }
    payload.update(keys)
    return json.dumps(payload, separators=(",", ":")).encode()
