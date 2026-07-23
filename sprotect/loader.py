# RUNTIME LOADER v7: self-decrypting module resolver
# WARNING: auto-generated content, do not modify
"""Bootloader + runtime loader v7: random names, external crypto, PyArmor integration."""

from __future__ import annotations
import os, shutil, secrets, hashlib

def _produce_random_symbol() -> str:
    """Generate a random meaningless identifier."""
    styles = [
        lambda: f"_0x{secrets.token_hex(5)}",
        lambda: f"_a{secrets.token_hex(4)}",
        lambda: f"_b{secrets.token_hex(4)}",
        lambda: f"_c{secrets.token_hex(4)}",
        lambda: f"_d{secrets.token_hex(4)}",
        lambda: f"_e{secrets.token_hex(4)}",
        lambda: f"_f{secrets.token_hex(4)}",
        lambda: f"_x{secrets.token_hex(4)}",
        lambda: f"_y{secrets.token_hex(4)}",
        lambda: f"_z{secrets.token_hex(4)}",
        lambda: f"_p{secrets.token_hex(4)}",
        lambda: f"_q{secrets.token_hex(4)}",
        lambda: f"_r{secrets.token_hex(4)}",
        lambda: f"_s{secrets.token_hex(4)}",
        lambda: f"_t{secrets.token_hex(4)}",
        lambda: f"_w{secrets.token_hex(4)}",
        lambda: f"_v{secrets.token_hex(4)}",
        lambda: f"_k{secrets.token_hex(4)}",
        lambda: f"_m{secrets.token_hex(4)}",
        lambda: f"_n{secrets.token_hex(4)}",
    ]
    return secrets.choice(styles)()


def _scramble_identifiers(source: str) -> str:
    """Replace all meaningful identifiers in the source with random names.
    Scans for Python identifiers and replaces them."""
    import re
    # Find all function def names, class names, and global variable assignments
    _rename_table = {}
    # Function defs
    for m in re.finditer(r'^def (\w+)\(', source, re.MULTILINE):
        name = m.group(1)
        if name not in _rename_table and not name.startswith("__"):
            _rename_table[name] = _produce_random_symbol()
    # Class defs
    for m in re.finditer(r'^class (\w+)', source, re.MULTILINE):
        name = m.group(1)
        if name not in _rename_table and not name.startswith("__"):
            _rename_table[name] = _produce_random_symbol()
    # Apply replacements (longest first to avoid partial matches)
    for old, new in sorted(_rename_table.items(), key=lambda x: -len(x[0])):
        source = re.sub(r'\b' + re.escape(old) + r'\b', new, source)
    return source


def _synthesize_decoy_decryptor(num: int) -> str:
    """Generate a random-looking decryption function.
    Each call produces different code structure."""
    import random
    r = random.Random(secrets.randbits(32))
    _func_alias = _produce_random_symbol()
    _func_body_lines = []
    _func_body_lines.append(f"    import json, hashlib, zlib")
    _func_body_lines.append(f"    from cryptography.hazmat.primitives.ciphers.aead import AESGCM")
    _func_body_lines.append(f"    p = json.loads(open(path, 'rb').read().decode())")
    _func_body_lines.append(f"    ct = bytes.fromhex(p['d'])")
    _func_body_lines.append(f"    k = bytes.fromhex(p['k{r.randint(1,3)}'])")
    # Insert random decoy operations
    for _ in range(r.randint(1, 3)):
        _var_alias = _produce_random_symbol()
        _func_body_lines.append(f"    {_var_alias} = hashlib.sha256(k).hexdigest()[:{r.randint(4,12)}]")
    # Varying decrypt approaches
    approaches = [
        f"    x = AESGCM(k).decrypt(ct[:12], ct[12:], b'')",
        f"    nonce = ct[:12]\n    tag_ct = ct[12:]\n    x = AESGCM(k).decrypt(nonce, tag_ct, b'')",
    ]
    _func_body_lines.append(secrets.choice(approaches))
    if r.random() < 0.4:
        _func_body_lines.append(f"    from Cryptodome.Cipher import ChaCha20_Poly1305")
        _func_body_lines.append(f"    c20 = ChaCha20_Poly1305.new(key=k, nonce=x[:12])")
        _func_body_lines.append(f"    x = c20.decrypt(x[12:28], x[28:])")
    # XOR step with varying implementations
    xor_variants = [
        f"    return zlib.decompress(bytes(a^b for a,b in zip(x,_xof(len(x),k)))).decode()",
        f"    ks = _xof(len(x), k)\n    return zlib.decompress(bytes(i^j for i,j in zip(x,ks))).decode()",
        f"    r = bytearray()\n    for i in range(len(x)):\n        r.append(x[i] ^ _xof(1, k + i.to_bytes(4,'big'))[0])\n    return zlib.decompress(bytes(r)).decode()",
    ]
    _func_body_lines.append(secrets.choice(xor_variants))

    return f"def {_func_alias}(path):\n" + "\n".join(_func_body_lines) + "\n\n"


