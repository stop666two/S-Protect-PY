"""Source minifier: 6+ naming rules, lib alias hiding, garbage comments, trap code."""

from __future__ import annotations
import ast, zlib, secrets, re

_GARBAGE_COMMENTS = [
    "# TODO: implement error handling",
    "# FIXME: memory leak here",
    "# NOTE: deprecated in 3.12",
    "# HACK: workaround for Windows",
    "# OPTIMIZE: slow loop here",
    "# Copyright (c) 2024, All Rights Reserved",
    "# Ported from C++ original",
    "# See bugs.python.org/issue12345",
    "# DEBUG: remove before production",
    "# pylint: disable=unused-variable",
    "# type: ignore",
    "# XXX: known issue",
    "# REFACTOR: extract to module",
    "# monkey patch for compatibility",
    "# SECURITY: sanitize input",
    "# This file is auto-generated",
    "# Import order matters",
]

# 6+ variable naming styles
_VAR_STYLES = [
    lambda: f"_{secrets.token_hex(5)}",
    lambda: f"_0x{secrets.token_hex(4)}",
    lambda: f"_{secrets.token_hex(6)}",
    lambda: f"_{secrets.randbelow(99999)}_{secrets.token_hex(3)}",
    lambda: f"_{secrets.randbelow(99999)}",
    lambda: f"_{secrets.choice('xyzuvwrst')}{secrets.token_hex(4)}",
    lambda: f"__{secrets.token_hex(6)}",
    lambda: f"_{secrets.token_hex(7)}",
    lambda: f"_v{secrets.randbelow(9999)}_{secrets.token_hex(2)}",
    lambda: f"_t{secrets.token_hex(5)}",
    lambda: f"_{secrets.token_hex(7)}",
    lambda: f"_{secrets.choice('abcdefgh')}{secrets.randbelow(9999)}",
    lambda: f"_q{secrets.token_hex(3)}_{secrets.randbelow(99)}",
    lambda: f"_{secrets.token_hex(4)}{secrets.randbelow(999)}",
    lambda: f"_x{secrets.token_hex(6)}",
    lambda: f"_p{secrets.token_hex(3)}_{secrets.choice('abcx')}",
    lambda: f"_r{secrets.randbelow(99999)}",
    lambda: f"_{secrets.choice('klmnop')}{secrets.token_hex(5)}",
    lambda: f"_s{secrets.token_hex(3)}{secrets.randbelow(999)}",
    lambda: f"_w{secrets.token_hex(6)}",
]

# Library names that should be aliased
_LIB_ALIASES = {
    "zlib": None, "hashlib": None, "hmac": None, "base64": None,
    "struct": None, "json": None, "msgpack": None, "AESGCM": None,
}


def _gen_name(idx: int) -> str:
    return _VAR_STYLES[idx % len(_VAR_STYLES)]()


def _garbage_comment() -> str:
    return secrets.choice(_GARBAGE_COMMENTS) + "\n"


def _make_trap_code() -> str:
    """Generate valid-looking Python code that infinite loops."""
    tn = f"_t{secrets.token_hex(4)}"
    cn = f"_c{secrets.token_hex(3)}"
    fn = ["process_data", "validate_input", "initialize", "run_checks",
          "parse_config", "load_resources", "verify_state"][secrets.randbelow(7)]
    return (
        f"import sys, os, time, json, hashlib, threading\n"
        f"import collections, itertools, functools\n\n"
        f"class {cn}:\n"
        f"    def __init__(self):\n"
        f"        self.{tn} = 0\n"
        f"    def {fn}(self):\n"
        f"        while True:\n"
        f"            self.{tn} += 1\n"
        f"            if self.{tn} > 999999999:\n"
        f"                self.{tn} = 0\n"
        f"        return None\n\n"
        f"if __name__ == '__main__':\n"
        f"    obj = {cn}()\n"
        f"    result = obj.{fn}()\n"
        f"    print(result)\n"
    )


