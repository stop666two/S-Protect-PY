"""Bootloader generator for self-contained encrypted projects.

Generates the entry point file and runtime modules that are bundled
into the output/ directory so encrypted projects can run independently
with zero external dependencies.
"""

from __future__ import annotations

import os


_RUNTIME_LOADER_SRC = r'''"""S-Protect runtime loader - auto-generated. Zero external deps."""
import sys, os, json, hmac, hashlib, importlib.abc, importlib.machinery
from types import ModuleType
from typing import Any

_RUNTIME_DIR = os.path.dirname(os.path.abspath(__file__))

def _xor_stream(key: bytes, data: bytes) -> bytes:
    out = bytearray(len(data))
    for i in range(0, len(data), 32):
        ctr = (i // 32).to_bytes(8, "big")
        stream = hmac.new(key, ctr, "sha256").digest()
        chunk = data[i:i+32]
        for j in range(len(chunk)):
            out[i+j] = chunk[j] ^ stream[j]
    return bytes(out)

def _decrypt_payload(payload: dict) -> str:
    key = bytes.fromhex(payload["key"])
    ct = bytes.fromhex(payload["data"])
    sig = payload.get("hmac", "")
    expected = hmac.new(key, ct, "sha256").hexdigest()
    if sig and not hmac.compare_digest(sig, expected):
        raise ValueError("Integrity check failed")
    plain = _xor_stream(key, ct)
    return plain.decode("utf-8")

class _EncryptedLoader(importlib.abc.Loader):
    def __init__(self, fullname: str, path: str):
        self.fullname, self.path = fullname, path
    def create_module(self, spec): return None
    def exec_module(self, module):
        with open(self.path, "rb") as f:
            src = _decrypt_payload(json.loads(f.read().decode("utf-8")))
        exec(compile(src, self.path, "exec"), module.__dict__)

class _EncryptedFinder(importlib.abc.MetaPathFinder):
    def __init__(self):
        self.runtime_dir = _RUNTIME_DIR
    def find_spec(self, fullname, path=None, target=None):
        pye = os.path.join(self.runtime_dir, fullname + ".pye")
        if os.path.isfile(pye):
            return importlib.machinery.ModuleSpec(
                fullname, _EncryptedLoader(fullname, pye), origin=pye)
        return None

def run_entry(entry_module: str) -> None:
    sys.meta_path.insert(0, _EncryptedFinder())
    entry_pye = os.path.join(_RUNTIME_DIR, entry_module + ".pye")
    if not os.path.isfile(entry_pye):
        raise FileNotFoundError(f"Entry not found: {entry_pye}")
    with open(entry_pye, "rb") as f:
        src = _decrypt_payload(json.loads(f.read().decode("utf-8")))
    exec(compile(src, entry_pye, "exec"), {"__name__": "__main__", "__file__": entry_pye})
'''


_BOOTLOADER_ENTRY_SRC = '''"""S-Protect encrypted entry point - auto-generated."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _runtime.loader import run_entry
run_entry("{entry}")
'''


def generate_bootloader(output_dir: str, entry_module: str) -> str:
    """Generate the bootloader entry file in output/.

    Args:
        output_dir: Path to output/ directory.
        entry_module: Entry module name without .py (e.g. "main").

    Returns:
        Path to the generated bootloader file.
    """
    entry_path = os.path.join(output_dir, entry_module.replace(".", os.sep) + ".py")
    os.makedirs(os.path.dirname(entry_path), exist_ok=True)
    with open(entry_path, "w", encoding="utf-8") as f:
        f.write(_BOOTLOADER_ENTRY_SRC.format(entry=entry_module))
    return entry_path


def generate_runtime_loader(output_dir: str) -> str:
    """Generate the runtime loader module in output/_runtime/loader.py.

    Args:
        output_dir: Path to output/ directory.

    Returns:
        Path to the generated loader file.
    """
    runtime_dir = os.path.join(output_dir, "_runtime")
    os.makedirs(runtime_dir, exist_ok=True)
    loader_path = os.path.join(runtime_dir, "loader.py")
    with open(loader_path, "w", encoding="utf-8") as f:
        f.write(_RUNTIME_LOADER_SRC)
    return loader_path


def generate_requirements(output_dir: str, extra_deps: list[str] | None = None) -> str:
    """Generate requirements.txt in output/.

    Args:
        output_dir: Path to output/ directory.
        extra_deps: Extra pip dependencies.

    Returns:
        Path to the generated requirements.txt.
    """
    req_path = os.path.join(output_dir, "requirements.txt")
    with open(req_path, "w", encoding="utf-8") as f:
        for dep in (extra_deps or []):
            f.write(dep + "\n")
    return req_path