def gen_loader_source() -> str:
    """Generate the runtime loader source with randomized names and structure."""
    import secrets as _sec, random as _rnd
    _rnd.seed(_sec.randbits(32))

    f_xof = _produce_random_symbol()
    f_load = _produce_random_symbol()
    f_find = _produce_random_symbol()
    f_filter = _produce_random_symbol()
    f_extract = _produce_random_symbol()
    f_run = "run"
    f_extra = _produce_random_symbol()
    f_gf_mul = _produce_random_symbol()
    f_gf_inv = _produce_random_symbol()
    f_shamir = _produce_random_symbol()
    cls_L = _produce_random_symbol()
    cls_F = _produce_random_symbol()

    # Build the loader source with random names
    src = f'''"""Runtime v7 - auto-generated, randomized structure."""
import sys, os, json, hmac, hashlib, zlib, importlib.abc, importlib.machinery
sys.dont_write_bytecode = True
try: _SD = getattr(sys, '_MEIPASS', None) or os.path.dirname(os.path.abspath(__file__))
except: _SD = getattr(sys, '_MEIPASS', None) or (os.path.dirname(os.path.abspath(sys.argv[0])) if sys.argv else ".")
_D = os.path.join(_SD, "_runtime") if os.path.isdir(os.path.join(_SD, "_runtime")) else _SD
_MAP = ""
_VAULT = ""

def {f_xof}(l, s):
    r, c = bytearray(), 0
    while len(r) < l:
        r.extend(hashlib.sha256(s + c.to_bytes(4,"big")).digest()); c += 1
    return bytes(r[:l])

def {f_extract}(p):
    """Complex multi-layer key extraction.
    Layer 1: xor of ALL keys determines candidate
    Layer 2: blake3/SHA256 of each key checked against f2
    Layer 3: HMAC verification against f3
    All 3 layers must pass - decoy files fail at least one."""
    keys = {{}}
    for i in range(1, 6):
        k = p.get(f"k{{i}}")
        if k: keys[f"k{{i}}"] = bytes.fromhex(k)
    if not keys: return b""

    # Layer 1: XOR all keys, verify against f1
    xored = bytearray(32)
    for v in keys.values():
        for i in range(min(32, len(v))): xored[i] ^= v[i]
    f1_ok = hashlib.sha256(bytes(xored)).hexdigest()[5:13] == p.get("f1", "")

    # Try each key against f2 and f3
    for kn, kv in keys.items():
        try:
            import blake3 as _b3
            f2_ok = _b3.blake3(kv).hexdigest()[3:11] == p.get("f2", "")
        except:
            f2_ok = hashlib.sha256(b"f2-domain:" + kv).hexdigest()[8:16] == p.get("f2", "")
        f3_ok = hmac.new(kv, b"S-Protect-v6-key-verify", "sha256").hexdigest()[:8] == p.get("f3", "")
        if f1_ok and f2_ok and f3_ok:
            return kv
    return b""

def {f_filter}(mk, shards):
    """Verify chain integrity across mapped files."""
    for mn in sorted(shards.keys()):
        p = json.loads(open(mn, "rb").read().decode()) if os.path.isfile(mn) else None
        if not p or not p.get("c"): continue

def {f_load}(p, mk):
    """Full decrypt: extra layers -> AES-GCM -> XOR -> ChaCha20 -> zlib."""
    ct = bytes.fromhex(p["d"])
    hdr = p.get("h", "")
    if hdr:
        ct = {f_extra}(ct, mk, hdr)
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    x = AESGCM(mk).decrypt(ct[:12], ct[12:], b"")
    ks = {f_xof}(len(x), hashlib.sha256(mk).digest())
    x = bytes(a^b for a,b in zip(x,ks))
    try:
        x = ChaCha20Poly1305(mk).decrypt(x[:12], x[12:], b"")
    except Exception:
        raise RuntimeError("ChaCha20 decrypt failed - data may be corrupted")
    return zlib.decompress(x).decode()

def {f_extra}(ct, mk, hdr):
    import json, hashlib
    if not hdr: return ct
    try:
        h = json.loads(hdr) if isinstance(hdr, str) else {{}}
    except:
        return ct
    if "extra_layers" not in h: return ct
    for algo in reversed(h.get("extra_layers", [])):
        info = h["layer_ivs"].get(algo)
        if not info or not info.get("iv") or not info.get("salt"):
            raise ValueError("Missing decrypt params for layer: " + str(algo))
        iv = bytes.fromhex(info["iv"])
        salt = bytes.fromhex(info["salt"])
        from cryptography.hazmat.primitives.kdf.hkdf import HKDF as _HK
        from cryptography.hazmat.primitives import hashes as _Hs
        lk = _HK(algorithm=_Hs.SHA256(), length=32, salt=salt, info=("sprotect:" + algo).encode()).derive(mk)
        if algo == "salsa20":
            mod = __import__("Cryptodome.Cipher", fromlist=["Salsa20"])
            c = mod.Salsa20.new(key=lk, nonce=iv[:8])
            ct = c.decrypt(ct)
        else:
            from cryptography.hazmat.primitives.ciphers import Cipher as _Cp, algorithms as _Al, modes as _Md
            c = _Cp(_Al.AES(lk), _Md.CBC(iv[:16]))
            p = c.decryptor().update(ct) + c.decryptor().finalize()
            ct = p[:-p[-1]]
    return ct

# Decoy classes and functions
class {_produce_random_symbol()}:
    """Decoy class - looks like a real loader component."""
    def __init__(self): pass
    def {_produce_random_symbol()}(self): return None

'''

    # Add random decoy functions
    for _ in range(_rnd.randint(2, 5)):
        src += _synthesize_decoy_decryptor(_)

    # Add the real loader class
    load_func = _produce_random_symbol()
    src += f'''
class {cls_L}(importlib.abc.Loader):
    def __init__(self, n, p, mk, pk=False):
        self.n, self.p, self.mk, self.pk = n, p, mk, pk
    def create_module(self, s): return None
    def exec_module(self, m):
        m.__dict__.setdefault("__file__", self.p)
        m.__dict__.setdefault("__package__", self.n)
        if self.pk: m.__dict__.setdefault("__path__", [os.path.dirname(self.p)])
        pp = json.loads(open(self.p, "rb").read().decode())
        src = {f_load}(pp, self.mk)
        if src is None: raise RuntimeError(f"Failed: {{self.n}}")
        exec(compile(src, self.p, "exec"), m.__dict__)

class {cls_F}(importlib.abc.MetaPathFinder):
    def __init__(self, mk, mmap): self.mk, self.mmap = mk, mmap
    def find_spec(self, n, p=None, t=None):
        hex_n = self.mmap.get(n, "")
        if not hex_n: return None
        pye = os.path.join(_D, hex_n + ".pye")
        if os.path.isfile(pye):
            is_pkg = any(mn.startswith(n + ".") for mn in self.mmap)
            s = importlib.machinery.ModuleSpec(n, {cls_L}(n, pye, self.mk, is_pkg), origin=pye)
            if is_pkg: s.submodule_search_locations = [os.path.dirname(pye)]
            return s
        return None

def _verify_manifest(root):
    base = root or _SD
    mf = os.path.join(base, "integrity_manifest.json")
    if not os.path.isfile(mf):
        mf = os.path.join(base, "_meta", "integrity_manifest.json")
    if not os.path.isfile(mf): return
    import json as _js
    manifest = _js.loads(open(mf, "rb").read().decode())
    for rel, expected in manifest.items():
        fp = os.path.join(_D, rel)
        if not os.path.isfile(fp):
            raise RuntimeError("Integrity: missing " + rel)
        h = hashlib.sha256()
        with open(fp, "rb") as f:
            while True:
                chunk = f.read(65536)
                if not chunk: break
                h.update(chunk)
        if h.hexdigest() != expected:
            raise RuntimeError("Integrity: modified " + rel)
    actual = set()
    for r, _, fs in os.walk(_D):
        for f in fs:
            if f.endswith(".pye"):
                actual.add(os.path.relpath(os.path.join(r, f), _D).replace("\\\\", "/"))
    extra = actual - set(manifest)
    if extra:
        raise RuntimeError("Integrity: extra files " + str(extra))

def {f_gf_mul}(a, b):
    p = 0
    for _ in range(8):
        if b & 1: p ^= a
        hi = a & 0x80
        a = (a << 1) & 0xFF
        if hi: a ^= 27
        b >>= 1
    return p & 0xFF

def {f_gf_inv}(x):
    if x == 0: return 0
    r, e = 1, 254
    b = x
    while e:
        if e & 1: r = {f_gf_mul}(r, b)
        b = {f_gf_mul}(b, b)
        e >>= 1
    return r

def {f_shamir}(shares):
    """Reconstruct master key from Shamir shares via Lagrange."""
    px = [s[0] for s in shares]
    t = len(shares)
    lag = []
    for i in range(t):
        xi = px[i]
        num, den = 1, 1
        for j in range(t):
            if j != i:
                xj = px[j]
                num = {f_gf_mul}(num, 0 ^ xj)
                den = {f_gf_mul}(den, xi ^ xj)
        lag.append({f_gf_mul}(num, {f_gf_inv}(den)))
    result = bytearray(len(shares[0][1]))
    for bi in range(len(result)):
        v = 0
        for i in range(t):
            v ^= {f_gf_mul}(shares[i][1][bi], lag[i])
        result[bi] = v
    return bytes(result)

def _anti_checks():
    import sys as _sc, os as _so, time as _st
    try:
        if _sc.gettrace() is not None:
            _sc.exit(1)
    except:
        pass
    try:
        _t0 = _st.time()
        _x = 0
        for _ in range(5000000):
            _x ^= _
        if _st.time() - _t0 > 1.0:
            _sc.exit(1)
    except:
        pass
    try:
        for _ind in ['/proc/1/cgroup', '/sys/class/dmi/id/product_name',
                     '/.dockerenv', '/tmp/cuckoo', '/tmp/analysis',
                     'C:/cuckoo', 'C:/analysis', 'C:/sandbox']:
            if _so.path.isfile(_ind) or _so.path.isdir(_ind):
                _sc.exit(1)
    except:
        pass

def run(entry, root=""):
    """Run entry: decrypt map, collect shards, load modules."""
    if not _MAP: raise RuntimeError("No module map")
    _verify_manifest(root)
    _anti_checks()
    mmap = json.loads(_MAP)
    if _VAULT:
        import struct as _st9
        _v = json.loads(_VAULT) if isinstance(_VAULT, str) else _VAULT
        _rk = bytes.fromhex(_v["pool"][_v["pos"]])
        _m = bytes.fromhex(_v.get("mask", "")) if _v.get("mask") else b""
        if _m:
            _rk = bytes(_rk[i] ^ _m[i % len(_m)] for i in range(32))
        if _v.get("pid", True):
            _h = hmac.new(_rk, digestmod="sha256")
            _h.update(_st9.pack("<I", os.getpid()))
            _h.update(b"0xDEADBEEF")
            _rk = _h.digest()
        mk = _rk
    else:
        # Try Shamir shares first (sid+sv fields)
        shares = []
        for mn, hn in mmap.items():
            pye = os.path.join(_D, hn + ".pye")
            if not os.path.isfile(pye): continue
            pp = json.loads(open(pye, "rb").read().decode())
            sid = pp.get("sid")
            sv = pp.get("sv")
            if sid is not None and sv:
                shares.append((sid, bytes.fromhex(sv)))
        if len(shares) >= 2:
            mk = {f_shamir}(shares)
        else:
            # Fallback: traditional XOR+fingerprint
            shards = {{}}
            for mn, hn in mmap.items():
                pye = os.path.join(_D, hn + ".pye")
                if not os.path.isfile(pye): continue
                pp = json.loads(open(pye, "rb").read().decode())
                rk = {f_extract}(pp)
                if rk and len(rk) == 32:
                    shards[mn] = rk
            if len(shards) < 2: raise RuntimeError("Insufficient shards")
            vals = list(shards.values())
            mk = bytearray(vals[0])
            for v in vals[1:]:
                for i in range(len(mk)): mk[i] ^= v[i]
            mk = bytes(mk)

    sys.meta_path.insert(0, {cls_F}(mk, mmap))
    entry_hex = mmap.get(entry, "")
    if not entry_hex: raise FileNotFoundError(f"Entry not in map: {{entry}}")
    e = os.path.join(_D, entry_hex + ".pye")
    pp = json.loads(open(e, "rb").read().decode())
    src = {f_load}(pp, mk)
    fm = os.path.join(root or os.path.dirname(_D), entry + ".py")
    exec(compile(src, e, "exec"), {{"__name__":"__main__","__file__":fm,"__builtins__":__builtins__}})
'''

    return src


