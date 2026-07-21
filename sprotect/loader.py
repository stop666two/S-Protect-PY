"""Bootloader and runtime loader generator."""

from __future__ import annotations
import os, shutil

_RUNTIME_SRC = r'''"""S-Protect runtime - auto-generated. Zero external deps."""
import sys, os, json, hmac, hashlib, importlib.abc, importlib.machinery
_D = os.path.dirname(os.path.abspath(__file__))

def _xor(k, d):
    o = bytearray(len(d))
    for i in range(0, len(d), 32):
        s = hmac.new(k, (i // 32).to_bytes(8, "big"), "sha256").digest()
        for j in range(min(32, len(d) - i)): o[i+j] = d[i+j] ^ s[j]
    return bytes(o)

def _dec(p):
    k = bytes.fromhex(p["k"]); d = bytes.fromhex(p["d"])
    if p.get("a") == "aes":
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM
        return AESGCM(k).decrypt(d[:12], d[12:], b"").decode()
    s = p.get("h","")
    if s and not hmac.compare_digest(s, hmac.new(k, d, "sha256").hexdigest()):
        raise ValueError("Integrity check failed")
    return _xor(k, d).decode()

def _load(p):
    return _dec(json.loads(open(p, "rb").read().decode()))

class _L(importlib.abc.Loader):
    def __init__(self, n, p, pk=False): self.n, self.p, self.pk = n, p, pk
    def create_module(self, s): return None
    def exec_module(self, m):
        m.__dict__.setdefault("__file__", self.p)
        m.__dict__.setdefault("__package__", self.n)
        if self.pk: m.__dict__.setdefault("__path__", [os.path.dirname(self.p)])
        exec(compile(_load(self.p), self.p, "exec"), m.__dict__)

class _F(importlib.abc.MetaPathFinder):
    def find_spec(self, n, p=None, t=None):
        r = n.replace(".", os.sep)
        for e in [r + ".pye", os.path.join(r, "__init__.pye")]:
            f = os.path.join(_D, e)
            if os.path.isfile(f):
                is_pkg = e.endswith("__init__.pye")
                s = importlib.machinery.ModuleSpec(n, _L(n, f, is_pkg), origin=f)
                if is_pkg: s.submodule_search_locations = [os.path.join(_D, r)]
                return s
        return None

def run(entry: str, root: str = ""):
    sys.meta_path.insert(0, _F())
    e = os.path.join(_D, entry.replace(".", os.sep) + ".pye")
    if not os.path.isfile(e): raise FileNotFoundError(f"Entry not found: {e}")
    src = _load(e)
    exec(compile(src, e, "exec"), {"__name__": "__main__", "__file__": os.path.join(root or os.path.dirname(_D), entry + ".py")})
'''

_BOOT_SRC = '''"""S-Protect encrypted entry - auto-generated."""
import sys, os
_R = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _R)
from _runtime.loader import run
run("{entry}", _R)
'''


def gen_boot(output_dir: str, entry_module: str, per_file_configs: dict[str, str]) -> str:
    ep = os.path.join(output_dir, entry_module.replace(".", os.sep) + ".py")
    os.makedirs(os.path.dirname(ep), exist_ok=True)
    with open(ep, "w", encoding="utf-8") as f: f.write(_BOOT_SRC.format(entry=entry_module))
    for src, dst in per_file_configs.items():
        shutil.copy2(src, dst)
    return ep

def gen_loader(output_dir: str) -> str:
    rd = os.path.join(output_dir, "_runtime"); os.makedirs(rd, exist_ok=True)
    lp = os.path.join(rd, "loader.py")
    with open(lp, "w", encoding="utf-8") as f: f.write(_RUNTIME_SRC)
    return lp
