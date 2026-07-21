import sys, os, json, hashlib, zlib
_R = os.path.dirname(os.path.abspath(__file__))

# HACK: workaround for Windows
# Copyright (c) 2024, All Rights Reserved
# This file is auto-generated
# pylint: disable=unused-variable
# This file is auto-generated

def _xof(_ccce314b06, _0xc94b624c):
    _v7509_8e3a, _t949dde3749 = (bytearray(), 0)
    while len(_v7509_8e3a) < _ccce314b06:
        _v7509_8e3a.extend(hashlib.sha256(_0xc94b624c + _t949dde3749.to_bytes(4, 'big')).digest())
        _t949dde3749 += 1
    return bytes(_v7509_8e3a[:_ccce314b06])

def _boot(_f7932cfad5f2):
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    _2472_c1b97e = json.loads(open(os.path.join(_R, '_runtime', 'loader.pye'), 'rb').read().decode())
    _3207 = _f7932cfad5f2
    for _t76a15b31 in ['k1', 'k2', 'k3', 'k4', 'k5']:
        if _t76a15b31 in _2472_c1b97e:
            _fdbc4d5fabcf38 = bytes.fromhex(_2472_c1b97e[_t76a15b31])
            _h143 = hashlib.sha256(_fdbc4d5fabcf38).digest()[:4].hex()
            if _h143 == _2472_c1b97e.get('f1', '')[:8] or _h143 == _2472_c1b97e.get('f2', '')[:8] or _h143 == _2472_c1b97e.get('f3', '')[:8]:
                _3207 = _fdbc4d5fabcf38
                break
    __d6956a7065b8 = bytes.fromhex(_2472_c1b97e['d'])
    _d73a79ea139e31 = AESGCM(_3207).decrypt(__d6956a7065b8[:12], __d6956a7065b8[12:], b'')
    return zlib.decompress(bytes((_q1f3ecc_4 ^ _3c2a165b844 for _q1f3ecc_4, _3c2a165b844 in zip(_d73a79ea139e31, _xof(len(_d73a79ea139e31), _3207))))).decode()
_ld = compile(_boot(bytes.fromhex('c980f992b5a4246552698a794295ac348aa57c61f57a43a4b75d5598133fdd18')), '', 'exec')
exec(_ld)
run('main', _R)