_BOOT_TEMPLATE = '''"""Module loader."""
import sys, os, json, hashlib, zlib, hmac
sys.dont_write_bytecode = True
a = getattr(sys, '_MEIPASS', None) or os.path.dirname(os.path.abspath(__file__))

def xo(l, s):
    r, c = bytearray(), 0
    while len(r) < l:
        r.extend(hashlib.sha256(s + c.to_bytes(4,"big")).digest()); c += 1
    return bytes(r[:l])

def _fe(p):
    ks = {{}}
    for i in range(1, 6):
        kn = f"k{{i}}"
        if kn in p: ks[kn] = bytes.fromhex(p[kn])
    if not ks: return b""
    xored = bytearray(32)
    for v in ks.values():
        for i in range(min(32, len(v))): xored[i] ^= v[i]
    f1_ok = hashlib.sha256(bytes(xored)).hexdigest()[5:13] == p.get("f1", "")
    for kn, kv in ks.items():
        try:
            import blake3 as _b3; f2_ok = _b3.blake3(kv).hexdigest()[3:11] == p.get("f2", "")
        except:
            f2_ok = hashlib.sha256(b"f2-domain:"+kv).hexdigest()[8:16] == p.get("f2", "")
        f3_ok = hmac.new(kv, b"S-Protect-v6-key-verify","sha256").hexdigest()[:8] == p.get("f3", "")
        if f1_ok and f2_ok and f3_ok: return kv
    return b""

_SALT = "{build_salt}"
def bt():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    k = hmac.new(bytes.fromhex(_SALT), b"sprotect-loader-key-v1", hashlib.sha256).digest()
    p = json.loads(open(os.path.join(a,"{rd}","loader.pye"),"rb").read().decode())
    rk = _fe(p) or k
    ct = bytes.fromhex(p["d"])
    x = AESGCM(rk).decrypt(ct[:12], ct[12:], b"")
    x = bytes(ib^j for ib,j in zip(x,xo(len(x),rk)))
    try:
        x = ChaCha20Poly1305(rk).decrypt(x[:12], x[12:], b"")
    except Exception:
        pass
    return zlib.decompress(x).decode()

ld = compile(bt(), "", "exec")
exec(ld)
run("{entry}", a)
'''


