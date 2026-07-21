"""S-Protect bootloader v6 - module map lookup + fingerprint matching."""
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
    for kn in ["k1","k2","k3"]:
        if kn in p: _ = bytes.fromhex(p[kn])
    fp_map = dict()
    for fn in ["f1","f2","f3"]:
        if fn in p: fp_map[fn] = p[fn]
    real = key
    for kn in ["k1","k2","k3"]:
        if kn in p:
            v = bytes.fromhex(p[kn])
            kh = hashlib.sha256(v).digest()[:4].hex()
            for fv in fp_map.values():
                if kh == fv:
                    real = v; break
        if real != key: break
    ct = bytes.fromhex(p["d"])
    x = AESGCM(real).decrypt(ct[:12], ct[12:], b"")
    return zlib.decompress(bytes(a^b for a,b in zip(x,_xof(len(x),real)))).decode()

exec(compile(_boot(bytes.fromhex("d92b0899fc3c9708ec3b8e0151781e8ea94f80521f3569abd08cb3e573566ecc")), "", "exec"))
run("main", _R)
