import os, sys, tempfile, threading, queue, io, gzip, zlib

def run_runtime_checks():
    results = []

    tmp = None
    try:
        tmp = os.path.join(tempfile.gettempdir(), "_spt_test.tmp")
        with open(tmp, "w") as f: f.write("test")
        with open(tmp, "r") as f: ok = f.read() == "test"
        results.append({"name": "File I/O", "status": ok, "detail": "ok" if ok else "fail"})
    except Exception as e:
        results.append({"name": "File I/O", "status": False, "detail": str(e)})
    finally:
        if tmp and os.path.exists(tmp): os.remove(tmp)

    try:
        q = queue.Queue()
        t = threading.Thread(target=lambda q: q.put(42), args=(q,), daemon=True)
        t.start()
        t.join(3)
        v = q.get_nowait()
        results.append({"name": "Threading", "status": v == 42, "detail": f"got {v}"})
    except Exception as e:
        results.append({"name": "Threading", "status": False, "detail": str(e)})

    try:
        b = io.BytesIO(b"buffer test")
        results.append({"name": "BytesIO", "status": b.read() == b"buffer test", "detail": "ok"})
    except Exception as e:
        results.append({"name": "BytesIO", "status": False, "detail": str(e)})

    try:
        c = gzip.compress(b"test data for compression")
        d = gzip.decompress(c)
        results.append({"name": "GZip", "status": d == b"test data for compression", "detail": f"ratio {len(c)/len(d):.1%}"})
    except Exception as e:
        results.append({"name": "GZip", "status": False, "detail": str(e)})

    return results
