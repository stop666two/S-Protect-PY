"""Cryptographic engine: multi-fingerprint, mixed real/decoy keys, random naming."""

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

def fp(key: bytes) -> str:
    """4-byte fingerprint of a key."""
    return hashlib.sha256(key).digest()[:4].hex()

def make_keys(real_key: bytes, decoy_count: int = 2) -> tuple[dict, str]:
    """Generate k1-k3 with real key at random position.
    Returns (keys_dict, real_key_name).
    Also generates 3 fingerprints - only one matches the real key."""
    decoys = [os.urandom(32) for _ in range(decoy_count)]
    pos = secrets.randbelow(decoy_count + 1)
    keys_list = decoys[:]
    keys_list.insert(pos, real_key)
    keys = {f"k{i+1}": keys_list[i].hex() for i in range(decoy_count + 1)}
    real_name = f"k{pos + 1}"

    # Generate 3 fingerprints: f1=real, f2=decoy, f3=decoy
    # f1 matches the real key; f2 and f3 are random
    fps = {
        "f1": fp(real_key),
        "f2": fp(os.urandom(32)),
        "f3": fp(os.urandom(32)),
    }
    # Randomly swap fingerprints so the real one isn't always f1
    swap = secrets.randbelow(3)
    fp_order = [f"f1", "f2", "f3"]
    fp_vals = [fp(real_key), fp(os.urandom(32)), fp(os.urandom(32))]
    fp_vals[0], fp_vals[swap] = fp_vals[swap], fp_vals[0]
    fps = {f"f{i+1}": fp_vals[i] for i in range(3)}

    return {**keys, **fps}, real_name


def encrypt_payload(source_data: bytes, real_key: bytes,
                    compress: int = 9, pad_max: int = 512,
                    decoy_count: int = 2) -> bytes:
    """Encrypt with random-key-position and multi-fingerprint."""
    compressed = zlib.compress(source_data, level=compress)
    xored = xor_stream(compressed, real_key)
    ct = aes_encrypt(xored, real_key)

    keys, _ = make_keys(real_key, decoy_count)
    pad = os.urandom(secrets.randbelow(pad_max + 1))
    payload = {"v": 6, "d": ct.hex(), "c": "", "p": pad.hex(), "h": sha256(source_data)}
    payload.update(keys)
    return json.dumps(payload, separators=(",", ":")).encode()


def generate_decoy_payload() -> bytes:
    """Generate a decoy .pye file - identical structure to real files.

    Decoy files MAY contain:
    - Valid-looking keys that could decrypt to something
    - Multiple fingerprints (some matching, some not)
    - The same field structure as real files
    """
    garbage = os.urandom(secrets.randbelow(500) + 100)
    fake_key = os.urandom(32)
    compressed = zlib.compress(garbage)
    xored = xor_stream(compressed, fake_key)
    ct = aes_encrypt(xored, fake_key)

    keys, _ = make_keys(fake_key, 2)
    # Randomize: sometimes give decoy files matching fingerprints
    # to make analysis harder (looks like it could be real)
    pad = os.urandom(secrets.randbelow(512) + 1)
    payload = {"v": 6, "d": ct.hex(), "c": "", "p": pad.hex(), "h": sha256(garbage)}
    payload.update(keys)
    return json.dumps(payload, separators=(",", ":")).encode()
