import os, json, msgpack, zlib, hashlib
os.chdir(r"D:\administrator\Documents\project\S-Protect-PY\output\_runtime")
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# Load loader.pye
raw = open("loader.pye", "rb").read()
p = msgpack.unpackb(raw[3:], strict_map_key=False)
d = p.get(2, b"")
ks = p.get(3, [b""]*5)
f = p.get(1, 0)
pos = (f >> 3) & 7
trap = (f >> 7) & 1
print(f"Flags: {f}, pos: {pos}, trap: {trap}")
k = ks[pos] if pos < len(ks) else ks[0]
for k2 in [k, ks[0]]:
    try:
        x = AESGCM(k2).decrypt(d[:12], d[12:], b"")
        src = zlib.decompress(x).decode()
        print(f"Decrypted OK, len={len(src)}")
        print(f"Has 'def run': {'def run' in src}")
        # Show first 200 chars
        print("---")
        print(src[:200])
        print("---")
        break
    except Exception as e:
        print(f"Fail with {k2.hex()[:8]}: {e}")
