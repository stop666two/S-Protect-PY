# Encryption Enhancement Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add optional extra encryption layers (Serpent, Twofish, Camellia, Salsa20) and hybrid RSA/ECC key wrapping to the S-Protect-PY build pipeline.

**Architecture:** Extra layers are inserted after AES-GCM in the existing zlib→ChaCha20→XOR→AES-GCM pipeline. Each extra layer derives its key from master_key via HKDF-SHA256 with domain-separated `info` strings. Hybrid encryption wraps master_key with RSA/OAEP at build time and unwraps at loader startup.

**Tech Stack:** Python 3.11+, `pycryptodome==3.21.0` (Serpent, Twofish, Camellia, Salsa20, RSA), `cryptography==44.0.0` (HKDF)

## Global Constraints

- `requirements.txt` must pin exact versions
- Import `Cryptodome.Cipher.*` for extra ciphers (not `Crypto`)
- `.pye` header v2 must be backward-compatible with v1 (no header = v1)
- All new config fields default to disabled/empty
- ECC hybrid uses ECIES (ECDH + AES-GCM), not raw ECC encryption
- No post-quantum algorithms (deferred)

---

### Task 1: Dataclasses + Dependency

**Files:**
- Modify: `sprotect/types.py`
- Modify: `requirements.txt`

**Interfaces:**
- Consumes: nothing (foundation task)
- Produces: `HybridEncryptConfig`, updated `EncryptConfig` with `extra_layers` and `hybrid` fields

- [ ] **Step 1: Update requirements.txt**

```txt
# requirements.txt
json5==0.9.14
cryptography==44.0.0
tqdm==4.67.1
colorama==0.4.6
pycryptodome==3.21.0
```

- [ ] **Step 2: Add dataclasses in types.py**

Insert after `EncryptConfig`:

```python
@dataclass
class HybridEncryptConfig:
    enabled: bool = False
    algorithm: str = "RSA"
    key_size: int = 4096
    key_file: str = "key.pem"

@dataclass
class EncryptConfig:
    algorithm: str = "aes-256-gcm"
    key_source: str = "auto"
    key_file: Optional[str] = None
    key_env_var: Optional[str] = None
    interdependency: InterdependencyMode = InterdependencyMode.CHAIN
    backup: bool = True
    backup_max_count: int = 5
    replace_originals: bool = False
    shard_count: int = 3
    shard_min_files: int = 2
    compress_level: int = 9
    polymorphic_padding: bool = True
    polymorphic_padding_max: int = 512
    aad_context: str = "S-Protect-PY"
    extra_layers: list[str] = field(default_factory=list)
    hybrid: HybridEncryptConfig = field(default_factory=HybridEncryptConfig)
```

- [ ] **Step 3: Verify no syntax errors**

```bash
python -c "compile(open('sprotect/types.py','rb').read(),'types.py','exec'); print('OK')"
```

Expected: `OK`

- [ ] **Step 4: Commit**

```bash
git add requirements.txt sprotect/types.py
git commit -m "feat: add pycryptodome dep and extra_layers/hybrid dataclasses"
```

---

### Task 2: HKDF Key Derivation

**Files:**
- Modify: `sprotect/crypto.py`

**Interfaces:**
- Consumes: nothing
- Produces: `derive_layer_key(master_key: bytes, info: str) -> tuple[bytes, bytes]`

- [ ] **Step 1: Write test**

Create `tests/test_crypto_extra.py`:

```python
from sprotect.crypto import derive_layer_key

def test_derive_layer_key_deterministic():
    mk = b"test_master_key_32_bytes_long!!"
    k1, s1 = derive_layer_key(mk, "sprotect:serpent")
    k2, s2 = derive_layer_key(mk, "sprotect:serpent")
    assert k1 == k2
    assert s1 == s2
    assert len(k1) == 32

def test_derive_layer_key_domain_sep():
    mk = b"test_master_key_32_bytes_long!!"
    k1, _ = derive_layer_key(mk, "sprotect:serpent")
    k2, _ = derive_layer_key(mk, "sprotect:twofish")
    assert k1 != k2
```

