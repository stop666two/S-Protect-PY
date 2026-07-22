"""Bootloader + runtime loader v7: random names, external crypto, PyArmor integration."""

from __future__ import annotations
import os, shutil, secrets, hashlib

def _rand_name() -> str:
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


def _randomized_source(source: str) -> str:
    """Replace all meaningful identifiers in the source with random names.
    Scans for Python identifiers and replaces them."""
    import re
    # Find all function def names, class names, and global variable assignments
    replacements = {}
    # Function defs
    for m in re.finditer(r'^def (\w+)\(', source, re.MULTILINE):
        name = m.group(1)
        if name not in replacements and not name.startswith("__"):
            replacements[name] = _rand_name()
    # Class defs
    for m in re.finditer(r'^class (\w+)', source, re.MULTILINE):
        name = m.group(1)
        if name not in replacements and not name.startswith("__"):
            replacements[name] = _rand_name()
    # Apply replacements (longest first to avoid partial matches)
    for old, new in sorted(replacements.items(), key=lambda x: -len(x[0])):
        source = re.sub(r'\b' + re.escape(old) + r'\b', new, source)
    return source


def _gen_decrypt_func(num: int) -> str:
    """Generate a random-looking decryption function.
    Each call produces different code structure."""
    import random
    r = random.Random(secrets.randbits(32))
    fname = _rand_name()
    body = []
    body.append(f"    import json, hashlib, zlib")
    body.append(f"    from cryptography.hazmat.primitives.ciphers.aead import AESGCM")
    body.append(f"    p = json.loads(open(path, 'rb').read().decode())")
    body.append(f"    ct = bytes.fromhex(p['d'])")
    body.append(f"    k = bytes.fromhex(p['k{r.randint(1,3)}'])")
    # Insert random decoy operations
    for _ in range(r.randint(1, 3)):
        vn = _rand_name()
        body.append(f"    {vn} = hashlib.sha256(k).hexdigest()[:{r.randint(4,12)}]")
    # Varying decrypt approaches
    approaches = [
        f"    x = AESGCM(k).decrypt(ct[:12], ct[12:], b'')",
        f"    nonce = ct[:12]\n    tag_ct = ct[12:]\n    x = AESGCM(k).decrypt(nonce, tag_ct, b'')",
    ]
    body.append(secrets.choice(approaches))
    # Optional ChaCha20 layer
    if r.random() < 0.4:
        body.append(f"    from Cryptodome.Cipher import ChaCha20_Poly1305")
        body.append(f"    c20 = ChaCha20_Poly1305.new(key=k, nonce=x[:12])")
        body.append(f"    x = c20.decrypt(x[12:28], x[28:])")
    # XOR step with varying implementations
    xor_variants = [
        f"    return zlib.decompress(bytes(a^b for a,b in zip(x,_xof(len(x),k)))).decode()",
        f"    ks = _xof(len(x), k)\n    return zlib.decompress(bytes(i^j for i,j in zip(x,ks))).decode()",
        f"    r = bytearray()\n    for i in range(len(x)):\n        r.append(x[i] ^ _xof(1, k + i.to_bytes(4,'big'))[0])\n    return zlib.decompress(bytes(r)).decode()",
    ]
    body.append(secrets.choice(xor_variants))

    return f"def {fname}(path):\n" + "\n".join(body) + "\n\n"


def gen_loader_source() -> str:
    """Generate the runtime loader source with randomized names and structure."""
    import secrets as _sec, random as _rnd
    _rnd.seed(_sec.randbits(32))

    f_xof = _rand_name()
    f_load = _rand_name()
    f_find = _rand_name()
    f_filter = _rand_name()
    f_extract = _rand_name()
    f_run = "run"
    f_extra = _rand_name()
    cls_L = _rand_name()
    cls_F = _rand_name()

    # Build the loader source with random names
    src = f'''"""Runtime v7 - auto-generated, randomized structure."""
import sys, os, json, hmac, hashlib, zlib, importlib.abc, importlib.machinery
sys.dont_write_bytecode = True
try:
    import locale; _enc = locale.getpreferredencoding() or "utf-8"
except: _enc = "utf-8"
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding=_enc, errors="replace")
    sys.stderr.reconfigure(encoding=_enc, errors="replace")
try: _SD = getattr(sys, '_MEIPASS', None) or os.path.dirname(os.path.abspath(__file__))
except: _SD = getattr(sys, '_MEIPASS', None) or (os.path.dirname(os.path.abspath(sys.argv[0])) if sys.argv else ".")
_D = os.path.join(_SD, "_runtime") if os.path.isdir(os.path.join(_SD, "_runtime")) else _SD
_MAP = ""

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
    """Full decrypt: extra layers → AES-GCM → XOR → ChaCha20 → zlib."""
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
class {_rand_name()}:
    """Decoy class - looks like a real loader component."""
    def __init__(self): pass
    def {_rand_name()}(self): return None

'''

    # Add random decoy functions
    for _ in range(_rnd.randint(2, 5)):
        src += _gen_decrypt_func(_)

    # Add the real loader class
    load_func = _rand_name()
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

