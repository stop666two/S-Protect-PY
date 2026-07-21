"""Tests for environment fingerprint binding.

All test artifacts are created inside the project's _test_temp directory.

Author: S-Protect Team
Version: 0.1.0
"""

from __future__ import annotations

import os

from sprotect.features.environment import EnvironmentBinder
from sprotect.types import EnvironmentConfig


def _config(
    bind_directory: str | None = None,
    bind_username: str | None = None,
    bind_env_vars: list[str] | None = None,
) -> EnvironmentConfig:
    return EnvironmentConfig(
        enabled=True,
        bind_directory=bind_directory,
        bind_username=bind_username,
        bind_env_vars=bind_env_vars or [],
    )


def test_verify_environment_no_bindings() -> None:
    """With no bindings configured, verify returns True."""
    binder = EnvironmentBinder(_config())
    assert binder.verify_environment() is True


def test_verify_environment_directory_match() -> None:
    """verify succeeds when bind_directory matches cwd."""
    cwd = os.path.abspath(os.getcwd())
    binder = EnvironmentBinder(_config(bind_directory=cwd))
    assert binder.verify_environment() is True


def test_verify_environment_directory_mismatch() -> None:
    """verify fails when bind_directory does not match cwd."""
    binder = EnvironmentBinder(_config(bind_directory="/nonexistent/path"))
    assert binder.verify_environment() is False


def test_generate_fingerprint_returns_hex() -> None:
    """Fingerprint is a 64-character lowercase hex string."""
    binder = EnvironmentBinder(_config())
    fp = binder.generate_fingerprint()
    assert len(fp) == 64
    int(fp, 16)  # raises ValueError if not valid hex
