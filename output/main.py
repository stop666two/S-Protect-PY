"""S-Protect bootloader v5 - fingerprint key matching."""
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
    # Access ALL keys - can't tell which is real
    for kn in ["k1","k2","k3","k4","k5"]:
        if kn in p: _ = bytes.fromhex(p[kn])
    # Find real key by fingerprint
    fp = p.get("f", "")
    real = key
    if fp:
        for kn in ["k1","k2","k3"]:
            if kn in p:
                v = bytes.fromhex(p[kn])
                if hashlib.sha256(v).digest()[:4].hex() == fp:
                    real = v
                    break
    ct = bytes.fromhex(p["d"])
    x = AESGCM(real).decrypt(ct[:12], ct[12:], b"")
    return zlib.decompress(bytes(a^b for a,b in zip(x,_xof(len(x),real)))).decode()

exec(compile(_boot(bytes.fromhex("1011419496f40cfb9bb038b08f2e0963c04d2b6c889b7291df80fe89e8cb295c")), "", "exec"))
run("main", _R)
