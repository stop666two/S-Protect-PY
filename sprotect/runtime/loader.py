"""Runtime module loader for encrypted .pye files.

Provides custom import hooks that intercept .pye module imports,
decrypt them in memory, and execute the resulting Python code.
This enables encrypted projects to run without exposing decrypted
source code on disk.

P4 Task 4-1 integration: loads the index.sig file, reconstructs
the private key from embedded shards, and uses RSA decryption to
unlock the JSON5 configuration before activating the import hook.

Author: S-Protect Team
Version: 0.1.0
"""

from __future__ import annotations

import importlib.abc
import importlib.machinery
import json
import os
import sys
from types import ModuleType
from typing import Any, Sequence

from sprotect.core.decryptor import decrypt_file
from sprotect.runtime.index import decrypt_index, verify_index_signature
from sprotect.runtime.shard_reconstructor import ShardReconstructor
from sprotect.types import Config
from sprotect.utils.crypto import rsa_decrypt


class EncryptedModuleLoader(importlib.abc.Loader):
    """Custom loader for .pye encrypted module files.

    Decrypts the .pye file content in memory and executes the
    resulting source code as a Python module.
    """

    def __init__(self, fullname: str, path: str) -> None:
        """Initialize the loader for a specific encrypted module.

        Args:
            fullname: Fully qualified module name (e.g. 'mymodule').
            path: Absolute path to the .pye file.
        """
        self.fullname = fullname
        self.path = path

    def create_module(self, spec: importlib.machinery.ModuleSpec) -> ModuleType | None:
        """Create a new module instance (defer to import system).

        Args:
            spec: The module spec for this module.

        Returns:
            None to let the import machinery create the module.
        """
        return None

    def exec_module(self, module: ModuleType) -> None:
        """Execute the module's decrypted source code.

        Reads the .pye file, decrypts it, and executes the source
        in the module's namespace.

        Args:
            module: The module object to populate.
        """
        with open(self.path, "rb") as f:
            encrypted_data = f.read()
        source_code, _ = decrypt_file(encrypted_data)
        code = compile(source_code, self.path, "exec")
        namespace = module.__dict__
        if "__file__" not in namespace and self.path:
            namespace["__file__"] = self.path
        exec(code, namespace)

    def get_code(self, fullname: str) -> Any:
        """Get the compiled code object for the module.

        Args:
            fullname: Fully qualified module name.

        Returns:
            The compiled code object.
        """
        with open(self.path, "rb") as f:
            encrypted_data = f.read()
        source_code, _ = decrypt_file(encrypted_data)
        return compile(source_code, self.path, "exec")

    def get_filename(self, fullname: str) -> str:
        """Get the filename associated with this module.

        Args:
            fullname: Fully qualified module name.

        Returns:
            The path to the .pye file.
        """
        return self.path

    def get_data(self, path: str) -> bytes:
        """Read raw data from a file path.

        Args:
            path: The file path to read.

        Returns:
            The raw bytes of the file.
        """
        with open(path, "rb") as f:
            return f.read()


class EncryptedPathFinder(importlib.abc.MetaPathFinder):
    """Meta path finder for .pye encrypted modules.

    Searches specified runtime directories for .pye files matching
    the requested module name.
    """

    def __init__(self, runtime_dir: str) -> None:
        """Initialize the finder with a runtime directory.

        Args:
            runtime_dir: Path to the _runtime directory containing
                         .pye files.
        """
        self.runtime_dir = runtime_dir

    def find_spec(
        self,
        fullname: str,
        path: Sequence[str] | None,
        target: ModuleType | None = None,
    ) -> importlib.machinery.ModuleSpec | None:
        """Search for a .pye module spec by module name.

        Args:
            fullname: Fully qualified module name to find.
            path: Search path (unused, finder uses its own dir).
            target: Optional target module (unused).

        Returns:
            A ModuleSpec if the .pye file is found, None otherwise.
        """
        pye_path = os.path.join(self.runtime_dir, fullname + ".pye")
        if os.path.isfile(pye_path):
            loader = EncryptedModuleLoader(fullname, pye_path)
            spec = importlib.machinery.ModuleSpec(
                name=fullname,
                loader=loader,
                origin=pye_path,
            )
            return spec
        return None


