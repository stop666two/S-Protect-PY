"""Runtime module loader for encrypted .pye files.

Provides custom import hooks that intercept .pye module imports,
decrypt them in memory, and execute the resulting Python code.
This enables encrypted projects to run without exposing decrypted
source code on disk.

Author: S-Protect Team
Version: 0.1.0
"""

from __future__ import annotations

import importlib.abc
import importlib.machinery
import os
import sys
from types import ModuleType
from typing import Any, Sequence

from sprotect.core.decryptor import decrypt_file
from sprotect.types import Config


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
        exec(code, module.__dict__)

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


def run_encrypted_project(project_dir: str, config: Config) -> None:
    """Run an encrypted project from its _runtime directory.

    Installs the EncryptedPathFinder into sys.meta_path, then imports
    and executes the project's entry module.

    Args:
        project_dir: Root directory of the encrypted project.
        config: Project configuration (used for entry file name).
    """
    runtime_dir = os.path.join(project_dir, "_runtime")
    if not os.path.isdir(runtime_dir):
        raise FileNotFoundError(f"Runtime directory not found: {runtime_dir}")

    finder = EncryptedPathFinder(runtime_dir)
    sys.meta_path.insert(0, finder)

    entry_module = config.project.entry.replace(".py", "")
    __import__(entry_module)
