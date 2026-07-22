"""Cryptographic engine: PyCryptodome ChaCha20, blake3, multi-layer key derivation."""

from __future__ import annotations
import os, hashlib, hmac, json, secrets, zlib
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes

def derive_layer_key(master_key: bytes, info: str) -> tuple[bytes, bytes]:
    salt = hashlib.sha256(info.encode()).digest()[:16]
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        info=info.encode(),
    )
    return hkdf.derive(master_key), salt

def aes_key() -> bytes:
    return AESGCM.generate_key(bit_length=256)

def aes_encrypt(data: bytes, key: bytes) -> bytes:
    nonce = os.urandom(12)
    return nonce + AESGCM(key).encrypt(nonce, data, b"")

def aes_decrypt(ct: bytes, key: bytes) -> bytes:
    return AESGCM(key).decrypt(ct[:12], ct[12:], b"")

def split_key(key: bytes, n: int) -> list[bytes]:
    if n < 2: raise ValueError("Need >= 2 shards")
    shards = [os.urandom(len(key)) for _ in range(n - 1)]
    final = bytearray(len(key))
    for i in range(len(key)):
        v = key[i]
        for s in shards: v ^= s[i]
        final[i] = v
    shards.append(bytes(final))
    return shards

def _xof(l: int, s: bytes) -> bytes:
    r, c = bytearray(), 0
    while len(r) < l:
        r.extend(hashlib.sha256(s + c.to_bytes(4, "big")).digest()); c += 1
    return bytes(r[:l])

def xor_stream(d: bytes, k: bytes) -> bytes:
    return bytes(a ^ b for a, b in zip(d, _xof(len(d), k)))

def chain_hash(payloads, key):
    import json
    n = len(payloads)
    sigs = []
    for i in range(n):
        p = payloads[(i + 1) % n]
        if isinstance(p, dict): d = p.get("d", "")
        elif isinstance(p, bytes): d = json.loads(p.decode()).get("d", "")
        else: d = ""
        h = hashlib.sha256(d.encode()).digest()
        sigs.append(hmac.new(key, h, "sha256").hexdigest())
    return sigs

def sha256(d: bytes) -> str:
    return hashlib.sha256(d).hexdigest()


# ---- ChaCha20-Poly1305 layer (via cryptography library) ----
def chacha20_encrypt(data: bytes, key: bytes) -> bytes:
    from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
    nonce = os.urandom(12)
    return nonce + ChaCha20Poly1305(key).encrypt(nonce, data, b"")

def chacha20_decrypt(ct: bytes, key: bytes) -> bytes:
    from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
    return ChaCha20Poly1305(key).decrypt(ct[:12], ct[12:], b"")


# ---- blake3 hashing ----
def blake3_hash(data: bytes) -> str:
    import blake3
    return blake3.blake3(data).hexdigest()


# ---- Complex multi-layer key fingerprint ----
def make_keys_complex(real_key: bytes, decoy_count: int = 4) -> tuple[dict, str]:
    """Generate k1-k5 with real key at random position.
    Uses complex multi-layer fingerprint verification:
    Layer 1: SHA256(xor_all_keys) truncated
    Layer 2: blake3(real_key) specific bytes
    Layer 3: HMAC of combined key material
    """
    decoys = [os.urandom(32) for _ in range(decoy_count)]
    pos = secrets.randbelow(decoy_count + 1)
    keys_list = decoys[:]
    keys_list.insert(pos, real_key)
    keys = {f"k{i+1}": keys_list[i].hex() for i in range(decoy_count + 1)}
    real_name = f"k{pos + 1}"

    # Complex fingerprint: XOR all keys, SHA256, take multiple slices
    xored = bytearray(32)
    for k in keys_list:
        for i in range(32): xored[i] ^= k[i]
    xored = bytes(xored)
    # f1 = SHA256(xor_of_all)[5:13] - depends on ALL keys
    # Only the real key set produces the correct xor result
    f1 = hashlib.sha256(xored).hexdigest()[5:13]
    try:
        f2 = blake3_hash(real_key)[3:11]
    except:
        f2 = hashlib.sha256(b"f2-domain:" + real_key).hexdigest()[8:16]
    # f3 = HMAC-SHA256(key_material, context)[:8]
    import hmac as _hm
    f3 = _hm.new(real_key, b"S-Protect-v6-key-verify", "sha256").hexdigest()[:8]

    return {**keys, "f1": f1, "f2": f2, "f3": f3}, real_name


