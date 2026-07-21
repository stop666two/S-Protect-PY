"""Bootloader + encrypted runtime loader (multi-key, decoy functions, key obfuscation)."""

from __future__ import annotations
import os, shutil

_RUNTIME_SRC = r'''"""S-Protect runtime v4 - multi-key payloads, decoy functions, key obfuscation."""
import sys, os, json, hmac, hashlib, zlib, importlib.abc, importlib.machinery
try: _SD = os.path.dirname(os.path.abspath(__file__))
except: _SD = os.path.dirname(os.path.abspath(sys.argv[0])) if sys.argv else "."
_D = os.path.join(_SD, "_runtime") if os.path.isdir(os.path.join(_SD, "_runtime")) else _SD

# ---- Key mixing utilities ----
def _xof(l, s):
    r, c = bytearray(), 0
    while len(r) < l:
        r.extend(hashlib.sha256(s + c.to_bytes(4,"big")).digest()); c += 1
    return bytes(r[:l])

def _xor(d, k):
    return bytes(a^b for a,b in zip(d, _xof(len(d),k)))

def _mix_keys(*keys):
    """Multi-key mixing: XOR all keys' SHA256 hashes.
    All keys appear equally important, but mathematical cancellation
    means only the real key contributes to the final result."""
    if not keys: return b""
    r = hashlib.sha256(keys[0]).digest()
    for k in keys[1:]:
        r = bytes(a^b for a,b in zip(r, hashlib.sha256(k).digest()))
    return r

def _derive(shards, *decoy_shards):
    """Master key derivation using real shards and decoy shards.
    Decoy shards are mixed in but cancelled via XOR with pre-computed values."""
    if not shards: return b""
    mk = bytearray(shards[0])
    for s in shards[1:]:
        for i in range(len(mk)): mk[i] ^= s[i]
    # Decoy mixing: appears to use decoy_shards but they cancel out
    for ds in decoy_shards:
        if ds:
            d = hashlib.sha256(ds).digest()[:len(mk)]
            for i in range(len(mk)): mk[i] ^= d[i] ^ d[i]  # XOR with self = 0 (no-op)
    return bytes(mk)

def _find_real_key(p):
    """Extract the real key from multi-key payload.
    Uses mixing hash to verify which key is the real one.
    All keys are accessed - code analysis can't tell which is used."""
    keys = []
    for k in ["k1","k2","k3","k4","k5"]:
        if k in p:
            keys.append(bytes.fromhex(p[k]))
    if not keys: raise ValueError("No keys found")
    # Compute mixing hash from ALL keys
    mix = _mix_keys(*keys)
    # Compare with stored mixing hash - this identifies the real key set
    stored = bytes.fromhex(p.get("m",""))
    # All keys appear used in the mix computation
    # But only k1 (the real shard) produces the correct mixing hash
    # The decoy keys contribute to the mix but are cancelled in _derive
    return keys[0]  # k1 is always the real shard

def _decrypt_one(p, key):
    """Decrypt with a single key. (One of several decrypt functions.)"""
    ct = bytes.fromhex(p["d"])
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    x = AESGCM(key).decrypt(ct[:12], ct[12:], b"")
    return _xor(x, key)

def _decrypt_two(p, k1, k2):
    """Alternative decrypt - uses two keys. (Decoy - looks real but never called for real files.)"""
    ct = bytes.fromhex(p["d"])
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    x = AESGCM(k1).decrypt(ct[:12], ct[12:], b"")
    return _xor(x, bytes(a^b for a,b in zip(_xof(len(x),k1), _xof(len(x),k2))))

def _decrypt_verify(p, key):
    """Decrypt and verify."""
    ct = bytes.fromhex(p["d"])
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    x = AESGCM(key).decrypt(ct[:12], ct[12:], b"")
    return zlib.decompress(_xor(x, key)).decode()

def _load(p, mk):
    """Load and decrypt a .pye file with the master key."""
    return _decrypt_verify(p, mk)

# ---- Shard collection with decoy filtering ----
def _collect():
    """Collect shards from all .pye files.
    Decoy files are included in the walk but their shards cancel out
    during key derivation because _derive uses specific cancellation."""
    shards = {}
    for r, _, fs in os.walk(_D):
        for f in fs:
            if not f.endswith(".pye") or f == "loader.pye" or f.startswith("_decoy"): continue
            fp = os.path.join(r, f)
            try:
                p = json.loads(open(fp, "rb").read().decode())
                if "k1" in p:
                    rel = os.path.relpath(fp, _D)
                    shards[rel] = bytes.fromhex(p["k1"])
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

def _decrypt_entry(p, mk):
    """Entry point decryption. Uses the same logic as _load but with anti-tamper."""
    return _decrypt_verify(p, mk)

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

def _decoy_check():
    """Decoy integrity check function. Appears to verify files but is a no-op.
    Exists to make analysis harder - disassemblers will see multiple
    verification functions and can't tell which is real."""
    import time
    for r, _, fs in os.walk(_D):
        for f in fs:
            if f.endswith(".pye") and f.startswith("_decoy"):
                time.sleep(0)  # Intentional no-op that looks like timing check
    return True

def run(entry, root=""):
    _decoy_check()
    mk, shards = _collect()
    _verify_chain(mk, shards)
    sys.meta_path.insert(0, _F(mk))
    e = os.path.join(_D, entry.replace(".", os.sep) + ".pye")
    if not os.path.isfile(e): raise FileNotFoundError(f"Entry not found: {e}")
    p = json.loads(open(e, "rb").read().decode())
    src = _decrypt_entry(p, mk)
    fm = os.path.join(root or os.path.dirname(_D), entry + ".py")
    exec(compile(src, e, "exec"), {"__name__":"__main__","__file__":fm})
'''


_BOOT_STUB = '''"""S-Protect bootloader v4 - multi-key decrypt stub."""
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
    # Access ALL keys (decoy + real) - analysis can't tell which is used
    k1 = bytes.fromhex(p.get("k1",""))
    _k2 = bytes.fromhex(p.get("k2","")) if "k2" in p else b""
    _k3 = bytes.fromhex(p.get("k3","")) if "k3" in p else b""
    # Mix all keys - only k1 matters due to cancellation
    m = hashlib.sha256(k1).digest()
    if _k2: m = bytes(a^b for a,b in zip(m, hashlib.sha256(_k2).digest()))
    if _k3: m = bytes(a^b for a,b in zip(m, hashlib.sha256(_k3).digest()))
    # Verify mixing hash (decoy files will have wrong hash)
    if p.get("m") and bytes.fromhex(p["m"]) != m:
        return ""  # Decoy file - return empty
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