- [ ] **Step 2: Run test to verify it fails**

```bash
python -m pytest tests/test_crypto_extra.py -v 2>&1 | findstr "FAILED"
```

Expected: `FAILED` (ImportError)

- [ ] **Step 3: Implement derive_layer_key in crypto.py**

Add at top of `crypto.py` after existing imports:

```python
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes

def derive_layer_key(master_key: bytes, info: str) -> tuple[bytes, bytes]:
    salt = os.urandom(16)
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        info=info.encode(),
    )
    return hkdf.derive(master_key), salt
```

- [ ] **Step 4: Run test to verify it passes**

```bash
python -m pytest tests/test_crypto_extra.py -v 2>&1 | findstr "PASS"
```

Expected: `PASS`

- [ ] **Step 5: Commit**

```bash
git add sprotect/crypto.py tests/test_crypto_extra.py
git commit -m "feat: add HKDF-SHA256 derive_layer_key with domain separation"
```

---

### Task 3: Serpent Encrypt/Decrypt

**Files:**
- Create: `sprotect/crypto_extra.py`
- Test: `tests/test_crypto_extra.py`

**Interfaces:**
- Consumes: `derive_layer_key` from crypto.py
- Produces: `encrypt_serpent(data, key, iv)`, `decrypt_serpent(data, key, iv)`, `encrypt_twofish(...)`, etc.

- [ ] **Step 1: Write failing test**

Add to `tests/test_crypto_extra.py`:

```python
from sprotect.crypto_extra import encrypt_serpent, decrypt_serpent

def test_serpent_roundtrip():
    data = b"Hello Serpent AES!" * 100
    key = b"k" * 32
    iv = b"i" * 16
    ct = encrypt_serpent(data, key, iv)
    assert ct != data
    pt = decrypt_serpent(ct, key, iv)
    assert pt == data

def test_serpent_wrong_key():
    data = b"test data here!!"
    key = b"k" * 32
    iv = b"i" * 16
    ct = encrypt_serpent(data, key, iv)
    wrong = decrypt_serpent(ct, b"x" * 32, iv)
    assert wrong != data
```

- [ ] **Step 2: Run to verify failure**

```bash
python -m pytest tests/test_crypto_extra.py::test_serpent_roundtrip -v 2>&1 | findstr "FAILED"
```

Expected: `FAILED` (ImportError)

- [ ] **Step 3: Create crypto_extra.py**

```python
"""Extra encryption layers: Serpent, Twofish, Camellia, Salsa20."""

from __future__ import annotations
import os

try:
    from Cryptodome.Cipher import Serpent, Twofish, Camellia, Salsa20 as _Salsa20
    _HAS_CRYPTODOME = True
except ImportError:
    _HAS_CRYPTODOME = False


def encrypt_serpent(data: bytes, key: bytes, iv: bytes) -> bytes:
    if not _HAS_CRYPTODOME: return data
    c = Serpent.new(key, Serpent.MODE_CBC, iv=iv[:16])
    return c.encrypt(_pad(data, 16))


def decrypt_serpent(data: bytes, key: bytes, iv: bytes) -> bytes:
    if not _HAS_CRYPTODOME: return data
    c = Serpent.new(key, Serpent.MODE_CBC, iv=iv[:16])
    return _unpad(c.decrypt(data))


def encrypt_twofish(data: bytes, key: bytes, iv: bytes) -> bytes:
    if not _HAS_CRYPTODOME: return data
    c = Twofish.new(key, Twofish.MODE_CBC, iv=iv[:16])
    return c.encrypt(_pad(data, 16))


def decrypt_twofish(data: bytes, key: bytes, iv: bytes) -> bytes:
    if not _HAS_CRYPTODOME: return data
    c = Twofish.new(key, Twofish.MODE_CBC, iv=iv[:16])
    return _unpad(c.decrypt(data))


def encrypt_camellia(data: bytes, key: bytes, iv: bytes) -> bytes:
    if not _HAS_CRYPTODOME: return data
    c = Camellia.new(key, Camellia.MODE_CBC, iv=iv[:16])
    return c.encrypt(_pad(data, 16))


def decrypt_camellia(data: bytes, key: bytes, iv: bytes) -> bytes:
    if not _HAS_CRYPTODOME: return data
    c = Camellia.new(key, Camellia.MODE_CBC, iv=iv[:16])
    return _unpad(c.decrypt(data))


def encrypt_salsa20(data: bytes, key: bytes, nonce: bytes) -> bytes:
    if not _HAS_CRYPTODOME: return data
    c = _Salsa20.new(key=key, nonce=nonce[:8])
    return c.encrypt(data)


def decrypt_salsa20(data: bytes, key: bytes, nonce: bytes) -> bytes:
    if not _HAS_CRYPTODOME: return data
    c = _Salsa20.new(key=key, nonce=nonce[:8])
    return c.decrypt(data)


def _pad(data: bytes, bs: int) -> bytes:
    pl = bs - len(data) % bs
    return data + bytes([pl] * pl)


def _unpad(data: bytes) -> bytes:
    return data[:-data[-1]]
```

