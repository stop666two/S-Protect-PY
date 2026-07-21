"""Tests for dead code injection.

Covers dead code block injection and behavioral correctness
verification after injection.

Author: S-Protect Team
Version: 0.1.0
"""

from __future__ import annotations

from sprotect.features.dead_code import DeadCodeInjector


def test_dead_code_injection() -> None:
    """Dead code injected at density 1.0, function still returns correct value."""
    source = """
def simple():
    return 42
"""
    injector = DeadCodeInjector(density=1.0)
    result = injector.inject(source)
    assert "__import__" in result
    assert "hashlib" in result
    exec_globals: dict = {}
    exec(compile(result, "<test>", "exec"), exec_globals)
    assert exec_globals["simple"]() == 42
