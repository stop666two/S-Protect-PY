"""S-Protect-PY type definitions."""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class ObfuscateLevel(Enum):
    L1 = 1; L2 = 2; L3 = 3; L4 = 4; L5 = 5

class InterdependencyMode(Enum):
    CHAIN = "chain"; FULL_MESH = "full-mesh"; HYBRID = "hybrid"

class NamingStyle(Enum):
    HEX = "hex"; CHINESE = "chinese"; INVISIBLE = "invisible"
    MATH_SYMBOLS = "math-symbols"; CUSTOM = "custom"

class AntiDebugAction(Enum):
    EXIT = "exit"; CORRUPT = "corrupt"; WARN = "warn"

class VirtualizationMode(Enum):
    PARTIAL = "partial"; FULL = "full"

class WatermarkLevel(Enum):
    FILE = "file"; CODE = "code"; RUNTIME = "runtime"


@dataclass
class RenameRules:
    style: NamingStyle = NamingStyle.HEX
    reserved: list[str] = field(default_factory=lambda: ["__init__", "main"])
    dictionary: Optional[dict] = None

@dataclass
class ObfuscateConfig:
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
    algorithm: str = "aes-256-gcm"
    key_source: str = "auto"
    interdependency: InterdependencyMode = InterdependencyMode.CHAIN
    backup: bool = True
    replace_originals: bool = False
    shard_count: int = 3

@dataclass
class AntiDebugConfig:
    enabled: bool = True
    action: AntiDebugAction = AntiDebugAction.EXIT
    checks: list[str] = field(default_factory=lambda: ["pdb", "ptrace", "debugger", "vm"])

@dataclass
class VirtualizationConfig:
    enabled: bool = False
    mode: VirtualizationMode = VirtualizationMode.PARTIAL
    functions: list[str] = field(default_factory=list)
    glob_patterns: list[str] = field(default_factory=list)

@dataclass
class WatermarkConfig:
    enabled: bool = True
    levels: list[WatermarkLevel] = field(default_factory=lambda: [WatermarkLevel.FILE, WatermarkLevel.CODE])
    batch_id: str = ""

@dataclass
class ExpirationConfig:
    enabled: bool = False
    expires_at: Optional[str] = None
    ntp_check: bool = True
    on_network_fail: str = "reject"

@dataclass
class EnvironmentConfig:
    enabled: bool = False
    bind_directory: Optional[str] = None
    bind_username: Optional[str] = None
    bind_env_vars: list[str] = field(default_factory=list)

@dataclass
class SandboxConfig:
    enabled: bool = True

@dataclass
class FilesConfig:
    include: list[str] = field(default_factory=lambda: ["**/*.py"])
    exclude: list[str] = field(default_factory=lambda: [])

@dataclass
class ProjectConfig:
    name: str = "unnamed"
    version: str = "1.0.0"
    entry: str = "main.py"

@dataclass
class OutputConfig:
    dir: str = "./dist"
    keep_source_map: bool = False

@dataclass
class Config:
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
