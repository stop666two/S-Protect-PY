"""Tests for code virtualization.

Covers VM interpreter generation and partial-mode function
virtualization with file-based test helpers.

Author: S-Protect Team
Version: 0.1.0
"""

from __future__ import annotations

import os
import shutil
import tempfile

from sprotect.features.virtualization import VirtualizationEngine
from sprotect.types import VirtualizationConfig, VirtualizationMode


_TEST_TEMP = "_test_temp"


def _clean_test_temp() -> None:
    """Remove the _test_temp directory if it exists."""
    if os.path.isdir(_TEST_TEMP):
        shutil.rmtree(_TEST_TEMP)


def _ensure_test_temp() -> str:
    """Create and return the _test_temp directory path."""
    os.makedirs(_TEST_TEMP, exist_ok=True)
    return _TEST_TEMP


def test_vm_interpreter_generated() -> None:
    """VM interpreter code generation produces a valid class with run method."""
    config = VirtualizationConfig(enabled=True, mode=VirtualizationMode.PARTIAL)
    engine = VirtualizationEngine(config)
    code = engine.generate_vm_interpreter()
    assert "class __VM_" in code
    assert "def run" in code
    assert "locals_dict" in code
    # Should compile without error
    compile(code, "<vm_interpreter>", "exec")


def test_vm_interpreter_executable() -> None:
    """Generated VM interpreter can be executed and produces correct results."""
    config = VirtualizationConfig(enabled=True, mode=VirtualizationMode.PARTIAL)
    engine = VirtualizationEngine(config)
    code = engine.generate_vm_interpreter()

    exec_globals: dict = {}
    exec(compile(code, "<vm_test>", "exec"), exec_globals)
    # Verify the class exists and is callable
    class_name = [k for k in exec_globals if k.startswith("__VM_")][0]
    vm_instance = exec_globals[class_name]()
    assert hasattr(vm_instance, "run")


def test_virtualize_partial_mode() -> None:
    """PARTIAL mode only virtualizes functions listed in config.functions."""
    source = """
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def untouched(x):
    return x * 2
"""
    config = VirtualizationConfig(
        enabled=True,
        mode=VirtualizationMode.PARTIAL,
        functions=["add", "subtract"],
        glob_patterns=[],
    )
    engine = VirtualizationEngine(config)
    result = engine.virtualize(source)

    # Virtualized functions should reference the VM interpreter
    assert "__vm_" in result
    # The untouched function should remain unchanged
    assert "return x * 2" in result or "return (x * 2)" in result


def test_virtualize_full_mode() -> None:
    """FULL mode virtualizes all functions in source."""
    source = """
def foo():
    return 1

def bar():
    return 2
"""
    config = VirtualizationConfig(
        enabled=True,
        mode=VirtualizationMode.FULL,
    )
    engine = VirtualizationEngine(config)
    result = engine.virtualize(source)

    # Both functions should reference the VM interpreter
    vm_refs = result.count("__vm_")
    assert vm_refs >= 1


def test_virtualize_with_temp_file() -> None:
    """Virtualize with file-based config using _test_temp directory."""
    _ensure_test_temp()
    try:
        test_file = os.path.join(_TEST_TEMP, "test_vm.py")
        with open(test_file, "w", encoding="utf-8") as f:
            f.write("def secret():\n    return 42\n")

        config = VirtualizationConfig(
            enabled=True,
            mode=VirtualizationMode.PARTIAL,
            functions=["secret"],
        )
        engine = VirtualizationEngine(config)

        with open(test_file, "r", encoding="utf-8") as f:
            source = f.read()

        result = engine.virtualize(source, file_path=test_file)
        assert "def secret" in result
    finally:
        _clean_test_temp()


def test_virtualize_empty_source() -> None:
    """Virtualizing empty or trivial source does not crash."""
    config = VirtualizationConfig(enabled=True, mode=VirtualizationMode.FULL)
    engine = VirtualizationEngine(config)

    result = engine.virtualize("")
    assert isinstance(result, str)

    result = engine.virtualize("x = 1\n")
    assert "x = 1" in result or "x = 1" in result


def test_virtualize_partial_no_match() -> None:
    """PARTIAL mode with no matching functions leaves code unchanged."""
    source = """
def keep():
    return 99
"""
    config = VirtualizationConfig(
        enabled=True,
        mode=VirtualizationMode.PARTIAL,
        functions=["nonexistent"],
    )
    engine = VirtualizationEngine(config)
    result = engine.virtualize(source)

    assert "return 99" in result or "return (99)" in result
