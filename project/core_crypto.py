"""Crypto/encoding module - XOR, base64, hash chains."""
from core_math import xor_bytes, sha256_digest, base64_encode, base64_decode


def xor_chain(data, keys):
    result = data.encode() if isinstance(data, str) else data
    for k in keys:
        result = xor_bytes(result, k.encode() if isinstance(k, str) else k)
    return result.hex()


def hash_chain(data, rounds=3):
    h = data.encode() if isinstance(data, str) else data
    for _ in range(rounds):
        h = sha256_digest(h).encode()
    return h.decode()


def double_encode(data):
    return base64_encode(base64_encode(data))


def double_decode(data):
    return base64_decode(base64_decode(data))


def xor_encrypt(data, key):
    d = data.encode() if isinstance(data, str) else data
    k = key.encode() if isinstance(key, str) else key
    k = k * (len(d) // len(k) + 1)
    return xor_bytes(d, k[:len(d)]).hex()
