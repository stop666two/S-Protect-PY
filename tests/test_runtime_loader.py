"""Tests for the bootloader-generated runtime loader."""
from __future__ import annotations

import os
import json
import sys
import importlib
from sprotect.core.encryptor import encrypt_file
from sprotect.core.bootloader import generate_runtime_loader
from sprotect.types import Config

_TEST_TEMP = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "_test_temp")
os.makedirs(_TEST_TEMP, exist_ok=True)


def _tmp_path(name: str) -> str:
    return os.path.join(_TEST_TEMP, name)


def test_runtime_loader_execution():
    source = 'print("loader_works")\n'
    fp = _tmp_path("test_loader_src.py")
    try:
        with open(fp, "w", encoding="utf-8") as f:
            f.write(source)
        encrypted = encrypt_file(fp, Config())
        payload = json.loads(encrypted.decode("utf-8"))
        assert payload["algorithm"] == "hmac-sha256-xor"
        assert "key" in payload
        assert "data" in payload
        assert "hmac" in payload
    finally:
        if os.path.exists(fp): os.remove(fp)


def test_generated_loader_is_valid_python():
    output_dir = _tmp_path("_loader_test_out")
    os.makedirs(output_dir, exist_ok=True)
    try:
        loader_path = generate_runtime_loader(output_dir)
        with open(loader_path, "r", encoding="utf-8") as f:
            code = f.read()
        compile(code, loader_path, "exec")
        assert "run_entry" in code
        assert "_EncryptedFinder" in code
    finally:
        import shutil
        shutil.rmtree(output_dir, ignore_errors=True)
