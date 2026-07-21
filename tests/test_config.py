"""Tests for JSON5 configuration loading.

All test artifacts are created inside the project's _test_temp directory.
"""

from __future__ import annotations

import os

import pytest

from sprotect.config import generate_default_config, load_config
from sprotect.types import Config, InterdependencyMode

_TEST_TEMP = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "_test_temp")
os.makedirs(_TEST_TEMP, exist_ok=True)


def _tmp_path(name: str) -> str:
    return os.path.join(_TEST_TEMP, name)


def test_load_default_config() -> None:
    """Load config without arguments should return a default Config."""
    config = load_config()
    assert isinstance(config, Config)
    assert config.encrypt.interdependency == InterdependencyMode.CHAIN


def test_load_custom_config() -> None:
    """Load a custom JSON5 config file and verify field overrides."""
    content = (
        '{ project: { name: "testapp", entry: "app.py" },'
        '  encrypt: { algorithm: "aes-256-gcm", shard_count: 5 } }'
    )
    tmp = _tmp_path("_test_config.json5")
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(content)
    try:
        config = load_config(tmp)
        assert config.project.name == "testapp"
        assert config.encrypt.shard_count == 5
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)


def test_generate_default_config() -> None:
    """Generate a default config file then load and verify it."""
    tmp = _tmp_path("_test_default.json5")
    try:
        generate_default_config(tmp)
        config = load_config(tmp)
        assert isinstance(config, Config)
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)


def test_invalid_enum_value() -> None:
    """Invalid enum value should raise ValueError."""
    content = "{ obfuscate: { level: 99 } }"
    tmp = _tmp_path("_test_bad.json5")
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(content)
    try:
        with pytest.raises(ValueError):
            load_config(tmp)
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)