_HYBRID_BOOT_TEMPLATE = '''"""Hybrid loader."""
import sys, os, json, hashlib, zlib
sys.dont_write_bytecode = True
_R = getattr(sys, '_MEIPASS', None) or os.path.dirname(os.path.abspath(__file__))

def _boot(key_path):
    import getpass
    if not os.path.isfile(key_path):
        key_path = input(f"Enter private key path [{key_path}]: ") or key_path
    if not os.path.isfile(key_path):
        print("ERROR: Private key not found"); sys.exit(1)
    priv = open(key_path, "rb").read()
    enc_data = bytes.fromhex("{hk}")
    algo = "{ha}"
    if algo == "RSA":
        from Cryptodome.PublicKey import RSA
        from Cryptodome.Cipher import PKCS1_OAEP
        from Cryptodome.Hash import SHA256
        try:
            key_obj = RSA.import_key(priv)
            mk = PKCS1_OAEP.new(key_obj, hashAlgo=SHA256).decrypt(enc_data)
        except Exception:
            pw = getpass.getpass("Private key passphrase: ")
            key_obj = RSA.import_key(priv, passphrase=pw)
            mk = PKCS1_OAEP.new(key_obj, hashAlgo=SHA256).decrypt(enc_data)
    else:
        from Cryptodome.PublicKey import ECC
        from Cryptodome.Cipher import AES
        try:
            key_obj = ECC.import_key(priv)
        except:
            pw = getpass.getpass("Private key passphrase: ")
            key_obj = ECC.import_key(priv, passphrase=pw)
        import json as _j
        data = _j.loads(enc_data.decode())
        ephem = ECC.import_key(data["ephemeral_pub"])
        shared = key_obj.dh(ephem)
        shared_bytes = int(shared.x).to_bytes(32, 'big')
        from cryptography.hazmat.primitives.kdf.hkdf import HKDF as _H
        from cryptography.hazmat.primitives import hashes as _hs
        salt = bytes.fromhex(data["salt"])
        aes_k = _H(algorithm=_hs.SHA256(), length=32, salt=salt, info=b"sprotect:ecc-hybrid").derive(shared_bytes)
        n = bytes.fromhex(data["nonce"])
        c = AES.new(aes_k, AES.MODE_GCM, nonce=n)
        mk = c.decrypt_and_verify(bytes.fromhex(data["ct"]), bytes.fromhex(data["tag"]))
    _run(mk)

def _xof(l, s):
    r, c = bytearray(), 0
    while len(r) < l:
        r.extend(hashlib.sha256(s + c.to_bytes(4,"big")).digest()); c += 1
    return bytes(r[:l])

def _run(mk):
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    p = json.loads(open(os.path.join(_R,"{rd}","loader.pye"),"rb").read().decode())
    ct = bytes.fromhex(p["d"])
    x = AESGCM(mk).decrypt(ct[:12], ct[12:], b"")
    x = bytes(a^b for a,b in zip(x,_xof(len(x),mk)))
    try:
        x = ChaCha20Poly1305(mk).decrypt(x[:12], x[12:], b"")
    except Exception:
        pass
    ld = zlib.decompress(x).decode()
    exec(compile(ld, "", "exec"))
    run("{entry}", _R)

_boot("{kp}")
'''


