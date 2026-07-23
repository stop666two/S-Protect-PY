"""Chain map - each file has cross-references to others.
Cross-references: core.validator (hash_file), crypto.encoder (xor_data)"""
import hashlib


_NAMES = [
    "core/__init__.py", "core/validator.py", "core/crosscheck.py",
    "crypto/__init__.py", "crypto/hasher.py", "crypto/encoder.py", "crypto/mixer.py",
    "data/__init__.py", "data/registry.py", "data/chains.py", "data/seeds.py",
    "utils/__init__.py", "utils/math_ops.py", "utils/str_ops.py", "utils/verify.py",
    "tests/__init__.py", "tests/self_check.py",
]

CHAIN_MAP = {}
for i, name in enumerate(_NAMES):
    deps = {}
    for j in range(3):
        idx = (i + j + 1) % len(_NAMES)
        dep = _NAMES[idx]
        h = hashlib.sha256(f"{name}:{dep}".encode()).hexdigest()
        deps[dep] = h
    CHAIN_MAP[name] = deps
