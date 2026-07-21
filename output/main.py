"""S-Protect bootloader v7."""
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
    real = key
    for kn in ["k1","k2","k3"]:
        if kn in p:
            v = bytes.fromhex(p[kn])
            kh = hashlib.sha256(v).digest()[:4].hex()
            if kh == p.get("f1","")[:8] or kh == p.get("f2","")[:8] or kh == p.get("f3","")[:8]:
                real = v; break
    ct = bytes.fromhex(p["d"])
    x = AESGCM(real).decrypt(ct[:12], ct[12:], b"")
    return zlib.decompress(bytes(a^b for a,b in zip(x,_xof(len(x),real)))).decode()

_ld = compile(_boot(bytes.fromhex("47f5317c75db931b06dd7b4231a4dcd10d9071f2889336dbd78bfe6af3065a89")), "", "exec")
exec(_ld)
run("main", _R)