- [ ] **Step 4: Run test to verify it passes**

```bash
python -m pytest tests/test_crypto_extra.py::test_serpent_roundtrip tests/test_crypto_extra.py::test_serpent_wrong_key -v 2>&1 | findstr "PASS"
```

Expected: `PASS`

- [ ] **Step 5: Add Twofish/Camellia/Salsa20 tests**

Add to `tests/test_crypto_extra.py`:

```python
def test_twofish_roundtrip():
    data = b"Hello Twofish CBC!" * 50
    key = b"t" * 32
    iv = b"i" * 16
    ct = encrypt_twofish(data, key, iv)
    assert ct != data
    pt = decrypt_twofish(ct, key, iv)
    assert pt == data

def test_camellia_roundtrip():
    data = b"Hello Camellia CBC!" * 50
    key = b"c" * 32
    iv = b"i" * 16
    ct = encrypt_camellia(data, key, iv)
    assert ct != data
    pt = decrypt_camellia(ct, key, iv)
    assert pt == data

def test_salsa20_roundtrip():
    data = b"Hello Salsa20 stream!" * 50
    key = b"s" * 32
    nonce = b"n" * 8
    ct = encrypt_salsa20(data, key, nonce)
    assert ct != data
    pt = decrypt_salsa20(ct, key, nonce)
    assert pt == data
```

- [ ] **Step 6: Run all extra cipher tests**

```bash
python -m pytest tests/test_crypto_extra.py -v 2>&1 | findstr "PASSED"
```

Expected: 6 PASSED

- [ ] **Step 7: Commit**

```bash
git add sprotect/crypto_extra.py tests/test_crypto_extra.py
git commit -m "feat: add Serpent/Twofish/Camellia/Salsa20 encrypt/decrypt"
```

---

### Task 4: Updated encrypt_payload/decrypt_payload with Extra Layers

**Files:**
- Modify: `sprotect/crypto.py`
- Test: `tests/test_crypto_extra.py`

**Interfaces:**
- Consumes: `derive_layer_key` (Task 2), `crypto_extra.*` (Task 3)
- Produces: `encrypt_payload_v2(data, key, extra_layers)` → `(ct_bytes, header_dict)`

- [ ] **Step 1: Write failing test**

Add to `tests/test_crypto_extra.py`:

```python
from sprotect.crypto import encrypt_payload_v2, decrypt_payload_v2

def test_encrypt_payload_v2_no_extra():
    data = b"test source code here"
    key = b"m" * 32
    ct, hdr = encrypt_payload_v2(data, key, [])
    assert "version" in hdr
    assert hdr["extra_layers"] == []
    pt = decrypt_payload_v2(ct, key, hdr)
    assert pt == data

def test_encrypt_payload_v2_with_serpent():
    data = b"test source with serpent" * 100
    key = b"m" * 32
    ct, hdr = encrypt_payload_v2(data, key, ["serpent"])
    assert "serpent" in hdr["layer_ivs"]
    pt = decrypt_payload_v2(ct, key, hdr)
    assert pt == data

def test_encrypt_payload_v2_all_layers():
    data = b"test source ALL layers" * 200
    key = b"m" * 32
    ct, hdr = encrypt_payload_v2(data, key, ["serpent", "twofish", "camellia"])
    for algo in ["serpent", "twofish", "camellia"]:
        assert algo in hdr["layer_ivs"]
    pt = decrypt_payload_v2(ct, key, hdr)
    assert pt == data
```

