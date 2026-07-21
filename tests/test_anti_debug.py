"""Tests for the runtime anti-debugging module.

Covers detection checks, action modes, and memory response.

Author: S-Protect Team
Version: 0.1.0
"""

from __future__ import annotations

import sys

import pytest

from sprotect.runtime.anti_debug import AntiDebug
from sprotect.types import AntiDebugAction, AntiDebugConfig


def _make_config(
    enabled: bool = True,
    action: AntiDebugAction = AntiDebugAction.EXIT,
    checks: list[str] | None = None,
) -> AntiDebugConfig:
    return AntiDebugConfig(
        enabled=enabled,
        action=action,
        checks=checks or ["pdb"],
    )


def test_no_debugger_detected() -> None:
    """Normal execution should not trigger detection."""
    config = _make_config(checks=["pdb", "debugger", "vm"])
    ad = AntiDebug(config)
    result = ad.run_checks()
    assert result is True


def test_debugger_detected() -> None:
    """sys.settrace should trigger pdb check and exit."""
    config = _make_config(checks=["pdb"])
    ad = AntiDebug(config)

    original = sys.gettrace()
    try:
        sys.settrace(lambda f, e, a: None)
        with pytest.raises(SystemExit):
            ad.run_checks()
    finally:
        sys.settrace(original)


def test_warn_action_does_not_exit() -> None:
    """Warn action should print warning and return, not exit."""
    config = _make_config(action=AntiDebugAction.WARN, checks=["pdb"])
    ad = AntiDebug(config)

    original = sys.gettrace()
    try:
        sys.settrace(lambda f, e, a: None)
        result = ad.run_checks()
        assert result is False
    finally:
        sys.settrace(original)


def test_disabled_returns_true() -> None:
    """Disabled anti-debug should always return True."""
    config = _make_config(enabled=False, checks=["pdb"])
    ad = AntiDebug(config)

    original = sys.gettrace()
    try:
        sys.settrace(lambda f, e, a: None)
        result = ad.run_checks()
        assert result is True
    finally:
        sys.settrace(original)


def test_memory_wipe() -> None:
    """_memory_wipe should zero-fill bytearray objects without error."""
    config = _make_config()
    ad = AntiDebug(config)
    ad._memory_wipe()


def test_memory_corrupt() -> None:
    """_memory_corrupt should run without error on bytearray contents."""
    config = _make_config()
    ad = AntiDebug(config)
    ad._memory_corrupt()