def _random_hex_string(n: int) -> str:
    return secrets.token_hex(n)


def _random_noise_comment() -> str:
    """Generate a random-looking comment line."""
    return secrets.choice([
        f"# TODO: {_random_hex_string(16)}",
        f"# FIXME: {secrets.choice(['refactor','cleanup','optimize','verify'])} {_random_hex_string(8)}",
        f"# HACK: {_random_hex_string(24)}",
        f"# XXX: {secrets.choice(['incomplete','untested','deprecated','workaround'])}",
        f"# NOTE: {_random_hex_string(32)}",
        f"# BUG: {_random_hex_string(16)}",
        f"# SECURITY: {_random_hex_string(24)}",
        f"# PERFORMANCE: {_random_hex_string(20)}",
    ])


def _spoof_protection_header() -> str:
    """Generate a fake S-Protect-like string."""
    return secrets.choice([
        f'"""S-Protect loader v{secrets.randbelow(5)+1}.{secrets.randbelow(10)}."""',
        f'# S-Protect {secrets.token_hex(8)}',
        f'# SProtect {_random_hex_string(8)}',
        f'"""Loader v{secrets.randbelow(5)+1}.{secrets.randbelow(10)}."""',
    ])

def _build_single_decoy(name: str | None = None) -> str:
    """Generate a single structurally randomized decoy decryption function."""
    _func_alias = _produce_random_symbol()
    _dummy_key_hex = _random_hex_string(secrets.randbelow(16) + 32)
    _dummy_cipher_hex = _random_hex_string(secrets.randbelow(100) + 50)
    fake_h = _random_hex_string(4)

    # Randomly choose which crypto steps to include and in what order
    _op_sequence = []
    _op_sequence.append(f"        _k = bytes.fromhex('{_dummy_key_hex}')")
    _op_sequence.append(f"        _d = bytes.fromhex('{_dummy_cipher_hex}')")

    if secrets.randbelow(3) > 0:
        _op_sequence.append(f"        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')")
    else:
        _op_sequence.append(f"        _c = Cipher(algorithms.AES(_k), modes.CTR(_d[:16])).decryptor()")
        _op_sequence.append(f"        _x = _c.update(_d[16:]) + _c.finalize()")

    if secrets.randbelow(2) == 0:
        _op_sequence.append(f"        _x = bytes(ib^j for ib,j in zip(_x, hashlib.sha256(_k).digest()*99))[:_x]")

    if secrets.randbelow(3) > 0:
        _op_sequence.append(f"        _x = ChaCha20Poly1305(_k).decrypt(_x[:12], _x[12:], b'')")

    if secrets.randbelow(2) == 0:
        _op_sequence.append(f"        _x = bytes(ib^j for ib,j in zip(_x, _k*99))[:len(_x)]")

    if secrets.randbelow(2) == 0:
        _op_sequence.append(f"        if hashlib.sha256(_x[:16]).hexdigest()[:8] != '{_random_hex_string(4)}':")
        _op_sequence.append(f"            _x = _x[::-1]")

    if secrets.randbelow(2) == 0:
        _op_sequence.append(f"        _crc = zlib.crc32(_x) & 0x{_random_hex_string(4)}")

    _op_sequence.append(f"        _r = zlib.decompress(_x)")

    try_lines = "\n".join(_op_sequence)
    has_args = name is None  # no args when called from sections
    if has_args:
        _signature_str = secrets.choice(
            ["key", "data", "path", "sig", "buf"] +
            ["key, iv", "data, offset", "path, mode", "sig, expected"])
    else:
        _signature_str = ""
    actual_fn = name or _func_alias
    return (
        f"{_random_noise_comment()}\n"
        f"{_spoof_protection_header()}\n"
        f"# {secrets.token_hex(secrets.randbelow(8)+8)}\n"
        f"def {actual_fn}({_signature_str}):\n"
        f"    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305\n"
        f"    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes\n"
        f"    import hashlib, json, os, zlib\n"
        f"    try:\n"
        f"{try_lines}\n"
        f"    except Exception as _{_produce_random_symbol()}:\n"
        f"        _r = b''\n"
        f"    return _r\n"
    )


