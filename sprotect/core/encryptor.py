"""Encryption engine for S-Protect-PY.

Encrypts Python source files using HMAC-SHA256 stream cipher.
Outputs self-contained encrypted projects to output/ directory.
Runtime decryption uses only Python stdlib (zero external deps).
"""

from __future__ import annotations

import hmac
import hashlib
import json
import os
import secrets
from pathlib import Path

from sprotect.core.obfuscator import Obfuscator
from sprotect.core.project import find_python_files
from sprotect.core.bootloader import generate_bootloader, generate_runtime_loader
from sprotect.types import Config


def _xor_stream(key: bytes, data: bytes) -> bytes:
    out = bytearray(len(data))
    for i in range(0, len(data), 32):
        ctr = (i // 32).to_bytes(8, "big")
        stream = hmac.new(key, ctr, "sha256").digest()
        chunk = data[i:i+32]
        for j in range(len(chunk)):
            out[i+j] = chunk[j] ^ stream[j]
    return bytes(out)


def encrypt_file(file_path: str, config: Config) -> bytes:
    """Encrypt a single Python source file.

    Reads source, optionally obfuscates, encrypts with HMAC stream cipher,
    returns JSON payload with key, ciphertext, and HMAC integrity tag.

    Args:
        file_path: Path to .py file.
        config: Project configuration.

    Returns:
        JSON-encoded bytes: {key, data, hmac, source_hash}
    """
    with open(file_path, "rb") as f:
        source_bytes = f.read()
    source_code = source_bytes.decode("utf-8")

    if config.obfuscate.level.value >= 1:
        obf = Obfuscator(config.obfuscate)
        source_code = obf.obfuscate(source_code)

    source_data = source_code.encode("utf-8")
    source_hash = hashlib.sha256(source_data).hexdigest()
    key = secrets.token_bytes(32)
    ct = _xor_stream(key, source_data)
    sig = hmac.new(key, ct, "sha256").hexdigest()

    payload = {
        "type": "encrypted_python",
        "algorithm": "hmac-sha256-xor",
        "key": key.hex(),
        "data": ct.hex(),
        "hmac": sig,
        "source_hash": source_hash,
    }
    return json.dumps(payload, indent=2).encode("utf-8")


def build_project(project_dir: str, output_dir: str, config: Config) -> None:
    """Build an encrypted project from project/ to output/.

    1. Scans all .py files in project_dir
    2. Obfuscates + encrypts each file
    3. Writes encrypted .pye files to output/_runtime/
    4. Generates bootloader entry point in output/
    5. Structure mirrors the original project

    Args:
        project_dir: Source project directory.
        output_dir: Output directory for encrypted project.
        config: Project configuration.
    """
    py_files = find_python_files(project_dir, config)
    runtime_dir = os.path.join(output_dir, "_runtime")
    os.makedirs(runtime_dir, exist_ok=True)

    for py_path in py_files:
        rel = os.path.relpath(py_path, project_dir)
        pye_name = rel.replace(".py", ".pye")
        pye_path = os.path.join(runtime_dir, pye_name)
        os.makedirs(os.path.dirname(pye_path), exist_ok=True)
        payload = encrypt_file(py_path, config)
        with open(pye_path, "wb") as f:
            f.write(payload)

    generate_runtime_loader(output_dir)
    entry_module = config.project.entry.replace(".py", "")
    generate_bootloader(output_dir, entry_module)

    req_path = os.path.join(output_dir, "requirements.txt")
    if not os.path.exists(req_path):
        with open(req_path, "w", encoding="utf-8") as f:
            f.write("# Add your project dependencies here\n")


def encrypt_files(file_paths: list[str], config: Config) -> list[str]:
    """Encrypt individual files, output .pye alongside source.

    Args:
        file_paths: List of paths to .py files.
        config: Project configuration.

    Returns:
        List of output .pye paths.
    """
    out_paths: list[str] = []
    for fp in file_paths:
        payload = encrypt_file(fp, config)
        pye_path = fp.replace(".py", ".pye")
        with open(pye_path, "wb") as f:
            f.write(payload)
        out_paths.append(pye_path)
    return out_paths
