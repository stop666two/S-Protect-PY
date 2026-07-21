"""Tests for the encryption and decryption engine.

Covers round-trip encryption/decryption, wrong-key rejection, and
combined obfuscation + encryption.

Author: S-Protect Team
Version: 0.1.0
"""

from __future__ import annotations

import os

import pytest

from sprotect.core.decryptor import decrypt_file
from sprotect.core.encryptor import encrypt_file
from sprotect.types import Config, ObfuscateConfig, ObfuscateLevel, NamingStyle, RenameRules

_TEST_TEMP = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "_test_temp")
os.makedirs(_TEST_TEMP, exist_ok=True)


def _tmp_path(name: str) -> str:
    return os.path.join(_TEST_TEMP, name)


def _write_source(path: str, content: str) -> str:
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path


SAMPLE_CODE = """
def greet(name: str) -> str:
    return "Hello, " + name + "!"
"""


def test_encrypt_decrypt_roundtrip() -> None:
    """Encrypting and then decrypting should return the original content."""
    py_path = _tmp_path("_test_roundtrip.py")
    pye_path = _tmp_path("_test_roundtrip.pye")

    _write_source(py_path, SAMPLE_CODE)
    config = Config()
    config.obfuscate = ObfuscateConfig(
        level=ObfuscateLevel.L1,
        rename_variables=False,
        rename_functions=False,
        rename_classes=False,
        encrypt_strings=False,
        encrypt_numbers=False,
        control_flow_flattening=False,
        dead_code_injection=False,
    )

    try:
        payload = encrypt_file(py_path, config)

        with open(pye_path, "wb") as f:
            f.write(payload)

        with open(pye_path, "rb") as f:
            encrypted_data = f.read()

        decrypted, _ = decrypt_file(encrypted_data)

        exec_orig: dict = {}
        exec(compile(SAMPLE_CODE.strip(), "<orig>", "exec"), exec_orig)
        exec_dec: dict = {}
        exec(compile(decrypted.strip(), "<dec>", "exec"), exec_dec)
        assert exec_dec["greet"]("World") == exec_orig["greet"]("World")
    finally:
        for p in (py_path, pye_path):
            if os.path.exists(p):
                os.remove(p)


def test_decrypt_wrong_key_fails() -> None:
    """Decrypting with a wrong AES key should raise an error."""
    py_path = _tmp_path("_test_wrongkey.py")
    _write_source(py_path, SAMPLE_CODE)
    config = Config()

    try:
        payload = encrypt_file(py_path, config)

        payload_str = payload.decode("utf-8")
        payload_str = payload_str.replace('"aes-256-gcm"', '"aes-256-gcm"')
        import json

        parsed = json.loads(payload_str)
        parsed["aes_key"] = "ff" * 32
        tampered = json.dumps(parsed).encode("utf-8")

        with pytest.raises(Exception):
            decrypt_file(tampered)
    finally:
        if os.path.exists(py_path):
            os.remove(py_path)


def test_encrypt_with_obfuscation() -> None:
    """Encrypting with obfuscation enabled should transform the source."""
    py_path = _tmp_path("_test_obfenc.py")
    _write_source(py_path, SAMPLE_CODE)

    obf_config = ObfuscateConfig(
        level=ObfuscateLevel.L1,
        rename_variables=True,
        rename_functions=True,
        encrypt_strings=False,
        encrypt_numbers=False,
        control_flow_flattening=False,
        dead_code_injection=False,
    )
    config = Config()
    config.obfuscate = obf_config

    try:
        payload = encrypt_file(py_path, config)
        decrypted, _ = decrypt_file(payload)

        assert "greet" not in decrypted
        assert "Hello" in decrypted

        exec_globals: dict = {}
        exec(compile(decrypted, "<test>", "exec"), exec_globals)
        func_name = [
            k for k in exec_globals
            if callable(exec_globals[k]) and not k.startswith("__")
        ][0]
        assert exec_globals[func_name]("World") == "Hello, World!"
    finally:
        if os.path.exists(py_path):
            os.remove(py_path)


def test_decrypt_corrupted_data_fails() -> None:
    """Decrypting corrupted ciphertext should raise an error."""
    py_path = _tmp_path("_test_corrupted.py")
    _write_source(py_path, SAMPLE_CODE)
    config = Config()

    try:
        payload = encrypt_file(py_path, config)

        raw = bytearray(payload)
        if len(raw) > 100:
            raw[len(raw) // 2] ^= 0xFF

        with pytest.raises(Exception):
            decrypt_file(bytes(raw))
    finally:
        if os.path.exists(py_path):
            os.remove(py_path)
