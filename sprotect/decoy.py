# DECOY GENERATOR: synthetic module fabricator
# PURPOSE: indistinguishable from real code under static analysis
"""Decoy code generator: generates real-looking Python code indistinguishable from real code."""

from __future__ import annotations
import secrets, hashlib, zlib, os
from sprotect.minify import minify_source


_T75c2f = [
    "def {name}({args}):\n{body}\n    return {result}\n",
    "def {name}({args}):\n{body}\n    return {result}\n",
    "class {name}:\n    def __init__(self):\n        self.{attr} = {val}\n    def {method}(self):\n        return self.{attr}\n",
]

_M94e1d = [
    "import sys, os, json, hashlib\n",
    "import threading, time, queue\n",
    "from collections import OrderedDict\n",
    "import functools, itertools, operator\n",
]

_N23a8f = [
    "process", "validate", "check", "verify", "parse", "load", "init",
    "run_checks", "calc_hash", "read_config", "merge_data", "filter_results",
]

_V67b4c = [
    "data", "key", "result", "tmp", "buf", "val", "status", "code",
    "items", "index", "offset", "length", "total", "count",
]


def _gen_fake_name() -> str:
    return secrets.choice(_N23a8f) + "_" + secrets.token_hex(2)


def _gen_fake_body() -> str:
    """Generate a realistic-looking function body."""
    patterns = [
        f"    {secrets.choice(_V67b4c)} = {secrets.choice(_V67b4c)} + {secrets.randbelow(100)}\n    if {secrets.choice(_V67b4c)} > {secrets.randbelow(50)}:\n        {secrets.choice(_V67b4c)} = {secrets.choice(_V67b4c)} ^ {secrets.randbelow(255)}\n    else:\n        {secrets.choice(_V67b4c)} = ~{secrets.choice(_V67b4c)} & {secrets.randbelow(65535)}\n",
        f"    {secrets.choice(_V67b4c)} = {{}}\n    for i in range({secrets.randbelow(10) + 1}):\n        {secrets.choice(_V67b4c)}[i] = hashlib.sha256(str(i).encode()).hexdigest()[:{secrets.randbelow(16) + 4}]\n    {secrets.choice(_V67b4c)} = sum({secrets.choice(_V67b4c)}.values())\n",
        f"    {secrets.choice(_V67b4c)} = bytearray()\n    for i in range({secrets.randbelow(100) + 10}):\n        {secrets.choice(_V67b4c)}.append((i * {secrets.randbelow(7) + 3}) & {secrets.randbelow(255)})\n    {secrets.choice(_V67b4c)} = bytes({secrets.choice(_V67b4c)})\n",
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
        source += secrets.choice(_M94e1d)
    source += "\n"
    
    # 2-5 functions/classes
    for _ in range(secrets.randbelow(4) + 2):
        template = secrets.choice(_T75c2f)
        if "class" in template:
            cn = _gen_fake_name()
            attr = secrets.choice(_V67b4c)
            val = secrets.randbelow(9999)
            method = _gen_fake_name()
            source += template.format(name=cn, attr=attr, val=val, method=method)
        else:
            fn = _gen_fake_name()
            argc = secrets.randbelow(3) + 1
            args = ", ".join(secrets.choice(_V67b4c) for _ in range(argc))
            body = _gen_fake_body()
            result = secrets.choice(_V67b4c)
            source += template.format(name=fn, args=args, body=body, result=result)
        source += "\n"
    
    return source


def generate_trap_source() -> str:
    """Generate code that infinite loops - but looks like valid processing."""
    vn = secrets.choice(_V67b4c)
    fn = secrets.choice(_N23a8f) + "_" + secrets.token_hex(2)
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


