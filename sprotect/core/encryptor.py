"""Encryption engine for S-Protect-PY.

Encrypts individual Python files and entire projects using AES-256-GCM.
When configured, applies AST-based obfuscation before encryption.
Outputs JSON payloads containing algorithm metadata, AES key, ciphertext,
and source hash for integrity verification.

Author: S-Protect Team
Version: 0.1.0
"""

from __future__ import annotations

import json
import os

from sprotect.core.obfuscator import Obfuscator
from sprotect.core.project import find_python_files
from sprotect.types import Config
from sprotect.utils.crypto import aes_encrypt, generate_aes_key, sha256_hash


def encrypt_file(file_path: str, config: Config) -> bytes:
    """Encrypt a single Python source file.

    1. Reads the source file.
    2. If obfuscation is enabled, applies the Obfuscator.
    3. Generates an AES key and encrypts the (obfuscated) source.
    4. Returns a JSON payload with type, algorithm, aes_key, data, and
       source_hash fields.

    Args:
        file_path: Path to the .py file to encrypt.
        config: Project configuration (encrypt + obfuscate settings).

    Returns:
        JSON-encoded bytes containing the encryption payload.

    Raises:
        FileNotFoundError: If file_path does not exist.
    """
    with open(file_path, "rb") as f:
        source_bytes = f.read()

    source_code = source_bytes.decode("utf-8")

    if config.obfuscate.level.value >= 1:
        obf = Obfuscator(config.obfuscate)
        source_code = obf.obfuscate(source_code)

    source_data = source_code.encode("utf-8")
    source_hash = sha256_hash(source_data)
    aes_key = generate_aes_key()
    encrypted = aes_encrypt(source_data, aes_key)

    payload = {
        "type": "encrypted_python",
        "algorithm": "aes-256-gcm",
        "aes_key": aes_key.hex(),
        "data": encrypted.hex(),
        "source_hash": source_hash,
    }

    return json.dumps(payload, indent=2).encode("utf-8")


def encrypt_project(project_dir: str, config: Config) -> None:
    """Encrypt all .py files in a project.

    Scans project_dir for .py files, encrypts each one, and writes
    the encrypted payload to a _runtime/ subdirectory with a .pye
    extension.

    Args:
        project_dir: Root directory of the project to encrypt.
        config: Project configuration.

    Raises:
        FileNotFoundError: If project_dir does not exist.
    """
    py_files = find_python_files(project_dir, config)
    runtime_dir = os.path.join(project_dir, "_runtime")
    os.makedirs(runtime_dir, exist_ok=True)

    for py_path in py_files:
        rel = os.path.relpath(py_path, project_dir)
        pye_name = rel.replace(".py", ".pye")
        pye_path = os.path.join(runtime_dir, pye_name)
        os.makedirs(os.path.dirname(pye_path), exist_ok=True)

        payload = encrypt_file(py_path, config)
        with open(pye_path, "wb") as f:
            f.write(payload)


def encrypt_files(file_paths: list[str], config: Config) -> list[str]:
    """Encrypt a specific list of files, generating .pye output.

    Each .py file is encrypted and written to a sibling .pye file in
    the same directory.

    Args:
        file_paths: List of absolute paths to .py files.
        config: Project configuration.

    Returns:
        List of absolute paths to the generated .pye files.
    """
    out_paths: list[str] = []
    for fp in file_paths:
        payload = encrypt_file(fp, config)
        pye_path = fp.replace(".py", ".pye")
        with open(pye_path, "wb") as f:
            f.write(payload)
        out_paths.append(pye_path)
    return out_paths
