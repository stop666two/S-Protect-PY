"""Project scanning and file verification utilities.

Provides functions to locate Python source files within a project
directory and validate their syntax and existence.
"""

from __future__ import annotations

import ast
import os
from pathlib import PurePath
from typing import Optional

from sprotect.types import Config


def _glob_match(path: str, pattern: str) -> bool:
    """Match a path against a glob pattern, supporting ``**``.

    Args:
        path: Relative file path (e.g. ``subdir/file.py``).
        pattern: Glob pattern (e.g. ``**/*.py``, ``tests/**``).

    Returns:
        True if the path matches the pattern.
    """
    import fnmatch
    parts = path.replace("\\", "/").split("/")
    pat_parts = pattern.replace("\\", "/").split("/")

    def _match(pp, pi, si):
        if pi == len(pat_parts) and si == len(parts):
            return True
        if pi >= len(pat_parts):
            return False
        if pat_parts[pi] == "**":
            if pi + 1 == len(pat_parts):
                return True
            for i in range(si, len(parts) + 1):
                if _match(pp, pi + 1, i):
                    return True
            return False
        if si >= len(parts):
            return False
        if fnmatch.fnmatch(parts[si], pat_parts[pi]):
            return _match(pp, pi + 1, si + 1)
        return False

    return _match(pattern, 0, 0)


def find_python_files(project_dir: str, config: Config) -> list[str]:
    """Recursively find all .py files in a project directory.

    Applies include/exclude patterns from ``config.files``.
    Skips files not matching include patterns.

    Args:
        project_dir: Root directory of the project.
        config: Project configuration (files.include, files.exclude).

    Returns:
        Sorted list of absolute paths to .py files.
    """
    inc = config.files.include or ["**/*.py"]
    exc = config.files.exclude or []
    root_abs = os.path.abspath(project_dir)
    result: list[str] = []
    for root, dirs, files in os.walk(root_abs):
        dirs[:] = [d for d in dirs if not d.startswith("_") and not d.startswith(".")]
        for f in files:
            if not f.endswith(".py"):
                continue
            fp = os.path.join(root, f)
            rel = os.path.relpath(fp, root_abs).replace("\\", "/")

            def _any_match(patterns: list[str], p: str) -> bool:
                for pat in patterns:
                    if _glob_match(p, pat):
                        return True
                return False

            if not _any_match(inc, rel):
                continue
            if _any_match(exc, rel):
                continue
            result.append(fp)
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
