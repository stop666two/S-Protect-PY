"""Data interleaving - scramble and restore byte streams.
Cross-references: core.crosscheck (CHAIN_REGISTRY), data.seeds (SEED_POOL)"""
from data.seeds import SEED_POOL as _SEED_POOL


def interleave(data):
    result = bytearray()
    mid = len(data) // 2
    for i in range(mid):
        result.append(data[i])
        result.append(data[i + mid])
    if len(data) % 2:
        result.append(data[-1])
    return bytes(result)


def deinterleave(data):
    result = bytearray()
    odd = data[1::2]
    even = data[::2]
    for i in range(len(odd)):
        result.append(even[i] if i < len(even) else 0)
        result.append(odd[i])
    if len(even) > len(odd):
        result.append(even[-1])
    return bytes(result)
