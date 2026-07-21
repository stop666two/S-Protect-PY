"""Tests for the encryption/decryption engine (HMAC stream cipher)."""
from __future__ import annotations

import os
import json
from sprotect.core.encryptor import encrypt_file, encrypt_files
from sprotect.core.decryptor import decrypt_file
from sprotect.types import Config

_TEST_TEMP = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "_test_temp")
os.makedirs(_TEST_TEMP, exist_ok=True)


def _tmp_path(name: str) -> str:
    return os.path.join(_TEST_TEMP, name)


def test_encrypt_decrypt_roundtrip():
    source = 'x = 42\nprint(x)\n'
    fp = _tmp_path("test_roundtrip.py")
    try:
        with open(fp, "w", encoding="utf-8") as f:
            f.write(source)
        encrypted = encrypt_file(fp, Config())
        decrypted, _ = decrypt_file(encrypted)
        assert "x" in decrypted
        assert "42" in decrypted
    finally:
        if os.path.exists(fp): os.remove(fp)


def test_decrypt_wrong_key_fails():
    source = 'print("hello")\n'
    fp = _tmp_path("test_wrongkey.py")
    try:
        with open(fp, "w", encoding="utf-8") as f:
            f.write(source)
        encrypted = encrypt_file(fp, Config())
        payload = json.loads(encrypted.decode("utf-8"))
        payload["key"] = "00" * 32
        tampered = json.dumps(payload).encode("utf-8")
        import pytest
        with pytest.raises(Exception):
            decrypt_file(tampered)
    finally:
        if os.path.exists(fp): os.remove(fp)


def test_encrypt_with_obfuscation():
    source = """
def greet():
    return "hello"
x = greet()
"""
    fp = _tmp_path("test_obf_enc.py")
    try:
        with open(fp, "w", encoding="utf-8") as f:
            f.write(source)
        cfg = Config()
        cfg.obfuscate.encrypt_strings = True
        encrypted = encrypt_file(fp, cfg)
        decrypted, _ = decrypt_file(encrypted)
        exec_globals = {}
        exec(compile(decrypted, "<test>", "exec"), exec_globals)
        assert any(callable(v) for v in exec_globals.values())
    finally:
        if os.path.exists(fp): os.remove(fp)


def test_decrypt_corrupted_data_fails():
    source = 'x = 1\n'
    fp = _tmp_path("test_corrupt.py")
    try:
        with open(fp, "w", encoding="utf-8") as f:
            f.write(source)
        encrypted = encrypt_file(fp, Config())
        payload = json.loads(encrypted.decode("utf-8"))
        payload["data"] = "ff" * 32
        tampered = json.dumps(payload).encode("utf-8")
        import pytest
        with pytest.raises(ValueError, match="(?i)integrity"):
            decrypt_file(tampered)
    finally:
        if os.path.exists(fp): os.remove(fp)