def verify_fingerprint(p: dict, potential_key: bytes) -> bool:
    """Verify if a key matches ALL 3 fingerprint conditions."""
    # Get all keys
    all_keys = []
    for i in range(1, 6):
        k = p.get(f"k{i}")
        if k: all_keys.append(bytes.fromhex(k))
    if not all_keys: return False

    # f1 check: SHA256(XOR of all keys)[5:13]
    xored = bytearray(32)
    for k in all_keys:
        for i in range(min(32, len(k))): xored[i] ^= k[i]
    f1_expected = hashlib.sha256(bytes(xored)).hexdigest()[5:13]
    if p.get("f1", "") != f1_expected: return False

    try:
        f2_expected = blake3_hash(potential_key)[3:11]
    except:
        f2_expected = hashlib.sha256(b"f2-domain:" + potential_key).hexdigest()[8:16]
    if p.get("f2", "") != f2_expected: return False

    # f3 check: HMAC-SHA256
    import hmac as _hm
    f3_expected = _hm.new(potential_key, b"S-Protect-v6-key-verify", "sha256").hexdigest()[:8]
    if p.get("f3", "") != f3_expected: return False

    return True


def encrypt_payload(source_data: bytes, real_key: bytes,
                    compress: int = 9, pad_max: int = 512) -> bytes:
    """Encrypt with ChaCha20 + AES-GMC dual layer + complex fingerprints."""
    compressed = zlib.compress(source_data, level=compress)
    c20 = chacha20_encrypt(compressed, real_key)
    # Layer 2: XOR obfuscation
    xored = xor_stream(c20, hashlib.sha256(real_key).digest())
    # Layer 3: AES-GCM
    ct = aes_encrypt(xored, real_key)

    keys, _ = make_keys_complex(real_key, 4)
    pad = os.urandom(secrets.randbelow(pad_max + 1))
    payload = {"v": 7, "d": ct.hex(), "c": "", "p": pad.hex(), "h": sha256(source_data)}
    payload.update(keys)
    return json.dumps(payload, separators=(",", ":")).encode()


def generate_decoy_payload() -> bytes:
    """Decoy file - identical structure, garbage content."""
    garbage = os.urandom(secrets.randbelow(500) + 100)
    fake_key = os.urandom(32)
    compressed = zlib.compress(garbage)
    try:
        c20 = chacha20_encrypt(compressed, fake_key)
    except:
        c20 = compressed
    xored = xor_stream(c20, hashlib.sha256(fake_key).digest())
    ct = aes_encrypt(xored, fake_key)

    keys, _ = make_keys_complex(fake_key, 2)
    pad = os.urandom(secrets.randbelow(512) + 1)
    payload = {"v": 7, "d": ct.hex(), "c": "", "p": pad.hex(), "h": sha256(garbage)}
    payload.update(keys)
    return json.dumps(payload, separators=(",", ":")).encode()


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
        iv = os.urandom(16) if algo != "salsa20" else os.urandom(8)
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


# ---- RSA hybrid encryption for master key wrapping ----
def rsa_generate_keypair(key_size: int = 4096, passphrase: str = "") -> tuple[bytes, bytes]:
    from Cryptodome.PublicKey import RSA
    key = RSA.generate(key_size)
    if passphrase:
        priv = key.export_key(passphrase=passphrase, pkcs=8, protection="scryptAndAES256-CBC")
    else:
        priv = key.export_key()
    pub = key.publickey().export_key()
    return pub, priv


def rsa_encrypt_master_key(master_key: bytes, public_key_pem: bytes) -> bytes:
    from Cryptodome.PublicKey import RSA
    from Cryptodome.Cipher import PKCS1_OAEP
    from Cryptodome.Hash import SHA256
    pub = RSA.import_key(public_key_pem)
    cipher = PKCS1_OAEP.new(pub, hashAlgo=SHA256)
    return cipher.encrypt(master_key)


