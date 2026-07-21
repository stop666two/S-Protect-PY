"""Bootloader + runtime loader v6: random-hex names, module map, multi-fingerprint."""

from __future__ import annotations
import os, shutil

_RUNTIME_SRC = r'''"""S-Protect runtime v6 - random hex names, module map, multi-fingerprint."""
import sys, os, json, hmac, hashlib, zlib, importlib.abc, importlib.machinery
try: _SD = os.path.dirname(os.path.abspath(__file__))
except: _SD = os.path.dirname(os.path.abspath(sys.argv[0])) if sys.argv else "."
_D = os.path.join(_SD, "_runtime") if os.path.isdir(os.path.join(_SD, "_runtime")) else _SD

# Encrypted module map (populated at build time)
_MAP_ENCRYPTED = ""

# ---- Decoy analysis function 1: looks like it verifies file integrity ----
def _decoy_verify_1():
    """Decoy verification function. Looks real but never actually runs."""
    import time
    for r, _, fs in os.walk(_D):
        for f in fs:
            if f.endswith(".pye") and not f.startswith("loader"):
                time.sleep(0.0001)
    return True

# ---- Decoy analysis function 2: looks like key sanity check ----
def _decoy_verify_2(p):
    """Decoy: appears to validate key structure. Does nothing useful."""
    cnt = sum(1 for k in ["k1","k2","k3","k4","k5"] if k in p)
    if cnt < 2: return False
    return True

# ---- Real key extraction with multi-fingerprint ----
def _xor_of(d, k):
    r, c = bytearray(), 0
    while len(r) < len(d):
        h = hashlib.sha256(k + c.to_bytes(4,"big")).digest()
        for i in range(min(len(h), len(d)-len(r))): r.append(d[len(r)] ^ h[i])
        c += 1
    return bytes(r)

def _extract_key(p):
    """Extract real key from multi-fingerprint payload.
    All 3 fingerprints are checked - analysis can't tell which is the match.
    Real files have exactly one matching fingerprint among f1/f2/f3."""
    keys = {}
    for kn in ["k1","k2","k3","k4","k5"]:
        if kn in p: keys[kn] = bytes.fromhex(p[kn])
    fps = {}
    for fn in ["f1","f2","f3","f4","f5"]:
        if fn in p: fps[fn] = p[fn]
    # Find which key's fingerprint matches any of f1/f2/f3
    for kn, kv in keys.items():
        kh = hashlib.sha256(kv).digest()[:4].hex()
        for fn, fv in fps.items():
            if kh == fv:
                return kv  # Found matching key
    # Fallback: try k1 (may be wrong for decoys)
    return keys.get("k1", b"")

# ---- Decoy decrypt function ----
def _decrypt_decoy(p, k):
    """Decoy decrypt function. Looks real, called in dead code paths."""
    ct = bytes.fromhex(p.get("d", ""))
    if not ct: return ""
    try:
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM
        x = AESGCM(k).decrypt(ct[:12], ct[12:], b"")
        return zlib.decompress(_xor_of(x, k)).decode()
    except: return ""

# ---- Real decrypt functions ----
def _decrypt_real(p, k):
    """Real decryption. Used for actual module loading."""
    ct = bytes.fromhex(p["d"])
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    x = AESGCM(k).decrypt(ct[:12], ct[12:], b"")
    return zlib.decompress(_xor_of(x, k)).decode()

def _load_module(p, mk):
    return _decrypt_real(p, mk)

# ---- Module map decryption ----
def _decrypt_map():
    """Decrypt the module map from _MAP_ENCRYPTED."""
    if not _MAP_ENCRYPTED: return {}
    p = json.loads(_MAP_ENCRYPTED)
    k = _extract_key(p)
    if not k: return {}
    return json.loads(_decrypt_real(p, k))

# ---- Shard collection ----
def _collect(mmap):
    """Collect shards from mapped files only.
    Files not in the module map (decoys) are skipped."""
    shards = {}
    for mod_name, hex_name in mmap.items():
        pye = os.path.join(_D, hex_name + ".pye")
        if not os.path.isfile(pye):
            # Also check subdirectories
            found = False
            for r, _, fs in os.walk(_D):
                for f in fs:
                    if f == hex_name + ".pye":
                        pye = os.path.join(r, f)
                        found = True
                        break
                if found: break
            if not found: continue
        try:
            p = json.loads(open(pye, "rb").read().decode())
            real = _extract_key(p)
            if real and len(real) == 32:
                shards[mod_name] = real
        except: pass
    if len(shards) < 2: raise RuntimeError("Insufficient shards")
    vals = list(shards.values())
    mk = bytearray(vals[0])
    for v in vals[1:]:
        for i in range(len(mk)): mk[i] ^= v[i]
    return bytes(mk), shards

def _verify_chain(mk, shards, mmap):
    for mod_name in sorted(shards.keys()):
        hex_n = mmap.get(mod_name, "")
        if not hex_n: continue
        pye = os.path.join(_D, hex_n + ".pye")
        try:
            p = json.loads(open(pye, "rb").read().decode())
            if not p.get("c"): continue
            # Find next file in chain
            names = sorted(shards.keys())
            idx = names.index(mod_name)
            next_n = names[(idx + 1) % len(names)]
            next_hex = mmap.get(next_n, "")
            if not next_hex: continue
            q = json.loads(open(os.path.join(_D, next_hex + ".pye"), "rb").read().decode())
            h = hashlib.sha256(q.get("d", "").encode()).digest()
            if not hmac.compare_digest(hmac.new(mk, h, "sha256").hexdigest(), p["c"]):
                raise ValueError(f"Chain broken: {mod_name}")
        except: pass

# ---- Module loader ----
class _L(importlib.abc.Loader):
    def __init__(self, n, p, mk, pk=False):
        self.n, self.p, self.mk, self.pk = n, p, mk, pk
    def create_module(self, s): return None
    def exec_module(self, m):
        m.__dict__.setdefault("__file__", self.p)
        m.__dict__.setdefault("__package__", self.n)
        if self.pk: m.__dict__.setdefault("__path__", [os.path.dirname(self.p)])
        p = json.loads(open(self.p, "rb").read().decode())
        src = _load_module(p, self.mk)
        if src is None: raise RuntimeError(f"Failed: {self.n}")
        exec(compile(src, self.p, "exec"), m.__dict__)

class _F(importlib.abc.MetaPathFinder):
    def __init__(self, mk, mmap): self.mk, self.mmap = mk, mmap
    def find_spec(self, n, p=None, t=None):
        hex_n = self.mmap.get(n, "")
        if not hex_n:
            # Try package lookup
            for mn, hn in self.mmap.items():
                if mn.startswith(n + "."):
                    hex_n = self.mmap.get(n, "")
                    if hex_n: break
            if not hex_n: return None
        pye = os.path.join(_D, hex_n + ".pye")
        if os.path.isfile(pye):
            is_pkg = any(mn.startswith(n + ".") for mn in self.mmap)
            spec = importlib.machinery.ModuleSpec(n, _L(n, pye, self.mk, is_pkg), origin=pye)
            if is_pkg: spec.submodule_search_locations = [os.path.dirname(pye)]
            return spec
        return None

def run(entry, root=""):
    mmap = _decrypt_map()
    mk, shards = _collect(mmap)
    _verify_chain(mk, shards, mmap)
    _decoy_verify_1()
    sys.meta_path.insert(0, _F(mk, mmap))
    entry_hex = mmap.get(entry, "")
    if not entry_hex:
        raise FileNotFoundError(f"Entry not found in map: {entry}")
    e = os.path.join(_D, entry_hex + ".pye")
    if not os.path.isfile(e): raise FileNotFoundError(f"Entry not found: {e}")
    p = json.loads(open(e, "rb").read().decode())
    src = _decrypt_real(p, mk)
    fm = os.path.join(root or os.path.dirname(_D), entry + ".py")
    exec(compile(src, e, "exec"), {"__name__":"__main__","__file__":fm})
'''


