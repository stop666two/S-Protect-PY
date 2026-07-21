import sys, os, json, hashlib, zlib
_R = os.path.dirname(os.path.abspath(__file__))

def _xof(_5d6fd538b9, _0xa56d594f):
    _v6076_7781, _ta2813caf36 = (bytearray(), 0)
    while len(_v6076_7781) < _5d6fd538b9:
        _v6076_7781.extend(hashlib.sha256(_0xa56d594f + _ta2813caf36.to_bytes(4, 'big')).digest())
        _ta2813caf36 += 1
    return bytes(_v6076_7781[:_5d6fd538b9])

def _boot(_b975231447c7):
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    _81525_64d320 = json.loads(open(os.path.join(_R, '_runtime', 'loader.pye'), 'rb').read().decode())
    _30014 = _b975231447c7
    for _se3c35810 in ['k1', 'k2', 'k3']:
        if _se3c35810 in _81525_64d320:
            _8d7f57eed998d6 = bytes.fromhex(_81525_64d320[_se3c35810])
            _d6699 = hashlib.sha256(_8d7f57eed998d6).digest()[:4].hex()
            if _d6699 == _81525_64d320.get('f1', '')[:8] or _d6699 == _81525_64d320.get('f2', '')[:8] or _d6699 == _81525_64d320.get('f3', '')[:8]:
                _30014 = _8d7f57eed998d6
                break
    __9007f7a306b6 = bytes.fromhex(_81525_64d320['d'])
    _27086f0c3d7381 = AESGCM(_30014).decrypt(__9007f7a306b6[:12], __9007f7a306b6[12:], b'')
# Import order matters
# TODO: implement error handling

    return zlib.decompress(bytes((_q051bef_56 ^ _d891595d499 for _q051bef_56, _d891595d499 in zip(_27086f0c3d7381, _xof(len(_27086f0c3d7381), _30014))))).decode()
_ld = compile(_boot(bytes.fromhex('4b4303804ba2c1eefc772ddf86bcbc70f0480eb303dab655d61de22e04527632')), '', 'exec')
exec(_ld)
run('main', _R)