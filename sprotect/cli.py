"""S-Protect-PY command-line interface.

Subcommands:
  build      Build encrypted project from project/ to output/
  encrypt    Encrypt individual files
  config     Manage configuration
  check      Check files
  version    Show version
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence

from sprotect import __version__
from sprotect.config import generate_default_config, load_config
from sprotect.core.encryptor import build_project, encrypt_files
from sprotect.core.backup import backup_project


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sprotect",
        description="S-Protect-PY: Python code protection toolkit.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("build", help="Build encrypted project (project/ -> output/)")
    p.add_argument("--project", default="./project", help="Source project directory (default: ./project)")
    p.add_argument("--output", default="./output", help="Output directory (default: ./output)")
    p.add_argument("-c", "--config", help="Path to sprotect.json5")

    p = sub.add_parser("encrypt", help="Encrypt individual files")
    p.add_argument("files", nargs="+", help=".py files to encrypt")
    p.add_argument("-c", "--config", help="Path to sprotect.json5")

    p = sub.add_parser("config", help="Manage configuration")
    ps = p.add_subparsers(dest="config_action", required=True)
    ps.add_parser("init", help="Generate default sprotect.json5")
    ps.add_parser("show", help="Show current configuration")

    p = sub.add_parser("check", help="Check .py files for syntax errors")
    p.add_argument("files", nargs="+", help="Files to check")

    sub.add_parser("version", help="Show version")

    return parser


def _cmd_build(args: argparse.Namespace) -> int:
    cfg = load_config(getattr(args, "config", None))
    project_dir = str(Path(args.project).resolve())
    output_dir = str(Path(args.output).resolve())

    if not Path(project_dir).is_dir():
        print(f"Error: project directory not found: {project_dir}", file=sys.stderr)
        return 1

    if cfg.encrypt.backup:
        backup_project(project_dir)

    build_project(project_dir, output_dir, cfg)

    print(f"Project '{cfg.project.name}' encrypted successfully.")
    print(f"  Source:  {project_dir}")
    print(f"  Output:  {output_dir}")
    print(f"  Entry:   {cfg.project.entry}")
    print(f"  Runtime: {Path(output_dir, '_runtime').resolve()}")
    print()
    print(f"To run:  python {cfg.project.entry}  (in the output directory)")
    return 0


def _cmd_encrypt(args: argparse.Namespace) -> int:
    cfg = load_config(getattr(args, "config", None))
    files = [str(Path(f).resolve()) for f in args.files]
    for f in files:
        if not Path(f).exists():
            print(f"Error: file not found: {f}", file=sys.stderr)
            return 1
    outputs = encrypt_files(files, cfg)
    for dst in outputs:
        print(f"  Encrypted: {dst}")
    return 0


def _cmd_config(args: argparse.Namespace) -> int:
    if args.config_action == "init":
        dest = generate_default_config("sprotect.json5")
        print(f"Default configuration generated: {dest.resolve()}")
        return 0
    if args.config_action == "show":
        cfg = load_config()
        import json5 as _j
        print(_j.dumps(cfg, indent=2, default=str))
        return 0
    print(f"Error: unknown config action: {args.config_action}", file=sys.stderr)
    return 1


def _cmd_check(args: argparse.Namespace) -> int:
    all_ok = True
    for f in args.files:
        p = Path(f)
        if not p.exists():
            print(f"  NOT FOUND: {f}")
            all_ok = False
            continue
        try:
            compile(p.read_text(encoding="utf-8"), str(p), "exec")
            print(f"  OK: {f}")
        except SyntaxError as e:
            print(f"  SYNTAX ERROR: {f} - {e}")
            all_ok = False
    return 0 if all_ok else 1


def _cmd_version() -> int:
    print(f"S-Protect-PY v{__version__}")
    return 0


build_parser = _build_parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    handlers = {
        "build": lambda a: _cmd_build(a),
        "encrypt": lambda a: _cmd_encrypt(a),
        "config": lambda a: _cmd_config(a),
        "check": lambda a: _cmd_check(a),
        "version": lambda a: _cmd_version(),
    }

    handler = handlers.get(args.command)
    if handler is None:
        parser.print_help()
        return 1

    try:
        return handler(args)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
