"""Bootloader generator for self-contained encrypted projects.

Generates the entry point file and runtime modules that are bundled
into the output/ directory so encrypted projects can run independently
with zero external dependencies.
"""

from __future__ import annotations

import os


_RUNTIME_LOADER_SRC = r'''"""S-Protect runtime loader - auto-generated. Zero external deps."""
import sys, os, json, hmac, hashlib, importlib.abc, importlib.machinery

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
    def __init__(self, fullname, path, is_pkg=False):
        self.fullname, self.path, self.is_pkg = fullname, path, is_pkg
    def create_module(self, spec):
        return None
    def exec_module(self, module):
        module.__dict__.setdefault("__file__", self.path)
        module.__dict__.setdefault("__package__", self.fullname)
        if self.is_pkg:
            module.__dict__.setdefault("__path__", [os.path.dirname(self.path)])
        with open(self.path, "rb") as f:
            src = _decrypt_payload(json.loads(f.read().decode("utf-8")))
        exec(compile(src, self.path, "exec"), module.__dict__)

class _EncryptedFinder(importlib.abc.MetaPathFinder):
    def __init__(self):
        self.runtime_dir = _RUNTIME_DIR
    def find_spec(self, fullname, path=None, target=None):
        rel = fullname.replace(".", os.sep)
        pye = os.path.join(self.runtime_dir, rel + ".pye")
        if os.path.isfile(pye):
            return importlib.machinery.ModuleSpec(
                fullname, _EncryptedLoader(fullname, pye), origin=pye)
        init_pye = os.path.join(self.runtime_dir, rel, "__init__.pye")
        if os.path.isfile(init_pye):
            spec = importlib.machinery.ModuleSpec(
                fullname, _EncryptedLoader(fullname, init_pye, is_pkg=True),
                origin=init_pye, is_package=True)
            spec.submodule_search_locations = [os.path.join(self.runtime_dir, rel)]
            return spec
        return None

def run_entry(entry_module: str, project_dir: str = "") -> None:
    sys.meta_path.insert(0, _EncryptedFinder())
    rel = entry_module.replace(".", os.sep) + ".pye"
    entry_pye = os.path.join(_RUNTIME_DIR, rel)
    if not os.path.isfile(entry_pye):
        raise FileNotFoundError(f"Entry not found: {entry_pye}")
    with open(entry_pye, "rb") as f:
        src = _decrypt_payload(json.loads(f.read().decode("utf-8")))
    fake_main = os.path.join(project_dir or os.path.dirname(_RUNTIME_DIR), entry_module + ".py")
    exec(compile(src, entry_pye, "exec"), {"__name__": "__main__", "__file__": fake_main})
'''


_BOOTLOADER_ENTRY_SRC = '''"""S-Protect encrypted entry point - auto-generated."""
import sys, os
_project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _project_root)
from _runtime.loader import run_entry
run_entry("{entry}", _project_root)
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
