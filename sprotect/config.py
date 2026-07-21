"""S-Protect-PY configuration loader.

JSON5-based configuration loading, validation, and default generation.
Supports all configuration types defined in sprotect.types.

Author: S-Protect Team
Version: 0.1.0
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Optional

import json5

from sprotect.types import (
    AntiDebugAction,
    AntiDebugConfig,
    Config,
    EncryptConfig,
    EnvironmentConfig,
    ExpirationConfig,
    InterdependencyMode,
    NamingStyle,
    ObfuscateConfig,
    ObfuscateLevel,
    OutputConfig,
    ProjectConfig,
    RenameRules,
    SandboxConfig,
    VirtualizationConfig,
    VirtualizationMode,
    WatermarkConfig,
    WatermarkLevel,
)


def _try_parse_enum(enum_type: type, value: Any) -> Any:
    """Try to parse a string or int into an enum member."""
    if isinstance(value, enum_type):
        return value
    if isinstance(value, str):
        try:
            return enum_type[value.upper()]
        except KeyError:
            try:
                return enum_type(value)
            except ValueError:
                raise ValueError(f"Invalid value {value!r} for {enum_type.__name__}")
    if isinstance(value, int):
        try:
            return enum_type(value)
        except ValueError:
            raise ValueError(f"Invalid integer {value} for {enum_type.__name__}")
    raise TypeError(f"Cannot convert {type(value).__name__} to {enum_type.__name__}")


def _dict_to_rename_rules(data: dict[str, Any]) -> RenameRules:
    """Convert a dict to RenameRules."""
    style = data.get("style", "hex")
    if isinstance(style, str):
        style = _try_parse_enum(NamingStyle, style)
    reserved = data.get("reserved", ["__init__", "main"])
    dictionary = data.get("dictionary", None)
    return RenameRules(style=style, reserved=reserved, dictionary=dictionary)


def _dict_to_obfuscate_config(data: dict[str, Any]) -> ObfuscateConfig:
    """Convert a dict to ObfuscateConfig."""
    level = data.get("level", 3)
    if not isinstance(level, ObfuscateLevel):
        level = _try_parse_enum(ObfuscateLevel, level)
    rename_rules = data.get("rename_rules", {})
    if isinstance(rename_rules, dict):
        rename_rules = _dict_to_rename_rules(rename_rules)
    return ObfuscateConfig(
        level=level,
        rename_variables=data.get("rename_variables", True),
        rename_functions=data.get("rename_functions", True),
        rename_classes=data.get("rename_classes", True),
        rename_rules=rename_rules,
        encrypt_strings=data.get("encrypt_strings", True),
        encrypt_numbers=data.get("encrypt_numbers", False),
        control_flow_flattening=data.get("control_flow_flattening", True),
        dead_code_injection=data.get("dead_code_injection", False),
    )


def _dict_to_encrypt_config(data: dict[str, Any]) -> EncryptConfig:
    """Convert a dict to EncryptConfig."""
    interdependency = data.get("interdependency", "chain")
    if not isinstance(interdependency, InterdependencyMode):
        interdependency = _try_parse_enum(InterdependencyMode, interdependency)
    return EncryptConfig(
        algorithm=data.get("algorithm", "aes-256-gcm"),
        key_source=data.get("key_source", "auto"),
        interdependency=interdependency,
        backup=data.get("backup", True),
        replace_originals=data.get("replace_originals", False),
        shard_count=data.get("shard_count", 3),
    )


def _dict_to_anti_debug_config(data: dict[str, Any]) -> AntiDebugConfig:
    """Convert a dict to AntiDebugConfig."""
    action = data.get("action", "exit")
    if not isinstance(action, AntiDebugAction):
        action = _try_parse_enum(AntiDebugAction, action)
    return AntiDebugConfig(
        enabled=data.get("enabled", True),
        action=action,
        checks=data.get("checks", ["ptrace", "debugger", "breakpoint", "timing"]),
    )


def _dict_to_virtualization_config(data: dict[str, Any]) -> VirtualizationConfig:
    """Convert a dict to VirtualizationConfig."""
    mode = data.get("mode", "partial")
    if not isinstance(mode, VirtualizationMode):
        mode = _try_parse_enum(VirtualizationMode, mode)
    return VirtualizationConfig(
        enabled=data.get("enabled", False),
        mode=mode,
        functions=data.get("functions", []),
        glob_patterns=data.get("glob_patterns", []),
    )


def _dict_to_watermark_config(data: dict[str, Any]) -> WatermarkConfig:
    """Convert a dict to WatermarkConfig."""
    levels = data.get("levels", ["file", "code"])
    parsed_levels: list[WatermarkLevel] = []
    for lv in levels:
        if not isinstance(lv, WatermarkLevel):
            lv = _try_parse_enum(WatermarkLevel, lv)
        parsed_levels.append(lv)
    return WatermarkConfig(
        enabled=data.get("enabled", True),
        levels=parsed_levels,
        batch_id=data.get("batch_id", ""),
    )


def _dict_to_expiration_config(data: dict[str, Any]) -> ExpirationConfig:
    """Convert a dict to ExpirationConfig."""
    return ExpirationConfig(
        enabled=data.get("enabled", False),
        expires_at=data.get("expires_at", None),
        ntp_check=data.get("ntp_check", True),
        on_network_fail=data.get("on_network_fail", "reject"),
    )


def _dict_to_environment_config(data: dict[str, Any]) -> EnvironmentConfig:
    """Convert a dict to EnvironmentConfig."""
    return EnvironmentConfig(
        enabled=data.get("enabled", False),
        bind_directory=data.get("bind_directory", None),
        bind_username=data.get("bind_username", None),
        bind_env_vars=data.get("bind_env_vars", []),
    )


def _dict_to_sandbox_config(data: dict[str, Any]) -> SandboxConfig:
    """Convert a dict to SandboxConfig."""
    return SandboxConfig(
        enabled=data.get("enabled", True),
    )


def _dict_to_project_config(data: dict[str, Any]) -> ProjectConfig:
    """Convert a dict to ProjectConfig."""
    return ProjectConfig(
        name=data.get("name", "unnamed"),
        version=data.get("version", "1.0.0"),
        entry=data.get("entry", "main.py"),
    )


def _dict_to_output_config(data: dict[str, Any]) -> OutputConfig:
    """Convert a dict to OutputConfig."""
    return OutputConfig(
        dir=data.get("dir", "./dist"),
        keep_source_map=data.get("keep_source_map", False),
    )


def _dict_to_config(data: dict[str, Any]) -> Config:
    """Convert a nested dict to a Config object."""
    return Config(
        obfuscate=_dict_to_obfuscate_config(data.get("obfuscate", {})),
        encrypt=_dict_to_encrypt_config(data.get("encrypt", {})),
        anti_debug=_dict_to_anti_debug_config(data.get("anti_debug", {})),
        virtualization=_dict_to_virtualization_config(data.get("virtualization", {})),
        watermark=_dict_to_watermark_config(data.get("watermark", {})),
        expiration=_dict_to_expiration_config(data.get("expiration", {})),
        environment=_dict_to_environment_config(data.get("environment", {})),
        sandbox=_dict_to_sandbox_config(data.get("sandbox", {})),
        project=_dict_to_project_config(data.get("project", {})),
        output=_dict_to_output_config(data.get("output", {})),
    )


def _find_config(path: Optional[str] = None) -> Optional[Path]:
    """Search for a sprotect.json5 configuration file."""
    if path is not None:
        p = Path(path)
        if p.exists():
            return p
        return None

    candidates = [
        Path.cwd() / "sprotect.json5",
        Path.cwd() / "sprotect.json",
        Path.cwd() / ".sprotect.json5",
        Path.cwd() / ".sprotect.json",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate

    home = Path.home()
    home_candidates = [
        home / ".sprotect" / "sprotect.json5",
        home / ".sprotect" / "sprotect.json",
    ]
    for candidate in home_candidates:
        if candidate.exists():
            return candidate

    return None


def load_config(path: Optional[str] = None) -> Config:
    """Load configuration from a JSON5 file.

    Searches for sprotect.json5 in the current directory, user home,
    or the path specified by the caller. Returns a default Config
    if no configuration file is found.

    Args:
        path: Optional explicit path to a JSON5 config file.

    Returns:
        A populated Config object.
    """
    config_path = _find_config(path)
    if config_path is None:
        return Config()

    raw = config_path.read_text(encoding="utf-8")
    data: dict[str, Any] = json5.loads(raw)
    return _dict_to_config(data)


def generate_default_config(path: str) -> Path:
    """Generate a default sprotect.json5 configuration file.

    Args:
        path: Destination file path.

    Returns:
        Path to the generated file.
    """
    default = {
        "obfuscate": {
            "level": 3,
            "rename_variables": True,
            "rename_functions": True,
            "rename_classes": True,
            "rename_rules": {
                "style": "hex",
                "reserved": ["__init__", "main"],
            },
            "encrypt_strings": True,
            "encrypt_numbers": False,
            "control_flow_flattening": True,
            "dead_code_injection": False,
        },
        "encrypt": {
            "algorithm": "aes-256-gcm",
            "key_source": "auto",
            "interdependency": "chain",
            "backup": True,
            "replace_originals": False,
            "shard_count": 3,
        },
        "anti_debug": {
            "enabled": True,
            "action": "exit",
            "checks": ["ptrace", "debugger", "breakpoint", "timing"],
        },
        "virtualization": {
            "enabled": False,
            "mode": "partial",
            "functions": [],
            "glob_patterns": [],
        },
        "watermark": {
            "enabled": True,
            "levels": ["file", "code"],
            "batch_id": "",
        },
        "expiration": {
            "enabled": False,
            "expires_at": None,
            "ntp_check": True,
            "on_network_fail": "reject",
        },
        "environment": {
            "enabled": False,
            "bind_directory": None,
            "bind_username": None,
            "bind_env_vars": [],
        },
        "sandbox": {
            "enabled": True,
        },
        "project": {
            "name": "unnamed",
            "version": "1.0.0",
            "entry": "main.py",
        },
        "output": {
            "dir": "./dist",
            "keep_source_map": False,
        },
    }

    dest = Path(path)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(default, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return dest
