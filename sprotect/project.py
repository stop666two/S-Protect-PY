"""Project file scanning with glob support."""

from __future__ import annotations
import os, fnmatch
from sprotect.types import Config

def _glob_match(path: str, pattern: str) -> bool:
    parts = path.replace("\\", "/").split("/")
    pats = pattern.replace("\\", "/").split("/")
    def m(pi, si):
        if pi == len(pats) and si == len(parts): return True
        if pi >= len(pats): return False
        if pats[pi] == "**":
            if pi + 1 == len(pats): return True
            for i in range(si, len(parts) + 1):
                if m(pi + 1, i): return True
            return False
        if si >= len(parts): return False
        return fnmatch.fnmatch(parts[si], pats[pi]) and m(pi + 1, si + 1)
    return m(0, 0)

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
                return any(_glob_match(rel, p) for p in patterns)
            if not any_match(inc): continue
            if any_match(exc): continue
            result.append(fp)
    result.sort()
    return result