- [ ] **Step 2: Run to verify failure**

```bash
python -m pytest tests/test_crypto_extra.py::test_encrypt_payload_v2_no_extra -v 2>&1 | findstr "FAILED"
```

Expected: `FAILED`

- [ ] **Step 3: Implement encrypt_payload_v2 / decrypt_payload_v2 in crypto.py**

Add to end of `sprotect/crypto.py`:

```python
def encrypt_payload_v2(source_data: bytes, real_key: bytes,
                       extra_layers: list[str] = None,
                       compress: int = 9) -> tuple[bytes, dict]:
    from sprotect.crypto_extra import (
        encrypt_serpent, encrypt_twofish, encrypt_camellia, encrypt_salsa20,
    )
    extra_layers = extra_layers or []
    data = zlib.compress(source_data, level=compress)
    try:
        c20 = chacha20_encrypt(data, real_key)
    except Exception:
        c20 = data
    xored = xor_stream(c20, hashlib.sha256(real_key).digest())
    ct = aes_encrypt(xored, real_key)
    layer_ivs = {}
    for algo in extra_layers:
        lk, salt = derive_layer_key(real_key, f"sprotect:{algo}")
        iv = os.urandom(16)
        layer_ivs[algo] = {"iv": iv.hex(), "salt": salt.hex()}
        fn = {
            "serpent": encrypt_serpent, "twofish": encrypt_twofish,
            "camellia": encrypt_camellia, "salsa20": encrypt_salsa20,
        }.get(algo)
        if fn:
            ct = fn(ct, lk, iv)
    header = {
        "version": 2,
        "extra_layers": extra_layers,
        "layer_ivs": layer_ivs,
        "hybrid": False,
    }
    return ct, header


def decrypt_payload_v2(data: bytes, real_key: bytes, header: dict) -> bytes:
    from sprotect.crypto_extra import (
        decrypt_serpent, decrypt_twofish, decrypt_camellia, decrypt_salsa20,
    )
    ct = data
    for algo in reversed(header.get("extra_layers", [])):
        info = header["layer_ivs"].get(algo, {})
        iv = bytes.fromhex(info.get("iv", ""))
        salt = bytes.fromhex(info.get("salt", ""))
        lk, _ = derive_layer_key(real_key, f"sprotect:{algo}")
        fn = {
            "serpent": decrypt_serpent, "twofish": decrypt_twofish,
            "camellia": decrypt_camellia, "salsa20": decrypt_salsa20,
        }.get(algo)
        if fn:
            ct = fn(ct, lk, iv)
    ct = aes_decrypt(ct, real_key)
    ct = xor_stream(ct, hashlib.sha256(real_key).digest())
    try:
        ct = chacha20_decrypt(ct, real_key)
    except Exception:
        pass
    return zlib.decompress(ct)
```

- [ ] **Step 4: Run tests to verify pass**

```bash
python -m pytest tests/test_crypto_extra.py::test_encrypt_payload_v2_no_extra tests/test_crypto_extra.py::test_encrypt_payload_v2_with_serpent tests/test_crypto_extra.py::test_encrypt_payload_v2_all_layers -v 2>&1 | findstr "PASS"
```

Expected: 3 PASSED

- [ ] **Step 5: Commit**

```bash
git add sprotect/crypto.py tests/test_crypto_extra.py
git commit -m "feat: add encrypt_payload_v2 with extra layer support"
```

---

### Task 5: .pye Header v2 Read/Write

**Files:**
- Create: `sprotect/decrypt.py` (rewrite)
- Test: `tests/test_crypto_extra.py`

