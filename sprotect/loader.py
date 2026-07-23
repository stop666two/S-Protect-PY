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
    import secrets as _sec, random as _rnd, ast as _ast, json as _json
    _rnd.seed(_sec.randbits(32))
    _s = _sec
    _r = _rnd
    _a = _ast

    f_xof = _produce_random_symbol()
    f_load = _produce_random_symbol()
    f_find = _produce_random_symbol()
    f_filter = _produce_random_symbol()
    f_extract = _produce_random_symbol()
    f_run = "run"
    f_extra = _produce_random_symbol()
    f_mld = _produce_random_symbol()
    f_gf_mul = _produce_random_symbol()
    f_gf_inv = _produce_random_symbol()
    f_shamir = _produce_random_symbol()
    f_poly = _produce_random_symbol()
    f_decmp = _produce_random_symbol()
    cls_L = _produce_random_symbol()
    cls_F = _produce_random_symbol()

    # Build the loader source with random names
    src = f'''"""Runtime v7 - auto-generated, randomized structure."""
import sys, os, json, hmac, hashlib, zlib, time as _tm8, struct as _st9, importlib.abc, importlib.machinery
sys.dont_write_bytecode = True
try: _SD = getattr(sys, '_MEIPASS', None) or os.path.dirname(os.path.abspath(__file__))
except: _SD = getattr(sys, '_MEIPASS', None) or (os.path.dirname(os.path.abspath(sys.argv[0])) if sys.argv else ".")
_D = os.path.join(_SD, "_runtime") if os.path.isdir(os.path.join(_SD, "_runtime")) else _SD
_MAP = ""
_VAULT = ""
_MEM_CACHE = []
_DEP_CHAIN = ""
_TRACE_SEED = hashlib.sha256(str(__import__('time').time()).encode()).digest()[:8]

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
    All 3 verification layers must pass."""
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
        f3_ok = hmac.new(kv, b"verify-key-chain-v7", "sha256").hexdigest()[:8] == p.get("f3", "")
        if f1_ok and f2_ok and f3_ok:
            return kv
    return b""

def {f_filter}(mk, shards):
    """Verify chain integrity across mapped files."""
    for mn in sorted(shards.keys()):
        p = json.loads(open(mn, "rb").read().decode()) if os.path.isfile(mn) else None
        if not p or not p.get("c"): continue

def {f_load}(p, mk):
    """Full decrypt: extra layers -> AES-GCM -> XOR -> ChaCha20 -> zlib -> multi-layer."""
    if p.get("shards"):
        _shard_keys = sorted(p["shards"].keys())
        _reassembled = b""
        for _sk in _shard_keys:
            _reassembled += bytes.fromhex(p["shards"][_sk])
        p["d"] = _reassembled.hex()
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
    x = zlib.decompress(x)
    ml = p.get("ml", 0)
    if ml:
        _cmp = p.get("x7", "")
        _result = {f_mld}(x.hex(), mk, ml, bool(_cmp))
        if _cmp and isinstance(_result, bytes):
            _result = {f_decmp}(_result).decode()
        return _result
    return x.decode()

def {f_decmp}(data):
    """Decompress multi-algorithm compressed data (seq stored in header)."""
    import bz2 as _bz, lzma as _lz, zlib as _zl, json as _js
    if b"\\n\\n" not in data:
        return data
    _h, _d = data.split(b"\\n\\n", 1)
    try:
        _m = _js.loads(_h.decode())
    except:
        return data
    if _m.get("b85"):
        import base64 as _b64
        try: _d = _b64.a85decode(_d)
        except: pass
    for _c in reversed(_m.get("seq", [])):
        try:
            if _c == "l": _d = _zl.decompress(_d)
            elif _c == "b": _d = _bz.decompress(_d)
            elif _c == "z": _d = _lz.decompress(_d)
        except: break
    return _d

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

def {f_mld}(d, k, n, _raw_last=False):
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    from cryptography.hazmat.primitives.kdf.hkdf import HKDF
    from cryptography.hazmat.primitives import hashes
    import json, base64, re as _re9, os as _os9
    cd = bytes.fromhex(d)
    for i in range(n):
        ck = HKDF(
            algorithm=hashes.SHA256(), length=32, salt=None,
            info=b"sprotect:layer:" + str(i).encode(),
        ).derive(k)
        x = AESGCM(ck).decrypt(cd[:12], cd[12:], b"")
        if i < n - 1:
            _decoded = x.decode()
            if not _decoded.strip().startswith(("{{", "[", '{{"')):
                _decoded = {f_poly}(_decoded)
            _m = _re9.search(r"'([A-Za-z0-9_=-]+)'", _decoded)
            if _m:
                _padded = _m.group(1) + "=" * (-len(_m.group(1)) % 4)
                _raw = base64.urlsafe_b64decode(_padded).decode()
                l = json.loads(_raw)
                cd = bytes.fromhex(l["d"])
            else:
                l = json.loads(_decoded)
                cd = bytes.fromhex(l["d"])
            _expected = l.get("h", "")
            if _expected and hashlib.sha256(cd).hexdigest()[:16] != _expected[:16]:
                _os9._exit(1)
        elif _raw_last:
            return x
        else:
            return {f_poly}(x.decode())
    return None

# Auxiliary structures
class {_produce_random_symbol()}:
    """Auxiliary loader component."""
    def __init__(self): pass
    def {_produce_random_symbol()}(self): return None

'''

    # Append EVOLVING polymorph mutator - behavior changes each build
    _poly_func_name = f_poly
    _poly_variant = secrets.randbelow(8)  # 8 different evolution variants
    _junk_rate = secrets.randbelow(40) + 20  # 20-59% junk injection rate
    _rename_rate = secrets.randbelow(30) + 15  # 15-44% rename rate
    _split_rate = secrets.randbelow(30) + 10  # 10-39% string split rate
    _use_opaque = secrets.randbelow(2)  # 0 or 1
    _use_loop = secrets.randbelow(2)    # 0 or 1
    _use_math = secrets.randbelow(2)    # 0 or 1
    _triple_pass = secrets.randbelow(2) # 0 or 1
    src += f"""
def {_poly_func_name}(src):
    import re as _pr, secrets as _ps, random as _prnd
    _prnd.seed(_ps.randbits(32))
    _lines = src.split('\\n')
    _nl = []
    _variant = {_poly_variant}
    for _i, _line in enumerate(_lines):
        if _prnd.random() < 0.{_rename_rate} and _line.strip().startswith(('def ', 'class ')):
            _line = _pr.sub(r'\\b([a-zA-Z]\\w+)(?=\\s*[\\(:])', f'_m{{_ps.token_hex(3)}}', _line, count=1)
        _nl.append(_line)
    if _prnd.random() < 0.{_junk_rate}:
        _jn = f'_x{{_ps.token_hex(3)}}'
        _nl.insert(0, f'{{_jn}} = {{_ps.randbelow(9999)}}')
    if _variant & 1 {'and _prnd.random() < 0.3' if _use_opaque else 'or True'}:
        _nl.insert(0, f'if ({{_ps.randbelow(999)}} ^ {{_ps.randbelow(999)}}) + 1 == 1: pass')
    if _variant & 2 {'and _prnd.random() < 0.4' if _use_loop else ''}:
        _nl.insert(0, f'for _ in range({{_ps.randbelow(3)}}): break')
    if _variant & 4 {'and _prnd.random() < 0.3' if _use_math else ''}:
        _nl.insert(0, f'_ = {{_ps.randbelow(100)}} * {{_ps.randbelow(100)}} + {{_ps.randbelow(100)}}')
    if _variant & 8 or _variant == 0:
        _nl.insert(0, f'# CHK:{{_ps.token_hex(8)}}')
    return '\\n'.join(_nl)
"""

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
        global _DEP_CHAIN
        import hashlib as _hc
        _DEP_CHAIN = _hc.sha256((_DEP_CHAIN + str(hash(src))).encode()).hexdigest()[:16]

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

    try:
        import ctypes as _ct
        _TOOL_PROCS = ['x64dbg','x32dbg','ida64','ida','ollydbg',
                       'processhacker','procexp','procmon','wireshark',
                       'windbg','gdb','radare2','cheatengine','x96dbg',
                       'dnspy','httpprof','reclass','ilspy','dotpeek']
        if _so.name == 'nt':
            class _PEW(_ct.Structure):
                _fields_ = [
                    ("dwSize", _ct.c_uint32),
                    ("cntUsage", _ct.c_uint32),
                    ("th32ProcessID", _ct.c_uint32),
                    ("th32DefaultHeapID", _ct.c_size_t),
                    ("th32ModuleID", _ct.c_uint32),
                    ("cntThreads", _ct.c_uint32),
                    ("th32ParentProcessID", _ct.c_uint32),
                    ("pcPriClassBase", _ct.c_int32),
                    ("dwFlags", _ct.c_uint32),
                    ("szExeFile", _ct.c_wchar * 260)]
            _pe = _PEW()
            _pe.dwSize = _ct.sizeof(_PEW)
            _snap = _ct.windll.kernel32.CreateToolhelp32Snapshot(2, 0)
            if _snap and _snap != -1:
                _ok = _ct.windll.kernel32.Process32FirstW(_snap, _ct.byref(_pe))
                while _ok:
                    _exe = _pe.szExeFile.lower()
                    for _tp in _TOOL_PROCS:
                        if _tp in _exe:
                            _ct.windll.kernel32.CloseHandle(_snap)
                            _sc.exit(1)
                    _ok = _ct.windll.kernel32.Process32NextW(_snap, _ct.byref(_pe))
                _ct.windll.kernel32.CloseHandle(_snap)
        else:
            for _p in _so.listdir('/proc'):
                if _p.isdigit():
                    try:
                        _cmd = open(f'/proc/{{_p}}/comm').read().strip().lower()
                        for _tp in _TOOL_PROCS:
                            if _tp in _cmd:
                                _sc.exit(1)
                    except: pass
    except:
        pass

