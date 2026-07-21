"""End-to-end integration tests using envtest.py as the target."""
from __future__ import annotations

import os
import sys
import shutil
import subprocess
import tempfile

# 项目根目录
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_TEST_TEMP = os.path.join(PROJECT_ROOT, "_test_temp")
os.makedirs(_TEST_TEMP, exist_ok=True)


def test_envtest_encrypt_decrypt_roundtrip():
    """Encrypt envtest.py then verify the .pye payload structure."""
    envtest_path = os.path.join(PROJECT_ROOT, "envtest.py")
    assert os.path.exists(envtest_path), "envtest.py not found"

    from sprotect.core.encryptor import encrypt_file
    from sprotect.types import Config, ObfuscateConfig

    config = Config(obfuscate=ObfuscateConfig(encrypt_strings=False, encrypt_numbers=False))
    encrypted = encrypt_file(envtest_path, config)
    assert isinstance(encrypted, bytes)
    assert len(encrypted) > 0

    from sprotect.core.decryptor import decrypt_file
    decrypted, _ = decrypt_file(encrypted)
    assert "def main" in decrypted
    assert "envtest" in decrypted


def test_encrypt_project_structure():
    """Encrypt envtest.py as a project and verify _runtime/ structure."""
    envtest_path = os.path.join(PROJECT_ROOT, "envtest.py")
    import tempfile
    tmpdir = os.path.join(_TEST_TEMP, "_integ_test_" + str(os.getpid()))
    os.makedirs(tmpdir, exist_ok=True)
    shutil.copy2(envtest_path, os.path.join(tmpdir, "envtest.py"))
    try:
        from sprotect.core.project import find_python_files
        from sprotect.core.encryptor import encrypt_project
        from sprotect.types import Config, ObfuscateConfig, ProjectConfig

        config = Config(project=ProjectConfig(name="test", entry="envtest.py"),
                        obfuscate=ObfuscateConfig(encrypt_strings=False, encrypt_numbers=False))
        files = find_python_files(tmpdir, config)
        assert len(files) >= 1

        encrypt_project(tmpdir, config)
        runtime_dir = os.path.join(tmpdir, "_runtime")
        assert os.path.exists(runtime_dir)

        pye_file = os.path.join(runtime_dir, "envtest.pye")
        assert os.path.exists(pye_file), f"Missing {pye_file}"

        import json
        with open(pye_file, "r", encoding="utf-8") as f:
            payload = json.load(f)
        assert payload["type"] == "encrypted_python"
        assert "aes_key" in payload
        assert "data" in payload
        assert "source_hash" in payload
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


def test_obfuscated_envtest_still_executable():
    """Obfuscate envtest.py contents and verify the code still compiles."""
    envtest_path = os.path.join(PROJECT_ROOT, "envtest.py")
    with open(envtest_path, "r", encoding="utf-8") as f:
        source = f.read()

    from sprotect.core.obfuscator import Obfuscator
    from sprotect.types import ObfuscateConfig, ObfuscateLevel

    config = ObfuscateConfig(level=ObfuscateLevel.L3, encrypt_strings=False, encrypt_numbers=True)
    obf = Obfuscator(config)
    obfuscated = obf.obfuscate(source)
    assert obfuscated is not None
    assert len(obfuscated) > 0

    compile(obfuscated, "<test>", "exec")


def test_obfuscator_string_encryption_compiles():
    """Obfuscate a simple source with string/number encryption and verify it compiles."""
    source = 'x = "hello"\ny = 42\nz = x + "world"\nprint(z)\n'
    from sprotect.core.obfuscator import Obfuscator
    from sprotect.types import ObfuscateConfig, ObfuscateLevel

    config = ObfuscateConfig(level=ObfuscateLevel.L3, encrypt_strings=True, encrypt_numbers=True)
    obf = Obfuscator(config)
    obfuscated = obf.obfuscate(source)
    assert obfuscated is not None
    assert len(obfuscated) > 0

    compile(obfuscated, "<test>", "exec")


def test_project_file_discovery():
    """Test that find_python_files discovers .py files correctly."""
    from sprotect.core.project import find_python_files
    from sprotect.types import Config

    config = Config()
    files = find_python_files(PROJECT_ROOT, config)
    py_files = [f for f in files if f.endswith(".py")]
    assert len(py_files) >= 1
    assert any("envtest.py" in f for f in py_files)


def test_cli_version_exit_code():
    """Test that CLI version command returns 0."""
    from sprotect.cli import main
    result = main(["version"])
    assert result == 0


def test_backup_creates_zip():
    """Test backup creates a valid archive."""
    from sprotect.core.backup import backup_project
    tmpdir = os.path.join(_TEST_TEMP, "_backup_test_" + str(os.getpid()))
    os.makedirs(tmpdir, exist_ok=True)
    test_file = os.path.join(tmpdir, "test.py")
    with open(test_file, "w", encoding="utf-8") as f:
        f.write("x = 1\n")
    try:
        backup_path = backup_project(tmpdir)
        assert os.path.exists(backup_path)
        assert backup_path.endswith(".zip")
        import zipfile
        with zipfile.ZipFile(backup_path, "r") as zf:
            names = zf.namelist()
            assert any("test.py" in n for n in names)
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)
