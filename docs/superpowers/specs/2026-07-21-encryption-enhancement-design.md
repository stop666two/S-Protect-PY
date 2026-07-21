# Encryption Enhancement Design

**Date**: 2026-07-21
**Status**: Draft
**Version**: 1.0

## 1. Motivation

Current protection pipeline (zlib → ChaCha20 → XOR → AES-256-GCM) uses only two standard ciphers. Adding extra layers increases protection depth and makes brute-force/cryptanalysis impractical.

## 2. Architecture

### 2.1 Layered Encryption Pipeline

```
Existing:  zlib → ChaCha20 → XOR → AES-GCM → .pye
Enhanced:  zlib → ChaCha20 → XOR → AES-GCM → [Serpent] → [Twofish] → [Camellia] → .pye
```

- Each extra layer is optional, enabled via config `encrypt.extra_layers` array.
- Layers execute in order specified in config; decryption reverses the order.
- Each extra layer derives its key via HKDF-SHA256 from master_key with domain separation (unique `info` string per algorithm), so compromising one layer does not leak keys for others.

### 2.2 Hybrid Encryption (RSA/ECC)

```
build.py                     loader startup
───────                      ──────────────
master_key                   1. Decrypt RSA-encrypted master_key with private key
    │                            ↓
    ├── → encrypt with       2. Derive per-layer keys via HKDF
    │    public key               ↓
    │    ↓                    3. Decrypt each .pye using standard pipeline
    ├── store RSA-wrapped
    │    master_key in loader
    │
    └── auto-generate RSA key
        pair, save key.pem
```

- Only one key pair per project build.
- At build time: public key encrypts master_key → stored inside loader stub.
- At runtime: loader prompts user for private key passphrase → decrypts master_key → proceeds with normal decryption.
- If hybrid encryption is disabled (default), master_key is stored in plain (as today).

### 2.3 Post-Quantum Cryptography (Deferred)

Post-quantum algorithms (Kyber, Dilithium) require `liboqs-python` which needs native C extensions. This introduces platform-specific build issues. Decision: **defer until a stable Python-native PQ library emerges or upstream demand is confirmed**.

## 3. Algorithm Details

| Algorithm | Block Size | Key Size | Mode | Source |
|-----------|-----------|----------|------|--------|
| Serpent | 128 bit | 256 bit | CBC + PKCS7 | pycryptodome |
| Twofish | 128 bit | 256 bit | CBC + PKCS7 | pycryptodome |
| Camellia | 128 bit | 256 bit | CBC + PKCS7 | pycryptodome |
| Salsa20 | n/a (stream) | 256 bit | raw | pycryptodome |

All symmetric extra layers use random IV/nonce stored prepended to the ciphertext.

## 4. Key Derivation (HKDF Domain Separation)

```
layer_key = HKDF-SHA256(master_key, length=32, salt=random_16_bytes, info=b"sprotect:serpent")
layer_key = HKDF-SHA256(master_key, length=32, salt=random_16_bytes, info=b"sprotect:twofish")
layer_key = HKDF-SHA256(master_key, length=32, salt=random_16_bytes, info=b"sprotect:camellia")
```

Each info string is unique to the algorithm, stored in per-file `.pye` header so the decryptor knows which HKDF params to use.

## 5. Config Changes (`types.py`)

### New dataclass

```python
@dataclass
class ExtraLayerConfig:
    enabled: bool = False
    algorithm: str = ""  # serpent, twofish, camellia, salsa20

@dataclass
class HybridEncryptConfig:
    enabled: bool = False
    algorithm: str = "RSA"       # RSA | ECC
    key_size: int = 4096         # RSA bit length or ECC curve id
    key_file: str = "key.pem"

@dataclass
class EncryptConfig:
    # ... existing fields ...
    extra_layers: list[str] = field(default_factory=list)
    hybrid: HybridEncryptConfig = field(default_factory=HybridEncryptConfig)
```

### Config builder update (`config.py`)

```python
def _extral(d): ...   # Parse extra_layers and hybrid from json5
```

## 6. File Format Changes (`.pye` header)

Current `.pye` layout (msgpack):

```
[file_magic, enc_data, key_shards, f1, f2, f3, ...]
```

New layout:

```
[file_magic, header, enc_data, key_shards, f1, f2, f3, ...]
```

Where `header` is a msgpack dict:

```python
header = {
    "version": 2,
    "extra_layers": ["serpent", "twofish"],     # algorithms applied
    "layer_ivs": {                               # IV per extra layer
        "serpent": b"<16 bytes>",
        "twofish": b"<16 bytes>",
    },
    "hybrid": False,                             # whether master_key is RSA-encrypted
    "hybrid_salt": b""                           # HKDF salt (only present when hybrid=True)
}
```

The header is stored as-is (not encrypted) so the decryptor knows which algorithms to apply and in what order. The IVs are unique per file.

## 7. Module Changes

### 7.1 `crypto.py` — New functions

