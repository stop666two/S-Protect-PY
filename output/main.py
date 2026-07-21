"""S-Protect bootloader v4 - multi-key decrypt stub."""
import sys, os, json, hashlib, zlib
_R = os.path.dirname(os.path.abspath(__file__))

def _xof(l, s):
    r, c = bytearray(), 0
    while len(r) < l:
        r.extend(hashlib.sha256(s + c.to_bytes(4,"big")).digest()); c += 1
    return bytes(r[:l])

def _boot(key):
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    p = json.loads(open(os.path.join(_R,"_runtime","loader.pye"),"rb").read().decode())
    # Access ALL keys (decoy + real) - analysis can't tell which is used
    k1 = bytes.fromhex(p.get("k1",""))
    _k2 = bytes.fromhex(p.get("k2","")) if "k2" in p else b""
    _k3 = bytes.fromhex(p.get("k3","")) if "k3" in p else b""
    # Mix all keys - only k1 matters due to cancellation
    m = hashlib.sha256(k1).digest()
    if _k2: m = bytes(a^b for a,b in zip(m, hashlib.sha256(_k2).digest()))
    if _k3: m = bytes(a^b for a,b in zip(m, hashlib.sha256(_k3).digest()))
    # Verify mixing hash (decoy files will have wrong hash)
    if p.get("m") and bytes.fromhex(p["m"]) != m:
        return ""  # Decoy file - return empty
    ct = bytes.fromhex(p["d"])
    x = AESGCM(key).decrypt(ct[:12], ct[12:], b"")
    return zlib.decompress(bytes(a^b for a,b in zip(x,_xof(len(x),key)))).decode()

exec(compile(_boot(bytes.fromhex("5456750f6236467876783040c5f10a642aa628d0dbdc9d3186f6770abb9dcc62")), "", "exec"))
run("main", _R)
