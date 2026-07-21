"""S-Protect-PY type definitions.

Defines the global type system including enums, dataclasses, and
configuration models used across all protection layers.

Author: S-Protect Team
Version: 0.1.0
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class ObfuscateLevel(Enum):
    """Obfuscation intensity levels."""
    L1 = 1
    L2 = 2
    L3 = 3
    L4 = 4
    L5 = 5


class InterdependencyMode(Enum):
    """Multi-file interdependency topology."""
    CHAIN = "chain"
    FULL_MESH = "full-mesh"
    HYBRID = "hybrid"


class NamingStyle(Enum):
    """Obfuscated identifier naming style."""
    HEX = "hex"
    CHINESE = "chinese"
    INVISIBLE = "invisible"
    MATH_SYMBOLS = "math-symbols"
    CUSTOM = "custom"


class AntiDebugAction(Enum):
    """Action taken when a debugger is detected."""
    EXIT = "exit"
    CORRUPT = "corrupt"
    WARN = "warn"


class VirtualizationMode(Enum):
    """Virtualization coverage mode."""
    PARTIAL = "partial"
    FULL = "full"


class WatermarkLevel(Enum):
    """Watermark embedding level."""
    FILE = "file"
    CODE = "code"
    RUNTIME = "runtime"


@dataclass
class RenameRules:
    """Naming rules for identifier obfuscation."""
    style: NamingStyle = NamingStyle.HEX
    reserved: list[str] = field(default_factory=lambda: ["__init__", "main"])
    dictionary: Optional[dict] = None


@dataclass
class ObfuscateConfig:
    """Configuration for code obfuscation."""
    level: ObfuscateLevel = ObfuscateLevel.L3
    rename_variables: bool = True
    rename_functions: bool = True
    rename_classes: bool = True
    rename_rules: RenameRules = field(default_factory=RenameRules)
    encrypt_strings: bool = True
    encrypt_numbers: bool = False
    control_flow_flattening: bool = True
    dead_code_injection: bool = False


@dataclass
class EncryptConfig:
    """Configuration for file encryption."""
    algorithm: str = "aes-256-gcm"
    key_source: str = "auto"
    interdependency: InterdependencyMode = InterdependencyMode.CHAIN
    backup: bool = True
    replace_originals: bool = False
    shard_count: int = 3


@dataclass
class AntiDebugConfig:
    """Configuration for anti-debugging measures."""
    enabled: bool = True
    action: AntiDebugAction = AntiDebugAction.EXIT
    checks: list[str] = field(default_factory=lambda: [
        "ptrace", "debugger", "breakpoint", "timing"
    ])


@dataclass
class VirtualizationConfig:
    """Configuration for bytecode virtualization."""
    enabled: bool = False
    mode: VirtualizationMode = VirtualizationMode.PARTIAL
    functions: list[str] = field(default_factory=list)
    glob_patterns: list[str] = field(default_factory=list)


@dataclass
class WatermarkConfig:
    """Configuration for digital watermarking."""
    enabled: bool = True
    levels: list[WatermarkLevel] = field(default_factory=lambda: [
        WatermarkLevel.FILE, WatermarkLevel.CODE
    ])
    batch_id: str = ""


@dataclass
class ExpirationConfig:
    """Configuration for time-based expiration."""
    enabled: bool = False
    expires_at: Optional[str] = None
    ntp_check: bool = True
    on_network_fail: str = "reject"


@dataclass
class EnvironmentConfig:
    """Configuration for environment binding."""
    enabled: bool = False
    bind_directory: Optional[str] = None
    bind_username: Optional[str] = None
    bind_env_vars: list[str] = field(default_factory=list)


@dataclass
class SandboxConfig:
    """Configuration for sandbox detection."""
    enabled: bool = True


@dataclass
class ProjectConfig:
    """Project metadata."""
    name: str = "unnamed"
    version: str = "1.0.0"
    entry: str = "main.py"


@dataclass
class FilesConfig:
    """File inclusion/exclusion patterns for project scanning."""
    include: list[str] = field(default_factory=lambda: ["**/*.py"])
    exclude: list[str] = field(default_factory=lambda: [
        "**/__pycache__/**", "**/.git/**", "**/_runtime/**",
        "**/_backup/**", "**/_test_temp/**",
    ])


@dataclass
class OutputConfig:
    """Output directory and artifact settings."""
    dir: str = "./dist"
    keep_source_map: bool = False


@dataclass
class Config:
    """Top-level configuration aggregating all sub-configs."""
    files: FilesConfig = field(default_factory=FilesConfig)
    obfuscate: ObfuscateConfig = field(default_factory=ObfuscateConfig)
    encrypt: EncryptConfig = field(default_factory=EncryptConfig)
    anti_debug: AntiDebugConfig = field(default_factory=AntiDebugConfig)
    virtualization: VirtualizationConfig = field(default_factory=VirtualizationConfig)
    watermark: WatermarkConfig = field(default_factory=WatermarkConfig)
    expiration: ExpirationConfig = field(default_factory=ExpirationConfig)
    environment: EnvironmentConfig = field(default_factory=EnvironmentConfig)
    sandbox: SandboxConfig = field(default_factory=SandboxConfig)
    project: ProjectConfig = field(default_factory=ProjectConfig)
    output: OutputConfig = field(default_factory=OutputConfig)
