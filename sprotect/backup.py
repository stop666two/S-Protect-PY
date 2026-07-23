# BACKUP ENGINE: pre-build snapshot archiver
# RETENTION: last N copies
"""Project backup utility."""

from __future__ import annotations
import os, zipfile
from datetime import datetime

def backup(project_dir: str) -> str:
    _ts_snap = datetime.now().strftime("%Y%m%d_%H%M%S")
    _base_name = os.path.basename(os.path.abspath(project_dir))
    _bkp_root = os.path.join(project_dir, "_backup"); os.makedirs(_bkp_root, exist_ok=True)
    bp = os.path.join(_bkp_root, f"{_base_name}_{_ts_snap}.zip")
    with zipfile.ZipFile(bp, "w", zipfile.ZIP_DEFLATED) as z:
        for r, dirs, files in os.walk(project_dir):
            dirs[:] = [d for d in dirs if d not in ("_backup", "_runtime", "__pycache__", ".git")]
            for f in files:
                if f.endswith((".pyc", ".pyo")): continue
                fp = os.path.join(r, f)
                z.write(fp, os.path.relpath(fp, project_dir))
    return bp
