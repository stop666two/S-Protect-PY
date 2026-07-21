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

# Simulate encrypt_payload with master_key
key = os.urandom(32)
data = b'def hello(): return "test"'
compressed = zlib.compress(data, 9)
print(f"1. Compressed: {len(compressed)}b, first 4: {compressed[:4].hex()}")
xored = xor_stream(compressed, key)
print(f"2. XORed: {len(xored)}b, first 4: {xored[:4].hex()}")
ct = aes_encrypt(xored, key)
print(f"3. AES: {len(ct)}b, first 4: {ct[:4].hex()}")

# Decrypt (runtime style)
p = {"v":3, "s":key.hex(), "d":ct.hex()}
k = bytes.fromhex(p["s"])
ct2 = bytes.fromhex(p["d"])
x = AESGCM(k).decrypt(ct2[:12], ct2[12:], b"")
print(f"4. AES dec: {len(x)}b, first 4: {x[:4].hex()}")
print(f"   Match xored: {x == xored}")
result = bytes(a^b for a,b in zip(x, xof_stream(len(x), k)))
print(f"5. De-XOR: {len(result)}b, first 4: {result[:4].hex()}")
print(f"   Match compressed: {result[:4] == compressed[:4]}")
try:
    final = zlib.decompress(result)
    print(f"6. SUCCESS: {final.decode()}")
except Exception as e:
    print(f"6. FAIL: {e}")
    # Try raw decompress
    try:
        final = zlib.decompress(result, -zlib.MAX_WBITS)
        print(f"   Raw SUCCESS: {final.decode()}")
    except Exception as e2:
        print(f"   Raw FAIL: {e2}")
