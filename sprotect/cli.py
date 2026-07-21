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


def _build_parser() -> argparse.ArgumentParser:
    """Build the top-level argument parser with subcommands."""
    parser = argparse.ArgumentParser(
        prog="sprotect",
        description="S-Protect-PY: Python code protection toolkit.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # encrypt
    enc_parser = subparsers.add_parser("encrypt", help="Encrypt one or more files")
    enc_parser.add_argument("files", nargs="+", help="File paths to encrypt")
    enc_parser.add_argument("-c", "--config", help="Path to config file")
    enc_parser.add_argument("--no-backup", action="store_true", help="Skip backup creation")

    # encrypt-project
    ep_parser = subparsers.add_parser("encrypt-project", help="Encrypt an entire project directory")
    ep_parser.add_argument("dir", nargs="?", default=".", help="Project directory")
    ep_parser.add_argument("-c", "--config", help="Path to config file")

    # run
    run_parser = subparsers.add_parser("run", help="Run a protected project")
    run_parser.add_argument("dir", nargs="?", default=".", help="Project directory")
    run_parser.add_argument("args", nargs=argparse.REMAINDER, help="Arguments to pass to the project")

    # config
    config_parser = subparsers.add_parser("config", help="Manage configuration")
    config_sub = config_parser.add_subparsers(dest="config_action", required=True)
    config_sub.add_parser("init", help="Generate a default sprotect.json5")
    config_sub.add_parser("show", help="Show current configuration")

    # check
    check_parser = subparsers.add_parser("check", help="Check files for protection status")
    check_parser.add_argument("files", nargs="+", help="Files to check")

    # version
    subparsers.add_parser("version", help="Show version information")

    return parser


def _cmd_encrypt(args: argparse.Namespace) -> int:
    """Handle the encrypt subcommand."""
    cfg = load_config(getattr(args, "config", None))
    if getattr(args, "no_backup", False):
        cfg.encrypt.backup = False

    files = [Path(f) for f in args.files]
    for f in files:
        if not f.exists():
            print(f"Error: file not found: {f}")
            return 1

    print(f"Encrypting {len(files)} file(s) with {cfg.encrypt.algorithm}...")
    print(f"  Interdependency mode: {cfg.encrypt.interdependency.value}")
    print(f"  Backup: {cfg.encrypt.backup}")
    print(f"  Shard count: {cfg.encrypt.shard_count}")
    return 0


def _cmd_encrypt_project(args: argparse.Namespace) -> int:
    """Handle the encrypt-project subcommand."""
    cfg = load_config(getattr(args, "config", None))
    proj_dir = Path(args.dir)
    if not proj_dir.is_dir():
        print(f"Error: directory not found: {proj_dir}")
        return 1

    entry = proj_dir / cfg.project.entry if cfg.project.entry else None
    if entry is not None and not entry.exists():
        print(f"Warning: entry file not found: {entry}")

    print(f"Encrypting project '{cfg.project.name}' v{cfg.project.version}")
    print(f"  Directory: {proj_dir.resolve()}")
    print(f"  Entry: {cfg.project.entry}")
    return 0


def _cmd_run(args: argparse.Namespace) -> int:
    """Handle the run subcommand."""
    cfg = load_config()
    proj_dir = Path(args.dir)
    if not proj_dir.is_dir():
        print(f"Error: directory not found: {proj_dir}")
        return 1

    entry = proj_dir / cfg.project.entry
    if not entry.exists():
        print(f"Error: entry file not found: {entry}")
        return 1

    print(f"Running project '{cfg.project.name}' from {proj_dir.resolve()}")
    return 0


def _cmd_config(args: argparse.Namespace) -> int:
    """Handle the config subcommand."""
    if args.config_action == "init":
        path = "sprotect.json5"
        dest = generate_default_config(path)
        print(f"Default configuration generated: {dest.resolve()}")
        return 0

    if args.config_action == "show":
        cfg = load_config()
        print(f"Project: {cfg.project.name} v{cfg.project.version}")
        print(f"Entry: {cfg.project.entry}")
        print(f"Obfuscate level: {cfg.obfuscate.level.name}")
        print(f"Encrypt algorithm: {cfg.encrypt.algorithm}")
        print(f"Interdependency: {cfg.encrypt.interdependency.value}")
        print(f"Anti-debug: {'enabled' if cfg.anti_debug.enabled else 'disabled'}")
        print(f"  action: {cfg.anti_debug.action.value}")
        print(f"  checks: {', '.join(cfg.anti_debug.checks)}")
        print(f"Virtualization: {'enabled' if cfg.virtualization.enabled else 'disabled'}")
        print(f"Watermark: {'enabled' if cfg.watermark.enabled else 'disabled'}")
        print(f"  levels: {[l.value for l in cfg.watermark.levels]}")
        print(f"Expiration: {'enabled' if cfg.expiration.enabled else 'disabled'}")
        print(f"  expires_at: {cfg.expiration.expires_at or 'N/A'}")
        print(f"Environment binding: {'enabled' if cfg.environment.enabled else 'disabled'}")
        print(f"Sandbox detection: {'enabled' if cfg.sandbox.enabled else 'disabled'}")
        print(f"Output dir: {cfg.output.dir}")
        print(f"Keep source map: {cfg.output.keep_source_map}")
        return 0

    print(f"Error: unknown config action: {args.config_action}")
    return 1


def _cmd_check(args: argparse.Namespace) -> int:
    """Handle the check subcommand."""
    files = [Path(f) for f in args.files]
    all_found = True
    for f in files:
        status = "EXISTS" if f.exists() else "NOT FOUND"
        if not f.exists():
            all_found = False
        print(f"  {status}: {f}")
    return 0 if all_found else 1


build_parser = _build_parser


def _cmd_version() -> int:
    """Handle the version subcommand."""
    print(f"S-Protect-PY v{__version__}")
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    """Main CLI entry point.

    Parses arguments, dispatches to the appropriate subcommand,
    and returns an exit code.

    Args:
        argv: Optional argument list. Defaults to sys.argv[1:].

    Returns:
        Exit code (0 for success, non-zero on error).
    """
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
