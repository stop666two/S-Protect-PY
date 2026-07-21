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
    """Generate the runtime loader source with ALL random names and varying structure."""
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
try: _SD = os.path.dirname(os.path.abspath(__file__))
except: _SD = os.path.dirname(os.path.abspath(sys.argv[0])) if sys.argv else "."
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
            f2_ok = hashlib.sha256(kv).hexdigest()[3:11] == p.get("f2", "")
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
    """Full decrypt: AES-GCM then XOR then ChaCha20 then zlib."""
    ct = bytes.fromhex(p["d"])
    hdr = p.get("h", "")
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    x = AESGCM(mk).decrypt(ct[:12], ct[12:], b"")
    ks = {f_xof}(len(x), hashlib.sha256(mk).digest())
    x = bytes(a^b for a,b in zip(x,ks))
    try:
        x = ChaCha20Poly1305(mk).decrypt(x[:12], x[12:], b"")
    except Exception:
        pass
    if hdr:
        x = {f_extra}(x, mk, hdr)
    return zlib.decompress(x).decode()

def {f_extra}(ct, mk, hdr):
    import json, hashlib
    try:
        h = json.loads(hdr) if isinstance(hdr, str) else {{}}
    except:
        return ct
    for algo in reversed(h.get("extra_layers", [])):
        info = h["layer_ivs"].get(algo, {{}})
        iv = bytes.fromhex(info.get("iv", ""))
        salt = bytes.fromhex(info.get("salt", ""))
        lk = hashlib.pbkdf2_hmac("sha256", mk, salt, 1, 32)
        if algo == "serpent" or algo == "twofish" or algo == "camellia":
            mod = __import__("Cryptodome.Cipher", fromlist=[algo.capitalize()])
            cls = getattr(mod, algo.capitalize())
            c = cls.new(lk, cls.MODE_CBC, iv=iv[:16])
            ct = c.decrypt(ct)[:-ct[-1]]
        elif algo == "salsa20":
            mod = __import__("Cryptodome.Cipher", fromlist=["Salsa20"])
            c = mod.Salsa20.new(key=lk, nonce=iv[:8])
            ct = c.decrypt(ct)
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

def run(entry, root=""):
    """Run entry: decrypt map, collect shards, load modules."""
    if not _MAP: raise RuntimeError("No module map")
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


_BOOT_STUB = '''"""S-Protect bootloader v7."""
import sys, os, json, hashlib, zlib
_R = os.path.dirname(os.path.abspath(__file__))

def _xof(l, s):
    r, c = bytearray(), 0
    while len(r) < l:
        r.extend(hashlib.sha256(s + c.to_bytes(4,"big")).digest()); c += 1
    return bytes(r[:l])

def _boot(key):
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    p = json.loads(open(os.path.join(_R,"{rd}","loader.pye"),"rb").read().decode())
    real = key
    for kn in ["k1","k2","k3","k4","k5"]:
        if kn in p:
            v = bytes.fromhex(p[kn])
            kh = hashlib.sha256(v).digest()[:4].hex()
            if kh == p.get("f1","")[:8] or kh == p.get("f2","")[:8] or kh == p.get("f3","")[:8]:
                real = v; break
    ct = bytes.fromhex(p["d"])
    x = AESGCM(real).decrypt(ct[:12], ct[12:], b"")
    x = bytes(a^b for a,b in zip(x,_xof(len(x),real)))
    try:
        x = ChaCha20Poly1305(real).decrypt(x[:12], x[12:], b"")
    except Exception:
        pass
    return zlib.decompress(x).decode()

_ld = compile(_boot(bytes.fromhex("{lk}")), "", "exec")
exec(_ld)
run("{entry}", _R)
'''


_HYBRID_BOOT_STUB = '''"""S-Protect bootloader v7 (hybrid)."""
import sys, os, json, hashlib, zlib
_R = os.path.dirname(os.path.abspath(__file__))

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


def gen_boot(output_dir: str, entry_module: str, entry_hex: str,
             per_file_configs: dict[str, str], loader_key: bytes,
             hybrid_key: bytes | None = None, algorithm: str = "RSA") -> str:
    ep = os.path.join(output_dir, entry_module.replace(".", os.sep) + ".py")
    os.makedirs(os.path.dirname(ep), exist_ok=True)
    if hybrid_key is not None:
        boot = _HYBRID_BOOT_STUB.format(
            rd="_runtime", entry=entry_module,
            hk=hybrid_key.hex(), ha=algorithm, kp="sprotect_private.pem")
    else:
        boot = _BOOT_STUB.format(lk=loader_key.hex(), rd="_runtime", entry=entry_module)
    from sprotect.minify import minify_source
    boot = minify_source(boot, add_garbage=True)
    with open(ep, "w", encoding="utf-8") as f: f.write(boot)
    for src, dst in per_file_configs.items():
        shutil.copy2(src, dst)
    return ep
