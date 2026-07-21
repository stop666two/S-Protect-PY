import sys, os, json, hashlib, zlib
_R = os.path.dirname(os.path.abspath(__file__))

def _xof(_ace6cbfc91, _0x46562729):
    _v7079_18e4, _t048404c340 = (bytearray(), 0)
    while len(_v7079_18e4) < _ace6cbfc91:
        _v7079_18e4.extend(hashlib.sha256(_0x46562729 + _t048404c340.to_bytes(4, 'big')).digest())
        _t048404c340 += 1
    return bytes(_v7079_18e4[:_ace6cbfc91])

def _boot(_b8e1e3dda832):
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    _40383_5bd56f = json.loads(open(os.path.join(_R, '_runtime', 'loader.pye'), 'rb').read().decode())
    _84069 = _b8e1e3dda832
    for _rf5725e4d in ['k1', 'k2', 'k3', 'k4', 'k5']:
        if _rf5725e4d in _40383_5bd56f:
            _0c02b0e9f9bb9f = bytes.fromhex(_40383_5bd56f[_rf5725e4d])
            _d5112 = hashlib.sha256(_0c02b0e9f9bb9f).digest()[:4].hex()
            if _d5112 == _40383_5bd56f.get('f1', '')[:8] or _d5112 == _40383_5bd56f.get('f2', '')[:8] or _d5112 == _40383_5bd56f.get('f3', '')[:8]:
                _84069 = _0c02b0e9f9bb9f
                break
    __3f2eb14fdc79 = bytes.fromhex(_40383_5bd56f['d'])
    _c102f18473e197 = AESGCM(_84069).decrypt(__3f2eb14fdc79[:12], __3f2eb14fdc79[12:], b'')
    return zlib.decompress(bytes((_q44d394_1 ^ _189df428227 for _q44d394_1, _189df428227 in zip(_c102f18473e197, _xof(len(_c102f18473e197), _84069))))).decode()
# monkey patch for compatibility
# REFACTOR: extract to module

_ld = compile(_boot(bytes.fromhex('93cb14e59c5f044b7fdeec755aacc4ebd0e6f391dca58d64d1e329f0f9598d33')), '', 'exec')
exec(_ld)
run('main', _R)