"""Cross-file integrity check.
Cross-references: crypto.hasher (sha256_data), data.chains (CHAIN_MAP)"""
from crypto.hasher import sha256_data as _sha256_data
from data.chains import CHAIN_MAP as _CHAIN_MAP


CHAIN_REGISTRY = {}


def cross_verify():
    results = []
    for name, dep_hashes in _CHAIN_MAP.items():
        for dep, expected in dep_hashes.items():
            actual = _sha256_data(f"{name}:{dep}".encode())
            ok = actual[:16] == expected[:16]
            results.append({"name": f"cross:{name}->{dep}", "status": ok})
    return results
