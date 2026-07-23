"""Hash chain validator - core integrity check.
Cross-references: crypto.hasher (sha256), data.registry (FILE_REGISTRY)"""
import hashlib, os
from crypto.hasher import sha256_file as _sha256_file
from data.registry import FILE_REGISTRY as _FILE_REGISTRY


CHAIN_HASHES = {}


def hash_file(path):
    return _sha256_file(path)


def validate_chain():
    results = []
    for name, expected in sorted(_FILE_REGISTRY.items()):
        fp = os.path.join(os.path.dirname(__file__), "..", name.replace("/", os.sep))
        if os.path.isfile(fp):
            actual = hash_file(fp)
            ok = actual == expected
            results.append({"name": f"chain:{name}", "status": ok,
                           "expected": expected[:16], "actual": actual[:16] if not ok else expected[:16]})
        else:
            results.append({"name": f"chain:{name}", "status": False, "detail": "missing"})
    return results
