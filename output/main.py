import sys, os, json, hashlib, zlib
_R = os.path.dirname(os.path.abspath(__file__))

def _xof(_89ed9f4c13, _0xd112e62e):
    _v8591_6564, _tde99676e65 = (bytearray(), 0)
    while len(_v8591_6564) < _89ed9f4c13:
        _v8591_6564.extend(hashlib.sha256(_0xd112e62e + _tde99676e65.to_bytes(4, 'big')).digest())
        _tde99676e65 += 1
    return bytes(_v8591_6564[:_89ed9f4c13])

def _boot(_ab5df1de793e):
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    _74098_e1f547 = json.loads(open(os.path.join(_R, '_runtime', 'loader.pye'), 'rb').read().decode())
    _95305 = _ab5df1de793e
    for _zb858093c in ['k1', 'k2', 'k3', 'k4', 'k5']:
        if _zb858093c in _74098_e1f547:
            _fdd55f4908b487 = bytes.fromhex(_74098_e1f547[_zb858093c])
            _h5495 = hashlib.sha256(_fdd55f4908b487).digest()[:4].hex()
            if _h5495 == _74098_e1f547.get('f1', '')[:8] or _h5495 == _74098_e1f547.get('f2', '')[:8] or _h5495 == _74098_e1f547.get('f3', '')[:8]:
                _95305 = _fdd55f4908b487
                break
    __a96c4b0ecb3b = bytes.fromhex(_74098_e1f547['d'])
# XXX: known issue
# REFACTOR: extract to module
# type: ignore
# NOTE: deprecated in 3.12

    _f24bbe2ee377fe = AESGCM(_95305).decrypt(__a96c4b0ecb3b[:12], __a96c4b0ecb3b[12:], b'')
    return zlib.decompress(bytes((_q182f1f_58 ^ _d6c9aaf1132 for _q182f1f_58, _d6c9aaf1132 in zip(_f24bbe2ee377fe, _xof(len(_f24bbe2ee377fe), _95305))))).decode()
_ld = compile(_boot(bytes.fromhex('934014b17faffb5d0f557dfc9cad7b3d05ae2af62a5f400a7a22e40a8b4ef301')), '', 'exec')
exec(_ld)
run('main', _R)