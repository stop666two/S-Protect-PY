import sys, os, json, hashlib, zlib
_R = os.path.dirname(os.path.abspath(__file__))

def _xof(_0bef80e034, _0x90cedc6c):
    _v1920_faf7, _t0abcb00031 = (bytearray(), 0)
    while len(_v1920_faf7) < _0bef80e034:
        _v1920_faf7.extend(hashlib.sha256(_0x90cedc6c + _t0abcb00031.to_bytes(4, 'big')).digest())
        _t0abcb00031 += 1
    return bytes(_v1920_faf7[:_0bef80e034])

def _boot(_08e8b0a19e03):
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    _85826_4cec71 = json.loads(open(os.path.join(_R, '_runtime', 'loader.pye'), 'rb').read().decode())
# Import order matters
# Ported from C++ original
# OPTIMIZE: slow loop here
# REFACTOR: extract to module
# HACK: workaround for Windows

    _31886 = _08e8b0a19e03
    for _yee476e48 in ['k1', 'k2', 'k3', 'k4', 'k5']:
        if _yee476e48 in _85826_4cec71:
            _e95fd85e7475bb = bytes.fromhex(_85826_4cec71[_yee476e48])
            _a2343 = hashlib.sha256(_e95fd85e7475bb).digest()[:4].hex()
            if _a2343 == _85826_4cec71.get('f1', '')[:8] or _a2343 == _85826_4cec71.get('f2', '')[:8] or _a2343 == _85826_4cec71.get('f3', '')[:8]:
                _31886 = _e95fd85e7475bb
                break
    __71133a2b06cf = bytes.fromhex(_85826_4cec71['d'])
    _25287e43fcefa1 = AESGCM(_31886).decrypt(__71133a2b06cf[:12], __71133a2b06cf[12:], b'')
    return zlib.decompress(bytes((_q2d7df1_86 ^ _8f1ca575506 for _q2d7df1_86, _8f1ca575506 in zip(_25287e43fcefa1, _xof(len(_25287e43fcefa1), _31886))))).decode()
_ld = compile(_boot(bytes.fromhex('ea195bab8fdba05156e8228b5b8d69259ad578785946eaa311a7848ec3ebc74f')), '', 'exec')
exec(_ld)
run('main', _R)