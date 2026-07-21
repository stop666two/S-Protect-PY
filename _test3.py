import os, json, zlib, hashlib
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def xof_stream(l, s):
    r, c = bytearray(), 0
    while len(r) < l:
        r.extend(hashlib.sha256(s + c.to_bytes(4, "big")).digest()); c += 1
    return bytes(r[:l])

# Test with actual loader.pye
os.chdir(r"D:\administrator\Documents\project\S-Protect-PY\output\_runtime")
p = json.loads(open("loader.pye", "rb").read().decode())
print(f"Payload v: {p['v']}")
print(f"Data len: {len(p['d'])}")

# Collect ALL shards
shards = {}
for root, dirs, files in os.walk("."):
    for f in files:
        if f.endswith(".pye") and f != "loader.pye":
            q = json.loads(open(os.path.join(root, f), "rb").read().decode())
            if "s" in q and len(q["s"]) == 64:
                rel = os.path.relpath(os.path.join(root, f), ".")
                shards[rel] = bytes.fromhex(q["s"])

print(f"Shards found: {len(shards)}")
vals = list(shards.values())
mk = bytearray(vals[0])
for v in vals[1:]:
    for i in range(len(mk)): mk[i] ^= v[i]
mk = bytes(mk)
print(f"Master key: {mk.hex()[:16]}...")

# Try to decrypt main.pye
main_p = json.loads(open("main.pye", "rb").read().decode())
print(f"Main 's' field: {main_p['s'][:16]}...")
print(f"Master key == main s: {mk.hex() == main_p['s']}")

ct = bytes.fromhex(main_p["d"])
try:
    x = AESGCM(mk).decrypt(ct[:12], ct[12:], b"")
    result = bytes(a^b for a,b in zip(x, xof_stream(len(x), mk)))
    final = zlib.decompress(result)
    print(f"SUCCESS! {len(final)}b")
except Exception as e:
    print(f"FAIL: {e}")
    # Try with main_p['s'] as key
    try:
        k = bytes.fromhex(main_p["s"])
        x = AESGCM(k).decrypt(ct[:12], ct[12:], b"")
        result = bytes(a^b for a,b in zip(x, xof_stream(len(x), k)))
        final = zlib.decompress(result)
        print(f"With s field as key: SUCCESS! {len(final)}b")
    except Exception as e2:
        print(f"With s field as key: FAIL: {e2}")
