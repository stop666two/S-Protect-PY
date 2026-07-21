"""Tests for CLI argument parsing."""
from __future__ import annotations

from sprotect.cli import build_parser


def test_version_command() -> None:
    """Parse the version subcommand."""
    parser = build_parser()
    args = parser.parse_args(["version"])
    assert args.command == "version"


def test_encrypt_command() -> None:
    """Parse the encrypt subcommand with file arguments."""
    parser = build_parser()
    args = parser.parse_args(["encrypt", "file1.py", "file2.py"])
    assert args.command == "encrypt"
    assert args.files == ["file1.py", "file2.py"]


def test_encrypt_project_command() -> None:
    """Parse the encrypt-project subcommand with a directory."""
    parser = build_parser()
    args = parser.parse_args(["encrypt-project", "./src"])
    assert args.command == "encrypt-project"
    assert args.dir == "./src"


def test_config_init_command() -> None:
    """Parse the config init subcommand."""
    parser = build_parser()
    args = parser.parse_args(["config", "init"])
    assert args.command == "config"
    assert args.config_action == "init"


def test_config_show_command() -> None:
    """Parse the config show subcommand."""
    parser = build_parser()
    args = parser.parse_args(["config", "show"])
    assert args.command == "config"
    assert args.config_action == "show"


def test_check_command() -> None:
    """Parse the check subcommand with a file argument."""
    parser = build_parser()
    args = parser.parse_args(["check", "target.py"])
    assert args.command == "check"
    assert args.files == ["target.py"]


def test_run_command() -> None:
    """Parse the run subcommand with a directory."""
    parser = build_parser()
    args = parser.parse_args(["run", "."])
    assert args.command == "run"
    assert args.dir == "."


def test_encrypt_multiple_files() -> None:
    """Parse the encrypt subcommand with multiple files."""
    parser = build_parser()
    args = parser.parse_args(["encrypt", "a.py", "b.py", "c.py"])
    assert args.files == ["a.py", "b.py", "c.py"]
