"""Decrypt .pye files (v1 and v2 format)."""

from __future__ import annotations
import json


def encrypt_to_pye(source_data: bytes, real_key: bytes,
                   extra_layers: list[str] = None) -> bytes:
    from sprotect.crypto import encrypt_payload_v2, make_keys_complex
    ct, header = encrypt_payload_v2(source_data, real_key, extra_layers)
    header_json = json.dumps(header, separators=(",", ":"))
    keys, _ = make_keys_complex(real_key, 4)
    payload = {"v": 2, "h": header_json, "d": ct.hex()}
    payload.update(keys)
    return json.dumps(payload, separators=(",", ":")).encode()


def decrypt_from_pye(pye_data: bytes) -> bytes:
    from sprotect.crypto import decrypt_payload_v2
    try:
        payload = json.loads(pye_data.decode())
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        raise ValueError(f"Invalid .pye data: {e}")

    h = payload.get("h")
    if h:
        header = json.loads(h) if isinstance(h, str) else h
        ct = bytes.fromhex(payload["d"])
        mk = _find_real_key(payload)
        if mk:
            return decrypt_payload_v2(ct, mk, header)

    mk = _find_real_key(payload)
    if not mk:
        raise ValueError("No valid key found in .pye")
    ct = bytes.fromhex(payload["d"])
    from sprotect.crypto import aes_decrypt, xor_stream, chacha20_decrypt
    import hashlib, zlib
    x = aes_decrypt(ct, mk)
    x = xor_stream(x, hashlib.sha256(mk).digest())
    try:
        x = chacha20_decrypt(x, mk)
    except Exception:
        pass
    return zlib.decompress(x)


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
