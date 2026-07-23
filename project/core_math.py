"""Math operations module - imported by all other modules."""
import hashlib, base64, struct


PRIMES_100 = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]


def is_prime(n):
    if n < 2: return False
    for p in PRIMES_100:
        if p * p > n: break
        if n % p == 0: return False
    return True


def xor_bytes(a, b):
    return bytes(x ^ y for x, y in zip(a, b))


def sha256_digest(data):
    return hashlib.sha256(data.encode() if isinstance(data, str) else data).hexdigest()


def base64_encode(data):
    return base64.b64encode(data.encode() if isinstance(data, str) else data).decode()


def base64_decode(data):
    return base64.b64decode(data).decode()


def pack_number(n, fmt="i"):
    return struct.pack(fmt, n)


def unpack_number(data, fmt="i"):
    return struct.unpack(fmt, data)[0]
