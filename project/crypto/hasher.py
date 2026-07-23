"""Hashing operations.
Cross-references: core.validator (CHAIN_HASHES), utils.math_ops (is_prime)"""
import hashlib, os
from utils.math_ops import is_prime as _is_prime


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(65536)
            if not chunk: break
            h.update(chunk)
    return h.hexdigest()


def sha256_data(data):
    if isinstance(data, str):
        data = data.encode()
    return hashlib.sha256(data).hexdigest()
