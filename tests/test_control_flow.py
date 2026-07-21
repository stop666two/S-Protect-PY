"""Tests for control flow flattening.

Covers function flattening with state-dispatch loops and behavioral
correctness verification.

Author: S-Protect Team
Version: 0.1.0
"""

from __future__ import annotations

from sprotect.features.control_flow import ControlFlowFlattener


def test_flatten_simple_function() -> None:
    """Function with >=3 statements is flattened, result remains correct."""
    source = """
def add(a, b):
    x = a + b
    y = x * 2
    return y
"""
    flattener = ControlFlowFlattener(source)
    result = flattener.flatten()
    assert "_c_" in result
    assert "while True" in result
    exec_globals: dict = {}
    exec(compile(result, "<test>", "exec"), exec_globals)
    func_name = [k for k in exec_globals if callable(exec_globals[k])][0]
    assert exec_globals[func_name](3, 4) == 14


def test_skip_short_function() -> None:
    """Functions with fewer than 3 statements are not flattened."""
    source = """
def short():
    return 1
"""
    flattener = ControlFlowFlattener(source)
    result = flattener.flatten()
    assert "while True" not in result
    exec_globals: dict = {}
    exec(compile(result, "<test>", "exec"), exec_globals)
    assert exec_globals["short"]() == 1
