"""Custom self-extracting packager (alternative to PyInstaller)."""
from __future__ import annotations
import os, sys, zlib, base64, struct, marshal, json, hashlib
from pathlib import Path


def _find_python_dll() -> str | None:
    """Locate python3xx.dll for bundling."""
    for p in sys.path:
        d = os.path.join(p, "..", "..")
        if os.name == "nt":
            for f in os.listdir(d):
                if f.lower().startswith("python3") and f.lower().endswith(".dll"):
                    return os.path.join(d, f)
    return None


def _embed_data(data: bytes) -> str:
    """Compress and encode data for embedding."""
    compressed = zlib.compress(data, 9)
    return base64.a85encode(compressed).decode()


_STUB_TEMPLATE = '''"""Self-extracting encrypted package."""
import sys, os, zlib, base64, marshal, json, importlib.abc, importlib.machinery

_EMBEDDED = {embedded}
_MANIFEST = {manifest}

def _decrypt(data: bytes, key: bytes) -> bytes:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    return AESGCM(key).decrypt(data[:12], data[12:], b"")

def _decompress(data: bytes) -> bytes:
    return zlib.decompress(data)

_RD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_runtime")
os.makedirs(_RD, exist_ok=True)

for fname, (ct, kh) in _EMBEDDED.items():
    key = bytes.fromhex(kh)
    try:
        raw = _decompress(_decrypt(bytes.fromhex(ct), key))
    except Exception:
        continue
    open(os.path.join(_RD, fname), "wb").write(raw)

_KEY = bytes.fromhex("{loader_key}")
_LDR = os.path.join(_RD, "loader.pye")
if os.path.isfile(_LDR):
    import subprocess as _sp
    _sp.run([sys.executable, os.path.join(os.path.dirname(_RD), "main.py")], cwd=os.path.dirname(_RD))
'''


def pack_to_single_file(output_dir: str, target_exe: str,
                        loader_key: bytes, extra_files: list[str] = None) -> str:
    """Package encrypted output into a single self-extracting .py script."""
    out_dir = Path(output_dir)
    if not out_dir.is_dir():
        raise FileNotFoundError(f"Output dir not found: {output_dir}")

    runtime_dir = out_dir / "_runtime"
    if not runtime_dir.is_dir():
        raise FileNotFoundError(f"Runtime dir not found: {runtime_dir}")

    embedded = {}
    for f in sorted(runtime_dir.iterdir()):
        if f.suffix == ".pye":
            data = f.read_bytes()
            kh = hashlib.sha256(data).hexdigest()[:32]
            embedded[f.name] = (data.hex(), kh)

    script = _STUB_TEMPLATE.format(
        embedded=json.dumps(embedded),
        manifest=json.dumps(list(embedded.keys())),
        loader_key=loader_key.hex(),
    )

    output = Path(target_exe)
    output.write_text(script, encoding="utf-8")
    return str(output.resolve())


def pack_to_onefile(output_dir: str, target: str,
                    loader_key: bytes, include_python: bool = False) -> str:
    """Package output + Python into a single zip-based executable."""
    import zipfile, tempfile, shutil

    out_dir = Path(output_dir)
    target_path = Path(target)
    target_path = target_path.with_suffix(".pyz")

    with zipfile.ZipFile(target_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in out_dir.rglob("*"):
            if f.is_file():
                zf.write(f, f.relative_to(out_dir))

        if include_python:
            python_dll = _find_python_dll()
            if python_dll:
                zf.write(python_dll, os.path.basename(python_dll))

    return str(target_path.resolve())
