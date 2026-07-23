# PACK MODULE: PyInstaller integration bridge
# TARGET: single-file executable

"""Pack encrypted output into single executable via PyInstaller."""

from __future__ import annotations
import os, sys, subprocess, shutil, glob, ast, re
from sprotect.types import PackConfig


def _harvest_dependencies(project_dir: str) -> list[str]:
    """Scan .py files for imports to help PyInstaller find them."""
    imports: set[str] = set()
    for f in sorted(glob.glob(os.path.join(project_dir, "**", "*.py"), recursive=True)):
        try:
            tree = ast.parse(open(f, encoding="utf-8-sig").read())
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.add(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module and not node.module.startswith("_"):
                        imports.add(node.module)
        except SyntaxError:
            pass
    return sorted(imports)


def pack(output_dir: str, cfg: PackConfig) -> str | None:
    """Run PyInstaller on output_dir to produce a single exe.

    Returns path to the generated executable, or None on failure.
    """
    if not shutil.which("pyinstaller"):
        print("  PyInstaller not found. Install with: pip install pyinstaller")
        return None

    output_dir = os.path.abspath(output_dir)
    _parent_dir = os.path.dirname(output_dir)
    _artifact_name = os.path.basename(output_dir)

    _entry_point = os.path.join(output_dir, "main.py")
    if not os.path.isfile(_entry_point):
        print(f"  Entry not found: {_entry_point}")
        return None

    project_dir = os.path.join(os.path.dirname(output_dir), "project")
    if not os.path.isdir(project_dir):
        project_dir = output_dir
    _dep_list = _harvest_dependencies(project_dir)
    _hidden_imports_args = [
        "--hidden-import=hmac", "--hidden-import=json", "--hidden-import=zlib",
        "--hidden-import=hashlib", "--hidden-import=importlib.abc",
        "--hidden-import=importlib.machinery",
        "--hidden-import=cryptography", "--hidden-import=cryptography.hazmat.primitives.ciphers.aead",
        "--hidden-import=blake3", "--hidden-import=Cryptodome",
    ] + [f"--hidden-import={m}" for m in _dep_list]
    for pkg in set(m.split(".")[0] for m in _dep_list):
        if pkg not in ("cryptography", "Cryptodome"):
            _hidden_imports_args.append(f"--collect-all={pkg}")
    _exec_args = [
        sys.executable, "-m", "PyInstaller",
        "--distpath", os.path.join(_parent_dir, "dist"),
        "--workpath", os.path.join(_parent_dir, "build"),
        "--specpath", _parent_dir,
        "--name", _artifact_name,
    ] + _hidden_imports_args
    _exec_args.append("--add-data")
    _exec_args.append(f"{output_dir}{os.pathsep}.")
    if cfg.onefile:
        _exec_args.append("--onefile")
    else:
        _exec_args.append("--onedir")
    if not cfg.console:
        _exec_args.append("--noconsole")
    if cfg.icon:
        _exec_args.append(f"--icon={cfg.icon}")
    _exec_args.extend(cfg.extra_args)
    _exec_args.append(_entry_point)

    print(f"  Packing with PyInstaller...")
    try:
        r = subprocess.run(_exec_args, capture_output=True, text=True, timeout=300)
        if r.returncode != 0:
            print(f"  PyInstaller failed (rc={r.returncode})")
            for line in r.stderr.split("\n")[-10:]:
                if line.strip():
                    print(f"    {line.strip()}")
            return None
    except FileNotFoundError:
        print("  PyInstaller not found. Install with: pip install pyinstaller")
        return None
    except subprocess.TimeoutExpired:
        print("  PyInstaller timed out (300s)")
        return None

    if cfg.onefile:
        exe_path = os.path.join(_parent_dir, "dist", f"{_artifact_name}.exe")
    else:
        exe_path = os.path.join(_parent_dir, "dist", _artifact_name, f"{_artifact_name}.exe")

    if os.path.isfile(exe_path):
        size_mb = os.path.getsize(exe_path) / (1024 * 1024)
        print(f"  Packed: {exe_path} ({size_mb:.1f} MB)")
        return exe_path

    print(f"  Pack output not found: {exe_path}")
    return None
