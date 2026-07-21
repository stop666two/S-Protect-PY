"""Decoy code generator: generates real-looking Python code indistinguishable from real code."""

from __future__ import annotations
import secrets, hashlib, zlib, os
from sprotect.minify import minify_source


_FUNCTION_TEMPLATES = [
    "def {name}({args}):\n    {body}\n    return {result}\n",
    "async def {name}({args}):\n    {body}\n    return {result}\n",
    "class {name}:\n    def __init__(self):\n        self.{attr} = {val}\n    def {method}(self):\n        return self.{attr}\n",
]

_IMPORTS = [
    "import sys, os, json, hashlib\n",
    "import threading, time, queue\n",
    "from collections import OrderedDict\n",
    "import functools, itertools, operator\n",
]

_FUNCTION_NAMES = [
    "process", "validate", "check", "verify", "parse", "load", "init",
    "run_checks", "calc_hash", "read_config", "merge_data", "filter_results",
]

_VAR_NAMES = [
    "data", "key", "result", "tmp", "buf", "val", "status", "code",
    "items", "index", "offset", "length", "total", "count",
]


def _rand_func_name() -> str:
    return secrets.choice(_FUNCTION_NAMES) + "_" + secrets.token_hex(2)


def _rand_body() -> str:
    """Generate a realistic-looking function body."""
    patterns = [
        f"    {secrets.choice(_VAR_NAMES)} = {secrets.choice(_VAR_NAMES)} + {secrets.randbelow(100)}\n    if {secrets.choice(_VAR_NAMES)} > {secrets.randbelow(50)}:\n        {secrets.choice(_VAR_NAMES)} = {secrets.choice(_VAR_NAMES)} ^ {secrets.randbelow(255)}\n    else:\n        {secrets.choice(_VAR_NAMES)} = ~{secrets.choice(_VAR_NAMES)} & {secrets.randbelow(65535)}\n",
        f"    {secrets.choice(_VAR_NAMES)} = {{}}\n    for i in range({secrets.randbelow(10) + 1}):\n        {secrets.choice(_VAR_NAMES)}[i] = hashlib.sha256(str(i).encode()).hexdigest()[:{secrets.randbelow(16) + 4}]\n    {secrets.choice(_VAR_NAMES)} = sum({secrets.choice(_VAR_NAMES)}.values())\n",
        f"    {secrets.choice(_VAR_NAMES)} = bytearray()\n    for i in range({secrets.randbelow(100) + 10}):\n        {secrets.choice(_VAR_NAMES)}.append((i * {secrets.randbelow(7) + 3}) & {secrets.randbelow(255)})\n    {secrets.choice(_VAR_NAMES)} = bytes({secrets.choice(_VAR_NAMES)})\n",
    ]
    return secrets.choice(patterns)


def generate_decoy_source() -> str:
    """Generate a complete, valid Python module that looks exactly like real code.
    
    The output goes through the SAME pipeline as real code:
    minify_source() → zlib.compress() → encrypt
    Making it indistinguishable from real encrypted files.
    """
    source = ""
    
    # Random imports
    for _ in range(secrets.randbelow(3) + 1):
        source += secrets.choice(_IMPORTS)
    source += "\n"
    
    # 2-5 functions/classes
    for _ in range(secrets.randbelow(4) + 2):
        template = secrets.choice(_FUNCTION_TEMPLATES)
        if "class" in template:
            cn = _rand_func_name()
            attr = secrets.choice(_VAR_NAMES)
            val = secrets.randbelow(9999)
            method = _rand_func_name()
            source += template.format(name=cn, attr=attr, val=val, method=method)
        else:
            fn = _rand_func_name()
            argc = secrets.randbelow(3) + 1
            args = ", ".join(secrets.choice(_VAR_NAMES) for _ in range(argc))
            body = _rand_body()
            result = secrets.choice(_VAR_NAMES)
            source += template.format(name=fn, args=args, body=body, result=result)
        source += "\n"
    
    return source


def generate_trap_source() -> str:
    """Generate code that infinite loops - but looks like valid processing."""
    vn = secrets.choice(_VAR_NAMES)
    fn = secrets.choice(_FUNCTION_NAMES) + "_" + secrets.token_hex(2)
    cn = "Processor" + secrets.token_hex(3)
    return (
        f"import sys, os, json, threading, time\n\n"
        f"class {cn}:\n"
        f"    def __init__(self):\n"
        f"        self.{vn} = 0\n"
        f"    def {fn}(self):\n"
        f"        while True:\n"
        f"            self.{vn} += 1\n"
        f"            if self.{vn} > 999999999:\n"
        f"                self.{vn} = 0\n"
        f"            time.sleep(0.001)\n"
        f"        return self.{vn}\n\n"
        f"def main():\n"
        f"    obj = {cn}()\n"
        f"    return obj.{fn}()\n\n"
        f"if __name__ == '__main__':\n"
        f"    main()\n"
    )


def make_decoy_payload(source: str, real_key: bytes) -> bytes:
    """Process decoy source through the SAME pipeline as real code:
    minify → compress → encrypt.
    This makes decoy and real files structurally identical.
    """
    from sprotect.minify import minify_source
    from sprotect.crypto import aes_encrypt
    
    # Same minification as real code
    minified = minify_source(source, add_garbage=False)
    # Same compression
    compressed = zlib.compress(minified.encode(), 9)
    # Same encryption
    ct = aes_encrypt(compressed, real_key)
    
    import json
    # Same payload structure as real files
    keys = {"k1": real_key.hex(), "k2": os.urandom(32).hex(), "k3": os.urandom(32).hex()}
    f1 = hashlib.sha256(real_key).digest()[:4].hex()
    from sprotect.crypto import verify_fingerprint
    # Generate matching fingerprints
    import hmac as _hm
    import os as _os
    k2_b = _os.urandom(32); k3_b = _os.urandom(32)
    xored = bytearray(32)
    for kb in [real_key, k2_b, k3_b]:
        for i in range(min(32, len(kb))): xored[i] ^= kb[i]
    fingerprints = {
        "f1": hashlib.sha256(bytes(xored)).hexdigest()[5:13],
        "f2": hashlib.sha256(real_key).hexdigest()[3:11],
        "f3": _hm.new(real_key, b"S-Protect-v6-key-verify", "sha256").hexdigest()[:8],
    }
    
    payload = {
        "v": 7, "d": ct.hex(), "c": _os.urandom(32).hex(),
        "p": _os.urandom(_os.urandom(1)[0]).hex(), "h": hashlib.sha256(source.encode()).hexdigest(),
    }
    payload.update(keys)
    payload.update(fingerprints)
    return json.dumps(payload, separators=(",", ":")).encode()
