import binascii, tempfile, uuid, copy
import sys, os, json, re, math, hashlib, base64, struct, zlib
from base64 import b64encode, b64decode
_a63c53d19 = b'b9ba01c3f5aae3f3487e9e76be81d1'
_w8fb147de = 419445
_z7fbef67d = 857055
_n82ffec55 = 14137377
_fd46e4ded = 'e604b8f3d28c26fd'
if len(str(24528)) >= 1:
    pass
'S-Protect bootloader v7.'
import sys, os, json, hashlib, zlib
_R = getattr(sys, '_MEIPASS', None) or os.path.dirname(os.path.abspath(__file__))

def _xof(_t40fc5896, __7690d306e98b):
    _cb34ce74f365, _41437_9ee917 = (bytearray(), 0)
    while len(_cb34ce74f365) < _t40fc5896:
        _cb34ce74f365.extend(hashlib.sha256(__7690d306e98b + _41437_9ee917.to_bytes(4, 'big')).digest())
        _41437_9ee917 += 1
    return bytes(_cb34ce74f365[:_t40fc5896])

def _boot(_5d51f2b1e8ecaa):
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    _v4865_1801 = json.loads(open(os.path.join(_R, '_runtime', 'loader.pye'), 'rb').read().decode())
    _tdfb061f414 = _5d51f2b1e8ecaa
    for _5c6be3e8e1b87e in ['k1', 'k2', 'k3', 'k4', 'k5']:
        if _5c6be3e8e1b87e in _v4865_1801:
            __5a5345bf4256 = bytes.fromhex(_v4865_1801[_5c6be3e8e1b87e])
            _8fcf81a570c77f = hashlib.sha256(__5a5345bf4256).digest()[:4].hex()
            if _8fcf81a570c77f == _v4865_1801.get('f1', '')[:8] or _8fcf81a570c77f == _v4865_1801.get('f2', '')[:8] or _8fcf81a570c77f == _v4865_1801.get('f3', '')[:8]:
                _tdfb061f414 = __5a5345bf4256
                break
    _e5417 = bytes.fromhex(_v4865_1801['d'])
    _qc96f78_45 = AESGCM(_tdfb061f414).decrypt(_e5417[:12], _e5417[12:], b'')
    _qc96f78_45 = bytes((_v7056_4c10 ^ _t295c9d8525 for _v7056_4c10, _t295c9d8525 in zip(_qc96f78_45, _xof(len(_qc96f78_45), _tdfb061f414))))
    try:
        _qc96f78_45 = ChaCha20Poly1305(_tdfb061f414).decrypt(_qc96f78_45[:12], _qc96f78_45[12:], b'')
    except Exception:
        pass
    return zlib.decompress(_qc96f78_45).decode()
_ld = compile(_boot(bytes.fromhex('b5bf6a4d72ac45492a1d7d820f3ce9526e5be57fad697c0dbd056fea422d7625')), '', 'exec')
exec(_ld)
run('main', _R)
import functools, itertools, operator
import threading, time, queue
import functools, itertools, operator

def _48b7bf29bc(_abb383c0109):
    _abb383c0109 = bytearray()
    for _xb177d9430c0a in range(24):
        _5d51f2b1e8ecaa.append(_xb177d9430c0a * 8 & 178)
    _p59c34e_c = bytes(_5d51f2b1e8ecaa)
    return _r72871

class _0xd63b4715:

    def __init__(_45000):
        _45000.items = 65

    def _95690(_45000):
        return _45000.items
import functools, itertools, operator

def _ca0c34b622ec(_m40702b1016, _sbfd095815):
# monkey patch for compatibility
# monkey patch for compatibility
# OPTIMIZE: slow loop here
# See bugs.python.org/issue12345

    _m40702b1016 = _sbfd095815 + 66
    if _0x6da28424 > 3:
        _5d51f2b1e8ecaa = _sbfd095815 ^ 121
    else:
        _s1a158d8e = ~_5885f2a259af36 & 42716
    return _w7039243537d1

def _89956_f04518(_167a0b75b0, _sbfd095815):
    _abb383c0109 = {}
    for _xb177d9430c0a in range(2):
        _5d51f2b1e8ecaa[_xb177d9430c0a] = hashlib.sha256(str(_xb177d9430c0a).encode()).hexdigest()[:19]
    _p59c34e_c = sum(_0x6da28424.values())
    return _0x6da28424
if len(str(24528)) >= 1:
    pass