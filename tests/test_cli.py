"""Tests for CLI argument parsing."""
from __future__ import annotations
from sprotect.cli import build_parser


def test_version_command():
    parser = build_parser()
    args = parser.parse_args(["version"])
    assert args.command == "version"


def test_build_command():
    parser = build_parser()
    args = parser.parse_args(["build", "--project", "./src", "--output", "./dist"])
    assert args.command == "build"
    assert args.project == "./src"
    assert args.output == "./dist"


def test_build_command_defaults():
    parser = build_parser()
    args = parser.parse_args(["build"])
    assert args.command == "build"
    assert args.project == "./project"
    assert args.output == "./output"


def test_encrypt_command():
    parser = build_parser()
    args = parser.parse_args(["encrypt", "file1.py", "file2.py"])
    assert args.command == "encrypt"
    assert args.files == ["file1.py", "file2.py"]


def test_config_init_command():
    parser = build_parser()
    args = parser.parse_args(["config", "init"])
    assert args.command == "config"
    assert args.config_action == "init"


def test_config_show_command():
    parser = build_parser()
    args = parser.parse_args(["config", "show"])
    assert args.command == "config"
    assert args.config_action == "show"


def test_check_command():
    parser = build_parser()
    args = parser.parse_args(["check", "target.py"])
    assert args.command == "check"
    assert args.files == ["target.py"]


def test_encrypt_multiple_files():
    parser = build_parser()
    args = parser.parse_args(["encrypt", "a.py", "b.py", "c.py"])
    assert args.files == ["a.py", "b.py", "c.py"]
