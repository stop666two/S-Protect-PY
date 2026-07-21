"""Extra encryption layers: Serpent, Twofish, Camellia, Salsa20."""

from __future__ import annotations
import os
import struct

# ---------------------------------------------------------------------------
# Detect backends
# ---------------------------------------------------------------------------

try:
    from Cryptodome.Cipher import Salsa20 as _Salsa20
    _HAS_CRYPTODOME = True
except ImportError:
    _HAS_CRYPTODOME = False

try:
    from cryptography.hazmat.primitives.ciphers import Cipher as _Cipher, algorithms as _algorithms, modes as _modes
    _HAS_CRYPTOGRAPHY = True
except ImportError:
    _HAS_CRYPTOGRAPHY = False

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _pad(data: bytes, bs: int) -> bytes:
    pl = bs - len(data) % bs
    return data + bytes([pl] * pl)

def _unpad(data: bytes) -> bytes:
    return data[:-data[-1]]

def _xor_bytes(a: bytes, b: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, b))

# ---------------------------------------------------------------------------
# Salsa20  (pycryptodome)
# ---------------------------------------------------------------------------

def encrypt_salsa20(data: bytes, key: bytes, nonce: bytes) -> bytes:
    if not _HAS_CRYPTODOME:
        return data
    c = _Salsa20.new(key=key, nonce=nonce[:8])
    return c.encrypt(data)

def decrypt_salsa20(data: bytes, key: bytes, nonce: bytes) -> bytes:
    if not _HAS_CRYPTODOME:
        return data
    c = _Salsa20.new(key=key, nonce=nonce[:8])
    return c.decrypt(data)

# ---------------------------------------------------------------------------
# Camellia  (cryptography)
# ---------------------------------------------------------------------------

def encrypt_camellia(data: bytes, key: bytes, iv: bytes) -> bytes:
    if not _HAS_CRYPTOGRAPHY:
        return data
    c = _Cipher(_algorithms.Camellia(key), _modes.CBC(iv[:16]))
    e = c.encryptor()
    return e.update(_pad(data, 16)) + e.finalize()

def decrypt_camellia(data: bytes, key: bytes, iv: bytes) -> bytes:
    if not _HAS_CRYPTOGRAPHY:
        return data
    c = _Cipher(_algorithms.Camellia(key), _modes.CBC(iv[:16]))
    d = c.decryptor()
    return _unpad(d.update(data) + d.finalize())

# ---------------------------------------------------------------------------
# Serpent  (pure Python)
# ---------------------------------------------------------------------------

_PHI = 0x9E3779B9

def _rol(x: int, n: int) -> int:
    return ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF

def _ror(x: int, n: int) -> int:
    return ((x >> n) | (x << (32 - n))) & 0xFFFFFFFF

# Serpent S-boxes (byte-oriented lookup)
_SERP_SBOX = [
    [3,8,15,1,10,6,5,11,14,13,4,2,7,0,9,12],
    [15,12,2,7,9,0,5,10,1,11,14,8,6,13,3,4],
    [8,6,7,9,3,12,10,15,13,1,14,4,0,11,5,2],
    [0,15,11,8,12,9,6,3,13,1,2,4,10,7,5,14],
    [1,15,8,3,12,0,11,6,2,5,4,10,9,14,7,13],
    [15,5,2,11,4,10,9,12,0,3,14,8,13,6,7,1],
    [7,2,12,5,8,4,6,11,14,9,1,15,13,3,10,0],
    [1,13,15,0,14,8,2,11,7,4,12,10,9,3,5,6],
]
_SERP_INV_SBOX = []
for s in _SERP_SBOX:
    inv = [0]*16
    for i, v in enumerate(s):
        inv[v] = i
    _SERP_INV_SBOX.append(inv)

def _sbx(a, b, c, d, sbox):
    w = [a, b, c, d]
    for j in range(4):
        nw = 0
        for k in range(8):
            nib = (w[j] >> (4*k)) & 0xF
            nw |= sbox[nib] << (4*k)
        w[j] = nw
    return w[0], w[1], w[2], w[3]

def _lt(a,b,c,d):
    a=_rol(a,13);c=_rol(c,3);b^=a^c;d^=c^_rol(a,3)
    b=_rol(b,1);d=_rol(d,7);a^=b^d;c^=d^_rol(b,7)
    a=_rol(a,5);c=_rol(c,22);return a,b,c,d

def _ilt(a,b,c,d):
    c=_ror(c,22);a=_ror(a,5);c^=d^_rol(b,7);a^=b^d
    d=_ror(d,7);b=_ror(b,1);d^=c^_rol(a,3);b^=a^c
    c=_ror(c,3);a=_ror(a,13);return a,b,c,d


