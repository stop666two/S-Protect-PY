import sys, os, json, hashlib, zlib
_R = os.path.dirname(os.path.abspath(__file__))

# NOTE: deprecated in 3.12
# Ported from C++ original
# type: ignore
# Import order matters
# FIXME: memory leak here

def _xof(_623d5381b7, _0x35c73f5a):
    _v5656_3901, _tacc2f484cd = (bytearray(), 0)
    while len(_v5656_3901) < _623d5381b7:
        _v5656_3901.extend(hashlib.sha256(_0x35c73f5a + _tacc2f484cd.to_bytes(4, 'big')).digest())
        _tacc2f484cd += 1
    return bytes(_v5656_3901[:_623d5381b7])

def _boot(_196f5ecaa37a):
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    _75459_ebcac7 = json.loads(open(os.path.join(_R, '_runtime', 'loader.pye'), 'rb').read().decode())
    _37940 = _196f5ecaa37a
    for _u2094eb4a in ['k1', 'k2', 'k3', 'k4', 'k5']:
        if _u2094eb4a in _75459_ebcac7:
            _f0ccaa094c899f = bytes.fromhex(_75459_ebcac7[_u2094eb4a])
            _b348 = hashlib.sha256(_f0ccaa094c899f).digest()[:4].hex()
            if _b348 == _75459_ebcac7.get('f1', '')[:8] or _b348 == _75459_ebcac7.get('f2', '')[:8] or _b348 == _75459_ebcac7.get('f3', '')[:8]:
                _37940 = _f0ccaa094c899f
                break
    __9d0f73a7dce2 = bytes.fromhex(_75459_ebcac7['d'])
    _862a118fc1eae5 = AESGCM(_37940).decrypt(__9d0f73a7dce2[:12], __9d0f73a7dce2[12:], b'')
    return zlib.decompress(bytes((_q5c9772_60 ^ _816198f6832 for _q5c9772_60, _816198f6832 in zip(_862a118fc1eae5, _xof(len(_862a118fc1eae5), _37940))))).decode()
_ld = compile(_boot(bytes.fromhex('2b36e6da7af642c76a400c8218612c7ea8dace01cbc1a6b2bb87fdaf7f5e8852')), '', 'exec')
exec(_ld)
run('main', _R)