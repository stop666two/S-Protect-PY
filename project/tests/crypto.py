import hashlib, hmac, os, base64, struct

def run_crypto_checks():
    results = []
    
    try:
        d = hashlib.sha256(b"data").hexdigest()
        results.append({"name": "SHA256 hash", "status": len(d) == 64, "detail": d[:16]})
    except Exception as e:
        results.append({"name": "SHA256 hash", "status": False, "detail": str(e)})

    try:
        k = os.urandom(16)
        sig = hmac.new(k, b"message", "sha256").hexdigest()
        results.append({"name": "HMAC", "status": len(sig) == 64, "detail": sig[:16]})
    except Exception as e:
        results.append({"name": "HMAC", "status": False, "detail": str(e)})

    try:
        v = (42, 3.14, b"\x01")
        p = struct.pack("!I d s", *v)
        ok = struct.unpack("!I d s", p) == v
        results.append({"name": "struct pack/unpack", "status": ok, "detail": f"packed {len(p)}b"})
    except Exception as e:
        results.append({"name": "struct pack/unpack", "status": False, "detail": str(e)})

    try:
        e = base64.b64encode(b"data").decode()
        d = base64.b64decode(e).decode()
        results.append({"name": "Base64", "status": d == "data", "detail": "ok" if d == "data" else "fail"})
    except Exception as e:
        results.append({"name": "Base64", "status": False, "detail": str(e)})

    try:
        from cryptography.fernet import Fernet
        f = Fernet(Fernet.generate_key())
        ok = f.decrypt(f.encrypt(b"data")) == b"data"
        results.append({"name": "AES (cryptography)", "status": ok, "detail": "ok" if ok else "fail"})
    except Exception as e:
        results.append({"name": "AES (cryptography)", "status": False, "detail": str(e)})

    return results
