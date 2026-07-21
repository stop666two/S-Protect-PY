"""Bootloader + encrypted runtime loader (two-layer key system)."""

from __future__ import annotations
import os, shutil

_RUNTIME_SRC = r'''"""S-Protect runtime v3 - sharded master key + chain integrity."""
import sys, os, json, hmac, hashlib, zlib, importlib.abc, importlib.machinery
try: _SD = os.path.dirname(os.path.abspath(__file__))
except: _SD = os.path.dirname(os.path.abspath(sys.argv[0])) if sys.argv else "."
_D = os.path.join(_SD, "_runtime") if os.path.isdir(os.path.join(_SD, "_runtime")) else _SD

def _xor(d, k):
    r, c = bytearray(), 0
    while len(r) < len(d):
        h = hashlib.sha256(k + c.to_bytes(4, "big")).digest()
        for i in range(min(len(h), len(d)-len(r))): r.append(d[len(r)] ^ h[i])
        c += 1
    return bytes(r)

def _dec(p, k):
    if p.get("v") != 3: raise ValueError("Bad version")
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    ct = bytes.fromhex(p["d"])
    x = AESGCM(k).decrypt(ct[:12], ct[12:], b"")
    return zlib.decompress(_xor(x, k)).decode()

def _reconstruct_master():
    """Collect shards from ALL .pye files to reconstruct master key."""
    shards = {}
    for r, _, fs in os.walk(_D):
        for f in fs:
            if not f.endswith(".pye") or f == "loader.pye": continue
            p = json.loads(open(os.path.join(r, f), "rb").read().decode())
            if "s" in p and len(p["s"]) == 64:
                shards[os.path.relpath(os.path.join(r, f), _D)] = bytes.fromhex(p["s"])
    if len(shards) < 2: raise RuntimeError("Insufficient shards")
    vals = list(shards.values())
    mk = bytearray(vals[0])
    for v in vals[1:]:
        for i in range(len(mk)): mk[i] ^= v[i]
    return bytes(mk), shards

def _verify_chain(mk, shards):
    fs = sorted(shards.keys()); n = len(fs)
    for i in range(n):
        p = json.loads(open(os.path.join(_D, fs[i]), "rb").read().decode())
        if not p.get("c"): continue
        q = json.loads(open(os.path.join(_D, fs[(i+1)%n]), "rb").read().decode())
        h = hashlib.sha256(q.get("d", "").encode()).digest()
        if not hmac.compare_digest(hmac.new(mk, h, "sha256").hexdigest(), p["c"]):
            raise ValueError(f"Chain broken: {fs[i]}")

class _L(importlib.abc.Loader):
    def __init__(self, n, p, mk, pk=False):
        self.n, self.p, self.mk, self.pk = n, p, mk, pk
    def create_module(self, s): return None
    def exec_module(self, m):
        m.__dict__.setdefault("__file__", self.p)
        m.__dict__.setdefault("__package__", self.n)
        if self.pk: m.__dict__.setdefault("__path__", [os.path.dirname(self.p)])
        p = json.loads(open(self.p, "rb").read().decode())
        exec(compile(_dec(p, self.mk), self.p, "exec"), m.__dict__)

class _F(importlib.abc.MetaPathFinder):
    def __init__(self, mk): self.mk = mk
    def find_spec(self, n, p=None, t=None):
        r = n.replace(".", os.sep)
        for e in [r+".pye", os.path.join(r,"__init__.pye")]:
            f = os.path.join(_D, e)
            if os.path.isfile(f):
                pk = e.endswith("__init__.pye")
                s = importlib.machinery.ModuleSpec(n, _L(n,f,self.mk,pk), origin=f)
                if pk: s.submodule_search_locations = [os.path.join(_D, r)]
                return s
        return None

def run(entry, root=""):
    mk, shards = _reconstruct_master()
    _verify_chain(mk, shards)
    sys.meta_path.insert(0, _F(mk))
    e = os.path.join(_D, entry.replace(".", os.sep) + ".pye")
    if not os.path.isfile(e): raise FileNotFoundError(f"Entry not found: {e}")
    p = json.loads(open(e, "rb").read().decode())
    src = _dec(p, mk)
    fm = os.path.join(root or os.path.dirname(_D), entry + ".py")
    exec(compile(src, e, "exec"), {"__name__":"__main__","__file__":fm})
'''


_BOOT_STUB = '''"""S-Protect bootloader - loader key only (master key sharded)."""
import sys, os, json, hashlib, zlib
_R = os.path.dirname(os.path.abspath(__file__))

def _xof(l, s):
    r, c = bytearray(), 0
    while len(r) < l:
        r.extend(hashlib.sha256(s + c.to_bytes(4, "big")).digest()); c += 1
    return bytes(r[:l])

def _boot(key):
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    p = json.loads(open(os.path.join(_R,"{rd}","loader.pye"),"rb").read().decode())
    ct = bytes.fromhex(p["d"])
    x = AESGCM(key).decrypt(ct[:12], ct[12:], b"")
    return zlib.decompress(bytes(a^b for a,b in zip(x,_xof(len(x),key)))).decode()

exec(compile(_boot(bytes.fromhex("{lk}")), "", "exec"))
run("{entry}", _R)
'''


def gen_loader_source() -> str:
    return _RUNTIME_SRC


def gen_boot(output_dir: str, entry_module: str, per_file_configs: dict[str, str],
             loader_key: bytes) -> str:
    ep = os.path.join(output_dir, entry_module.replace(".", os.sep) + ".py")
    os.makedirs(os.path.dirname(ep), exist_ok=True)
    boot = _BOOT_STUB.format(lk=loader_key.hex(), rd="_runtime", entry=entry_module)
    with open(ep, "w", encoding="utf-8") as f: f.write(boot)
    for src, dst in per_file_configs.items():
        shutil.copy2(src, dst)
    return ep