def _load_index_sig(runtime_dir: str) -> tuple[dict, bytes, bytes]:
    """Load and decrypt the index.sig file from the runtime directory.

    Reads ``index.sig`` (JSON with ``index_key``, ``signing_key``,
    ``encrypted_index``, ``rsa_encrypted_config`` fields), decrypts
    the index, verifies its signature, and returns the index dict,
    the signing key, and the RSA-encrypted config blob.

    Args:
        runtime_dir: Path to the ``_runtime`` directory.

    Returns:
        A tuple of (index_dict, signing_key, rsa_encrypted_config).

    Raises:
        FileNotFoundError: If index.sig does not exist.
        ValueError: If index signature verification fails.
    """
    sig_path = os.path.join(runtime_dir, "index.sig")
    if not os.path.isfile(sig_path):
        raise FileNotFoundError(f"Index file not found: {sig_path}")

    with open(sig_path, "rb") as f:
        sig_data = json.loads(f.read().decode("utf-8"))

    index_key = bytes.fromhex(sig_data["index_key"])
    signing_key = bytes.fromhex(sig_data["signing_key"])
    encrypted_index = bytes.fromhex(sig_data["encrypted_index"])
    rsa_encrypted_config = bytes.fromhex(sig_data["rsa_encrypted_config"])

    index = decrypt_index(encrypted_index, index_key)
    if not verify_index_signature(index, signing_key):
        raise ValueError("Index signature verification failed")

    return index, signing_key, rsa_encrypted_config


def _decrypt_config(
    rsa_encrypted_config: bytes, private_key: bytes
) -> Config:
    """Decrypt the RSA-encrypted JSON5 configuration.

    Args:
        rsa_encrypted_config: RSA OAEP ciphertext of the config JSON.
        private_key: PEM-encoded RSA private key bytes.

    Returns:
        A Config object parsed from the decrypted JSON.
    """
    from sprotect.config import _dict_to_config

    plaintext = rsa_decrypt(rsa_encrypted_config, private_key)
    config_data: dict = json.loads(plaintext.decode("utf-8"))
    return _dict_to_config(config_data)


def run_encrypted_project(project_dir: str, config: Config) -> None:
    """Run an encrypted project from its _runtime directory.

    Two modes:
      1. Full secure mode: loads index.sig, reconstructs private key from
         shards, decrypts RSA-encrypted config, installs import hook.
      2. Simple mode: directly decrypts the entry .pye file and runs it.

    Args:
        project_dir: Root directory of the encrypted project.
        config: Project configuration (used for entry file name).
    """
    runtime_dir = os.path.join(project_dir, "_runtime")
    if not os.path.isdir(runtime_dir):
        raise FileNotFoundError(f"Runtime directory not found: {runtime_dir}")

    sig_path = os.path.join(runtime_dir, "index.sig")
    if os.path.isfile(sig_path):
        index, signing_key, rsa_encrypted_config = _load_index_sig(runtime_dir)
        reconstructor = ShardReconstructor(runtime_dir, index)
        private_key = reconstructor.reconstruct_private_key()
        resolved_config = _decrypt_config(rsa_encrypted_config, private_key)
        entry_module = resolved_config.project.entry.replace(".py", "")
    else:
        entry_module = config.project.entry.replace(".py", "")

    finder = EncryptedPathFinder(runtime_dir)
    sys.meta_path.insert(0, finder)

    mod = __import__(entry_module)
    mod.__dict__.setdefault("__name__", "__main__")
    main_fn = mod.__dict__.get("main")
    if main_fn is not None and callable(main_fn):
        main_fn()
