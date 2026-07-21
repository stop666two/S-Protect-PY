"""Project scanning and file verification utilities.

Provides functions to locate Python source files within a project
directory and validate their syntax and existence.

Author: S-Protect Team
Version: 0.1.0
"""

from __future__ import annotations

import ast
import os
from typing import Optional

from sprotect.types import Config

_EXCLUDED_DIRS = frozenset({"_runtime", "_backup", "__pycache__", ".git", ".pytest_cache", "_test_temp"})


def find_python_files(project_dir: str, config: Config) -> list[str]:
    """Recursively find all .py files in a project directory.

    Excludes _runtime, _backup, __pycache__, .git, and .pytest_cache
    directories. The project's entry file (from config) is always
    included when found.

    Args:
        project_dir: Root directory of the project.
        config: Project configuration (used for entry file info).

    Returns:
        Sorted list of absolute paths to .py files.
    """
    result: list[str] = []
    for root, dirs, files in os.walk(project_dir):
        dirs[:] = [d for d in dirs if d not in _EXCLUDED_DIRS]
        for f in files:
            if f.endswith(".py"):
                result.append(os.path.join(root, f))
    result.sort()
    return result


def check_files(file_paths: list[str], config: Config) -> list[tuple[str, bool, str]]:
    """Check a list of files for existence and valid Python syntax.

    Args:
        file_paths: List of absolute file paths to check.
        config: Project configuration (unused currently, reserved).

    Returns:
        List of (file_path, is_valid, error_message) tuples. For valid
        files the error_message is an empty string.
    """
    results: list[tuple[str, bool, str]] = []
    for fp in file_paths:
        if not os.path.isfile(fp):
            results.append((fp, False, "File not found"))
            continue
        try:
            with open(fp, "rb") as f:
                source = f.read()
            ast.parse(source)
            results.append((fp, True, ""))
        except SyntaxError as e:
            results.append((fp, False, f"Syntax error: {e}"))
        except Exception as e:
            results.append((fp, False, f"Error: {e}"))
    return results
