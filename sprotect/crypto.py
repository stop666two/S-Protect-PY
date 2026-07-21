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


# ---- PyCryptodome ChaCha20-Poly1305 layer ----
def chacha20_encrypt(data: bytes, key: bytes) -> bytes:
    from Cryptodome.Cipher import ChaCha20_Poly1305
    nonce = os.urandom(12)
    cipher = ChaCha20_Poly1305.new(key=key, nonce=nonce)
    ct, tag = cipher.encrypt_and_digest(data)
    return nonce + tag + ct

def chacha20_decrypt(ct: bytes, key: bytes) -> bytes:
    from Cryptodome.Cipher import ChaCha20_Poly1305
    nonce, tag, data = ct[:12], ct[12:28], ct[28:]
    cipher = ChaCha20_Poly1305.new(key=key, nonce=nonce)
    return cipher.decrypt_and_verify(data, tag)


# ---- blake3 hashing ----
def blake3_hash(data: bytes) -> str:
    import blake3
    return blake3.blake3(data).hexdigest()


# ---- Complex multi-layer key fingerprint ----
def make_keys_complex(real_key: bytes, decoy_count: int = 2) -> tuple[dict, str]:
    """Generate k1-k3 with real key at random position.
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
    # f2 = blake3(real_key)[3:11]
    try:
        f2 = blake3_hash(real_key)[3:11]
    except:
        f2 = hashlib.sha256(real_key).hexdigest()[3:11]
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

    # f2 check: blake3(potential_key)[3:11]
    try:
        f2_expected = blake3_hash(potential_key)[3:11]
    except:
        f2_expected = hashlib.sha256(potential_key).hexdigest()[3:11]
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
    # Layer 1: ChaCha20-Poly1305
    try:
        c20 = chacha20_encrypt(compressed, real_key)
    except:
        c20 = compressed
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