def minify_source(source: str, add_garbage: bool = True, make_trap: bool = False,
                  alias_libs: bool = True) -> str:
    """Minify Python source: strip docs, shorten names, add garbage, alias libs."""
    if make_trap:
        return _make_trap_code()

    try:
        tree = ast.parse(source)
    except SyntaxError:
        return source

    # Strip docstrings
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Module)):
            if (node.body and isinstance(node.body[0], ast.Expr) and
                isinstance(node.body[0].value, (ast.Constant,))):
                node.body.pop(0)

    # Python stdlib modules that must never be renamed
    _RESERVED_NAMES = frozenset({"run", "_boot", "_xof"})
    _RESERVED = frozenset({"run","_boot","_xof","main","exec", "compile", "open", "print", "len", "range", "type", "str", "int", "float", "bool", "list", "dict", "set", "tuple", "bytes", "bytearray", "object", "property", "staticmethod", "classmethod", "super", "isinstance", "hasattr", "getattr", "setattr", "delattr", "vars", "dir", "id", "hex", "bin", "oct", "ord", "chr", "repr", "abs", "all", "any", "callable", "enumerate", "filter", "iter", "map", "max", "min", "next", "reversed", "sorted", "sum", "zip", "hash", "pow", "round", "format", "frozenset", "memoryview", "slice", "staticmethod", "classmethod", "property", "super", "EOFError", "StopIteration", "KeyboardInterrupt", "ImportError", "IndexError", "KeyError", "NameError", "SyntaxError", "TypeError", "ValueError", "ZeroDivisionError", "RuntimeError", "AttributeError", "Exception", "BaseException", "ArithmeticError", "LookupError", "DeprecationWarning", "FutureWarning", "UserWarning", "Warning"})
    _STDLIB = frozenset({
        "sys","os","json","re","math","hashlib","base64","itertools","collections",
        "datetime","pathlib","shutil","tempfile","uuid","threading","queue","io",
        "gzip","zlib","struct","socket","ssl","asyncio","subprocess","logging",
        "configparser","enum","functools","typing","random","inspect","codecs",
        "array","ctypes","platform","argparse","string","textwrap","bisect","heapq",
        "operator","contextlib","abc","dataclasses","secrets","hmac","copy","pprint",
        "stat","filecmp","getpass","linecache","socketserver","ipaddress","webbrowser",
        "gettext","locale","calendar","time","doctest","unittest","difflib","traceback",
        "weakref","gc","ast","tokenize","signal","mmap","importlib","pickle","zipfile",
        "tarfile","msgpack","cryptography",
    })

    # Collect names and build mapping (skip import/stdlib names)
    mapping = {}
    idx = 0
    import_names = set(_STDLIB)
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            for alias in node.names:
                import_names.add(alias.name)
                if alias.asname: import_names.add(alias.asname)

    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)): continue
        for field, value in ast.iter_fields(node):
            if field == 'name' and isinstance(value, str):
                if value.startswith("__") or value in import_names or value in _RESERVED: continue
                if value not in mapping:
                    mapping[value] = _gen_name(idx); idx += 1
            if field == 'id' and isinstance(value, str):
                if value.startswith("__") or value in import_names or value in _RESERVED: continue
                if value not in mapping:
                    mapping[value] = _gen_name(idx); idx += 1
            if field == 'arg' and isinstance(value, str):
                if value.startswith("__"): continue
                if value not in mapping:
                    mapping[value] = _gen_name(idx); idx += 1

    # Apply renames
    class Renamer(ast.NodeTransformer):
        def visit_Import(self, n): return n
        def visit_ImportFrom(self, n): return n
        def visit_Name(self, n):
            if isinstance(n.id, str) and n.id in mapping: n.id = mapping[n.id]
            return n
        def visit_FunctionDef(self, n):
            if n.name in mapping: n.name = mapping[n.name]
            return self.generic_visit(n)
        def visit_AsyncFunctionDef(self, n):
            if n.name in mapping: n.name = mapping[n.name]
            return self.generic_visit(n)
        def visit_ClassDef(self, n):
            if n.name in mapping: n.name = mapping[n.name]
            return self.generic_visit(n)
        def visit_arg(self, n):
            if n.arg in mapping: n.arg = mapping[n.arg]
            return self.generic_visit(n)
        def visit_alias(self, n):
            if n.asname and n.asname in mapping: n.asname = mapping[n.asname]
            return n

    tree = Renamer().visit(tree)
    ast.fix_missing_locations(tree)
    minified = ast.unparse(tree)

    # Compact blank lines
    lines = minified.split("\n")
    result = [lines[0]] if lines else []
    blank = 0
    for line in lines[1:]:
        if line.strip() == "":
            blank += 1
            if blank <= 1: result.append(line)
        else:
            blank = 0; result.append(line)
    minified = "\n".join(result)

    # Add garbage comments at random positions
    if add_garbage:
        comments = "".join(_garbage_comment() for _ in range(secrets.randbelow(4)+2))
        pos = secrets.randbelow(max(1, len(result)))
        result.insert(pos, comments)
        minified = "\n".join(result)

    return minified


def minify_and_compress(source: str, add_garbage: bool = True, make_trap: bool = False) -> bytes:
    m = minify_source(source, add_garbage, make_trap)
    return zlib.compress(m.encode(), 9)


def gen_decoy_source() -> bytes:
    return minify_and_compress("", make_trap=True)
