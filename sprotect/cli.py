"""S-Protect-PY command-line interface.

Provides subcommands for encrypting, running, configuring, and
inspecting protected Python projects.

Author: S-Protect Team
Version: 0.1.0
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence

from sprotect import __version__
from sprotect.config import generate_default_config, load_config
from sprotect.core.encryptor import encrypt_files, encrypt_project as do_encrypt_project
from sprotect.core.backup import backup_project
from sprotect.runtime.loader import run_encrypted_project


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sprotect",
        description="S-Protect-PY: Python code protection toolkit.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    enc_parser = subparsers.add_parser("encrypt", help="Encrypt one or more files")
    enc_parser.add_argument("files", nargs="+", help="File paths to encrypt")
    enc_parser.add_argument("-c", "--config", help="Path to config file")
    enc_parser.add_argument("--no-backup", action="store_true", help="Skip backup creation")

    ep_parser = subparsers.add_parser("encrypt-project", help="Encrypt an entire project directory")
    ep_parser.add_argument("dir", nargs="?", default=".", help="Project directory")
    ep_parser.add_argument("-c", "--config", help="Path to config file")

    run_parser = subparsers.add_parser("run", help="Run a protected project")
    run_parser.add_argument("dir", nargs="?", default=".", help="Project directory")
    run_parser.add_argument("args", nargs=argparse.REMAINDER, help="Arguments to pass to the project")

    config_parser = subparsers.add_parser("config", help="Manage configuration")
    config_sub = config_parser.add_subparsers(dest="config_action", required=True)
    config_sub.add_parser("init", help="Generate a default sprotect.json5")
    config_sub.add_parser("show", help="Show current configuration")

    check_parser = subparsers.add_parser("check", help="Check files for protection status")
    check_parser.add_argument("files", nargs="+", help="Files to check")

    subparsers.add_parser("version", help="Show version information")

    return parser


def _cmd_encrypt(args: argparse.Namespace) -> int:
    cfg = load_config(getattr(args, "config", None))

    files = [str(Path(f).resolve()) for f in args.files]
    for f in files:
        if not Path(f).exists():
            print(f"Error: file not found: {f}", file=sys.stderr)
            return 1

    if cfg.encrypt.backup and not getattr(args, "no_backup", False):
        backup_project(str(Path.cwd()))

    outputs = encrypt_files(files, cfg)
    for dst in outputs:
        src = dst.replace(".pye", ".py")
        print(f"  Encrypted: {src} -> {dst}")
    return 0


def _cmd_encrypt_project(args: argparse.Namespace) -> int:
    cfg = load_config(getattr(args, "config", None))
    proj_dir = str(Path(args.dir).resolve())
    if not Path(proj_dir).is_dir():
        print(f"Error: directory not found: {proj_dir}", file=sys.stderr)
        return 1

    entry = Path(proj_dir) / cfg.project.entry
    if not entry.exists():
        print(f"Warning: entry file not found: {entry}")

    if cfg.encrypt.backup:
        backup_project(proj_dir)

    do_encrypt_project(proj_dir, cfg)
    print(f"Project '{cfg.project.name}' encrypted successfully.")
    print(f"  Runtime files: {Path(proj_dir, '_runtime').resolve()}")
    print(f"  Entry: {cfg.project.entry}")
    return 0


def _cmd_run(args: argparse.Namespace) -> int:
    proj_dir = str(Path(args.dir).resolve())
    if not Path(proj_dir).is_dir():
        print(f"Error: directory not found: {proj_dir}", file=sys.stderr)
        return 1

    cfg = load_config()
    cfg.project.entry = cfg.project.entry or "main.py"
    try:
        run_encrypted_project(proj_dir, cfg)
    except Exception as e:
        print(f"Error running project: {e}", file=sys.stderr)
        return 1
    return 0


def _cmd_config(args: argparse.Namespace) -> int:
    if args.config_action == "init":
        dest = generate_default_config("sprotect.json5")
        print(f"Default configuration generated: {dest.resolve()}")
        return 0

    if args.config_action == "show":
        cfg = load_config()
        import json5 as _json5
        print(_json5.dumps(cfg, indent=2, default=str))
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

    command_map = {
        "encrypt": _cmd_encrypt,
        "encrypt-project": _cmd_encrypt_project,
        "run": _cmd_run,
        "config": _cmd_config,
        "check": _cmd_check,
        "version": lambda a: _cmd_version(),
    }

    handler = command_map.get(args.command)
    if handler is None:
        parser.print_help()
        return 1

    try:
        return handler(args)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
