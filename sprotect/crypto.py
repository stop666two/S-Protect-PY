"""Cryptographic engine: random-key-position payloads, decoy files, chain integrity."""

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

def key_fingerprint(key: bytes) -> str:
    """4-byte fingerprint of a key. Used to identify which key is real."""
    return hashlib.sha256(key).digest()[:4].hex()


def encrypt_payload(source_data: bytes, real_key: bytes,
                    compress: int = 9, pad_max: int = 512,
                    decoy_count: int = 2) -> bytes:
    """Encrypt with randomly-positioned real key.

    Payload has k1, k2, k3 - ONE is the real key (randomly chosen),
    the others are decoys. The 'f' field stores the fingerprint
    of the real key so the loader can identify it.
    """
    compressed = zlib.compress(source_data, level=compress)
    xored = xor_stream(compressed, real_key)
    ct = aes_encrypt(xored, real_key)

    # Generate decoy keys (32 bytes each, look identical to real)
    decoys = [os.urandom(32) for _ in range(decoy_count)]

    # Randomly decide which position gets the real key
    real_pos = secrets.randbelow(decoy_count + 1)  # 0, 1, or 2
    keys_list = decoys[:]  # Start with all decoys
    keys_list.insert(real_pos, real_key)  # Insert real key at random position

    keys = {f"k{i+1}": keys_list[i].hex() for i in range(decoy_count + 1)}
    fp = key_fingerprint(real_key)

    pad = os.urandom(secrets.randbelow(pad_max + 1))
    payload = {
        "v": 5, "d": ct.hex(), "c": "", "p": pad.hex(),
        "h": sha256(source_data), "f": fp,
    }
    payload.update(keys)
    return json.dumps(payload, separators=(",", ":")).encode()


def generate_decoy_payload() -> bytes:
    """Generate a decoy .pye file with the SAME structure as real files.

    - Same fields: v, d, c, p, h, f, k1, k2, k3
    - Identical format and size range
    - 'Encrypted' data that decompresses to garbage
    - Real-looking keys and fingerprint
    """
    garbage = os.urandom(secrets.randbelow(500) + 100)
    fake_key = os.urandom(32)
    compressed = zlib.compress(garbage)
    xored = xor_stream(compressed, fake_key)
    ct = aes_encrypt(xored, fake_key)

    # Generate decoy keys just like real payloads
    decoy_keys = [os.urandom(32) for _ in range(3)]
    real_pos = secrets.randbelow(3)
    decoy_keys.insert(real_pos, fake_key)
    del decoy_keys[3]

    keys = {f"k{i+1}": decoy_keys[i].hex() for i in range(3)}
    fp = key_fingerprint(secrets.token_bytes(8))  # Random fingerprint

    pad = os.urandom(secrets.randbelow(512) + 1)
    payload = {
        "v": 5, "d": ct.hex(), "c": "", "p": pad.hex(),
        "h": sha256(garbage), "f": fp,
    }
    payload.update(keys)
    return json.dumps(payload, separators=(",", ":")).encode()