def run(entry, root=""):
    """Run entry: decrypt map, collect shards, load modules."""
    if not _MAP: raise RuntimeError("No module map")
    _verify_manifest(root)
    mmap = json.loads(_MAP)
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
    exec(compile(src, e, "exec"), {{"__name__":"__main__","__file__":fm}})
'''

    return src


_BOOT_STUB = '''"""Module loader."""
import sys, os, json, hashlib, zlib, hmac
sys.dont_write_bytecode = True
try:
    import locale; _enc = locale.getpreferredencoding() or "utf-8"
except: _enc = "utf-8"
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding=_enc, errors="replace")
    sys.stderr.reconfigure(encoding=_enc, errors="replace")
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

LIST = {lk_list}
def bt():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    k = bytes.fromhex("".join(LIST[i] for i in [{lk_idx}]))
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


_HYBRID_BOOT_STUB = '''"""Hybrid loader."""
import sys, os, json, hashlib, zlib
sys.dont_write_bytecode = True
try:
    import locale; _enc = locale.getpreferredencoding() or "utf-8"
except: _enc = "utf-8"
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding=_enc, errors="replace")
    sys.stderr.reconfigure(encoding=_enc, errors="replace")
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


def _rand_hex(n: int) -> str:
    return secrets.token_hex(n)


def _rand_comment() -> str:
    """Generate a random-looking comment line."""
    return secrets.choice([
        f"# TODO: {_rand_hex(16)}",
        f"# FIXME: {secrets.choice(['refactor','cleanup','optimize','verify'])} {_rand_hex(8)}",
        f"# HACK: {_rand_hex(24)}",
        f"# XXX: {secrets.choice(['incomplete','untested','deprecated','workaround'])}",
        f"# NOTE: {_rand_hex(32)}",
        f"# BUG: {_rand_hex(16)}",
        f"# SECURITY: {_rand_hex(24)}",
        f"# PERFORMANCE: {_rand_hex(20)}",
    ])


def _sprotect_fake() -> str:
    """Generate a fake S-Protect-like string."""
    return secrets.choice([
        f'"""S-Protect loader v{secrets.randbelow(5)+1}.{secrets.randbelow(10)}."""',
        f'# S-Protect {secrets.token_hex(8)}',
        f'# SProtect {_rand_hex(8)}',
        f'"""Loader v{secrets.randbelow(5)+1}.{secrets.randbelow(10)}."""',
    ])

def _gen_one_decoy_func(name: str | None = None) -> str:
    """Generate a single structurally randomized decoy decryption function."""
    fn = _rand_name()
    fake_key = _rand_hex(secrets.randbelow(16) + 32)
    fake_ct = _rand_hex(secrets.randbelow(100) + 50)
    fake_h = _rand_hex(4)

    # Randomly choose which crypto steps to include and in what order
    steps = []
    steps.append(f"        _k = bytes.fromhex('{fake_key}')")
    steps.append(f"        _d = bytes.fromhex('{fake_ct}')")

    if secrets.randbelow(3) > 0:
        steps.append(f"        _x = AESGCM(_k).decrypt(_d[:12], _d[12:], b'')")
    else:
        steps.append(f"        _c = Cipher(algorithms.AES(_k), modes.CTR(_d[:16])).decryptor()")
        steps.append(f"        _x = _c.update(_d[16:]) + _c.finalize()")

    if secrets.randbelow(2) == 0:
        steps.append(f"        _x = bytes(ib^j for ib,j in zip(_x, hashlib.sha256(_k).digest()*99))[:_x]")

    if secrets.randbelow(3) > 0:
        steps.append(f"        _x = ChaCha20Poly1305(_k).decrypt(_x[:12], _x[12:], b'')")

    if secrets.randbelow(2) == 0:
        steps.append(f"        _x = bytes(ib^j for ib,j in zip(_x, _k*99))[:len(_x)]")

    if secrets.randbelow(2) == 0:
        steps.append(f"        if hashlib.sha256(_x[:16]).hexdigest()[:8] != '{_rand_hex(4)}':")
        steps.append(f"            _x = _x[::-1]")

    if secrets.randbelow(2) == 0:
        steps.append(f"        _crc = zlib.crc32(_x) & 0x{_rand_hex(4)}")

    steps.append(f"        _r = zlib.decompress(_x)")

    try_lines = "\n".join(steps)
    has_args = name is None  # no args when called from sections
    if has_args:
        args = secrets.choice(
            ["key", "data", "path", "sig", "buf"] +
            ["key, iv", "data, offset", "path, mode", "sig, expected"])
    else:
        args = ""
    actual_fn = name or fn
    return (
        f"{_rand_comment()}\n"
        f"{_sprotect_fake()}\n"
        f"# {secrets.token_hex(secrets.randbelow(8)+8)}\n"
        f"def {actual_fn}({args}):\n"
        f"    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305\n"
        f"    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes\n"
        f"    import hashlib, json, os, zlib\n"
        f"    try:\n"
        f"{try_lines}\n"
        f"    except Exception as _{_rand_name()}:\n"
        f"        _r = b''\n"
        f"    return _r\n"
    )


def _gen_decoy_boot_like(count: int) -> str:
    """Generate structurally varied decoy functions."""
    return "\n".join(_gen_one_decoy_func() for _ in range(count))


def _gen_massive_padding(target_kb: int = 55) -> str:
    """Generate varied padding with comments, strings, fake logic."""
    lines = []
    size = 0
    comment_types = [
        lambda: f"# {secrets.choice(['TODO','FIXME','HACK','XXX','BUG','NOTE','XXX','SECURITY','PERF'])}: {_rand_hex(secrets.randbelow(40)+10)}",
        lambda: f"# {secrets.choice(['refactor','review','optimize','verify','test','cleanup'])} {_rand_hex(16)}",
        lambda: f"# v{secrets.randbelow(10)}.{secrets.randbelow(99)}.{secrets.randbelow(999)} - {_rand_hex(20)}",
        lambda: f"# Copyright (c) 202{secrets.randbelow(6)} {_rand_hex(16)}",
        lambda: f"# License: {secrets.choice(['MIT','Apache-2.0','GPL-3.0','BSD','Proprietary'])}",
        lambda: f"# {secrets.choice(['DEPRECATED','UNUSED','LEGACY','EXPERIMENTAL'])}: {_rand_hex(12)}",
        lambda: f"# {secrets.choice(['assert','ensure','check','validate'])} {_rand_hex(16)}",
        lambda: f"# type: ignore[{_rand_hex(8)}]",
        lambda: f"# pragma: {secrets.choice(['no cover','no mutate','skip CI'])}",
    ]
    while size < target_kb * 1024:
        block = "\n".join(
            secrets.choice(comment_types)()
            for _ in range(secrets.randbelow(15) + 8)
        )
        block += f"\n_{_rand_name()} = {secrets.choice([
            f"'{_rand_hex(secrets.randbelow(200)+100)}'",
            f"b'{_rand_hex(secrets.randbelow(100)+50)}'",
            f"0x{_rand_hex(secrets.randbelow(8)+2)}",
            str(secrets.randbelow(2**32)),
        ])}\n"
        lines.append(block)
        size += len(block) + 1
    return "\n".join(lines)


_gen_fake_imports_large = """import sys, os, json, re, math, hashlib, base64, struct, zlib
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


def _gen_fake_real_func(real_bt_template: str, idx: int, all_frags, frag_list_code) -> tuple[str, str]:
    """Generate one realistic-looking function + its exec call.
    Returns (function_def, exec_line). Only one (idx 0) is the truly real one."""
    fn = _rand_name()
    if idx == 0:
        # The ONE real function - uses the REAL bt template unmodified
        body_start = real_bt_template.index("def bt():") + len("def bt():")
        real_body = real_bt_template[body_start:]
        real_body = real_body.replace("bt", fn)
        func_def = f"def {fn}():{real_body}"
        # Real exec line - no try/except (just like original)
        exec_line = f"_e = compile({fn}(), '', 'exec')\nexec(_e)"
    else:
        # Fake "real" function - looks identical but will fail
        # Copy the structure but inject wrong key indices
        fake_idx_list = ", ".join(
            str(secrets.randbelow(len(all_frags))) for _ in range(secrets.randbelow(3)+3))
        func_def = f"""def {fn}():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    import hashlib, json, os, zlib, hmac
    try:
        k = bytes.fromhex("".join({frag_list_code}[i] for i in [{fake_idx_list}]))
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
            exec_line = f"""try:
    _e = compile({fn}(), '', 'exec')
    exec(_e)
except Exception:
    pass"""
        else:
            exec_line = f"_e = compile({fn}(), '', 'exec')\nexec(_e)"
    return func_def, exec_line


def gen_boot(output_dir: str, entry_module: str, entry_hex: str,
             per_file_configs: dict[str, str], loader_key: bytes,
             hybrid_key: bytes | None = None, algorithm: str = "RSA") -> str:
    ep = os.path.join(output_dir, entry_module.replace(".", os.sep) + ".py")
    os.makedirs(os.path.dirname(ep), exist_ok=True)

    # --- Scatter the loader key into fragments ---
    lk_hex = loader_key.hex()
    frag_count = secrets.randbelow(4) + 5
    real_frags = []
    for i in range(frag_count):
        start = (i * 64) // frag_count
        end = ((i + 1) * 64) // frag_count
        real_frags.append(lk_hex[start:end])

    fake_frags = [_rand_hex(len(f)) for f in real_frags]
    all_frags = real_frags + fake_frags
    real_indices = list(range(frag_count))

    frag_var_names = [_rand_name() for _ in range(len(all_frags))]
    frag_defs = "\n".join(f"{n} = '{v}'" for n, v in zip(frag_var_names, all_frags))
    frag_list_code = f"[{', '.join(frag_var_names)}]"

    real_idx_list = ", ".join(str(i) for i in real_indices)
    boot = _BOOT_STUB.format(
        lk_list=frag_list_code, lk_idx=real_idx_list,
        rd="_runtime", entry=entry_module)

    # --- Generate 6 "real" functions (1 real + 5 doomed) + many decoys ---
    six_funcs = []   # (func_def, exec_line)
    for i in range(6):
        fd, el = _gen_fake_real_func(boot, i, all_frags, frag_list_code)
        six_funcs.append((fd, el))

    decoy_funcs = [_gen_one_decoy_func() for _ in range(secrets.randbelow(15)+20)]

    # --- Create 6 sections, each with fake execs ABOVE and BELOW the real exec ---
    sections = []
    for si in range(6):
        # Generate 3-6 fake execs BEFORE the real exec
        pre_fakes = []
        for _ in range(secrets.randbelow(4) + 3):
            fn = _rand_name()
            decoy_funcs.append(_gen_one_decoy_func(fn))
            if secrets.randbelow(2) == 0:
                pre_fakes.append(f"_e = compile({fn}(), '', 'exec')\nexec(_e)")
            else:
                pre_fakes.append(f"try:\n    _e = compile({fn}(), '', 'exec')\n    exec(_e)\nexcept Exception:\n    pass")
        # Generate 3-6 fake execs AFTER the real exec
        post_fakes = []
        for _ in range(secrets.randbelow(4) + 3):
            fn = _rand_name()
            decoy_funcs.append(_gen_one_decoy_func(fn))
            if secrets.randbelow(2) == 0:
                post_fakes.append(f"_e = compile({fn}(), '', 'exec')\nexec(_e)")
            else:
                post_fakes.append(f"try:\n    _e = compile({fn}(), '', 'exec')\n    exec(_e)\nexcept Exception:\n    pass")

        section = "\n".join(pre_fakes) + "\n" + six_funcs[si][1] + "\n" + "\n".join(post_fakes)
        sections.append(section)

    # --- Assemble: ALL function defs FIRST, then ALL exec blocks ---
    padding = _gen_massive_padding(40)
    decoy_func_block = "\n\n".join(decoy_funcs)
    all_real_func_defs = "\n\n".join(fd for fd, el in six_funcs)

    sep = "ld = compile"
    if sep in boot:
        def_part, _ = boot.split(sep, 1)
    else:
        def_part = boot

    all_defs = (_gen_fake_imports_large + "\n\n" + padding + "\n\n" +
                frag_defs + "\n\n" + def_part + "\n\n" +
                all_real_func_defs + "\n\n" + decoy_func_block)

    import random as _rnd
    _rnd.seed(secrets.randbits(32))
    _rnd.shuffle(sections)
    all_execs = "\n\n".join(sections)

    boot = all_defs + "\n\n" + all_execs

    from sprotect.minify import minify_source
    boot = minify_source(boot, add_garbage=True)
    with open(ep, "w", encoding="utf-8") as f: f.write(boot)
    for src, dst in per_file_configs.items():
        shutil.copy2(src, dst)
    return ep