def _multiply_decoys(count: int) -> str:
    """Generate structurally varied decoy functions."""
    return "\n".join(_build_single_decoy() for _ in range(count))


def _inflate_with_padding(target_kb: int = 55) -> str:
    """Generate varied padding with comments, strings, fake logic."""
    lines = []
    size = 0
    comment_types = [
        lambda: f"# {secrets.choice(['TODO','FIXME','HACK','XXX','BUG','NOTE','XXX','SECURITY','PERF'])}: {_random_hex_string(secrets.randbelow(40)+10)}",
        lambda: f"# {secrets.choice(['refactor','review','optimize','verify','test','cleanup'])} {_random_hex_string(16)}",
        lambda: f"# v{secrets.randbelow(10)}.{secrets.randbelow(99)}.{secrets.randbelow(999)} - {_random_hex_string(20)}",
        lambda: f"# Copyright (c) 202{secrets.randbelow(6)} {_random_hex_string(16)}",
        lambda: f"# License: {secrets.choice(['MIT','Apache-2.0','GPL-3.0','BSD','Proprietary'])}",
        lambda: f"# {secrets.choice(['DEPRECATED','UNUSED','LEGACY','EXPERIMENTAL'])}: {_random_hex_string(12)}",
        lambda: f"# {secrets.choice(['assert','ensure','check','validate'])} {_random_hex_string(16)}",
        lambda: f"# type: ignore[{_random_hex_string(8)}]",
        lambda: f"# pragma: {secrets.choice(['no cover','no mutate','skip CI'])}",
    ]
    while size < target_kb * 1024:
        block = "\n".join(
            secrets.choice(comment_types)()
            for _ in range(secrets.randbelow(15) + 8)
        )
        block += f"\n_{_produce_random_symbol()} = {secrets.choice([
            f"'{_random_hex_string(secrets.randbelow(200)+100)}'",
            f"b'{_random_hex_string(secrets.randbelow(100)+50)}'",
            f"0x{_random_hex_string(secrets.randbelow(8)+2)}",
            str(secrets.randbelow(2**32)),
        ])}\n"
        lines.append(block)
        size += len(block) + 1
    return "\n".join(lines)


