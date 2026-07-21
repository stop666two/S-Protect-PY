import os, json, zlib, hashlib
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def aes_encrypt(data, key):
    nonce = os.urandom(12)
    return nonce + AESGCM(key).encrypt(nonce, data, b"")

def xof_stream(l, s):
    r, c = bytearray(), 0
    while len(r) < l:
        r.extend(hashlib.sha256(s + c.to_bytes(4, "big")).digest()); c += 1
    return bytes(r[:l])

def xor_stream(d, k):
    return bytes(a^b for a,b in zip(d, xof_stream(len(d), k)))

# Test the actual encrypt_payload logic
key = os.urandom(32)
original = b'def hello(): return "test"'
compressed = zlib.compress(original, 9)
print(f"zlib header: {compressed[:2].hex()}")  # should start with 78da or similar

x_key = hashlib.sha256(key).digest()[:32]
print(f"XOR key first 4: {x_key[:4].hex()}")
xored = xor_stream(compressed, x_key)
print(f"XORed first 4: {xored[:4].hex()}")
ct = aes_encrypt(xored, key)
print(f"AES out first 4: {ct[:4].hex()}, len: {len(ct)}")
payload = json.dumps({"v":3, "s":key.hex(), "d":ct.hex()})

# Decrypt like bootloader
import json as _json
p = _json.loads(payload)
k = bytes.fromhex(p["s"])
ct2 = bytes.fromhex(p["d"])
print(f"AES ct2 first 4: {ct2[:4].hex()}, len: {len(ct2)}")
x = AESGCM(k).decrypt(ct2[:12], ct2[12:], b"")
print(f"AES decrypted first 4: {x[:4].hex()}, len: {len(x)}")
print(f"XORed originally: {xored[:4].hex()}")
print(f"Match xored: {x == xored}")
r2_key = hashlib.sha256(k).digest()[:32]
print(f"Rederived XOR key first 4: {r2_key[:4].hex()}")
result = bytes(a^b for a,b in zip(x, xof_stream(len(x), k)))
print(f"Result first 4: {result[:4].hex()}")
print(f"Compressed first 4: {compressed[:4].hex()}")
decompressed = zlib.decompress(result)
print(f"SUCCESS: {decompressed.decode()}")

# Now test with the actual output files
print("\n--- Testing output/_runtime/loader.pye ---")
p2 = _json.loads(open("output/_runtime/loader.pye", "rb").read().decode())
k2 = bytes.fromhex(p2["s"])
d2 = bytes.fromhex(p2["d"])
x2 = AESGCM(k2).decrypt(d2[:12], d2[12:], b"")
r2 = bytes(a^b for a,b in zip(x2, xof_stream(len(x2), k2)))
try:
    dec = zlib.decompress(r2)
    print(f"SUCCESS: {len(dec)} bytes")
except Exception as e:
    print(f"FAIL: {e}")
    # Check if the issue is the XOR layer
    try:
        dec_no_xor = zlib.decompress(x2)
        print(f"Without XOR SUCCESS: {len(dec_no_xor)} bytes")
    except Exception as e2:
        print(f"Without XOR also FAIL: {e2}")
        # Print what we got after AES
        print(f"AES output first 4 hex: {x2[:4].hex()}")
