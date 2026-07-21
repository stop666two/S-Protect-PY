"""Pack encrypted output into single executable via PyInstaller."""

from __future__ import annotations
import os, sys, subprocess, shutil
from sprotect.types import PackConfig


def pack(output_dir: str, cfg: PackConfig) -> str | None:
    """Run PyInstaller on output_dir to produce a single exe.

    Returns path to the generated executable, or None on failure.
    """
    if not shutil.which("pyinstaller"):
        print("  PyInstaller not found. Install with: pip install pyinstaller")
        return None

    output_dir = os.path.abspath(output_dir)
    parent = os.path.dirname(output_dir)
    out_name = os.path.basename(output_dir)

    entry = os.path.join(output_dir, "main.py")
    if not os.path.isfile(entry):
        print(f"  Entry not found: {entry}")
        return None

    args = [
        sys.executable, "-m", "PyInstaller",
        "--distpath", os.path.join(parent, "dist"),
        "--workpath", os.path.join(parent, "build"),
        "--specpath", parent,
        "--name", out_name,
        "--add-data", f"{output_dir}{os.pathsep}{out_name}",
    ]
    if cfg.onefile:
        args.append("--onefile")
    else:
        args.append("--onedir")
    if not cfg.console:
        args.append("--noconsole")
    if cfg.icon:
        args.append(f"--icon={cfg.icon}")
    args.extend(cfg.extra_args)
    args.append(entry)

    print(f"  Packing with PyInstaller...")
    try:
        r = subprocess.run(args, capture_output=True, text=True, timeout=300)
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
        exe_path = os.path.join(parent, "dist", f"{out_name}.exe")
    else:
        exe_path = os.path.join(parent, "dist", out_name, f"{out_name}.exe")

    if os.path.isfile(exe_path):
        size_mb = os.path.getsize(exe_path) / (1024 * 1024)
        print(f"  Packed: {exe_path} ({size_mb:.1f} MB)")
        return exe_path

    print(f"  Pack output not found: {exe_path}")
    return None
