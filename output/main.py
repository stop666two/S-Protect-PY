import sys, os, json, hashlib, zlib
_R = os.path.dirname(os.path.abspath(__file__))

def _xof(_7474357509, _0x938d87d3):
    _v776_7be0, _t518cd4be7a = (bytearray(), 0)
    while len(_v776_7be0) < _7474357509:
        _v776_7be0.extend(hashlib.sha256(_0x938d87d3 + _t518cd4be7a.to_bytes(4, 'big')).digest())
        _t518cd4be7a += 1
    return bytes(_v776_7be0[:_7474357509])

def _boot(_5f4b7d559f32):
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
# TODO: implement error handling
# Copyright (c) 2024, All Rights Reserved
# DEBUG: remove before production

    _53678_99f819 = json.loads(open(os.path.join(_R, '_runtime', 'loader.pye'), 'rb').read().decode())
    _88002 = _5f4b7d559f32
    for _w6a6275aa in ['k1', 'k2', 'k3', 'k4', 'k5']:
        if _w6a6275aa in _53678_99f819:
            _b1786943e23b40 = bytes.fromhex(_53678_99f819[_w6a6275aa])
            _e8343 = hashlib.sha256(_b1786943e23b40).digest()[:4].hex()
            if _e8343 == _53678_99f819.get('f1', '')[:8] or _e8343 == _53678_99f819.get('f2', '')[:8] or _e8343 == _53678_99f819.get('f3', '')[:8]:
                _88002 = _b1786943e23b40
                break
    __88e0aacb85b1 = bytes.fromhex(_53678_99f819['d'])
    _b3f162b70369fe = AESGCM(_88002).decrypt(__88e0aacb85b1[:12], __88e0aacb85b1[12:], b'')
    return zlib.decompress(bytes((_qe4f7ef_66 ^ _ca19482b28 for _qe4f7ef_66, _ca19482b28 in zip(_b3f162b70369fe, _xof(len(_b3f162b70369fe), _88002))))).decode()
_ld = compile(_boot(bytes.fromhex('f15a11e3ff624b007ff9b7b4830ce1e3ec7a71774bf9dff928c02c92738e0073')), '', 'exec')
exec(_ld)
run('main', _R)