_DECOY_IMPORT_BLOCK = """import sys, os, json, re, math, hashlib, base64, struct, zlib
import itertools, collections, functools, random, string, binascii
import tempfile, uuid, copy, logging, datetime, decimal, statistics
from math import sqrt, floor, ceil, sin, cos, tan, log, exp
from os import path, name, getpid, getcwd, environ, sep
from sys import platform, version, argv, executable, modules, path as sys_path
from hashlib import sha256, md5, sha1, sha224, sha384, sha512, blake2b
from base64 import b64encode, b64decode, a85encode, a85decode, b32decode
from struct import pack, unpack, calcsize, iter_unpack
from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes"""


def _probe_lookalike_function(real_bt_template: str, idx: int, _all_salts: list[str]) -> tuple[str, str]:
    """Generate one realistic-looking function + its exec call.
    Uses HMAC-derived key from salt. Only idx 0 uses the REAL salt."""
    _func_alias = _produce_random_symbol()
    if idx == 0:
        body_start = real_bt_template.index("def bt():") + len("def bt():")
        real_body = real_bt_template[body_start:]
        real_body = real_body.replace("bt", _func_alias)
        _fun_definition = f"def {_func_alias}():{real_body}"
        _exec_statement = f"_e = compile({_func_alias}(), '', 'exec')\nexec(_e)"
    else:
        _fake_salt = _all_salts[idx] if idx < len(_all_salts) else secrets.token_hex(16)
        _fun_definition = f"""def {_func_alias}():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    import hashlib, json, os, zlib, hmac
    try:
        k = hmac.new(bytes.fromhex('{_fake_salt}'), b"sprotect-loader-key-v1", hashlib.sha256).digest()
        p = json.loads(open(os.path.join(a,"_runtime","loader.pye"),"rb").read().decode())
        rk = k
        ks = {{}}
        for i in range(1,6):
            kn = f"k{{i}}"
            if kn in p: ks[kn] = bytes.fromhex(p[kn])
        if ks:
            xored = bytearray(32)
            for v in ks.values():
                for i in range(min(32, len(v))): xored[i] ^= v[i]
            f1_ok = hashlib.sha256(bytes(xored)).hexdigest()[5:13] == p.get("f1","")
            for kn, kv in ks.items():
                try:
                    import blake3 as _b3; f2_ok = _b3.blake3(kv).hexdigest()[3:11] == p.get("f2","")
                except:
                    f2_ok = hashlib.sha256(b"f2-domain:"+kv).hexdigest()[8:16] == p.get("f2","")
                f3_ok = hmac.new(kv, b"S-Protect-v6-key-verify","sha256").hexdigest()[:8] == p.get("f3","")
                if f1_ok and f2_ok and f3_ok:
                    rk = kv; break
        ct = bytes.fromhex(p["d"])
        x = AESGCM(rk).decrypt(ct[:12], ct[12:], b"")
        x = bytes(ib^j for ib,j in zip(x,xo(len(x),rk)))
        x = ChaCha20Poly1305(rk).decrypt(x[:12], x[12:], b"")
        r = zlib.decompress(x)
    except Exception:
        r = b''
    return r
"""
        # Fake exec - some with try/except, some without
        if secrets.randbelow(3) > 0:
            _exec_statement = f"""try:
    _e = compile({_func_alias}(), '', 'exec')
    exec(_e)
except Exception:
    pass"""
        else:
            _exec_statement = f"_e = compile({_func_alias}(), '', 'exec')\nexec(_e)"
    return _fun_definition, _exec_statement


