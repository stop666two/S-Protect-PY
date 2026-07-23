# BYTECODE SHIELD: code object encryption layer
# HOOK: import meta-path interception
"""Bytecode-level protection: encrypt .pyc and decrypt at runtime via import hook."""
from __future__ import annotations
import os, sys, marshal, zlib, hashlib, struct, types
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def protect_code(code: types.CodeType, key: bytes) -> bytes:
    """Serialize and encrypt a code object into a .pye container."""
    raw = marshal.dumps(code)
    compressed = zlib.compress(raw, 9)
    nonce = os.urandom(12)
    ct = nonce + AESGCM(key).encrypt(nonce, compressed, b"")
    return ct


def unprotect_code(data: bytes, key: bytes) -> types.CodeType:
    """Decrypt a .pye container back to a code object."""
    nonce = data[:12]
    ct = data[12:]
    compressed = AESGCM(key).decrypt(nonce, ct, b"")
    raw = zlib.decompress(compressed)
    return marshal.loads(raw)


class SecureImporter:
    """Import hook that transparently decrypts .pye files."""

    def __init__(self, runtime_dir: str, key: bytes):
        self._rt_path = runtime_dir
        self._decryption_key = key

    def find_spec(self, fullname, path=None, target=None):
        pye_path = os.path.join(self._rt_path, fullname.replace(".", os.sep) + ".pye")
        if os.path.isfile(pye_path):
            import importlib.machinery as _mach
            return _mach.ModuleSpec(fullname, self, origin=pye_path)
        return None

    def create_module(self, spec):
        return None

    def exec_module(self, module):
        pye_path = os.path.join(self._rt_path, module.__name__.replace(".", os.sep) + ".pye")
        with open(pye_path, "rb") as f:
            code = unprotect_code(f.read(), self._decryption_key)
        exec(code, module.__dict__)


def protect_pyc_file(pyc_path: str, key: bytes, output_path: str):
    """Protect a single .pyc file into encrypted .pye."""
    import importlib.util as _util
    code = _util.compile_source(open(pyc_path.replace(".pyc", ".py").replace(".pye", ".py")).read())
    ct = protect_code(code, key)
    with open(output_path, "wb") as f:
        f.write(ct)


def protect_source(source: str, key: bytes) -> bytes:
    """Compile and protect source code in one step."""
    code = compile(source, "<protected>", "exec")
    return protect_code(code, key)


def generate_loader_stub(entry_module: str, runtime_dir: str,
                         key_hex: str, extra_imports: list[str] = None) -> str:
    """Generate a self-contained loader stub for bytecode-protected projects."""
    imps = (extra_imports or []) + ["sys,os"]
    return f'''"""Protected runtime loader."""
import {", ".join(imps)}
from sprotect.bytecode_protect import SecureImporter

_KEY = bytes.fromhex("{key_hex}")
_RD = os.path.join(os.path.dirname(__file__), "{runtime_dir}")
sys.meta_path.insert(0, SecureImporter(_RD, _KEY))

from {entry_module} import __main__
'''
