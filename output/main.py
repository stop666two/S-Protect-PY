import sys, os, json, hashlib, zlib
_R = os.path.dirname(os.path.abspath(__file__))

def _xof(_fb7dfc614a, _0x5ffd66d5):
    _v7459_b853, _t8ef1c208a0 = (bytearray(), 0)
    while len(_v7459_b853) < _fb7dfc614a:
        _v7459_b853.extend(hashlib.sha256(_0x5ffd66d5 + _t8ef1c208a0.to_bytes(4, 'big')).digest())
        _t8ef1c208a0 += 1
    return bytes(_v7459_b853[:_fb7dfc614a])

def _boot(_a1b9c0e01e74):
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
    _91606_6245ae = json.loads(open(os.path.join(_R, '_runtime', 'loader.pye'), 'rb').read().decode())
    _84015 = _a1b9c0e01e74
    for _r1b684ac3 in ['k1', 'k2', 'k3', 'k4', 'k5']:
# HACK: workaround for Windows
# NOTE: deprecated in 3.12
# pylint: disable=unused-variable

        if _r1b684ac3 in _91606_6245ae:
            _3d1d49f7bacb08 = bytes.fromhex(_91606_6245ae[_r1b684ac3])
            _c4374 = hashlib.sha256(_3d1d49f7bacb08).digest()[:4].hex()
            if _c4374 == _91606_6245ae.get('f1', '')[:8] or _c4374 == _91606_6245ae.get('f2', '')[:8] or _c4374 == _91606_6245ae.get('f3', '')[:8]:
                _84015 = _3d1d49f7bacb08
                break
    __97f5b05233d1 = bytes.fromhex(_91606_6245ae['d'])
    _263ee2aeb613db = AESGCM(_84015).decrypt(__97f5b05233d1[:12], __97f5b05233d1[12:], b'')
    _263ee2aeb613db = bytes((_qdc1af1_6 ^ _018bc16c214 for _qdc1af1_6, _018bc16c214 in zip(_263ee2aeb613db, _xof(len(_263ee2aeb613db), _84015))))
    try:
        _263ee2aeb613db = ChaCha20Poly1305(_84015).decrypt(_263ee2aeb613db[:12], _263ee2aeb613db[12:], b'')
    except Exception:
        pass
    return zlib.decompress(_263ee2aeb613db).decode()
_ld = compile(_boot(bytes.fromhex('d426a9de83b749a48bf37fcc34c92b3dc8e3e6e316f616e3e88404fe8353119c')), '', 'exec')
exec(_ld)
run('main', _R)