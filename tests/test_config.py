"""Tests for JSON5 configuration loading."""
from __future__ import annotations

import os
import tempfile

import pytest

from sprotect.config import generate_default_config, load_config
from sprotect.types import Config, InterdependencyMode, ObfuscateLevel


def test_load_default_config() -> None:
    """Load config without arguments should return a default Config."""
    config = load_config()
    assert isinstance(config, Config)
    assert config.encrypt.interdependency == InterdependencyMode.CHAIN


def test_load_custom_config() -> None:
    """Load a custom JSON5 config file and verify field overrides."""
    content = """
    { project: { name: "testapp", entry: "app.py" },
      encrypt: { algorithm: "aes-256-gcm", shard_count: 5 } }
    """
    tmp = os.path.join(tempfile.gettempdir(), "_spt_test_config.json5")
    try:
        with open(tmp, "w", encoding="utf-8") as f:
            f.write(content)
        config = load_config(tmp)
        assert config.project.name == "testapp"
        assert config.encrypt.shard_count == 5
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)


def test_generate_default_config() -> None:
    """Generate a default config file then load and verify it."""
    tmp = os.path.join(tempfile.gettempdir(), "_spt_test_default.json5")
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
    tmp = os.path.join(tempfile.gettempdir(), "_spt_test_bad.json5")
    try:
        with open(tmp, "w", encoding="utf-8") as f:
            f.write(content)
        with pytest.raises(ValueError):
            load_config(tmp)
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)
