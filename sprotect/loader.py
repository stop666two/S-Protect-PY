"""Bootloader + runtime loader (random key position, decoy files, fingerprint matching)."""

from __future__ import annotations
import os, shutil

_RUNTIME_SRC = r'''"""S-Protect runtime v5 - random-key-position, fingerprint matching."""
import sys, os, json, hmac, hashlib, zlib, importlib.abc, importlib.machinery
try: _SD = os.path.dirname(os.path.abspath(__file__))
except: _SD = os.path.dirname(os.path.abspath(sys.argv[0])) if sys.argv else "."
_D = os.path.join(_SD, "_runtime") if os.path.isdir(os.path.join(_SD, "_runtime")) else _SD

def _xof(l, s):
    r, c = bytearray(), 0
    while len(r) < l:
        r.extend(hashlib.sha256(s + c.to_bytes(4,"big")).digest()); c += 1
    return bytes(r[:l])

def _xor(d, k):
    return bytes(a^b for a,b in zip(d, _xof(len(d),k)))

def _find_real(p):
    """Identify the real key by fingerprint matching.
    ALL keys are accessed - code analysis can't tell which one matches."""
    fp = p.get("f", "")
    if not fp: return bytes.fromhex(p.get("k1",""))  # Fallback
    for k in ["k1","k2","k3","k4","k5"]:
        if k in p:
            v = bytes.fromhex(p[k])
            if hashlib.sha256(v).digest()[:4].hex() == fp:
                return v
    return bytes.fromhex(p.get("k1",""))

def _decrypt_verify(p, key):
    """Decrypt and verify."""
    ct = bytes.fromhex(p["d"])
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    x = AESGCM(key).decrypt(ct[:12], ct[12:], b"")
    return zlib.decompress(_xor(x, key)).decode()

def _load(p, mk):
    return _decrypt_verify(p, mk)

def _collect():
    """Collect shards from all .pye files (skipping decoys).
    Real files have chain signatures; decoys have empty 'c' field."""
    shards = {}
    for r, _, fs in os.walk(_D):
        for f in fs:
            if not f.endswith(".pye") or f == "loader.pye": continue
            fp = os.path.join(r, f)
            try:
                p = json.loads(open(fp, "rb").read().decode())
                if not p.get("c"): continue  # Decoy files have empty chain
                real = _find_real(p)
                if real and len(real) == 32:
                    rel = os.path.relpath(fp, _D)
                    shards[rel] = real
            except: pass
    if len(shards) < 2: raise RuntimeError("Insufficient shards")
    vals = list(shards.values())
    mk = bytearray(vals[0])
    for v in vals[1:]:
        for i in range(len(mk)): mk[i] ^= v[i]
    return bytes(mk), shards

def _verify_chain(mk, shards):
    fs = sorted(shards.keys()); n = len(fs)
    for i in range(n):
        try:
            p = json.loads(open(os.path.join(_D, fs[i]), "rb").read().decode())
            if not p.get("c"): continue
            q = json.loads(open(os.path.join(_D, fs[(i+1)%n]), "rb").read().decode())
            h = hashlib.sha256(q.get("d", "").encode()).digest()
            if not hmac.compare_digest(hmac.new(mk, h, "sha256").hexdigest(), p["c"]):
                raise ValueError(f"Chain broken: {fs[i]}")
        except: pass

class _L(importlib.abc.Loader):
    def __init__(self, n, p, mk, pk=False):
        self.n, self.p, self.mk, self.pk = n, p, mk, pk
    def create_module(self, s): return None
    def exec_module(self, m):
        m.__dict__.setdefault("__file__", self.p)
        m.__dict__.setdefault("__package__", self.n)
        if self.pk: m.__dict__.setdefault("__path__", [os.path.dirname(self.p)])
        p = json.loads(open(self.p, "rb").read().decode())
        src = _load(p, self.mk)
        if src is None: raise RuntimeError(f"Failed to decrypt: {self.n}")
        exec(compile(src, self.p, "exec"), m.__dict__)

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
    mk, shards = _collect()
    _verify_chain(mk, shards)
    sys.meta_path.insert(0, _F(mk))
    e = os.path.join(_D, entry.replace(".", os.sep) + ".pye")
    if not os.path.isfile(e): raise FileNotFoundError(f"Entry not found: {e}")
    p = json.loads(open(e, "rb").read().decode())
    src = _decrypt_verify(p, mk)
    fm = os.path.join(root or os.path.dirname(_D), entry + ".py")
    exec(compile(src, e, "exec"), {"__name__":"__main__","__file__":fm})
'''


_BOOT_STUB = '''"""S-Protect bootloader v5 - fingerprint key matching."""
import sys, os, json, hashlib, zlib
_R = os.path.dirname(os.path.abspath(__file__))

def _xof(l, s):
    r, c = bytearray(), 0
    while len(r) < l:
        r.extend(hashlib.sha256(s + c.to_bytes(4,"big")).digest()); c += 1
    return bytes(r[:l])

def _boot(key):
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    p = json.loads(open(os.path.join(_R,"{rd}","loader.pye"),"rb").read().decode())
    # Access ALL keys - can't tell which is real
    for kn in ["k1","k2","k3","k4","k5"]:
        if kn in p: _ = bytes.fromhex(p[kn])
    # Find real key by fingerprint
    fp = p.get("f", "")
    real = key
    if fp:
        for kn in ["k1","k2","k3"]:
            if kn in p:
                v = bytes.fromhex(p[kn])
                if hashlib.sha256(v).digest()[:4].hex() == fp:
                    real = v
                    break
    ct = bytes.fromhex(p["d"])
    x = AESGCM(real).decrypt(ct[:12], ct[12:], b"")
    return zlib.decompress(bytes(a^b for a,b in zip(x,_xof(len(x),real)))).decode()

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
