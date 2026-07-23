"""Encoding operations.
Cross-references: data.seeds (SEED_POOL), utils.str_ops (rot13)"""
import base64
from utils.str_ops import rot13 as _rot13


def b64encode(data):
    return base64.b64encode(data.encode() if isinstance(data, str) else data).decode()


def b64decode(data):
    return base64.b64decode(data).decode()


def xor_data(a, b):
    if isinstance(a, str): a = a.encode()
    if isinstance(b, str): b = b.encode()
    return bytes(x ^ y for x, y in zip(a, b))