**Interfaces:**
- Consumes: `encrypt_payload_v2`, `decrypt_payload_v2`
- Produces: `encrypt_to_pye(data, key, extra_layers)`, `decrypt_from_pye(pye_data)`

- [ ] **Step 1: Write failing tests**

Add to `tests/test_crypto_extra.py`:

```python
def test_pye_v2_header_roundtrip():
    data = b"def foo(): pass"
    key = b"m" * 32
    pye = encrypt_to_pye(data, key, ["serpent"])
    pt = decrypt_from_pye(pye)
    assert pt == data

def test_pye_v1_backward_compat():
    # Simulate old v1 payload (no header)
    key = b"m" * 32
    from sprotect.crypto import encrypt_payload
    old = encrypt_payload(b"v1 compat test", key)
    pt = decrypt_from_pye(old)
    assert pt == b"v1 compat test"
```

- [ ] **Step 2: Run to verify failure**

```bash
python -m pytest tests/test_crypto_extra.py::test_pye_v2_header_roundtrip -v 2>&1 | findstr "FAILED"
```

Expected: `FAILED`

- [ ] **Step 3: Rewrite sprotect/decrypt.py**

```python
"""Decrypt .pye files (v1 and v2 format)."""

from __future__ import annotations
import json, msgpack


def encrypt_to_pye(source_data: bytes, real_key: bytes,
                   extra_layers: list[str] = None) -> bytes:
    from sprotect.crypto import encrypt_payload_v2
    ct, header = encrypt_payload_v2(source_data, real_key, extra_layers)
    header_bytes = msgpack.dumps(header)
    return msgpack.dumps({"h": header_bytes, "d": ct.hex()})


def decrypt_from_pye(pye_data: bytes) -> bytes:
    from sprotect.crypto import decrypt_payload_v2, encrypt_payload
    try:
        p = msgpack.loads(pye_data)
        header_bytes = p.get("h")
        if header_bytes:
            header = msgpack.loads(header_bytes)
            ct = bytes.fromhex(p["d"])
            master_key = _find_real_key(p) if p.get("keys") else None
            if master_key:
                return decrypt_payload_v2(ct, master_key, header)
            # Fallback: try standard decrypt
            payload = json.loads(pye_data.decode())
            return _decrypt_v1_fallback(payload)
    except (msgpack.exceptions.UnpackException, KeyError, json.JSONDecodeError, Exception):
        pass
    # v1 fallback
    payload = json.loads(pye_data.decode())
    return _decrypt_v1_fallback(payload)


def _find_real_key(p: dict) -> bytes | None:
    for i in range(1, 6):
        k = p.get(f"k{i}")
        if k:
            try:
                from sprotect.crypto import verify_fingerprint
                if verify_fingerprint(p, bytes.fromhex(k)):
                    return bytes.fromhex(k)
            except Exception:
                pass
    return None


def _decrypt_v1_fallback(payload: dict) -> bytes:
    from sprotect.crypto import aes_decrypt, xor_stream, chacha20_decrypt
    import hashlib, zlib
    mk = _find_real_key(payload)
    if not mk:
        raise ValueError("No valid key found")
    ct = bytes.fromhex(payload["d"])
    x = aes_decrypt(ct, mk)
    x = xor_stream(x, hashlib.sha256(mk).digest())
    try:
        x = chacha20_decrypt(x, mk)
    except Exception:
        pass
    return zlib.decompress(x)
```

- [ ] **Step 4: Run tests to verify pass**

```bash
python -m pytest tests/test_crypto_extra.py::test_pye_v2_header_roundtrip tests/test_crypto_extra.py::test_pye_v1_backward_compat -v 2>&1
```

Expected: 2 PASSED

- [ ] **Step 5: Commit**

```bash
git add sprotect/decrypt.py tests/test_crypto_extra.py
git commit -m "feat: add .pye header v2 with v1 backward compat"
```

---

### Task 6: Config Builder for Extra Layers + Hybrid

**Files:**
- Modify: `sprotect/config.py`

**Interfaces:**
- Consumes: `HybridEncryptConfig`, `EncryptConfig` with new fields
- Produces: `_extral(d)` builder, updated `_enc()` builder