def rsa_decrypt_master_key(encrypted_key: bytes, private_key_pem: bytes, passphrase: str = "") -> bytes:
    from Cryptodome.PublicKey import RSA
    from Cryptodome.Cipher import PKCS1_OAEP
    from Cryptodome.Hash import SHA256
    priv = RSA.import_key(private_key_pem, passphrase=passphrase)
    cipher = PKCS1_OAEP.new(priv, hashAlgo=SHA256)
    return cipher.decrypt(encrypted_key)


# ---- ECC hybrid encryption for master key wrapping (ECIES) ----
def ecc_generate_keypair(curve: str = "P-256", passphrase: str = "") -> tuple[bytes, bytes]:
    from Cryptodome.PublicKey import ECC
    if curve == "P-256":
        key = ECC.generate(curve="P-256")
    elif curve == "P-384":
        key = ECC.generate(curve="P-384")
    elif curve == "P-521":
        key = ECC.generate(curve="P-521")
    else:
        key = ECC.generate(curve="P-256")
    if passphrase:
        priv = key.export_key(passphrase=passphrase, protection="scryptAndAES256-CBC")
    else:
        priv = key.export_key(format="PEM")
    if isinstance(priv, str):
        priv = priv.encode()
    pub = key.public_key().export_key(format="PEM")
    if isinstance(pub, str):
        pub = pub.encode()
    return pub, priv


def ecc_encrypt_master_key(master_key: bytes, public_key_pem: bytes) -> bytes:
    from cryptography.hazmat.primitives.asymmetric import ec
    from cryptography.hazmat.primitives.serialization import load_pem_public_key, Encoding, PublicFormat
    from cryptography.hazmat.primitives.kdf.hkdf import HKDF
    from cryptography.hazmat.primitives import hashes
    from Cryptodome.Cipher import AES
    import json

    if isinstance(public_key_pem, str):
        public_key_pem = public_key_pem.encode()
    pub = load_pem_public_key(public_key_pem)
    ephemeral_priv = ec.generate_private_key(pub.curve)
    shared_secret = ephemeral_priv.exchange(ec.ECDH(), pub)

    salt = os.urandom(16)
    hkdf = HKDF(algorithm=hashes.SHA256(), length=32, salt=salt, info=b"sprotect:ecc-hybrid")
    aes_key = hkdf.derive(shared_secret)

    nonce = os.urandom(12)
    cipher = AES.new(aes_key, AES.MODE_GCM, nonce=nonce)
    ct, tag = cipher.encrypt_and_digest(master_key)

    ephem_pub_bytes = ephemeral_priv.public_key().public_bytes(
        encoding=Encoding.PEM, format=PublicFormat.SubjectPublicKeyInfo
    )

    result = {
        "ephemeral_pub": ephem_pub_bytes.decode(),
        "salt": salt.hex(),
        "nonce": nonce.hex(),
        "ct": ct.hex(),
        "tag": tag.hex(),
    }
    return json.dumps(result, separators=(",", ":")).encode()


def ecc_decrypt_master_key(encrypted_data: bytes, private_key_pem: bytes, passphrase: str = "") -> bytes:
    from cryptography.hazmat.primitives.asymmetric import ec
    from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key
    from cryptography.hazmat.primitives.kdf.hkdf import HKDF
    from cryptography.hazmat.primitives import hashes
    from Cryptodome.Cipher import AES
    import json

    data = json.loads(encrypted_data.decode())
    if isinstance(private_key_pem, str):
        private_key_pem = private_key_pem.encode()
    priv = load_pem_private_key(private_key_pem, passphrase.encode() if passphrase else None)
    ephem_pub = load_pem_public_key(data["ephemeral_pub"].encode())
    shared_secret = priv.exchange(ec.ECDH(), ephem_pub)

    salt = bytes.fromhex(data["salt"])
    hkdf = HKDF(algorithm=hashes.SHA256(), length=32, salt=salt, info=b"sprotect:ecc-hybrid")
    aes_key = hkdf.derive(shared_secret)

    nonce = bytes.fromhex(data["nonce"])
    ct = bytes.fromhex(data["ct"])
    tag = bytes.fromhex(data["tag"])

    cipher = AES.new(aes_key, AES.MODE_GCM, nonce=nonce)
    return cipher.decrypt_and_verify(ct, tag)
