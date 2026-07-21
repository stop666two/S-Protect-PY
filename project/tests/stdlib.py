import os, sys, json, hashlib, base64, struct, itertools, collections, datetime, math, random, re, string, pathlib, shutil, tempfile, uuid

def run_stdlib_checks():
    results = []
    for mod_name in ["os", "sys", "json", "re", "math", "hashlib", "base64", "itertools", "collections", "datetime", "pathlib", "shutil"]:
        try:
            __import__(mod_name)
            results.append({"name": f"module {mod_name}", "status": True, "detail": "ok"})
        except:
            results.append({"name": f"module {mod_name}", "status": False, "detail": "fail"})
    
    try:
        h = hashlib.sha256(b"test").hexdigest()
        results.append({"name": "SHA256", "status": True, "detail": h[:16]})
    except:
        results.append({"name": "SHA256", "status": False, "detail": "fail"})

    try:
        ok = json.loads(json.dumps({"a": 1})) == {"a": 1}
        results.append({"name": "JSON", "status": ok, "detail": "ok" if ok else "fail"})
    except:
        results.append({"name": "JSON", "status": False, "detail": "fail"})

    return results
