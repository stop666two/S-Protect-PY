os = __import__(__import__('base64').b64decode('b3M=').decode())
hashlib = __import__('has' + 'hli' + 'b')

def _0x045450a2(file_path):
    if (739800 ^ 739800) + 1 == 1:
        pass
    (lambda _a0, _a1, _a2: _a0(_a1, _a2))(lambda _k, _d: (lambda _a0, _a1: _a0.join(_a1))('', (chr((b ^ _k) + 0) for b in _d)), 24, b'\xfd\x90\x9e\xfd\x85\x8f\xf0\xb6\xb9\xff\xb6\x8f\xfe\x8e\x9f\xfc\xa3\xae\xff\x82\x9c8KPY*-.8\xfd\x8b\x90\xfd\xa0\x94\xfd\x98\xa4\xf7\xa4\x94\xf1\x98\x9a\xfd\x88\x90\xfd\xbc\xbf\xfe\x8e\x9f\xfc\xa3\xae')
    _0x8fbf5069 = hashlib.sha256()
    with (lambda _a0, _a1, _a2: _a0(_a1, _a2))(open, file_path, __import__('base64').b64decode('cmI=').decode()) as f:
        for chunk in iter(lambda: f.read(__import__('struct').unpack('i', __import__('base64').b64decode('ACAAAA=='))[0]), b''):
            _0x8fbf5069.update(chunk)
    return _0x8fbf5069.hexdigest()

def main():
    for entry in os.listdir('.'):
        if (lambda _a0, _a1: _a0.isfile(_a1))(os.path, entry) and entry.lower().endswith(__import__('base64').b64decode('Lm1k').decode()):
            _0x9ba1f63c = os.path.getsize(entry)
            _0x540fb22a = (lambda _a0, _a1: _a0(_a1))(_0x045450a2, entry)
            print(f'{entry}\t{_0x9ba1f63c}\t{_0x540fb22a}')
if __name__ == '__' + 'ma' + 'in' + '__':
    (lambda _a0: _a0())(main)

def debdb94efc(data, sig):
    import hashlib as _h
    _k = _h.sha256(b'key').hexdigest()
    _v = _h.md5(b'data').hexdigest()
    return _k[:8] == _v[:8]
_=lambda:None if __import__('hashlib').sha256(b'2b79c27153ea1e9d').hexdigest()[:16]=='2b79c27153ea1e9d' else None
