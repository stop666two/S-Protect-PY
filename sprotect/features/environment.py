"""Environment fingerprint binding for S-Protect-PY.

Binds encrypted projects to specific environments (directory, username,
environment variables) to prevent unauthorized relocation or execution.

Author: S-Protect Team
Version: 0.1.0
"""

from __future__ import annotations

import hashlib
import os
import platform

from sprotect.types import EnvironmentConfig


class EnvironmentBinder:
    """Environment fingerprint binder.

    Verifies that the current execution environment matches the
    expected bindings and generates a composite fingerprint from
    platform, node, cwd, username, and computername.
    """

    def __init__(self, config: EnvironmentConfig) -> None:
        """Initialize the binder with environment configuration.

        Args:
            config: Environment binding configuration.
        """
        self.config = config

    def verify_environment(self) -> bool:
        """Verify that the current environment matches the bindings.

        Checks the current working directory, username, and environment
        variable values against the configured bindings.  Returns
        ``True`` only if all enabled bindings match.

        Returns:
            True if the environment matches, False otherwise.
        """
        if self.config.bind_directory is not None:
            cwd = os.path.abspath(os.getcwd())
            bind_dir = os.path.abspath(self.config.bind_directory)
            if cwd != bind_dir:
                return False

        if self.config.bind_username is not None:
            try:
                current_user = os.getlogin()
            except OSError:
                current_user = os.environ.get("USERNAME", os.environ.get("USER", ""))
            if current_user != self.config.bind_username:
                return False

        for var_name in self.config.bind_env_vars:
            if var_name not in os.environ:
                return False

        return True

    def generate_fingerprint(self) -> str:
        """Generate a composite environment fingerprint.

        Computes SHA-256 of the concatenation of:
        ``platform + node + cwd + username + computername``

        Returns:
            A 64-character lowercase hex SHA-256 digest.
        """
        raw = "|".join([
            platform.system(),
            platform.node(),
            os.path.abspath(os.getcwd()),
            os.environ.get("USERNAME", os.environ.get("USER", "")),
            os.environ.get("COMPUTERNAME", platform.node()),
        ])
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()
