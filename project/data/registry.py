"""File hash registry - every file's SHA256 is listed here."""
import os, hashlib

_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def _compute_all_hashes():
    registry = {}
    for root, dirs, files in os.walk(_BASE):
        dirs[:] = [d for d in dirs if not d.startswith(("_", ".")) and d not in ("__pycache__",)]
        for f in files:
            if not f.endswith(".py"): continue
            fp = os.path.join(root, f)
            h = hashlib.sha256()
            with open(fp, "rb") as fh:
                while True:
                    chunk = fh.read(65536)
                    if not chunk: break
                    h.update(chunk)
            rel = os.path.relpath(fp, _BASE).replace("\\", "/")
            registry[rel] = h.hexdigest()
    return registry

FILE_REGISTRY = _compute_all_hashes()
