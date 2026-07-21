"""Tests for three-layer watermark injection.

All test artifacts are created inside the project's _test_temp directory.

Author: S-Protect Team
Version: 0.1.0
"""

from __future__ import annotations

import os

from sprotect.features.watermark import WatermarkInjector
from sprotect.types import WatermarkConfig, WatermarkLevel

_TEST_TEMP = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "_test_temp")
os.makedirs(_TEST_TEMP, exist_ok=True)


def _tmp_path(name: str) -> str:
    return os.path.join(_TEST_TEMP, name)


def _make_config(batch_id: str = "test-batch") -> WatermarkConfig:
    return WatermarkConfig(
        enabled=True,
        levels=[WatermarkLevel.FILE, WatermarkLevel.CODE, WatermarkLevel.RUNTIME],
        batch_id=batch_id,
    )


def test_inject_file_watermark_appends_comment() -> None:
    """File-level watermark appends a // WM: comment line."""
    tmp = _tmp_path("_test_wm_file.py")
    original = "x = 1\nprint(x)\n"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(original)

    injector = WatermarkInjector(_make_config("batch-1"))
    watermark = injector.inject_file_watermark(tmp)

    try:
        with open(tmp, "r", encoding="utf-8") as f:
            content = f.read()

        assert content.endswith("\n"), "file should end with a newline"
        assert "// WM:" in content, "watermark comment not found"
        assert "batch-1" in watermark, "batch_id should appear in watermark"
        assert watermark.startswith("// WM:"), "watermark should start with // WM:"
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)


def test_inject_code_watermark_adds_lambda() -> None:
    """Code-level watermark injects a no-op lambda with hash check."""
    source = "def foo(): pass\n"
    injector = WatermarkInjector(_make_config("batch-2"))
    result = injector.inject_code_watermark(source)

    assert "_WM = (lambda" in result, "watermark lambda not found"
    assert result.endswith(source), "original source should follow watermark"
    exec_globals: dict = {}
    exec(compile(result, "<test>", "exec"), exec_globals)
    assert exec_globals.get("foo") is not None
    assert exec_globals["foo"]() is None


def test_generate_runtime_check_produces_valid_code() -> None:
    """Runtime check code compiles and executes without error."""
    injector = WatermarkInjector(_make_config("batch-3"))
    code = injector.generate_runtime_check()

    assert "def _WM_verify" in code, "verify function not found"
    assert "_WM_verified" in code, "verified flag not found"

    exec_globals: dict = {}
    exec(compile(code, "<test>", "exec"), exec_globals)
    assert "_WM_verify" in exec_globals
    assert "_WM_verified" in exec_globals
    assert callable(exec_globals["_WM_verify"])
