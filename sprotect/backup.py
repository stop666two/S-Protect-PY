"""Project backup utility."""

from __future__ import annotations
import os, zipfile
from datetime import datetime

def backup(project_dir: str) -> str:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    name = os.path.basename(os.path.abspath(project_dir))
    bdir = os.path.join(project_dir, "_backup"); os.makedirs(bdir, exist_ok=True)
    bp = os.path.join(bdir, f"{name}_{ts}.zip")
    with zipfile.ZipFile(bp, "w", zipfile.ZIP_DEFLATED) as z:
        for r, dirs, files in os.walk(project_dir):
            dirs[:] = [d for d in dirs if d not in ("_backup", "_runtime", "__pycache__", ".git")]
            for f in files:
                if f.endswith((".pyc", ".pyo")): continue
                fp = os.path.join(r, f)
                z.write(fp, os.path.relpath(fp, project_dir))
    return bp
