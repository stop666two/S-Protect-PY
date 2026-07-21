"""Tests for AST-based code obfuscation engine.

Covers identifier renaming, string/number encryption, and reserved
name preservation across functions and classes.

Author: S-Protect Team
Version: 0.1.0
"""

from __future__ import annotations

from sprotect.core.obfuscator import Obfuscator
from sprotect.types import NamingStyle, ObfuscateConfig, ObfuscateLevel


def test_basic_rename() -> None:
    """Function names are replaced and the code remains executable."""
    source = """
def hello(name):
    return f"Hello, {name}!"
result = hello("World")
"""
    config = ObfuscateConfig(
        level=ObfuscateLevel.L1,
        encrypt_strings=False,
        encrypt_numbers=False,
    )
    obf = Obfuscator(config)
    result = obf.obfuscate(source)
    assert "hello" not in result

    exec_globals: dict = {}
    exec(compile(result, "<test>", "exec"), exec_globals)
    func_name = [
        k for k in exec_globals
        if callable(exec_globals[k]) and not k.startswith("__")
    ][0]
    assert exec_globals[func_name]("World") == "Hello, World!"


def test_encrypt_strings() -> None:
    """String literals are encrypted as base64.b64decode expressions."""
    source = """
def greet():
    return "Hello, World!"
result = greet()
"""
    config = ObfuscateConfig(
        level=ObfuscateLevel.L1,
        encrypt_strings=True,
        encrypt_numbers=False,
    )
    obf = Obfuscator(config)
    obfuscated = obf.obfuscate(source)
    assert "base64.b64decode" in obfuscated or "base64" in obfuscated
    assert "Hello, World!" not in obfuscated


def test_reserved_names() -> None:
    """Reserved names like __init__ and main are not renamed."""
    source = """
class MyClass:
    def __init__(self):
        pass

def main():
    return 42
"""
    config = ObfuscateConfig(
        level=ObfuscateLevel.L1,
        encrypt_strings=False,
        encrypt_numbers=False,
    )
    obf = Obfuscator(config)
    result = obf.obfuscate(source)
    assert "__init__" in result
    assert "main" in result


def test_class_rename() -> None:
    """Class names are replaced and the code remains executable."""
    source = """
class Calculator:
    def add(self, a, b):
        return a + b

calc = Calculator()
result = calc.add(2, 3)
"""
    config = ObfuscateConfig(
        level=ObfuscateLevel.L1,
        encrypt_strings=False,
        encrypt_numbers=False,
    )
    obf = Obfuscator(config)
    result = obf.obfuscate(source)
    assert "Calculator" not in result

    exec_globals: dict = {}
    exec(compile(result, "<test>", "exec"), exec_globals)
    class_name = [k for k in exec_globals if isinstance(exec_globals[k], type)][0]
    instance = exec_globals[class_name]()
    assert instance.add(2, 3) == 5
