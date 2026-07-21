"""Project backup and restore for S-Protect-PY.

Creates ZIP archives of the project directory with configurable
exclusions and restores them on demand.

Author: S-Protect Team
Version: 0.1.0
"""

from __future__ import annotations

import os
import zipfile
from datetime import datetime
from typing import Optional

_BACKUP_EXCLUDE = {"_backup", "_runtime", "__pycache__", ".git"}
_BACKUP_DIR = "_backup"


def backup_project(project_dir: str, suffix: Optional[str] = None) -> str:
    """Create a ZIP backup of the project directory.

    Excludes ``_backup/``, ``_runtime/``, ``__pycache__/``, and
    ``.git/`` directories.  The backup file is stored inside
    ``_backup/`` in the project directory.

    Args:
        project_dir: The root directory of the project to back up.
        suffix: Optional label appended to the backup filename.
                If omitted, a timestamp is used.

    Returns:
        The absolute path to the created backup ZIP file.
    """
    if suffix is None:
        suffix = datetime.now().strftime("pre_%Y%m%d_%H%M%S")

    backup_dir = os.path.join(project_dir, _BACKUP_DIR)
    os.makedirs(backup_dir, exist_ok=True)

    backup_path = os.path.join(backup_dir, f"{suffix}.zip")

    with zipfile.ZipFile(backup_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(project_dir):
            rel_root = os.path.relpath(root, project_dir)
            if rel_root == ".":
                rel_root = ""

            dirs[:] = [d for d in dirs if d not in _BACKUP_EXCLUDE]

            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.join(rel_root, file) if rel_root else file
                zf.write(file_path, arcname)

    return os.path.abspath(backup_path)


def restore_backup(backup_path: str, target_dir: str) -> None:
    """Restore a backup ZIP file to the target directory.

    Overwrites existing files.  Creates the target directory if it
    does not exist.

    Args:
        backup_path: Path to the backup ZIP file.
        target_dir: Directory to extract the backup into.
    """
    os.makedirs(target_dir, exist_ok=True)

    with zipfile.ZipFile(backup_path, "r") as zf:
        zf.extractall(target_dir)