- [ ] **Step 1: Update _enc() builder and add _extral()**

Replace `_enc(d)` in config.py:

```python
def _enc(d): return EncryptConfig(
    algorithm=_te(EncryptAlgorithm, d.get("algorithm","aes-256-gcm")).value,
    key_source=d.get("key_source","auto"),
    key_file=d.get("key_file"), key_env_var=d.get("key_env_var"),
    interdependency=_te(InterdependencyMode, d.get("interdependency","chain")),
    backup=d.get("backup",True), backup_max_count=d.get("backup_max_count",5),
    replace_originals=d.get("replace_originals",False),
    shard_count=d.get("shard_count",3), shard_min_files=d.get("shard_min_files",2),
    compress_level=d.get("compress_level",9),
    polymorphic_padding=d.get("polymorphic_padding",True),
    polymorphic_padding_max=d.get("polymorphic_padding_max",512),
    aad_context=d.get("aad_context","S-Protect-PY"),
    extra_layers=d.get("extra_layers",[]),
    hybrid=_extral_hybrid(d.get("hybrid",{})))
```

Add after `_files(d)`:

```python
def _extral_hybrid(d): return HybridEncryptConfig(
    enabled=d.get("enabled",False),
    algorithm=d.get("algorithm","RSA"),
    key_size=d.get("key_size",4096),
    key_file=d.get("key_file","key.pem"))
```

- [ ] **Step 2: Verify config compiles**

```bash
python -c "from sprotect.config import load_config; c=load_config(); print(c.encrypt.extra_layers, c.encrypt.hybrid)"
```

Expected: `[] HybridEncryptConfig(enabled=False, algorithm='RSA', key_size=4096, key_file='key.pem')`

- [ ] **Step 3: Commit**

```bash
git add sprotect/config.py
git commit -m "feat: add extra_layers and hybrid config builders"
```

---

### Task 7: encrypt.py Integration for Extra Layers

**Files:**
- Modify: `sprotect/encrypt.py`

**Interfaces:**
- Consumes: `encrypt_payload_v2`, extra layer support from crypto.py
- Produces: `.pye` files with v2 header when extra_layers is configured

- [ ] **Step 1: Update build() to pass extra_layers**

Replace the `encrypt_payload` call block in `encrypt.py:53-56`:

```python
            extra = fc.encrypt.extra_layers if fc.encrypt.extra_layers else []
            if extra:
                ct, hdr = encrypt_payload_v2(src.encode(), master_key, extra,
                                             config.encrypt.compress_level)
                payload_bytes = msgpack.dumps({"h": msgpack.dumps(hdr), "d": ct.hex()})
            else:
                payload_bytes = encrypt_payload(src.encode(), master_key,
                                           config.encrypt.compress_level,
                                           config.encrypt.polymorphic_padding_max)
```

Also update the chain_hash pass (lines 83-94) to handle both v1 and v2 format:

Replace `raw = open(pye_path, "rb").read()` logic with a helper that extracts `d` from both formats.

- [ ] **Step 2: Extract d field from v1/v2 uniformly**

Add to top of `encrypt.py`:

```python
import msgpack
```

Add a small helper:

```python
def _extract_d(pye_bytes: bytes) -> tuple[str, dict]:
    """Extract d field from v1 (JSON) or v2 (msgpack) .pye."""
    try:
        p = json.loads(pye_bytes.decode())
        return p.get("d", ""), p
    except (json.JSONDecodeError, UnicodeDecodeError):
        pass
    try:
        p = msgpack.loads(pye_bytes)
        h = msgpack.loads(p.get("h", b"")) if isinstance(p.get("h"), (bytes, bytearray)) else {}
        return p.get("d", ""), {**p, "__header": h}
    except Exception:
        pass
    return "", {}
```

- [ ] **Step 3: Run build test**

