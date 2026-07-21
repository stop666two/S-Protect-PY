import os; os.chdir(r"D:\administrator\Documents\project\S-Protect-PY")
t = open("sprotect/loader.py", "r").read()

# Fix _BOOT_STUB to use json again (revert to working format)
old = '''_BOOT_STUB = ''' + '"""' + '''S-Protect bootloader v11."""\nimport sys, os, hashlib, zlib, msgpack\n_R = os.path.dirname(os.path.abspath(__file__))

def _xof(l, s):
    r, c = bytearray(), 0
    while len(r) < l:
        r.extend(hashlib.sha256(s + c.to_bytes(4,"big")).digest()); c += 1
    return bytes(r[:l])

def _boot(key):
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    raw=open(os.path.join(_R,"{rd}","loader.pye"),"rb").read()
    if raw[:3]!=b"Sv7": return ""
    p=msgpack.unpackb(raw[3:],strict_map_key=False)
    d=p.get(2,b"");ks=p.get(3,[])
    for k in ks+[key]:
        if len(k)!=32: continue
        try: x=AESGCM(k).decrypt(d[:12],d[12:],b"");return zlib.decompress(x).decode()
        except: pass
    return ""

exec(compile(_boot(bytes.fromhex("{lk}")),"","exec"))
run("{entry}",_R)'''

new = '''_BOOT_STUB = ''' + '"""' + '''S-Protect bootloader v11."""\nimport sys, os, json, hashlib, zlib\n_R = os.path.dirname(os.path.abspath(__file__))

def _xof(l, s):
    r, c = bytearray(), 0
    while len(r) < l:
        r.extend(hashlib.sha256(s + c.to_bytes(4,"big")).digest()); c += 1
    return bytes(r[:l])

def _boot(key):
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    p = json.loads(open(os.path.join(_R,"{rd}","loader.pye"),"rb").read().decode())
    real = key
    for kn in ["k1","k2","k3"]:
        if kn in p:
            v = bytes.fromhex(p[kn])
            import hmac as _h
            if _h.new(v, b"S-Protect-v6-key-verify", "sha256").hexdigest()[:8] == p.get("f3","")[:8]:
                real = v; break
    ct = bytes.fromhex(p["d"])
    x = AESGCM(real).decrypt(ct[:12], ct[12:], b"")
    return zlib.decompress(bytes(a^b for a,b in zip(x,_xof(len(x),real)))).decode()

exec(compile(_boot(bytes.fromhex("{lk}")),"","exec"))
run("{entry}",_R)'''

t = t.replace(old, new)
open("sprotect/loader.py", "w").write(t)
print("Fixed!")
