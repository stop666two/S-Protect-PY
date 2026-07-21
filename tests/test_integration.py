"""End-to-end integration tests using envtest.py as target."""
from __future__ import annotations

import os
import sys
import shutil
from pathlib import Path
from sprotect.core.encryptor import build_project, encrypt_file
from sprotect.core.decryptor import decrypt_file
from sprotect.core.project import find_python_files
from sprotect.types import Config, ProjectConfig

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_TEST_TEMP = os.path.join(PROJECT_ROOT, "_test_temp")


def test_envtest_encrypt_decrypt_roundtrip():
    envtest = os.path.join(PROJECT_ROOT, "envtest.py")
    assert os.path.exists(envtest)
    encrypted = encrypt_file(envtest, Config())
    decrypted, _ = decrypt_file(encrypted)
    assert "def main" in decrypted


def test_build_project_structure():
    envtest = os.path.join(PROJECT_ROOT, "envtest.py")
    proj_dir = os.path.join(_TEST_TEMP, "_integ_proj")
    out_dir = os.path.join(_TEST_TEMP, "_integ_out")
    try:
        os.makedirs(proj_dir, exist_ok=True)
        shutil.copy2(envtest, os.path.join(proj_dir, "main.py"))
        cfg = Config(project=ProjectConfig(name="test", entry="main.py"))
        build_project(proj_dir, out_dir, cfg)
        assert os.path.isfile(os.path.join(out_dir, "main.py"))
        assert os.path.isfile(os.path.join(out_dir, "_runtime", "main.pye"))
        assert os.path.isfile(os.path.join(out_dir, "_runtime", "loader.py"))
    finally:
        shutil.rmtree(proj_dir, ignore_errors=True)
        shutil.rmtree(out_dir, ignore_errors=True)


def test_obfuscated_envtest_still_executable():
    envtest = os.path.join(PROJECT_ROOT, "envtest.py")
    with open(envtest, "r", encoding="utf-8") as f:
        source = f.read()
    from sprotect.core.obfuscator import Obfuscator
    from sprotect.types import ObfuscateConfig, ObfuscateLevel
    cfg = ObfuscateConfig(level=ObfuscateLevel.L3, encrypt_strings=False, encrypt_numbers=False)
    obf = Obfuscator(cfg)
    obfuscated = obf.obfuscate(source)
    compile(obfuscated, "<test>", "exec")


def test_project_file_discovery():
    files = find_python_files(PROJECT_ROOT, Config())
    py = [f for f in files if f.endswith(".py")]
    assert len(py) >= 1


def test_cli_version():
    from sprotect.cli import main
    assert main(["version"]) == 0