```bash
python -c "
import tempfile, os, json
from sprotect.encrypt import build
from sprotect.config import gen_default, load_config
tmp = tempfile.mkdtemp()
os.makedirs(os.path.join(tmp, 'project'))
open(os.path.join(tmp, 'project', 'main.py'), 'w').write('print(\"hello\")')
open(os.path.join(tmp, 'project', 'sprotect.json5'), 'w').write(json.dumps({'encrypt':{'extra_layers':['serpent','twofish']}}))
build(os.path.join(tmp, 'project'), os.path.join(tmp, 'output'), load_config(os.path.join(tmp, 'project', 'sprotect.json5')))
import glob; files = glob.glob(os.path.join(tmp, 'output', '_runtime', '*.pye'), recursive=True)
print(f'pye files: {len(files)}')
for f in files[:2]:
    raw = open(f,'rb').read()
    if b'version' in raw or b'h"' in raw:
        print(f'{os.path.basename(f)}: v2 format detected')
    else:
        print(f'{os.path.basename(f)}: v1 format')
import shutil; shutil.rmtree(tmp)
"
```

Expected: v2 format detected for the encrypted file

- [ ] **Step 4: Commit**

```bash
git add sprotect/encrypt.py
git commit -m "feat: integrate extra_layers into build pipeline"
```

---

### Task 8: Loader Runtime Support for Extra Layers

**Files:**
- Modify: `sprotect/loader.py`

**Interfaces:**
- Consumes: `.pye` v2 header with `extra_layers`, `layer_ivs`
- Produces: updated loader source that can decrypt v2 files

- [ ] **Step 1: Update gen_loader_source() to handle v2 format**

Add inside `gen_loader_source()` after the `_xof` function definition, a new function for extra layer decryption:

```python
# Inside loader source string, injected function:
def {f_extra}(ct, mk, hdr):
    import json
    try:
        h = json.loads(hdr) if isinstance(hdr, str) else {{}}
    except:
        return ct
    for algo in reversed(h.get("extra_layers", [])):
        info = h["layer_ivs"].get(algo, {{}})
        iv = bytes.fromhex(info.get("iv", ""))
        salt = bytes.fromhex(info.get("salt", ""))
        hkdf = __import__("hashlib").pbkdf2_hmac("sha256", mk, salt, 1, 32)
        if algo == "serpent":
            from Cryptodome.Cipher import Serpent
            c = Serpent.new(hkdf, Serpent.MODE_CBC, iv=iv[:16])
            ct = c.decrypt(ct)[:-ct[-1]]
        elif algo == "twofish":
            from Cryptodome.Cipher import Twofish
            c = Twofish.new(hkdf, Twofish.MODE_CBC, iv=iv[:16])
            ct = c.decrypt(ct)[:-ct[-1]]
        elif algo == "camellia":
            from Cryptodome.Cipher import Camellia
            c = Camellia.new(hkdf, Camellia.MODE_CBC, iv=iv[:16])
            ct = c.decrypt(ct)[:-ct[-1]]
        elif algo == "salsa20":
            from Cryptodome.Cipher import Salsa20
            c = Salsa20.new(key=hkdf, nonce=iv[:8])
            ct = c.decrypt(ct)
    return ct
```

Also add random name for `f_extra`:
```python
f_extra = _rand_name()
```

And inject into the source template:
```python
src = src.replace('_EXTRA_FUNC = ""', f"_{f_extra} = {f_extra}")
```

Actually the loader source is a raw string template - let me think about this more carefully.

The loader source in `gen_loader_source()` is built as a Python string with f-strings and template variables. I need to:

1. Add the extra layer decryption function as a random-named function
2. Modify the `_load` function to check for a header and call extra layer decrypt

Let me look at how the loader works:

The `f_load` function currently does:
```python
def {f_load}(p, mk):
    ct = bytes.fromhex(p["d"])
    x = AESGCM(mk).decrypt(ct[:12], ct[12:], b"")
    ks = {f_xof}(len(x), hashlib.sha256(mk).digest())
    return zlib.decompress(bytes(a^b for a,b in zip(x,ks))).decode()
```

I need to modify it to:
1. Check if `p` has a header field (v2 format)
2. If yes, parse the header for extra layers
3. Apply extra layer decryption after AES-GCM step

For the loader, since I can't use msgpack (need stdlib-only), I'll encode the header as a hex JSON string in a dedicated `.pye` field.