_BOOT_STUB = '''"""S-Protect bootloader v6 - module map lookup + fingerprint matching."""
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
    for kn in ["k1","k2","k3"]:
        if kn in p: _ = bytes.fromhex(p[kn])
    fp_map = dict()
    for fn in ["f1","f2","f3"]:
        if fn in p: fp_map[fn] = p[fn]
    real = key
    for kn in ["k1","k2","k3"]:
        if kn in p:
            v = bytes.fromhex(p[kn])
            kh = hashlib.sha256(v).digest()[:4].hex()
            for fv in fp_map.values():
                if kh == fv:
                    real = v; break
        if real != key: break
    ct = bytes.fromhex(p["d"])
    x = AESGCM(real).decrypt(ct[:12], ct[12:], b"")
    return zlib.decompress(bytes(a^b for a,b in zip(x,_xof(len(x),real)))).decode()

exec(compile(_boot(bytes.fromhex("{lk}")), "", "exec"))
run("{entry}", _R)
'''


def gen_loader_source() -> str:
    return _RUNTIME_SRC


def gen_boot(output_dir: str, entry_module: str, entry_hex: str,
             per_file_configs: dict[str, str], loader_key: bytes) -> str:
    ep = os.path.join(output_dir, entry_module.replace(".", os.sep) + ".py")
    os.makedirs(os.path.dirname(ep), exist_ok=True)
    boot = _BOOT_STUB.format(lk=loader_key.hex(), rd="_runtime", entry=entry_module)
    with open(ep, "w", encoding="utf-8") as f: f.write(boot)
    for src, dst in per_file_configs.items():
        shutil.copy2(src, dst)
    return ep