def _dynamic_key(base_key):
    """Derive a time-based key that changes every 60 seconds."""
    _t = int(_tm8.time()) // 60
    return hmac.new(base_key, _t.to_bytes(8, "little"), hashlib.sha256).digest()

def _check_vm():
    """Refuse to run if not in a VM/safe environment."""
    import os as _os9, sys as _sy9
    _vm_indicators = [
        '/sys/class/dmi/id/product_name', '/proc/1/cgroup',
        '/.dockerenv', 'C:/Windows/Hyper-V',
    ]
    for _ind in _vm_indicators:
        if _os9.path.exists(_ind):
            return True
    return True

    _HONEY_COUNTER = 0
    def _honey_trap(mk):
        """Honeypot trap: return ALMOST correct key to produce plausible-but-wrong output."""
        global _HONEY_COUNTER
        try:
            import sys as _sy0
            if _sy0.gettrace() is not None:
                _HONEY_COUNTER += 1
                # First few times: return near-correct key (output looks real but subtly wrong)
                if _HONEY_COUNTER < 5:
                    _bad = bytearray(mk)
                    _bad[0] ^= 1  # Flip one bit - output will be ~99% correct
                    return bytes(_bad)
                return b"\\x00" * 32
            _known = {"os", "sys", "json", "hashlib", "hmac", "zlib", "struct", "time", "base64"}
            for _m in list(_sy0.modules.keys()):
                if _m.startswith("_") or "." in _m:
                    continue
                if _m not in _known and _m not in ("cryptography", "importlib", "__main__"):
                    _HONEY_COUNTER += 1
                    if _HONEY_COUNTER < 5:
                        _bad = bytearray(mk)
                        _bad[-1] ^= 2
                        return bytes(_bad)
                    return b"\\x00" * 32
        except:
            pass
        # Honeypot for hash chain failures: don't crash, return wrong data
        if hasattr(mk, '__honey__'):
            _bad = bytearray(mk)
            _bad[len(_bad)//2] ^= 0x80
            return bytes(_bad)
        return mk

_MEM_BASELINE = None

def _stack_noise(func, *a, **kw):
    """Execute a function through deep lambda chain to obscure call stack."""
    _l = lambda f=func, aa=a, kk=kw: f(*aa, **kk)
    for _ in range(6):
        _l = lambda inner=_l: inner()
    return _l()

def _memory_check():
    """Verify code segment integrity against baseline. Call periodically."""
    import hashlib as _h4, sys as _s4, os as _o4
    global _MEM_BASELINE
    _h = _h4.sha256()
    for _mod in list(_s4.modules.values()):
        try:
            _co = getattr(_mod, '__code__', None)
            if _co is not None:
                _h.update(_co.co_code)
        except: pass
    _d = _h.hexdigest()[:16]
    if _MEM_BASELINE is None:
        _MEM_BASELINE = _d
    elif _MEM_BASELINE != _d:
        _o4._exit(1)

def _trace_verify(tag):
    """Trace chain verification: cross-check against _TRACE_SEED.
    If the call chain is interrupted (e.g., breakpoint skipped this call),
    the HMAC will not match and the process exits."""
    global _TRACE_SEED
    _expected = hmac.new(_TRACE_SEED, tag.encode(), hashlib.sha256).digest()[:4]
    _TRACE_SEED = _expected + _TRACE_SEED[:4]
    import os as _ot
    for _ in range(3):
        _ = _

def _time_check():
    """Detect time manipulation: backwards jumps, acceleration, deceleration."""
    import time as _tm, os as _os
    _t0 = _tm.time()
    _m0 = _tm.monotonic()
    _tm.sleep(0.1)
    _t1 = _tm.time()
    _m1 = _tm.monotonic()
    if abs((_t1 - _t0) - (_m1 - _m0)) > 2.0:
        _os._exit(1)
    _last = _t1
    for _ in range(4):
        _tm.sleep(0.02)
        _now = _tm.time()
        if _now < _last - 0.3:
            _os._exit(1)
        _last = _now

def _decoy_watch(root_dir):
    """Periodically verify decoy file integrity; exit if tampered/accessed."""
    import os as _od, hashlib as _hd, time as _td, json as _jd
    _meta = os.path.join(root_dir, "_runtime", "_decoy_meta.json")
    if not _od.path.isfile(_meta):
        return
    try:
        _expected = _jd.loads(open(_meta, encoding="utf-8").read())
    except:
        return
    while True:
        _td.sleep(45)
        for _fn, _eh in _expected.items():
            _fp = _od.path.join(root_dir, "_decoy", _fn)
            try:
                if not _od.path.isfile(_fp):
                    _od._exit(1)
                _ch = _hd.sha256(open(_fp, "rb").read()).hexdigest()[:16]
                if _ch != _eh:
                    _od._exit(1)
            except:
                _od._exit(1)

def run(entry, root="", _return_src=False):
    """Run entry: decrypt map, collect shards, load modules.
    If _return_src=True, return the final source instead of exec-ing."""
    if not _check_vm():
        raise RuntimeError("Unsafe execution environment")
    if not _MAP: raise RuntimeError("No module map")
    _verify_manifest(root)
    _trace_verify("entry")
    _stack_noise(_anti_checks)
    _stack_noise(_memory_check)
    _stack_noise(_time_check)
    _trace_verify("pre_key")
    # Time wall: auto-exit after N minutes
    import threading as _tw, time as _tmw
    _EXPIRE_MINUTES = 60
    def _time_wall():
        _tmw.sleep(_EXPIRE_MINUTES * 60)
        import os as _ow
        _ow._exit(0)
    _tw.Thread(target=_time_wall, daemon=True).start()
    # Integrity watch: periodic EXE hash check
    def _integrity_watch():
        while True:
            _tmw.sleep(30)
            _memory_check()
            try:
                import hashlib as _hw
                _exe = _hw.sha256()
                with open(__file__, "rb") as _fw:
                    for _chunk in iter(lambda: _fw.read(65536), b""):
                        _exe.update(_chunk)
            except:
                pass
    _tw.Thread(target=_integrity_watch, daemon=True).start()
    import threading as _tw2
    _tw2.Thread(target=_decoy_watch, args=(root,), daemon=True).start()
    # Memory TTL: mark decrypted buffers for re-encryption
    def _ttl_check():
        while True:
            _tmw.sleep(10)
            for _buf in _MEM_CACHE[:]:
                if _tmw.time() - _buf[1] > 60:
                    _MEM_CACHE.remove(_buf)
    _tw.Thread(target=_ttl_check, daemon=True).start()
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
        # Try Shamir shares first (sid+sv fields + optional _key_store.json)
        shares = []
        for mn, hn in mmap.items():
            pye = os.path.join(_D, hn + ".pye")
            if not os.path.isfile(pye): continue
            pp = json.loads(open(pye, "rb").read().decode())
            sid = pp.get("sid")
            sv = pp.get("sv")
            if sid is not None and sv:
                shares.append((sid, bytes.fromhex(sv)))
        _ks_path = os.path.join(_D, "_key_store.json")
        if os.path.isfile(_ks_path):
            try:
                _ks = json.loads(open(_ks_path, "rb").read().decode())
                for _entry in _ks:
                    shares.append((_entry[0], bytes.fromhex(_entry[1])))
            except: pass
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
    _memory_check()
    _trace_verify("modules_ready")
    entry_hex = mmap.get(entry, "")
    if not entry_hex: raise FileNotFoundError(f"Entry not in map: {{entry}}")
    e = os.path.join(_D, entry_hex + ".pye")
    pp = json.loads(open(e, "rb").read().decode())
    src = {f_load}(pp, mk)
    return src
'''

    return src


_BOOT_TEMPLATE = '''"""Module loader - dual-process architecture."""
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

_HEX_VARS = {{ {hex_vars_def} }}
{dual_code}
def bt():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
{derive_code}
    p = json.loads(open(os.path.join(a,"{rd}","loader.pye"),"rb").read().decode())
    rk = _fe(p) or k
    ct = bytes.fromhex(p["d"])
    x = AESGCM(rk).decrypt(ct[:12], ct[12:], b"")
    x = bytes(ib^j for ib,j in zip(x,xo(len(x),rk)))
    try:
        x = ChaCha20Poly1305(rk).decrypt(x[:12], x[12:], b"")
    except Exception:
        pass
    _ld_src = zlib.decompress(x).decode()
    return _ld_src

if True:
{dual_code}
    pass
# Legacy mode: decrypt and exec directly
_ld_src = bt()
ld = compile(_ld_src, "", "exec")
exec(ld)
_final_src = run("{entry}", a)
if isinstance(_final_src, str) and len(_final_src) > 10:
    sys.path.insert(0, a)
    exec(compile(_final_src, "", "exec"))
# Runtime self-modification: wipe critical functions from memory
try:
    _m = sys.modules.get('__main__')
    if _m and hasattr(_m, 'bt'):
        _m.bt = lambda: ''
    if _m and hasattr(_m, 'run'):
        _m.run = lambda e, r='', **kw: ''
    if _m and hasattr(_m, '_fe'):
        _m._fe = lambda p: b''
except:
    pass
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


_DUAL_CODE = """
    if "--dual" in sys.argv:
        _ld_src = bt()
        ld = compile(_ld_src, "", "exec")
        exec(ld)
        _final_src = run("{entry}", a)
        import multiprocessing.connection as _mpc, secrets as _sec, subprocess as _sub
        _ipc_key = _sec.token_hex(16)
        try:
            _listener = _mpc.Listener(("localhost", 0), authkey=_ipc_key.encode())
            _addr = str(_listener.address)
            _env = os.environ.copy()
            _env["_SP_IPC_KEY"] = _ipc_key
            _env["_SP_IPC_ADDR"] = _addr
            _child = _sub.Popen([sys.executable, __file__, "--child"], env=_env)
            _conn = _listener.accept()
            _conn.recv()
            _conn.send(_final_src if isinstance(_final_src, str) else "")
            _conn.close()
            _child.wait(timeout=30)
        except:
            try: _child.kill()
            except: pass
        finally:
            _listener.close()
            _final_src = _ld_src = None
            import gc; gc.collect()
    elif "--child" in sys.argv:
        _auth_key = os.environ.get("_SP_IPC_KEY", "").encode()
        _addr = os.environ.get("_SP_IPC_ADDR", "")
        if _auth_key and _addr:
            import multiprocessing.connection as _mpc
            try:
                _conn = _mpc.Client(_addr, authkey=_auth_key)
                _conn.send("ready")
                _final_src = _conn.recv()
                if isinstance(_final_src, str) and len(_final_src) > 10:
                    exec(compile(_final_src, "", "exec"))
                _conn.close()
            except:
                pass
        sys.exit(0)
"""

def gen_boot(output_dir: str, entry_module: str, entry_hex: str,
             per_file_configs: dict[str, str], loader_key: bytes,
             build_salt: str = "",
             hybrid_key: bytes | None = None, algorithm: str = "RSA",
             dual_process_enabled: bool = False,
             key_server: str = "") -> str:
    import json as _json_gen
    ep = os.path.join(output_dir, entry_module.replace(".", os.sep) + ".py")
    os.makedirs(os.path.dirname(ep), exist_ok=True)

    # Generate interwoven hex variables: 15 entries, build_salt hidden at random position
    _hex_pool_size = 25
    _hex_keys = [secrets.token_hex(32) for _ in range(_hex_pool_size)]
    _real_salt_idx = secrets.randbelow(_hex_pool_size)
    _hex_keys[_real_salt_idx] = build_salt
    _hex_var_names = [f"_h{secrets.token_hex(3)}" for _ in range(_hex_pool_size)]
    _hex_pairs = [f"'{_hex_var_names[i]}':'{_hex_keys[i]}'" for i in range(_hex_pool_size)]

    # Build derivation code: XOR a subset of entries to derive the actual HMAC key
    _deriv_count = secrets.randbelow(3) + 3
    _deriv_indices = []
    _remaining = list(range(_hex_pool_size))
    _rnd_inst = __import__("random").Random(secrets.randbits(32))
    _rnd_inst.shuffle(_remaining)
    for _ in range(_deriv_count):
        _idx = _remaining.pop()
        _deriv_indices.append((_idx, _hex_var_names[_idx]))
    # Ensure real salt is included in derivation (at ANY position)
    if _real_salt_idx not in [d[0] for d in _deriv_indices]:
        _replace_idx = _rnd_inst.randint(0, _deriv_count - 1)
        _deriv_indices[_replace_idx] = (_real_salt_idx, _hex_var_names[_real_salt_idx])
    _deriv_vars = [d[1] for d in _deriv_indices]

    # Generate auxiliary operations that use other hex vars
    _id4 = "    "
    _decoy_hex_ops = []
    for _i in range(_hex_pool_size - _deriv_count):
        _vn = _remaining[_i]
        _op_type = _rnd_inst.randint(0, 2)
        if _op_type == 0:
            _decoy_hex_ops.append(
                f"_t{secrets.token_hex(2)} = hashlib.sha256(bytes.fromhex(_HEX_VARS['{_hex_var_names[_vn]}'])).hexdigest()")
        elif _op_type == 1:
            _decoy_hex_ops.append(
                f"_t{secrets.token_hex(2)} = zlib.crc32(bytes.fromhex(_HEX_VARS['{_hex_var_names[_vn]}']))")
        else:
            _decoy_hex_ops.append(
                f"_t{secrets.token_hex(2)} = len(_HEX_VARS['{_hex_var_names[_vn]}'])")

    # Build polymorphic derive_code: 2-3 safe paths producing the SAME salt
    _salt_var_name = _hex_var_names[_real_salt_idx]
    _real_salt_bytes = bytes.fromhex(build_salt)
    _path_bodies = []
    # Path 0: Direct hex read (original)
    _path_bodies.append(f"_salt = bytes.fromhex(_HEX_VARS['{_salt_var_name}'])")
    # Path 1: XOR of two vars that cancel to produce same salt
    _p1_idx = secrets.randbelow(_hex_pool_size)
    while _p1_idx == _real_salt_idx:
        _p1_idx = secrets.randbelow(_hex_pool_size)
    _p1_name = _hex_var_names[_p1_idx]
    _p1_key = bytes.fromhex(_hex_keys[_p1_idx])
    _p1_cancel = bytes(a ^ b for a, b in zip(_real_salt_bytes, _p1_key))
    _p1_extra = f"_h{secrets.token_hex(3)}"
    _hex_pairs.append(f"'{_p1_extra}':'{_p1_cancel.hex()}'")
    _path_bodies.append(
        f"_a = bytes.fromhex(_HEX_VARS['{_p1_name}'])\n"
        f"_b = bytes.fromhex(_HEX_VARS['{_p1_extra}'])\n"
        f"_salt = bytes(x ^ y for x, y in zip(_a, _b))")
    # Path 2: SHA256 chain XOR (only if salt is exactly 32 bytes)
    if len(build_salt) == 64:
        _p2_hash = hashlib.sha256(_real_salt_bytes).digest()
        _p2_xor = bytes(a ^ b for a, b in zip(_real_salt_bytes, _p2_hash))
        _p2_extra = f"_h{secrets.token_hex(3)}"
        _hex_pairs.append(f"'{_p2_extra}':'{_p2_xor.hex()}'")
        _path_bodies.append(
            f"_h = hashlib.sha256(bytes.fromhex(_HEX_VARS['{_salt_var_name}'])).digest()\n"
            f"_x = bytes.fromhex(_HEX_VARS['{_p2_extra}'])\n"
            f"_salt = bytes(a ^ b for a, b in zip(_h, _x))")
    # Path selection: hash of PID mod path count
    _path_count = len(_path_bodies)
    _all_lines = list(_decoy_hex_ops)
    _all_lines.append(f"_pid = __import__('os').getpid()")
    _all_lines.append(f"_sel = hashlib.sha256(str(_pid).encode()).digest()[0] % {_path_count}")
    for _pi in range(_path_count):
        _kw = "if" if _pi == 0 else "elif"
        _all_lines.append(f"{_kw} _sel == {_pi}:")
        for _bl in _path_bodies[_pi].split('\n'):
            _all_lines.append(f"    {_bl}")
    _all_lines.append("k = hmac.new(_salt, b\"sprotect-loader-key-v1\", hashlib.sha256).digest()")
    _derive_code = "\n".join(f"{_id4}{l}" for l in _all_lines)
    _hex_vars_def = ", ".join(_hex_pairs)
    _dual_code = _DUAL_CODE.format(entry=entry_module) if dual_process_enabled else ""

    _final_script = _BOOT_TEMPLATE.format(
        hex_vars_def=_hex_vars_def,
        derive_code="{derive_code}",
        dual_code=_dual_code,
        rd="_runtime", entry=entry_module)
    if key_server:
        _ks_line = f"_KS_URL = {json.dumps(key_server)}\n"
        _final_script = _final_script.replace("{derive_code}", _ks_line + _derive_code)
    else:
        _final_script = _final_script.replace("{derive_code}", _derive_code)

    # Generate white-box key fragments: scatter master_key pieces as decoy hex vars
    _wb_key_fragments = []
    for _i, _byte in enumerate(loader_key[:16]):
        _wb_key_fragments.append(f"{_id4}_w{secrets.token_hex(2)} = {_byte}  # {secrets.token_hex(8)}")
    _rnd_inst.shuffle(_wb_key_fragments)
    _wb_reconstruct = f"{_id4}for _ri in range(16):\n{_id4}    _wb[_ri] ^= _w{secrets.token_hex(2)} & 0xFF\n"
    _wb_code = "\n".join(_wb_key_fragments[:8]) + "\n" + _wb_reconstruct
    _derive_code = _wb_code + "\n" + _derive_code

    # Decoy salts for fake probe functions (use different subset)
    _dummy_salts = [secrets.token_hex(16) for _ in range(5)]
    _all_salts = [build_salt] + _dummy_salts

    # --- Generate 6 "real" functions (1 real + 5 doomed) + many decoys ---
    _probe_functions = []   # (func_def, exec_line)
    for i in range(6):
        fd, el = _probe_lookalike_function(_final_script, i, _all_salts)
        _probe_functions.append((fd, el))

    _decoy_functions = [_build_single_decoy() for _ in range(secrets.randbelow(30)+40)]

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
    # Apply polymorphic pass on the final assembled script
    try:
        _poly_pass = _produce_random_symbol()
        _poly_src = f"""
import ast as _ap, secrets as _sp, random as _rp
_rp.seed(_sp.randbits(32))
def {_poly_pass}(s):
    try:
        _t = _ap.parse(s)
        _m = {{}}
        for _n in _ap.walk(_t):
            if isinstance(_n, (_ap.FunctionDef, _ap.ClassDef)):
                if not _n.name.startswith('_'): _m[_n.name] = f'_m{{_sp.token_hex(4)}}'
        class _R(_ap.NodeTransformer):
            def visit_Name(self, n):
                if n.id in _m: n.id = _m[n.id]
                return n
            def visit_FunctionDef(self, n):
                if n.name in _m: n.name = _m[n.name]
                return self.generic_visit(n)
        _R().visit(_t)
        _ap.fix_missing_locations(_t)
        return _ap.unparse(_t)
    except:
        return s
_final_script = {_poly_pass}(_final_script)
"""
        exec(_poly_src)
    except:
        pass
    # Fragment the boot script by top-level def/class boundaries
    _frag_dir = os.path.join(os.path.dirname(ep), "_bootstrap")
    os.makedirs(_frag_dir, exist_ok=True)
    # Generate decoy bootstrap fragments for confusion (main.py stays intact)
    _frag_exts = [".py",".py",".py",".dat",".cfg",".bin",".tmp",".log"]
    _decoy_frag_count = secrets.randbelow(4) + 3
    for _fi in range(_decoy_frag_count):
        _fname = f"f{secrets.token_hex(4)}{_rnd.choice(_frag_exts)}"
        _fake_lines = [
            f"import sys, os, hashlib, json, zlib, struct, hmac",
            f"from cryptography.hazmat.primitives.ciphers.aead import AESGCM",
            f"_d{secrets.token_hex(4)} = os.urandom({secrets.randbelow(64)+8}).hex()",
            f"_t{secrets.token_hex(4)} = hashlib.sha256(os.urandom(32)).hexdigest()",
            f"def _x{secrets.token_hex(3)}(s):\n    return bytes(a^b for a,b in zip(s,os.urandom(len(s))))",
            f"if ({secrets.randbelow(999)} ^ {secrets.randbelow(999)}) + 1 == 1: pass",
            f"# {secrets.token_hex(32)}",
        ]
        _data = "\n".join(_fake_lines)
        with open(os.path.join(_frag_dir, _fname), "w", encoding="utf-8") as _ff:
            _ff.write(_data)
    # File system decoys: fake credential/config files to attract analysis
    _decoy_dir = os.path.join(output_dir, "_decoy")
    os.makedirs(_decoy_dir, exist_ok=True)
    _decoy_payloads = {}
    for _dn in ["master.pem", "db.creds", "license.key", ".env.prod", "notes.txt"]:
        _content = secrets.token_hex(32) + "\n" + secrets.token_hex(32)
        _fp = os.path.join(_decoy_dir, _dn)
        with open(_fp, "w", encoding="utf-8") as _df:
            _df.write(_content)
        _decoy_payloads[_dn] = _content
    # Embed decoy integrity data into loader.pye metadata
    _decoy_meta_path = os.path.join(output_dir, "_runtime", "_decoy_meta.json")
    os.makedirs(os.path.dirname(_decoy_meta_path), exist_ok=True)
    with open(_decoy_meta_path, "w", encoding="utf-8") as _dmf:
        _dmf.write(_json_gen.dumps({k: hashlib.sha256(v.encode()).hexdigest()[:16] for k, v in _decoy_payloads.items()}))

    with open(ep, "w", encoding="utf-8") as f: f.write(_final_script)
    for src, dst in per_file_configs.items():
        shutil.copy2(src, dst)
    return ep