def gen_boot(output_dir: str, entry_module: str, entry_hex: str,
             per_file_configs: dict[str, str], loader_key: bytes,
             build_salt: str = "",
             hybrid_key: bytes | None = None, algorithm: str = "RSA") -> str:
    ep = os.path.join(output_dir, entry_module.replace(".", os.sep) + ".py")
    os.makedirs(os.path.dirname(ep), exist_ok=True)

    _final_script = _BOOT_TEMPLATE.format(
        build_salt=build_salt,
        rd="_runtime", entry=entry_module)

    # Decoy salts for fake probe functions
    _dummy_salts = [secrets.token_hex(16) for _ in range(5)]
    _all_salts = [build_salt] + _dummy_salts

    # --- Generate 6 "real" functions (1 real + 5 doomed) + many decoys ---
    _probe_functions = []   # (func_def, exec_line)
    for i in range(6):
        fd, el = _probe_lookalike_function(_final_script, i, _all_salts)
        _probe_functions.append((fd, el))

    _decoy_functions = [_build_single_decoy() for _ in range(secrets.randbelow(15)+20)]

    # --- Create 6 sections, each with fake execs ABOVE and BELOW the real exec ---
    _exec_sections = []
    for _section_index in range(6):
        # Generate 3-6 fake execs BEFORE the real exec
        _pre_exec_decoys = []
        for _ in range(secrets.randbelow(4) + 3):
            _func_alias = _produce_random_symbol()
            _decoy_functions.append(_build_single_decoy(_func_alias))
            if secrets.randbelow(2) == 0:
                _pre_exec_decoys.append(f"_e = compile({_func_alias}(), '', 'exec')\nexec(_e)")
            else:
                _pre_exec_decoys.append(f"try:\n    _e = compile({_func_alias}(), '', 'exec')\n    exec(_e)\nexcept Exception:\n    pass")
        # Generate 3-6 fake execs AFTER the real exec
        _post_exec_decoys = []
        for _ in range(secrets.randbelow(4) + 3):
            _func_alias = _produce_random_symbol()
            _decoy_functions.append(_build_single_decoy(_func_alias))
            if secrets.randbelow(2) == 0:
                _post_exec_decoys.append(f"_e = compile({_func_alias}(), '', 'exec')\nexec(_e)")
            else:
                _post_exec_decoys.append(f"try:\n    _e = compile({_func_alias}(), '', 'exec')\n    exec(_e)\nexcept Exception:\n    pass")

        section = "\n".join(_pre_exec_decoys) + "\n" + _probe_functions[_section_index][1] + "\n" + "\n".join(_post_exec_decoys)
        _exec_sections.append(section)

    # --- Assemble: ALL function defs FIRST, then ALL exec blocks ---
    _noise_padding = _inflate_with_padding(40)
    _decoy_function_block = "\n\n".join(_decoy_functions)
    _probe_function_defs = "\n\n".join(fd for fd, el in _probe_functions)

    _split_marker = "ld = compile"
    if _split_marker in _final_script:
        _definitions_section, _ = _final_script.split(_split_marker, 1)
    else:
        _definitions_section = _final_script

    _complete_definitions = (_DECOY_IMPORT_BLOCK + "\n\n" + _noise_padding + "\n\n" +
                _definitions_section + "\n\n" +
                _probe_function_defs + "\n\n" + _decoy_function_block)

    import random as _rnd
    _rnd.seed(secrets.randbits(32))
    _rnd.shuffle(_exec_sections)
    _execution_section = "\n\n".join(_exec_sections)

    _final_script = _complete_definitions + "\n\n" + _execution_section

    from sprotect.minify import minify_source
    _final_script = minify_source(_final_script, add_garbage=True)
    with open(ep, "w", encoding="utf-8") as f: f.write(_final_script)
    for src, dst in per_file_configs.items():
        shutil.copy2(src, dst)
    return ep
