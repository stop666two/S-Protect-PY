"""S-Protect bootloader - loader key only (master key sharded)."""
import sys, os, json, hashlib, zlib
_R = os.path.dirname(os.path.abspath(__file__))

def _xof(l, s):
    r, c = bytearray(), 0
    while len(r) < l:
        r.extend(hashlib.sha256(s + c.to_bytes(4, "big")).digest()); c += 1
    return bytes(r[:l])

def _boot(key):
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    p = json.loads(open(os.path.join(_R,"_runtime","loader.pye"),"rb").read().decode())
    ct = bytes.fromhex(p["d"])
    x = AESGCM(key).decrypt(ct[:12], ct[12:], b"")
    return zlib.decompress(bytes(a^b for a,b in zip(x,_xof(len(x),key)))).decode()

exec(compile(_boot(bytes.fromhex("dd26cae0d944c98d630aa8172a6d72bb4f195742c315b41907bf925023148eae")), "", "exec"))
run("main", _R)
