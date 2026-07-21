"""Tests for the runtime .pye module loader.

Covers EncryptedModuleLoader loading and EncryptedPathFinder
module discovery.

Author: S-Protect Team
Version: 0.1.0
"""

from __future__ import annotations

import os
import sys

from sprotect.core.encryptor import encrypt_file
from sprotect.runtime.loader import EncryptedModuleLoader, EncryptedPathFinder
from sprotect.types import Config, ObfuscateConfig, ObfuscateLevel

_TEST_TEMP = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "_test_temp")
os.makedirs(_TEST_TEMP, exist_ok=True)


def _tmp_path(name: str) -> str:
    return os.path.join(_TEST_TEMP, name)


def _no_obf_config() -> Config:
    """Return a Config with all obfuscation features disabled."""
    c = Config()
    c.obfuscate = ObfuscateConfig(
        level=ObfuscateLevel.L1,
        rename_variables=False,
        rename_functions=False,
        rename_classes=False,
        encrypt_strings=False,
        encrypt_numbers=False,
        control_flow_flattening=False,
        dead_code_injection=False,
    )
    return c


def test_encrypted_module_loader() -> None:
    """EncryptedModuleLoader should load a .pye file and execute its code."""
    py_path = _tmp_path("_test_loader_source.py")
    pye_path = _tmp_path("_test_loader_source.pye")

    source = """
TEST_VAR = 42

def test_func() -> str:
    return "loaded"
"""
    with open(py_path, "w", encoding="utf-8") as f:
        f.write(source)

    config = _no_obf_config()
    try:
        payload = encrypt_file(py_path, config)
        with open(pye_path, "wb") as f:
            f.write(payload)

        loader = EncryptedModuleLoader("_test_loader_source", pye_path)
        import importlib.util

        spec = importlib.util.spec_from_loader("_test_loader_source", loader)
        assert spec is not None

        module = importlib.util.module_from_spec(spec)
        loader.exec_module(module)

        assert hasattr(module, "TEST_VAR")
        assert module.TEST_VAR == 42
        assert module.test_func() == "loaded"
    finally:
        for p in (py_path, pye_path):
            if os.path.exists(p):
                os.remove(p)


def test_path_finder() -> None:
    """EncryptedPathFinder should find and load .pye modules from _runtime."""
    runtime_dir = os.path.join(_TEST_TEMP, "_runtime_test")
    os.makedirs(runtime_dir, exist_ok=True)

    py_path = _tmp_path("_test_finder_module.py")
    pye_path = os.path.join(runtime_dir, "_test_finder_module.pye")

    source = """
FOUND_VAR = "found"
"""
    with open(py_path, "w", encoding="utf-8") as f:
        f.write(source)

    config = _no_obf_config()
    try:
        payload = encrypt_file(py_path, config)
        with open(pye_path, "wb") as f:
            f.write(payload)

        finder = EncryptedPathFinder(runtime_dir)

        spec = finder.find_spec("_test_finder_module", None)
        assert spec is not None
        assert spec.name == "_test_finder_module"
        assert isinstance(spec.loader, EncryptedModuleLoader)
        assert spec.origin == pye_path

        module = spec.loader.load_module("_test_finder_module")
        assert hasattr(module, "FOUND_VAR")
        assert module.FOUND_VAR == "found"
    finally:
        if os.path.exists(py_path):
            os.remove(py_path)
        if os.path.exists(pye_path):
            os.remove(pye_path)