Actually, let me reconsider. The loader currently uses `json.loads(open(...).read().decode())`. For v2 files that use msgpack, this won't work.

Better approach: Keep v2 `.pye` files as **msgpack** but store the header as a JSON hex string inside. The loader imports `json` already.

Enhanced layout:
```python
# v2 .pye (msgpack)
{
    "h": b"..."     # msgpack header (containing version, extra_layers, layer_ivs)
    "d": "..."      # hex-encoded encrypted data
    "k1"-"k5": ...  # key shards
    "f1"-"f3": ...  # fingerprints
}
```

At loader runtime, it still reads the entire file and tries JSON first, then msgpack:
```python
try:
    p = json.loads(open(path, "rb").read().decode())
except (json.JSONDecodeError, UnicodeDecodeError):
    import msgpack
    p = msgpack.loads(open(path, "rb").read())
```

But msgpack isn't stdlib. Hmm. Let me think...

Alternative: Store v2 as JSON like v1, but add a `"h"` field that holds a JSON-escaped hex representation of the header:

```python
{
    "v": 2,
    "h": "{\"extra_layers\":[\"serpent\"],\"layer_ivs\":{\"serpent\":{\"iv\":\"...\",\"salt\":\"...\"}}}",
    "d": "...",
    "k1"-"k5": "...",
    "f1"-"f3": "..."
}
```

This way the loader can still use `json.loads()` and parse `h` as a JSON string. No msgpack needed at runtime.

Wait, but the loader already uses JSON. If I keep v2 as JSON too, it's fully backward compatible. Let me do that instead.

Actually, looking at `encrypt_to_pye` in the spec earlier, I used msgpack. But for the loader, JSON is simpler and already used. Let me change the v2 format to use JSON:

```python
# v2 .pye (JSON, same as v1)
{
    "v": 2,
    "h": "{\"extra_layers\":[\"serpent\"],\"layer_ivs\":{\"serpent\":{\"iv\":\"hexiv\",\"salt\":\"hexsalt\"}}}",
    "d": "hexdata...",
    "k1"-"k5": "...",
    "f1"-"f3": "..."
}
```

The header `h` is a JSON-encoded string within the JSON payload. This way:
- v1 files have no `h` field → backward compat
- v2 files have `h` field → loader parses it

Let me revise the plan for decrypt.py accordingly, and update the loader.

OK, let me just write the plan properly with this approach. I need to update Task 5's decrypt.py to use JSON instead of msgpack for the header.

Actually, looking at this from a practical standpoint - the encrypt.py currently writes JSON `.pye` files. Let me keep it as JSON. The header `h` can just be an escaped JSON string inside the JSON payload.

Let me revise the plan. Instead of msgpack for v2, I'll use plain JSON:

```python
# Task 5 - decrypt.py rewrite
def encrypt_to_pye(source_data, key, extra_layers=None):
    ct, header = encrypt_payload_v2(source_data, key, extra_layers)
    header_json = json.dumps(header, separators=(",", ":"))
    payload = {"v": 2, "h": header_json, "d": ct.hex()}
    return json.dumps(payload, separators=(",", ":")).encode()
```

And for the loader, I just need to:
1. After JSON parse, check if `p.get("h")` exists
2. If yes, parse it and call extra layer decryption

This is much simpler. Let me update the plan accordingly.

OK, I've been overthinking this. Let me just finalize the plan. I've already written a lot. Let me simplify:

For the loader task, I just need to:
1. Add the extra layer decryption function to the loader source
2. Modify the `f_load` function to handle v2 headers

Let me wrap up the plan and write it properly.<｜end▁of▁thinking｜>Now I have all the context. Let me write the complete implementation plan.

<｜｜DSML｜｜tool_calls>
<｜｜DSML｜｜invoke name="bash">
<｜｜DSML｜｜parameter name="command" string="true">$dir = "D:\administrator\Documents\project\S-Protect-PY\docs\superpowers\plans"; New-Item -ItemType Directory -Path $dir -Force > $null; Write-Output $dir