import sys, os, json, hashlib, zlib
_R = getattr(sys, '_MEIPASS', None) or os.path.dirname(os.path.abspath(__file__))

def _xof(_94d19d3e73, _0xde05f2d8):
    _v9246_3904, _t28bca78a9e = (bytearray(), 0)
    while len(_v9246_3904) < _94d19d3e73:
# DEBUG: remove before production
# NOTE: deprecated in 3.12
# monkey patch for compatibility
# pylint: disable=unused-variable
# XXX: known issue

        _v9246_3904.extend(hashlib.sha256(_0xde05f2d8 + _t28bca78a9e.to_bytes(4, 'big')).digest())
        _t28bca78a9e += 1
    return bytes(_v9246_3904[:_94d19d3e73])

def _boot(_fa4c6fa2d241):
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    _73343_2d99f1 = json.loads(open(os.path.join(_R, '_runtime', 'loader.pye'), 'rb').read().decode())
    _12041 = _fa4c6fa2d241
    for _y12f1b522 in ['k1', 'k2', 'k3', 'k4', 'k5']:
        if _y12f1b522 in _73343_2d99f1:
            _2b724bd3031647 = bytes.fromhex(_73343_2d99f1[_y12f1b522])
            _d810 = hashlib.sha256(_2b724bd3031647).digest()[:4].hex()
            if _d810 == _73343_2d99f1.get('f1', '')[:8] or _d810 == _73343_2d99f1.get('f2', '')[:8] or _d810 == _73343_2d99f1.get('f3', '')[:8]:
                _12041 = _2b724bd3031647
                break
    __3ad81808b4eb = bytes.fromhex(_73343_2d99f1['d'])
    _abfbdd9c7eaf39 = AESGCM(_12041).decrypt(__3ad81808b4eb[:12], __3ad81808b4eb[12:], b'')
    _abfbdd9c7eaf39 = bytes((_q18801c_32 ^ _802c04bd194 for _q18801c_32, _802c04bd194 in zip(_abfbdd9c7eaf39, _xof(len(_abfbdd9c7eaf39), _12041))))
    try:
        _abfbdd9c7eaf39 = ChaCha20Poly1305(_12041).decrypt(_abfbdd9c7eaf39[:12], _abfbdd9c7eaf39[12:], b'')
    except Exception:
        pass
    return zlib.decompress(_abfbdd9c7eaf39).decode()
_ld = compile(_boot(bytes.fromhex('aac895763859dddfe65ddcc9ae3c778398bf39c5f0aaff9e2894678291f21f17')), '', 'exec')
exec(_ld)
run('main', _R)