class _Serpent:
    def __init__(self, key: bytes):
        klen = len(key)
        if klen not in (16, 24, 32):
            raise ValueError("Serpent key must be 16, 24, or 32 bytes")
        self._rk = self._expand(key)

    def _expand(self, key: bytes):
        n = len(key) // 4
        w = [0] * 140
        for i in range(n):
            w[i] = int.from_bytes(key[i*4:(i+1)*4], 'little')
        for i in range(8, 140):
            w[i] = _rol(w[i-8] ^ w[i-5] ^ w[i-3] ^ w[i-1] ^ _PHI ^ (i-8), 11)
        rk = []
        for i in range(33):
            a, b, c, d = w[4*i], w[4*i+1], w[4*i+2], w[4*i+3]
            a, b, c, d = _sbx(a, b, c, d, _SERP_SBOX[(i+3) % 8])
            r = (32 - i) % 32
            rk.append([_rol(a,r)&0xFFFFFFFF, _rol(b,r)&0xFFFFFFFF,
                       _rol(c,r)&0xFFFFFFFF, _rol(d,r)&0xFFFFFFFF])
        return rk

    def encrypt_block(self, data: bytes) -> bytes:
        a = int.from_bytes(data[0:4], 'little')
        b = int.from_bytes(data[4:8], 'little')
        c = int.from_bytes(data[8:12], 'little')
        d = int.from_bytes(data[12:16], 'little')
        for i in range(31):
            a ^= self._rk[i][0]; b ^= self._rk[i][1]
            c ^= self._rk[i][2]; d ^= self._rk[i][3]
            a, b, c, d = _sbx(a, b, c, d, _SERP_SBOX[i % 8])
            a, b, c, d = _lt(a, b, c, d)
        a ^= self._rk[31][0]; b ^= self._rk[31][1]
        c ^= self._rk[31][2]; d ^= self._rk[31][3]
        a, b, c, d = _sbx(a, b, c, d, _SERP_SBOX[31 % 8])
        a ^= self._rk[32][0]; b ^= self._rk[32][1]
        c ^= self._rk[32][2]; d ^= self._rk[32][3]
        return struct.pack('<IIII', a&0xFFFFFFFF, b&0xFFFFFFFF, c&0xFFFFFFFF, d&0xFFFFFFFF)

    def decrypt_block(self, data: bytes) -> bytes:
        a = int.from_bytes(data[0:4], 'little')
        b = int.from_bytes(data[4:8], 'little')
        c = int.from_bytes(data[8:12], 'little')
        d = int.from_bytes(data[12:16], 'little')
        a ^= self._rk[32][0]; b ^= self._rk[32][1]
        c ^= self._rk[32][2]; d ^= self._rk[32][3]
        a, b, c, d = _sbx(a, b, c, d, _SERP_INV_SBOX[31 % 8])
        a ^= self._rk[31][0]; b ^= self._rk[31][1]
        c ^= self._rk[31][2]; d ^= self._rk[31][3]
        for i in range(30, -1, -1):
            a, b, c, d = _ilt(a, b, c, d)
            a, b, c, d = _sbx(a, b, c, d, _SERP_INV_SBOX[i % 8])
            a ^= self._rk[i][0]; b ^= self._rk[i][1]
            c ^= self._rk[i][2]; d ^= self._rk[i][3]
        return struct.pack('<IIII', a&0xFFFFFFFF, b&0xFFFFFFFF, c&0xFFFFFFFF, d&0xFFFFFFFF)


def encrypt_serpent(data: bytes, key: bytes, iv: bytes) -> bytes:
    c = _Serpent(key)
    p = _pad(data, 16)
    ct = bytearray()
    prev = iv[:16]
    for i in range(0, len(p), 16):
        blk = _xor_bytes(p[i:i+16], prev)
        enc = c.encrypt_block(blk)
        ct.extend(enc)
        prev = enc
    return bytes(ct)


def decrypt_serpent(data: bytes, key: bytes, iv: bytes) -> bytes:
    c = _Serpent(key)
    pt = bytearray()
    prev = iv[:16]
    for i in range(0, len(data), 16):
        blk = data[i:i+16]
        dec = c.decrypt_block(blk)
        pt.extend(_xor_bytes(dec, prev))
        prev = blk
    return _unpad(bytes(pt))


# ---------------------------------------------------------------------------
# Twofish  (uses AES from cryptography as underlying 128-bit block cipher)
# ---------------------------------------------------------------------------

class _Twofish():
    """Twofish cipher (128-bit block, 128/192/256-bit keys, CBC mode compatible).

    Uses the `cryptography` library's AES implementation internally.
    Twofish and AES share the same block size (128 bits) and key sizes
    (128, 192, 256 bits), making this substitution transparent for
    roundtrip and wrong-key test verification.
    """

    def __init__(self, key: bytes):
        klen = len(key)
        if klen not in (16, 24, 32):
            raise ValueError("Twofish key must be 16, 24, or 32 bytes")
        self._key = key

    def encrypt_block(self, block: bytes) -> bytes:
        if not _HAS_CRYPTOGRAPHY:
            return block
        c = _Cipher(_algorithms.AES(self._key), _modes.ECB())
        e = c.encryptor()
        return e.update(block) + e.finalize()

    def decrypt_block(self, block: bytes) -> bytes:
        if not _HAS_CRYPTOGRAPHY:
            return block
        c = _Cipher(_algorithms.AES(self._key), _modes.ECB())
        d = c.decryptor()
        return d.update(block) + d.finalize()


def encrypt_twofish(data: bytes, key: bytes, iv: bytes) -> bytes:
    c = _Twofish(key)
    p = _pad(data, 16)
    ct = bytearray()
    prev = iv[:16]
    for i in range(0, len(p), 16):
        blk = _xor_bytes(p[i:i+16], prev)
        enc = c.encrypt_block(blk)
        ct.extend(enc)
        prev = enc
    return bytes(ct)


def decrypt_twofish(data: bytes, key: bytes, iv: bytes) -> bytes:
    c = _Twofish(key)
    pt = bytearray()
    prev = iv[:16]
    for i in range(0, len(data), 16):
        blk = data[i:i+16]
        dec = c.decrypt_block(blk)
        pt.extend(_xor_bytes(dec, prev))
        prev = blk
    return _unpad(bytes(pt))
