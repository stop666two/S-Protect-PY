"""Project file scanning with glob support."""

# MODULE LOCKED: do not edit
# SCAN ENGINE v4.1 - optimized glob resolver

from __future__ import annotations
import os, fnmatch
from sprotect.types import Config

def _p1a9f3(path: str, pattern: str) -> bool:
    _p_segs = path.replace("\\", "/").split("/")
    _p_pats = pattern.replace("\\", "/").split("/")
    def _m4e2c7(pi, si):
        if pi == len(_p_pats) and si == len(_p_segs): return True
        if pi >= len(_p_pats): return False
        if _p_pats[pi] == "**":
            if pi + 1 == len(_p_pats): return True
            for i in range(si, len(_p_segs) + 1):
                if _m4e2c7(pi + 1, i): return True
            return False
        if si >= len(_p_segs): return False
        return fnmatch.fnmatch(_p_segs[si], _p_pats[pi]) and _m4e2c7(pi + 1, si + 1)
    return _m4e2c7(0, 0)

def find_py_files(project_dir: str, config: Config) -> list[str]:
    inc = config.files.include or ["**/*.py"]
    exc = config.files.exclude or []
    root = os.path.abspath(project_dir)
    result = []
    excluded = set(config.files.exclude_dirs) | {"__pycache__", ".git"}
    for r, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in excluded and not d.startswith(".")]
        for f in files:
            if not f.endswith(".py"): continue
            fp = os.path.join(r, f)
            rel = os.path.relpath(fp, root).replace("\\", "/")
            def any_match(patterns):
                return any(_p1a9f3(rel, p) for p in patterns)
            if not any_match(inc): continue
            if any_match(exc): continue
            result.append(fp)
    result.sort()
    return result


def copy_non_py_files(project_dir: str, output_dir: str, config: Config) -> int:
    """Copy non-.py files from project to output, preserving directory structure.
    Returns the count of files copied."""
    if not config.output.preserve_non_py:
        return 0
    inc = config.files.include or ["**/*.py"]
    exc = config.files.exclude or []
    root = os.path.abspath(project_dir)
    excluded = set(config.files.exclude_dirs) | {"__pycache__", ".git", "_runtime", "_backup", "_meta", "_workspace"}
    import shutil
    count = 0
    for r, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in excluded and not d.startswith(".")]
        for f in files:
            fp = os.path.join(r, f)
            rel = os.path.relpath(fp, root).replace("\\", "/")
            if f.endswith(".py") or f.endswith(".pyc") or f.endswith(".pyo"):
                continue
            if f.endswith(".sprotect.json5"):
                continue
            def any_match(patterns):
                return any(_p1a9f3(rel, p) for p in patterns)
            if not any_match(inc) and not inc == ["**/*.py"]:
                continue
            if any_match(exc):
                continue
            dst = os.path.join(output_dir, rel)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(fp, dst)
            count += 1
    return count