```python
# Extra layer encryption/decryption
def encrypt_serpent(data: bytes, key: bytes, iv: bytes) -> bytes
def decrypt_serpent(data: bytes, key: bytes, iv: bytes) -> bytes
def encrypt_twofish(data: bytes, key: bytes, iv: bytes) -> bytes
def decrypt_twofish(data: bytes, key: bytes, iv: bytes) -> bytes
def encrypt_camellia(data: bytes, key: bytes, iv: bytes) -> bytes
def decrypt_camellia(data: bytes, key: bytes, iv: bytes) -> bytes
def encrypt_salsa20(data: bytes, key: bytes, nonce: bytes) -> bytes
def decrypt_salsa20(data: bytes, key: bytes, nonce: bytes) -> bytes

# HKDF derivation
def derive_layer_key(master_key: bytes, info: str, salt: bytes = None) -> bytes

# Hybrid RSA
def rsa_generate_keypair(key_size: int, passphrase: str = "") -> tuple[bytes, bytes]
def rsa_encrypt_master_key(master_key: bytes, public_key_pem: bytes) -> bytes
def rsa_decrypt_master_key(encrypted_key: bytes, private_key_pem: bytes, passphrase: str = "") -> bytes
def ecc_generate_keypair(curve: str, passphrase: str = "") -> tuple[bytes, bytes]
def ecc_encrypt_master_key(master_key: bytes, public_key_pem: bytes) -> bytes
def ecc_decrypt_master_key(encrypted_key: bytes, private_key_pem: bytes, passphrase: str = "") -> bytes

# Updated pipeline
def encrypt_payload(data: bytes, key: bytes, extra_layers: list[str] = []) -> tuple[bytes, dict]
    # 1. zlib compress
    # 2. ChaCha20 encrypt
    # 3. XOR encrypt
    # 4. AES-GCM encrypt (as today)
    # 5. For each algo in extra_layers:
    #      - derive layer key via HKDF
    #      - generate random IV
    #      - encrypt with layer cipher
    # 6. Return (encrypted_data, layer_ivs_dict)

def decrypt_payload(data: bytes, key: bytes, header: dict) -> bytes
    # 1. Reverse order of extra_layers
    # 2. Standard decryption layers
```

### 7.2 `encrypt.py` — Build pipeline changes

- After `encrypt_payload`, new logic:
  - If `hybrid.enabled`: generate keypair, write key file, encrypt master_key with public key, store in bootloader
  - If `extra_layers`: pass to `encrypt_payload`, collect IVs, write `.pye` header
- `gen_boot()` updated to handle hybrid decryption flow

### 7.3 `loader.py` — Runtime loader changes

- Read new `.pye` header format (backward compat with v1)
- If `header["hybrid"]`:
  - Load bundled encrypted master_key
  - Prompt user for private key path (or passphrase)
  - Decrypt master_key before proceeding
- If `header["extra_layers"]`:
  - For each algorithm in reverse order, derive key and decrypt
- Version check: if header version > loader knows, abort with clear message

### 7.4 `config.py` — Config builder additions

- `_extral(d)` builder function for extra_layers/hybrid
- `_to_cfg()` calls `_extral()` after existing builders
- `gen_default()` includes new config sections

### 7.5 `types.py` — New dataclasses

- `ExtraLayerConfig`
- `HybridEncryptConfig`
- Updated `EncryptConfig`

## 8. Dependency Update

```txt
# requirements.txt
cryptography==44.0.0          # already present
pycryptodome==3.21.0           # NEW: Serpent, Twofish, Camellia, Salsa20
```

`pycryptodome` is a pure-Python-compatible library (C extensions optional but recommended for performance).

## 9. Backward Compatibility

- Old `.pye` files (no header) continue to work: decryptor checks for `file_magic` + `header` length; if header absent, assumes v1 layout.
- New loader can decrypt old files.
- Old loader cannot decrypt new files (version check will reject).
- Config without `extra_layers` / `hybrid` fields falls back to defaults (empty list / disabled).

## 10. Testing

- Unit tests per new algorithm: encrypt known plaintext, decrypt, verify roundtrip
- HKDF derivation test: same input → same key; different `info` → different key
- Hybrid RSA/ECC: generate → encrypt → decrypt roundtrip with correct/incorrect passphrase
- `encrypt_payload` integration: extra_layers roundtrip
- Backward compat: v1 files decrypt correctly with updated code
- Build integration: `sprotect build` with extra_layers/hybrid produces runnable output that decrypts at runtime
- pytest to include `pycryptodome` in test deps

## 11. Implementation Order

1. HKDF `derive_layer_key()` in crypto.py
2. Serpent encrypt/decrypt in crypto.py
3. Twofish encrypt/decrypt in crypto.py
4. Camellia encrypt/decrypt in crypto.py
5. Salsa20 encrypt/decrypt in crypto.py
6. Updated `encrypt_payload` / `decrypt_payload` with extra_layers support
7. `.pye` header v2 format
8. Config dataclasses + builder in types.py / config.py
9. encrypt.py integration (extra_layers)
10. loader.py runtime support for extra_layers
11. RSA keypair generation + hybrid encrypt/decrypt
12. ECC keypair generation + hybrid encrypt/decrypt
13. encrypt.py hybrid integration
14. loader.py hybrid runtime support
15. Default config update
16. Tests
