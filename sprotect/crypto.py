"""Cryptographic utilities: AES-256-GCM primary, HMAC-SHA256 fallback."""

from __future__ import annotations
import os, hashlib, hmac, struct, json
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization


def aes_key() -> bytes:
    return AESGCM.generate_key(bit_length=256)

def aes_encrypt(data: bytes, key: bytes) -> bytes:
    nonce = os.urandom(12)
    return nonce + AESGCM(key).encrypt(nonce, data, b"")

def aes_decrypt(ct: bytes, key: bytes) -> bytes:
    return AESGCM(key).decrypt(ct[:12], ct[12:], b"")

def hmac_xor_encrypt(data: bytes, key: bytes) -> tuple[bytes, str]:
    out = bytearray(len(data))
    for i in range(0, len(data), 32):
        stream = hmac.new(key, (i // 32).to_bytes(8, "big"), "sha256").digest()
        for j, s in enumerate(stream[:len(data) - i]):
            out[i + j] = data[i + j] ^ s
    ct = bytes(out)
    return ct, hmac.new(key, ct, "sha256").hexdigest()

def hmac_xor_decrypt(ct: bytes, key: bytes, sig: str) -> bytes:
    if sig and not hmac.compare_digest(sig, hmac.new(key, ct, "sha256").hexdigest()):
        raise ValueError("HMAC integrity check failed")
    out = bytearray(len(ct))
    for i in range(0, len(ct), 32):
        stream = hmac.new(key, (i // 32).to_bytes(8, "big"), "sha256").digest()
        for j, s in enumerate(stream[:len(ct) - i]):
            out[i + j] = ct[i + j] ^ s
    return bytes(out)

def rsa_keypair() -> tuple[bytes, bytes]:
    pk = rsa.generate_private_key(65537, 4096)
    return (pk.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8, serialization.NoEncryption()),
            pk.public_key().public_bytes(serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo))

def rsa_encrypt(data: bytes, pub: bytes) -> bytes:
    return serialization.load_pem_public_key(pub).encrypt(
        data, padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=None))

def rsa_decrypt(data: bytes, priv: bytes) -> bytes:
    return serialization.load_pem_private_key(priv, None).decrypt(
        data, padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=None))

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def encrypt_payload(source_data: bytes, algorithm: str = "aes-256-gcm") -> bytes:
    if algorithm == "aes-256-gcm":
        key = aes_key()
        ct = aes_encrypt(source_data, key)
        return json.dumps({"a":"aes","k":key.hex(),"d":ct.hex(),"h":sha256(source_data)}).encode()
    else:
        key = os.urandom(32)
        ct, sig = hmac_xor_encrypt(source_data, key)
        return json.dumps({"a":"xor","k":key.hex(),"d":ct.hex(),"h":sig,"s":sha256(source_data)}).encode()

def decrypt_payload(data: bytes) -> tuple[str, str]:
    p = json.loads(data.decode())
    if p["a"] == "aes":
        src = aes_decrypt(bytes.fromhex(p["d"]), bytes.fromhex(p["k"])).decode()
    else:
        src = hmac_xor_decrypt(bytes.fromhex(p["d"]), bytes.fromhex(p["k"]), p["h"]).decode()
    return src, p.get("s", "")
