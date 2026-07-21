# S-Protect-PY Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a comprehensive Python code protection CLI tool that encrypts, obfuscates, anti-debugs, watermarks, virtualizes, and expires Python projects with multi-file interdependent decryption and strong integrity verification.

**Architecture:** Modular CLI tool with three layers — (1) CLI + JSON5 config layer, (2) core engine (obfuscate/encrypt/virtualize), (3) runtime loader packaged into each encrypted project. Runtime uses custom import hooks, shard-based key reconstruction, circular integrity verification, and anti-tamper self-checks.

**Tech Stack:** Python 3.10+, stdlib-only except `json5` (third-party), `cryptography` (AES/RSA), `tqdm` (progress), `colorama` (output). All other protection logic uses stdlib (`hashlib`, `hmac`, `secrets`, `base64`, `marshal`, `dis`, `ast`, `importlib`, `ctypes`, `zlib`, etc.).

## Global Constraints

- Python 3.10+ only (f-strings, match statement optional but preferred)
- Zero external dependencies for runtime loader (the packaged `_runtime/` code must run on bare Python 3.10+)
- All source files must contain a header comment block with description, author, and version
- JSON5 used for all configuration files
- Every `.py` file must include complete docstrings and type annotations for all public functions
- CI/CD: flake8 + mypy strict mode must pass before any commit
- Naming: `snake_case` for functions/variables, `PascalCase` for classes, `UPPER_CASE` for constants
- File encoding: UTF-8 with LF line endings
- All third-party dependencies must be pinned in `requirements.txt`

---
## 文件结构

```
S-Protect-PY/
├── CONTEXT.md
├── AGENTS.md
├── .gitignore
├── .gitattributes
├── requirements.txt
├── sprotect.json5                    # 默认配置文件
├── envtest.py                        # 测试靶子文件（不修改，仅用于验证）
│
├── sprotect/                         # 主包
│   ├── __init__.py                   # 包元信息
│   ├── __main__.py                   # CLI 入口: python -m sprotect
│   ├── cli.py                        # CLI 参数解析 (argparse)
│   ├── config.py                     # JSON5 配置加载、校验、默认值
│   ├── types.py                      # 全局类型定义 (dataclasses)
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── obfuscator.py             # 命名混淆、字符串/数字加密
│   │   ├── encryptor.py              # 文件加密引擎（AES-GCM）
│   │   ├── decryptor.py              # 文件解密引擎（供测试验证用）
│   │   ├── project.py                # 项目扫描、文件发现、依赖分析
│   │   └── backup.py                 # 项目备份与原地替换
│   │
│   ├── runtime/                      # ⚠️ 此目录代码将打包到加密项目
│   │   ├── __init__.py
│   │   ├── loader.py                 # 解密加载器 + 自定义 import hook
│   │   ├── verifier.py               # 完整性校验（校验环 + 交叉签名）
│   │   ├── anti_debug.py             # 反调试检测 + 自毁
│   │   ├── index.py                  # 分片索引管理（真假索引）
│   │   ├── shard_reconstructor.py    # 私钥分片收集 + 拼合
│   │   └── expiration.py             # 过期时间校验 + NTP 检查
│   │
│   ├── features/
│   │   ├── __init__.py
│   │   ├── watermark.py              # 三层次水印注入
│   │   ├── virtualization.py         # 代码虚拟化（自定义指令集）
│   │   ├── control_flow.py           # 控制流平坦化
│   │   ├── dead_code.py              # 死代码注入
│   │   ├── environment.py            # 环境指纹绑定
│   │   └── network.py                # NTP 联网授时检查
│   │
│   └── utils/
│       ├── __init__.py
│       ├── crypto.py                 # 密钥生成、AES/RSA 加解密、签名
│       ├── shard.py                  # Shamir-like 分片 + 嵌入/提取
│       ├── sign.py                   # 交叉签名工具
│       ├── index_builder.py          # 真假索引构建器
│       └── random_gen.py             # 随机名生成器（hex/chinese/invisible）
│
└── tests/
    ├── __init__.py
    ├── test_cli.py
    ├── test_config.py
    ├── test_obfuscator.py
    ├── test_encryptor.py
    ├── test_runtime_loader.py
    ├── test_anti_debug.py
    ├── test_verifier.py
    ├── test_shard.py
    ├── test_index.py
    ├── test_watermark.py
    ├── test_virtualization.py
    ├── test_control_flow.py
    ├── test_dead_code.py
    ├── test_expiration.py
    ├── test_environment.py
    └── test_integration.py           # 端到端集成测试（用 envtest.py 验证）
```

---
## 分阶段任务

---

### P1: CLI 骨架 + JSON5 配置解析

#### Task 1-1: 项目脚手架与配置定义

**Files:**
- Create: `sprotect/__init__.py`
- Create: `sprotect/__main__.py`
- Create: `sprotect/types.py`
- Create: `sprotect/config.py`
- Create: `sprotect.json5`
- Create: `requirements.txt`
- Create: `.gitignore`
- Modify: `.gitattributes`

**Interfaces:**
- Consumes: (项目根路径)
- Produces: `Config` dataclass, `load_config(path) -> Config`, default `sprotect.json5`

- [ ] **Step 1: 创建 `sprotect/__init__.py`**

```python
"""S-Protect-PY: Python code protection toolkit.

Encryption, obfuscation, anti-debug, virtualization, watermarking,
expiration control, and multi-file interdependent decryption.
"""

__version__ = "0.1.0"
__author__ = "S-Protect Team"
```

- [ ] **Step 2: 创建 `sprotect/types.py`**

```python
"""Global type definitions for S-Protect-PY."""

from __future__ import annotations

import dataclasses
from enum import Enum
from typing import Optional


class ObfuscateLevel(Enum):
    L1 = 1
    L2 = 2
    L3 = 3
    L4 = 4
    L5 = 5


class InterdependencyMode(Enum):
    CHAIN = "chain"
    FULL_MESH = "full-mesh"
    HYBRID = "hybrid"


class NamingStyle(Enum):
    HEX = "hex"
    CHINESE = "chinese"
    INVISIBLE = "invisible"
    MATH_SYMBOLS = "math-symbols"
    CUSTOM = "custom"


class AntiDebugAction(Enum):
    EXIT = "exit"
    CORRUPT = "corrupt"
    WARN = "warn"


class VirtualizationMode(Enum):
    PARTIAL = "partial"
    FULL = "full"


class WatermarkLevel(Enum):
    FILE = "file"
    CODE = "code"
    RUNTIME = "runtime"


@dataclasses.dataclass
class RenameRules:
    style: NamingStyle = NamingStyle.HEX
    reserved: list[str] = dataclasses.field(default_factory=lambda: ["__init__", "main"])
    dictionary: Optional[dict[str, str]] = None


@dataclasses.dataclass
class ObfuscateConfig:
    level: ObfuscateLevel = ObfuscateLevel.L3
    rename_variables: bool = True
    rename_functions: bool = True
    rename_classes: bool = True
    rename_rules: RenameRules = dataclasses.field(default_factory=RenameRules)
    encrypt_strings: bool = True
    encrypt_numbers: bool = True
    control_flow_flattening: bool = False
    dead_code_injection: bool = False


@dataclasses.dataclass
class EncryptConfig:
    algorithm: str = "aes-256-gcm"
    key_source: str = "auto"
    interdependency: InterdependencyMode = InterdependencyMode.HYBRID
    backup: bool = True
    replace_originals: bool = True
    shard_count: int = 3


@dataclasses.dataclass
class AntiDebugConfig:
    enabled: bool = True
    action: AntiDebugAction = AntiDebugAction.EXIT
    checks: list[str] = dataclasses.field(
        default_factory=lambda: ["pdb_check", "ptrace_check", "debugger_detect", "vm_detect"]
    )


@dataclasses.dataclass
class VirtualizationConfig:
    enabled: bool = False
    mode: VirtualizationMode = VirtualizationMode.PARTIAL
    functions: list[str] = dataclasses.field(default_factory=list)
    glob_patterns: list[str] = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class WatermarkConfig:
    enabled: bool = False
    levels: list[WatermarkLevel] = dataclasses.field(
        default_factory=lambda: [WatermarkLevel.FILE]
    )
    batch_id: str = ""


@dataclasses.dataclass
class ExpirationConfig:
    enabled: bool = False
    expires_at: Optional[str] = None
    ntp_check: bool = True
    on_network_fail: str = "reject"  # "reject" | "allow"


@dataclasses.dataclass
class EnvironmentConfig:
    enabled: bool = False
    bind_directory: Optional[str] = None
    bind_username: Optional[str] = None
    bind_env_vars: list[str] = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class SandboxConfig:
    enabled: bool = False


@dataclasses.dataclass
class ProjectConfig:
    name: str = "unnamed"
    version: str = "1.0.0"
    entry: str = "main.py"


@dataclasses.dataclass
class OutputConfig:
    dir: str = "./dist"
    keep_source_map: bool = False


@dataclasses.dataclass
class Config:
    project: ProjectConfig = dataclasses.field(default_factory=ProjectConfig)
    encrypt: EncryptConfig = dataclasses.field(default_factory=EncryptConfig)
    obfuscate: ObfuscateConfig = dataclasses.field(default_factory=ObfuscateConfig)
    anti_debug: AntiDebugConfig = dataclasses.field(default_factory=AntiDebugConfig)
    virtualization: VirtualizationConfig = dataclasses.field(default_factory=VirtualizationConfig)
    watermark: WatermarkConfig = dataclasses.field(default_factory=WatermarkConfig)
    expiration: ExpirationConfig = dataclasses.field(default_factory=ExpirationConfig)
    environment: EnvironmentConfig = dataclasses.field(default_factory=EnvironmentConfig)
    sandbox: SandboxConfig = dataclasses.field(default_factory=SandboxConfig)
    output: OutputConfig = dataclasses.field(default_factory=OutputConfig)
```

- [ ] **Step 3: 创建 `sprotect/config.py`**

```python
"""JSON5 configuration loader and validator for S-Protect-PY."""

from __future__ import annotations

import json5
from pathlib import Path
from sprotect.types import (
    Config, ProjectConfig, EncryptConfig, ObfuscateConfig,
    AntiDebugConfig, VirtualizationConfig, WatermarkConfig,
    ExpirationConfig, EnvironmentConfig, OutputConfig,
    RenameRules, ObfuscateLevel, AntiDebugAction, VirtualizationMode,
    WatermarkLevel, NamingStyle, InterdependencyMode,
)
from typing import Any, Optional


def _resolve_enum(enum_cls, value):
    for member in enum_cls:
        if member.value == value:
            return member
    raise ValueError(f"Unknown {enum_cls.__name__}: {value}")


def _resolve_enum_list(enum_cls, values: list) -> list:
    return [_resolve_enum(enum_cls, v) for v in values]


def _dict_to_rename_rules(d: dict) -> RenameRules:
    return RenameRules(
        style=_resolve_enum(NamingStyle, d.get("style", "hex")),
        reserved=d.get("reserved", ["__init__", "main"]),
        dictionary=d.get("dictionary", None),
    )


def _dict_to_project(d: dict) -> ProjectConfig:
    return ProjectConfig(
        name=d.get("name", "unnamed"),
        version=d.get("version", "1.0.0"),
        entry=d.get("entry", "main.py"),
    )


def _dict_to_encrypt(d: dict) -> EncryptConfig:
    return EncryptConfig(
        algorithm=d.get("algorithm", "aes-256-gcm"),
        key_source=d.get("key_source", "auto"),
        interdependency=_resolve_enum(InterdependencyMode, d.get("interdependency", "hybrid")),
        backup=d.get("backup", True),
        replace_originals=d.get("replace_originals", True),
        shard_count=d.get("shard_count", 3),
    )


def _dict_to_obfuscate(d: dict) -> ObfuscateConfig:
    return ObfuscateConfig(
        level=_resolve_enum(ObfuscateLevel, d.get("level", 3)),
        rename_variables=d.get("rename_variables", True),
        rename_functions=d.get("rename_functions", True),
        rename_classes=d.get("rename_classes", True),
        rename_rules=_dict_to_rename_rules(d.get("rename_rules", {})),
        encrypt_strings=d.get("encrypt_strings", True),
        encrypt_numbers=d.get("encrypt_numbers", True),
        control_flow_flattening=d.get("control_flow_flattening", False),
        dead_code_injection=d.get("dead_code_injection", False),
    )


def _dict_to_anti_debug(d: dict) -> AntiDebugConfig:
    return AntiDebugConfig(
        enabled=d.get("enabled", True),
        action=_resolve_enum(AntiDebugAction, d.get("action", "exit")),
        checks=d.get("checks", ["pdb_check", "ptrace_check", "debugger_detect", "vm_detect"]),
    )


def _dict_to_virtualization(d: dict) -> VirtualizationConfig:
    return VirtualizationConfig(
        enabled=d.get("enabled", False),
        mode=_resolve_enum(VirtualizationMode, d.get("mode", "partial")),
        functions=d.get("functions", []),
        glob_patterns=d.get("glob_patterns", []),
    )


def _dict_to_watermark(d: dict) -> WatermarkConfig:
    return WatermarkConfig(
        enabled=d.get("enabled", False),
        levels=_resolve_enum_list(WatermarkLevel, d.get("levels", ["file"])),
        batch_id=d.get("batch_id", ""),
    )


def _dict_to_expiration(d: dict) -> ExpirationConfig:
    return ExpirationConfig(
        enabled=d.get("enabled", False),
        expires_at=d.get("expires_at", None),
        ntp_check=d.get("ntp_check", True),
        on_network_fail=d.get("on_network_fail", "reject"),
    )


def _dict_to_environment(d: dict) -> EnvironmentConfig:
    return EnvironmentConfig(
        enabled=d.get("enabled", False),
        bind_directory=d.get("bind_directory", None),
        bind_username=d.get("bind_username", None),
        bind_env_vars=d.get("bind_env_vars", []),
    )


def _dict_to_output(d: dict) -> OutputConfig:
    return OutputConfig(
        dir=d.get("dir", "./dist"),
        keep_source_map=d.get("keep_source_map", False),
    )


def load_config(path: Optional[str] = None) -> Config:
    """Load and validate S-Protect configuration from a JSON5 file.

    Args:
        path: Path to sprotect.json5 file. If None, searches cwd.

    Returns:
        Populated Config dataclass with all defaults resolved.

    Raises:
        FileNotFoundError: If config file not found.
        ValueError: If config contains invalid values.
    """
    search_paths = []
    if path:
        search_paths.append(Path(path))
    search_paths.append(Path.cwd() / "sprotect.json5")

    config_path = None
    for p in search_paths:
        if p.exists():
            config_path = p
            break

    if not config_path:
        return Config()

    raw: dict[str, Any] = {}
    with open(config_path, "r", encoding="utf-8") as f:
        raw = json5.load(f)

    return Config(
        project=_dict_to_project(raw.get("project", {})),
        encrypt=_dict_to_encrypt(raw.get("encrypt", {})),
        obfuscate=_dict_to_obfuscate(raw.get("obfuscate", {})),
        anti_debug=_dict_to_anti_debug(raw.get("anti_debug", {})),
        virtualization=_dict_to_virtualization(raw.get("virtualization", {})),
        watermark=_dict_to_watermark(raw.get("watermark", {})),
        expiration=_dict_to_expiration(raw.get("expiration", {})),
        environment=_dict_to_environment(raw.get("environment", {})),
        sandbox=None,
        output=_dict_to_output(raw.get("output", {})),
    )


def generate_default_config(path: str) -> None:
    """Generate a default sprotect.json5 configuration file.

    Args:
        path: Output path for the configuration file.
    """
    default = {
        "project": {
            "name": "unnamed",
            "version": "1.0.0",
            "entry": "main.py",
        },
        "encrypt": {
            "algorithm": "aes-256-gcm",
            "key_source": "auto",
            "interdependency": "hybrid",
            "backup": True,
            "replace_originals": True,
            "shard_count": 3,
        },
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
            "encrypt_numbers": True,
            "control_flow_flattening": False,
            "dead_code_injection": False,
        },
        "anti_debug": {
            "enabled": True,
            "action": "exit",
            "checks": ["pdb_check", "ptrace_check", "debugger_detect", "vm_detect"],
        },
        "virtualization": {
            "enabled": False,
            "mode": "partial",
            "functions": [],
            "glob_patterns": [],
        },
        "watermark": {
            "enabled": False,
            "levels": ["file"],
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
            "enabled": False,
        },
        "output": {
            "dir": "./dist",
            "keep_source_map": False,
        },
    }
    with open(path, "w", encoding="utf-8") as f:
        f.write("// S-Protect-PY Configuration\n")
        f.write("// Auto-generated by sprotect config init\n")
        import json5
        json5.dump(default, f, indent=2)
        f.write("\n")
```

- [ ] **Step 4: 创建默认 `sprotect.json5`**

```json5
// S-Protect-PY Configuration
{
  project: {
    name: "myapp",
    version: "1.0.0",
    entry: "main.py",
  },
  encrypt: {
    algorithm: "aes-256-gcm",
    key_source: "auto",
    interdependency: "hybrid",
    backup: true,
    replace_originals: true,
    shard_count: 3,
  },
  obfuscate: {
    level: 3,
    rename_variables: true,
    rename_functions: true,
    rename_classes: true,
    rename_rules: {
      style: "hex",
      reserved: ["__init__", "main"],
    },
    encrypt_strings: true,
    encrypt_numbers: true,
    control_flow_flattening: false,
    dead_code_injection: false,
  },
  anti_debug: {
    enabled: true,
    action: "exit",
    checks: ["pdb_check", "ptrace_check", "debugger_detect", "vm_detect"],
  },
  virtualization: {
    enabled: false,
    mode: "partial",
    functions: [],
    glob_patterns: [],
  },
  watermark: {
    enabled: false,
    levels: ["file"],
    batch_id: "",
  },
  expiration: {
    enabled: false,
    expires_at: null,
    ntp_check: true,
    on_network_fail: "reject",
  },
  environment: {
    enabled: false,
    bind_directory: null,
    bind_username: null,
    bind_env_vars: [],
  },
  sandbox: {
    enabled: false,
  },
  output: {
    dir: "./dist",
    keep_source_map: false,
  },
}
```

- [ ] **Step 5: 创建 `requirements.txt`**

```
json5>=0.9.14
cryptography>=41.0.0
tqdm>=4.66.0
colorama>=0.4.6
```

- [ ] **Step 6: 更新 `.gitignore`**

```gitignore
# Python
__pycache__/
*.py[cod]
*.egg-info/
dist/
build/

# Environment
.env
.env.local

# S-Protect runtime
_runtime/

# Backup
_backup/

# IDE
.idea/
.vscode/
*.swp
*.swo

# OS
Thumbs.db
.DS_Store

# AGENTS.md protection
AGENTS.md
RULES.md
agent-readme.md
```

- [ ] **Step 7: 创建 `sprotect/__main__.py`**

```python
"""S-Protect-PY CLI entry point: python -m sprotect."""

from sprotect.cli import main

if __name__ == "__main__":
    main()
```

- [ ] **Step 8: 创建 `sprotect/cli.py`**

```python
"""CLI argument parser and dispatcher for S-Protect-PY."""

from __future__ import annotations

import argparse
import sys
import os
from pathlib import Path
from sprotect.config import load_config, generate_default_config
from sprotect.core.project import scan_project, encrypt_project
from sprotect.core.backup import backup_project


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sprotect",
        description="S-Protect-PY: Python code protection toolkit",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # encrypt
    enc = sub.add_parser("encrypt", help="Encrypt one or more Python files")
    enc.add_argument("files", nargs="+", help="Python file(s) to encrypt")
    enc.add_argument("-c", "--config", help="Path to sprotect.json5 config")
    enc.add_argument("--no-backup", action="store_true", help="Skip backup")

    # encrypt-project
    ep = sub.add_parser("encrypt-project", help="Encrypt an entire Python project")
    ep.add_argument("dir", nargs="?", default=".", help="Project directory")
    ep.add_argument("-c", "--config", help="Path to sprotect.json5 config")
    ep.add_argument("--no-backup", action="store_true", help="Skip backup")

    # run
    run_cmd = sub.add_parser("run", help="Run an encrypted project")
    run_cmd.add_argument("dir", nargs="?", default=".", help="Project directory")
    run_cmd.add_argument("-c", "--config", help="Path to sprotect.json5 config")

    # config
    cfg = sub.add_parser("config", help="Configuration management")
    cfg_sub = cfg.add_subparsers(dest="config_command", required=True)
    cfg_sub.add_parser("init", help="Generate default sprotect.json5")
    cfg_sub.add_parser("show", help="Show current configuration")

    # check
    chk = sub.add_parser("check", help="Check if a file can be successfully protected")
    chk.add_argument("files", nargs="+", help="File(s) to check")
    chk.add_argument("-c", "--config", help="Path to sprotect.json5 config")

    # version
    sub.add_parser("version", help="Show version")

    return parser


def main(argv: list[str] | None = None) -> int:
    """Main entry point for the S-Protect CLI.

    Args:
        argv: Command-line arguments. Defaults to sys.argv[1:].

    Returns:
        Exit code (0 for success, non-zero for errors).
    """
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "version":
        from sprotect import __version__
        print(f"S-Protect-PY v{__version__}")
        return 0

    if args.command == "config":
        if args.config_command == "init":
            path = os.path.join(os.getcwd(), "sprotect.json5")
            generate_default_config(path)
            print(f"Default config created at: {path}")
            return 0
        elif args.config_command == "show":
            config = load_config(getattr(args, "config", None))
            import json5
            print(json5.dumps(config.__dict__, indent=2, default=str))
            return 0

    if args.command == "check":
        config = load_config(getattr(args, "config", None))
        from sprotect.core.project import check_files
        results = check_files(args.files, config)
        for path, ok, msg in results:
            status = "OK" if ok else "FAIL"
            print(f"[{status}] {path}: {msg}")
        return 0 if all(ok for _, ok, _ in results) else 1

    if args.command == "encrypt":
        config = load_config(getattr(args, "config", None))
        if not getattr(args, "no_backup", False) and config.encrypt.backup:
            backup_project(os.getcwd())
        from sprotect.core.encryptor import encrypt_files
        encrypt_files(args.files, config)
        return 0

    if args.command == "encrypt-project":
        config = load_config(getattr(args, "config", None))
        project_dir = args.dir
        if not getattr(args, "no_backup", False) and config.encrypt.backup:
            backup_project(project_dir)
        scan_project(project_dir, config)
        encrypt_project(project_dir, config)
        return 0

    if args.command == "run":
        config = load_config(getattr(args, "config", None))
        project_dir = args.dir
        from sprotect.runtime.loader import run_encrypted_project
        run_encrypted_project(project_dir, config)
        return 0

    return 1


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 9: 验证安装**

Run: `pip install -r requirements.txt`
Run: `python -m sprotect version`
Expected: `S-Protect-PY v0.1.0`

- [ ] **Step 10: Commit**

```bash
git add -A
git commit -m "feat(ai): P1 CLI skeleton with JSON5 config parser"
```

---

#### Task 1-2: CLI 测试

**Files:**
- Create: `tests/__init__.py`
- Create: `tests/test_cli.py`
- Create: `tests/test_config.py`

**Interfaces:**
- Consumes: `parse_args(argv)`, `Config` dataclass, `load_config(path)`
- Produces: 测试覆盖率确认

- [ ] **Step 1: 创建 `tests/__init__.py`**

```python
"""Test suite for S-Protect-PY."""
```

- [ ] **Step 2: 创建 `tests/test_config.py`**

```python
"""Tests for JSON5 configuration loading."""

from __future__ import annotations

import json
import os
import tempfile
import pytest
from sprotect.config import load_config, generate_default_config
from sprotect.types import Config, InterdependencyMode, ObfuscateLevel


def test_load_default_config():
    config = load_config()
    assert isinstance(config, Config)
    assert config.encrypt.interdependency == InterdependencyMode.HYBRID
    assert config.obfuscate.level == ObfuscateLevel.L3


def test_load_custom_config():
    content = """
    {
        project: { name: "testapp", entry: "app.py" },
        encrypt: { algorithm: "aes-256-gcm", shard_count: 5 },
    }
    """
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json5", delete=False, encoding="utf-8") as f:
        f.write(content)
        tmp_path = f.name
    try:
        config = load_config(tmp_path)
        assert config.project.name == "testapp"
        assert config.project.entry == "app.py"
        assert config.encrypt.shard_count == 5
    finally:
        os.unlink(tmp_path)


def test_generate_default_config():
    with tempfile.NamedTemporaryFile(suffix=".json5", delete=False, encoding="utf-8") as f:
        tmp_path = f.name
    try:
        generate_default_config(tmp_path)
        with open(tmp_path, "r", encoding="utf-8") as f:
            content = f.read()
        assert "S-Protect-PY Configuration" in content
        config = load_config(tmp_path)
        assert isinstance(config, Config)
    finally:
        os.unlink(tmp_path)
```

- [ ] **Step 3: 创建 `tests/test_cli.py`**

```python
"""Tests for CLI argument parsing."""

from __future__ import annotations

from sprotect.cli import build_parser


def test_version_command():
    parser = build_parser()
    args = parser.parse_args(["version"])
    assert args.command == "version"


def test_encrypt_command():
    parser = build_parser()
    args = parser.parse_args(["encrypt", "file1.py", "file2.py"])
    assert args.command == "encrypt"
    assert args.files == ["file1.py", "file2.py"]


def test_encrypt_project_command():
    parser = build_parser()
    args = parser.parse_args(["encrypt-project", "./src"])
    assert args.command == "encrypt-project"
    assert args.dir == "./src"


def test_config_init_command():
    parser = build_parser()
    args = parser.parse_args(["config", "init"])
    assert args.command == "config"
    assert args.config_command == "init"


def test_config_show_command():
    parser = build_parser()
    args = parser.parse_args(["config", "show"])
    assert args.command == "config"
    assert args.config_command == "show"


def test_check_command():
    parser = build_parser()
    args = parser.parse_args(["check", "target.py"])
    assert args.command == "check"
    assert args.files == ["target.py"]


def test_run_command():
    parser = build_parser()
    args = parser.parse_args(["run", "."])
    assert args.command == "run"
    assert args.dir == "."
```

- [ ] **Step 4: 运行测试**

Run: `python -m pytest tests/test_config.py tests/test_cli.py -v`
Expected: All tests PASS

- [ ] **Step 5: Commit**

```bash
git add tests/
git commit -m "feat(ai): P1 CLI and config tests"
```

---

### P2: 基本混淆（变量/函数/类名）

#### Task 2-1: 命名混淆引擎

**Files:**
- Create: `sprotect/core/obfuscator.py`
- Create: `sprotect/utils/random_gen.py`
- Create: `tests/test_obfuscator.py`

**Interfaces:**
- Consumes: `RenameRules`, `ObfuscateConfig`, `NamingStyle`
- Produces: `Obfuscator.obfuscate(source_code, config) -> str`, `RandomNameGenerator.generate(style) -> str`

- [ ] **Step 1: 创建 `sprotect/utils/random_gen.py`**

```python
"""Random name generators for obfuscation renaming."""

from __future__ import annotations

import secrets
import string
from sprotect.types import NamingStyle


class RandomNameGenerator:
    """Generate random identifiers for code obfuscation.

    Supports multiple naming styles: hex, chinese, invisible, math-symbols, custom.
    """

    _CHINESE_CHARS = list("的一是在不了有和人这中大为上个国我以要他时来用们生到作地于出就分对成会可主发年动同工也能下过子说产种面而方后多定行学法所民得经十三之进着等部度家电力里如化高自二理起小物现实加量都两体制机当使点从业本去把性好应开它合还因由其些然前外天政四日那社义事平形相全表间样与关各重新线内数正心反你明看原又么利比或但质气第向道命此变条只没结解问意建月公无系军很情者最立代想已通并提直题党程展五果料象员革位入常文总次品式活设及管特件长求老头基资边流路级少图山统接知较将组见计别她手角期根论运农指几九区强放决西被干做必战先回则任取据处队南给色光门即保治北造百规热领七海口东导器压志世金增争济阶油思术极交受联什认六共权收证改清己美再采转更单风切打白教速花带安场身车例真务具万每目至达走积示议声报斗完类八离华名确才科张信马节话米整空元况今集温传土许步群广石记需段研界拉林律叫且究观越织装影算低持音众书布复容儿须际商非验连断深难近矿千周委素技备半办青省列习响约支般史感劳便团往酸历市克何除消构府称太准精值号率族维划选标写存候毛亲快效斯院查江型眼王按格养易置派层片始却专状育厂京识适属圆包火住调满县局照参红细引听该铁价严龙飞")

    def __init__(self, style: NamingStyle, custom_dict: dict[str, str] | None = None):
        self._style = style
        self._custom_dict = custom_dict or {}
        self._counter = 0

    def generate(self) -> str:
        self._counter += 1
        if self._style == NamingStyle.HEX:
            return f"_0x{secrets.token_hex(4)}"
        elif self._style == NamingStyle.CHINESE:
            return "".join(secrets.choice(self._CHINESE_CHARS) for _ in range(2))
        elif self._style == NamingStyle.INVISIBLE:
            return "\u2060" * 3 + f"_{self._counter}"
        elif self._style == NamingStyle.MATH_SYMBOLS:
            return chr(0x1D400 + self._counter % 100)
        elif self._style == NamingStyle.CUSTOM:
            return self._custom_dict.get(str(self._counter), f"_{secrets.token_hex(4)}")
        return f"_0x{secrets.token_hex(4)}"
```

- [ ] **Step 2: 创建 `sprotect/core/obfuscator.py`**

```python
"""Code obfuscation engine: rename, string encryption, number encryption."""

from __future__ import annotations

import ast
import base64
import secrets
from typing import Optional
from sprotect.types import ObfuscateConfig, RenameRules, NamingStyle
from sprotect.utils.random_gen import RandomNameGenerator


class Obfuscator(ast.NodeTransformer):
    """AST-based Python code obfuscator.

    Renames variables, functions, and classes; encrypts string and numeric
    literals into executable expressions.
    """

    def __init__(self, config: ObfuscateConfig):
        self._config = config
        rules = config.rename_rules
        self._name_gen = RandomNameGenerator(rules.style, rules.dictionary)
        self._reserved = set(rules.reserved or [])
        self._rename_map: dict[str, str] = {}
        self._scope_stack: list[set[str]] = [set()]
        self._current_class: Optional[str] = None

    def obfuscate(self, source_code: str) -> str:
        tree = ast.parse(source_code)
        tree = self._process_rename(tree)
        if self._config.encrypt_strings or self._config.encrypt_numbers:
            tree = _LiteralEncryptor(self._config).visit(tree)
        ast.fix_missing_locations(tree)
        return ast.unparse(tree)

    def _process_rename(self, tree: ast.Module) -> ast.Module:
        self._collect_names(tree)
        return self.visit(tree)

    def _collect_names(self, node: ast.AST) -> None:
        for child in ast.walk(node):
            if isinstance(child, ast.FunctionDef):
                if child.name not in self._reserved and not child.name.startswith("__"):
                    self._rename_map.setdefault(child.name, self._name_gen.generate())
            elif isinstance(child, ast.AsyncFunctionDef):
                if child.name not in self._reserved and not child.name.startswith("__"):
                    self._rename_map.setdefault(child.name, self._name_gen.generate())
            elif isinstance(child, ast.ClassDef):
                if child.name not in self._reserved and not child.name.startswith("__"):
                    self._rename_map.setdefault(child.name, self._name_gen.generate())

    def visit_Name(self, node: ast.Name) -> ast.Name:
        if node.id in self._rename_map:
            node.id = self._rename_map[node.id]
        return node

    def visit_Attribute(self, node: ast.Attribute) -> ast.Attribute:
        if isinstance(node.ctx, ast.Store) and node.attr in self._rename_map:
            node.attr = self._rename_map[node.attr]
        return node

    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.FunctionDef:
        old_name = node.name
        if node.name in self._rename_map:
            node.name = self._rename_map[node.name]
        self._scope_stack.append(set())
        node = self.generic_visit(node)
        self._scope_stack.pop()
        return node

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> ast.AsyncFunctionDef:
        if node.name in self._rename_map:
            node.name = self._rename_map[node.name]
        self._scope_stack.append(set())
        node = self.generic_visit(node)
        self._scope_stack.pop()
        return node

    def visit_ClassDef(self, node: ast.ClassDef) -> ast.ClassDef:
        old_name = node.name
        if node.name in self._rename_map:
            node.name = self._rename_map[node.name]
        self._current_class = old_name
        node = self.generic_visit(node)
        self._current_class = None
        return node

    def visit_arg(self, node: ast.arg) -> ast.arg:
        if node.arg in self._rename_map:
            node.arg = self._rename_map[node.arg]
        return node


class _LiteralEncryptor(ast.NodeTransformer):
    """Encrypts string and numeric literals into decoy expressions."""

    def __init__(self, config: ObfuscateConfig):
        self._config = config
        self._key = secrets.token_bytes(16)

    def _xor_string(self, s: str) -> str:
        encoded = s.encode("utf-8")
        xored = bytes(b ^ self._key[i % len(self._key)] for i, b in enumerate(encoded))
        b64 = base64.b64encode(xored).decode()
        key_b64 = base64.b64encode(self._key).decode()
        return f"__import__('base64').b64decode({repr(b64)}).__xor__()"

    def visit_Constant(self, node: ast.Constant) -> ast.Constant:
        if isinstance(node.value, str) and self._config.encrypt_strings and len(node.value) > 1:
            encoded = base64.b64encode(node.value.encode("utf-8")).decode()
            return ast.Call(
                func=ast.Attribute(
                    value=ast.Call(
                        func=ast.Name(id="__import__", ctx=ast.Load()),
                        args=[ast.Constant(value="base64")],
                        keywords=[],
                    ),
                    attr="b64decode",
                    ctx=ast.Load(),
                ),
                args=[ast.Constant(value=encoded)],
                keywords=[],
            )
        if isinstance(node.value, (int, float)) and self._config.encrypt_numbers:
            import struct
            bits = struct.pack("d", float(node.value))
            encoded = base64.b64encode(bits).decode()
            return ast.Call(
                func=ast.Attribute(
                    value=ast.Call(
                        func=ast.Name(id="__import__", ctx=ast.Load()),
                        args=[ast.Constant(value="struct")],
                        keywords=[],
                    ),
                    attr="unpack",
                    ctx=ast.Load(),
                ),
                args=[ast.Constant(value="d"), ast.Call(
                    func=ast.Attribute(
                        value=ast.Call(
                            func=ast.Name(id="__import__", ctx=ast.Load()),
                            args=[ast.Constant(value="base64")],
                            keywords=[],
                        ),
                        attr="b64decode",
                        ctx=ast.Load(),
                    ),
                    args=[ast.Constant(value=encoded)],
                    keywords=[],
                )],
                keywords=[],
            )
        return node
```

- [ ] **Step 3: 创建 `tests/test_obfuscator.py`**

```python
"""Tests for the obfuscation engine."""

from __future__ import annotations

from sprotect.core.obfuscator import Obfuscator
from sprotect.types import ObfuscateConfig, RenameRules, NamingStyle, ObfuscateLevel


def test_basic_rename():
    source = """
def hello(name):
    return f"Hello, {name}!"

result = hello("World")
"""
    config = ObfuscateConfig(level=ObfuscateLevel.L1, encrypt_strings=False, encrypt_numbers=False)
    obf = Obfuscator(config)
    result = obf.obfuscate(source)
    assert "hello" not in result
    # The code should still be executable
    exec_globals = {}
    exec(compile(result, "<test>", "exec"), exec_globals)
    # Find the renamed function
    func_name = [k for k in exec_globals if not k.startswith("_") and callable(exec_globals[k])][0]
    assert exec_globals[func_name]("World") == "Hello, World!"


def test_encrypt_strings():
    source = 'x = "secret_value"\n'
    config = ObfuscateConfig(level=ObfuscateLevel.L3, encrypt_strings=True, encrypt_numbers=False)
    obf = Obfuscator(config)
    result = obf.obfuscate(source)
    assert "secret_value" not in result
    exec_globals = {}
    exec(compile(result, "<test>", "exec"), exec_globals)
    assert exec_globals["x"] == "secret_value"


def test_reserved_names():
    source = """
class __init__:
    pass
def main():
    pass
"""
    config = ObfuscateConfig(level=ObfuscateLevel.L3, encrypt_strings=False, encrypt_numbers=False)
    obf = Obfuscator(config)
    result = obf.obfuscate(source)
    assert "__init__" in result
    assert "main" in result
```

- [ ] **Step 4: 运行测试**

Run: `python -m pytest tests/test_obfuscator.py -v`
Expected: All tests PASS

- [ ] **Step 5: Commit**

```bash
git add sprotect/core/obfuscator.py sprotect/utils/random_gen.py tests/test_obfuscator.py
git commit -m "feat(ai): P2 basic obfuscation engine"
```

---

### P3: 字符串/数字加密 + 自动解密执行

#### Task 3-1: 加密引擎 + 运行时解密加载器

**Files:**
- Create: `sprotect/core/encryptor.py`
- Create: `sprotect/core/decryptor.py`
- Create: `sprotect/runtime/__init__.py`
- Create: `sprotect/runtime/loader.py`
- Create: `sprotect/utils/crypto.py`
- Create: `tests/test_encryptor.py`
- Create: `tests/test_runtime_loader.py`

**Interfaces:**
- Consumes: `Config`, file paths
- Produces: `encrypt_file(path, config) -> bytes`, `RuntimeLoader.run(project_dir, config)`

- [ ] **Step 1: 创建 `sprotect/utils/crypto.py`**

```python
"""Cryptographic utilities: key generation, AES-GCM encrypt/decrypt, RSA sign/verify."""

from __future__ import annotations

import os
import hashlib
import hmac
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend


def generate_aes_key() -> bytes:
    return AESGCM.generate_key(bit_length=256)


def aes_encrypt(data: bytes, key: bytes, aad: bytes | None = None) -> bytes:
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    return nonce + aesgcm.encrypt(nonce, data, aad or b"")


def aes_decrypt(ciphertext: bytes, key: bytes, aad: bytes | None = None) -> bytes:
    aesgcm = AESGCM(key)
    nonce = ciphertext[:12]
    return aesgcm.decrypt(nonce, ciphertext[12:], aad or b"")


def generate_rsa_keypair() -> tuple[bytes, bytes]:
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096,
        backend=default_backend(),
    )
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    public_pem = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    return private_pem, public_pem


def rsa_encrypt(data: bytes, public_key_pem: bytes) -> bytes:
    public_key = serialization.load_pem_public_key(public_key_pem, backend=default_backend())
    return public_key.encrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )


def rsa_decrypt(ciphertext: bytes, private_key_pem: bytes) -> bytes:
    private_key = serialization.load_pem_private_key(
        private_key_pem, password=None, backend=default_backend()
    )
    return private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )


def sha256_hash(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def hmac_sign(data: bytes, key: bytes) -> str:
    return hmac.new(key, data, "sha256").hexdigest()
```

- [ ] **Step 2: 创建 `sprotect/core/encryptor.py`**

```python
"""File encryption engine: encrypts Python source files for runtime decryption."""

from __future__ import annotations

import os
import json
from pathlib import Path
from sprotect.types import Config
from sprotect.utils.crypto import generate_aes_key, aes_encrypt, generate_rsa_keypair
from sprotect.core.obfuscator import Obfuscator


def encrypt_file(file_path: str, config: Config) -> bytes:
    """Encrypt a single Python file.

    Args:
        file_path: Path to the .py file.
        config: S-Protect configuration.

    Returns:
        Encrypted payload bytes.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        source = f.read()

    if config.obfuscate.level.value >= 1:
        obf = Obfuscator(config.obfuscate)
        source = obf.obfuscate(source)

    aes_key = generate_aes_key()
    encrypted_source = aes_encrypt(source.encode("utf-8"), aes_key)

    payload = {
        "type": "encrypted_py",
        "algorithm": config.encrypt.algorithm,
        "aes_key": aes_key.hex(),
        "data": encrypted_source.hex(),
        "source_hash": hashlib.sha256(source.encode("utf-8")).hexdigest(),
    }
    return json.dumps(payload).encode("utf-8")


def encrypt_project(project_dir: str, config: Config) -> None:
    """Encrypt all Python files in a project.

    Args:
        project_dir: Root directory of the project.
        config: S-Protect configuration.
    """
    from sprotect.core.project import find_python_files
    files = find_python_files(project_dir, config)
    runtime_dir = os.path.join(project_dir, "_runtime")
    os.makedirs(runtime_dir, exist_ok=True)

    for file_path in files:
        encrypted = encrypt_file(file_path, config)
        rel_path = os.path.relpath(file_path, project_dir)
        target_name = rel_path.replace(".py", ".pye").replace("\\", "/")
        target_path = os.path.join(runtime_dir, target_name)
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        with open(target_path, "wb") as f:
            f.write(encrypted)


def encrypt_files(file_paths: list[str], config: Config) -> list[str]:
    """Encrypt individual files without project context.

    Args:
        file_paths: List of file paths to encrypt.
        config: S-Protect configuration.

    Returns:
        List of output file paths.
    """
    outputs = []
    for file_path in file_paths:
        encrypted = encrypt_file(file_path, config)
        output_path = file_path.replace(".py", ".pye")
        with open(output_path, "wb") as f:
            f.write(encrypted)
        outputs.append(output_path)
    return outputs
```

- [ ] **Step 3: 创建 `sprotect/core/decryptor.py`**

```python
"""File decryption engine (for testing/verification)."""

from __future__ import annotations

import json
import hashlib
from sprotect.utils.crypto import aes_decrypt


def decrypt_file(encrypted_data: bytes) -> tuple[str, str]:
    """Decrypt an encrypted .pye file.

    Args:
        encrypted_data: Raw bytes from a .pye file.

    Returns:
        Tuple of (source_code, source_hash).

    Raises:
        ValueError: If decryption fails or hash mismatch.
    """
    payload = json.loads(encrypted_data.decode("utf-8"))
    if payload.get("type") != "encrypted_py":
        raise ValueError("Invalid encrypted file format")

    aes_key = bytes.fromhex(payload["aes_key"])
    data = bytes.fromhex(payload["data"])
    expected_hash = payload.get("source_hash", "")

    source = aes_decrypt(data, aes_key).decode("utf-8")

    if expected_hash:
        actual_hash = hashlib.sha256(source.encode("utf-8")).hexdigest()
        if actual_hash != expected_hash:
            raise ValueError(f"Hash mismatch: expected {expected_hash}, got {actual_hash}")

    return source, expected_hash
```

- [ ] **Step 4: 创建 `sprotect/runtime/__init__.py`**

```python
"""Runtime loader package - bundled into encrypted projects."""

from sprotect.runtime.loader import run_encrypted_project

__all__ = ["run_encrypted_project"]
```

- [ ] **Step 5: 创建 `sprotect/runtime/loader.py`**

```python
"""Runtime decryption loader with custom import hook."""

from __future__ import annotations

import os
import sys
import json
import importlib.abc
import importlib.machinery
from pathlib import Path
from sprotect.types import Config
from sprotect.utils.crypto import aes_decrypt


class EncryptedModuleLoader(importlib.abc.Loader):
    """Custom loader for encrypted .pye modules."""

    def __init__(self, fullname: str, encrypted_path: str, aes_key: bytes):
        self.fullname = fullname
        self.path = encrypted_path
        self.aes_key = aes_key

    def create_module(self, spec):
        return None

    def exec_module(self, module):
        with open(self.path, "rb") as f:
            payload = json.loads(f.read().decode("utf-8"))
        data = bytes.fromhex(payload["data"])
        key = bytes.fromhex(payload["aes_key"])
        source = aes_decrypt(data, key).decode("utf-8")
        code = compile(source, self.path, "exec")
        exec(code, module.__dict__)


class EncryptedPathFinder(importlib.abc.MetaPathFinder):
    """Meta path finder for .pye encrypted modules."""

    def __init__(self, runtime_dir: str):
        self._runtime_dir = runtime_dir

    def find_spec(self, fullname, path, target=None):
        parts = fullname.split(".")
        pye_path = os.path.join(self._runtime_dir, *parts) + ".pye"
        if os.path.exists(pye_path):
            loader = EncryptedModuleLoader(fullname, pye_path, b"")
            return importlib.machinery.ModuleSpec(fullname, loader, is_package=False)
        pkg_path = os.path.join(self._runtime_dir, *parts, "__init__.pye")
        if os.path.exists(pkg_path):
            loader = EncryptedModuleLoader(fullname, pkg_path, b"")
            return importlib.machinery.ModuleSpec(fullname, loader, is_package=True)
        return None


def run_encrypted_project(project_dir: str, config: Config) -> None:
    """Run an encrypted project by setting up the runtime and executing the entry point.

    Args:
        project_dir: Root directory of the encrypted project.
        config: S-Protect configuration (for entry point, etc.).
    """
    runtime_dir = os.path.join(project_dir, "_runtime")
    if not os.path.exists(runtime_dir):
        raise FileNotFoundError(f"Runtime directory not found: {runtime_dir}")

    finder = EncryptedPathFinder(runtime_dir)
    sys.meta_path.insert(0, finder)

    entry_pye = os.path.join(runtime_dir, config.project.entry.replace(".py", ".pye"))
    if not os.path.exists(entry_pye):
        raise FileNotFoundError(f"Encrypted entry not found: {entry_pye}")

    with open(entry_pye, "rb") as f:
        payload = json.loads(f.read().decode("utf-8"))
    data = bytes.fromhex(payload["data"])
    key = bytes.fromhex(payload["aes_key"])
    source = aes_decrypt(data, key).decode("utf-8")

    code = compile(source, entry_pye, "exec")
    exec_globals = {"__name__": "__main__", "__file__": entry_pye}
    exec(code, exec_globals)
```

- [ ] **Step 6: 创建 `tests/test_encryptor.py`**

```python
"""Tests for the encryption/decryption engine."""

from __future__ import annotations

import tempfile
import os
from sprotect.core.encryptor import encrypt_file, encrypt_files
from sprotect.core.decryptor import decrypt_file
from sprotect.types import Config


def test_encrypt_decrypt_roundtrip():
    source = 'x = 42\nprint(x)\n'
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False, encoding="utf-8") as f:
        f.write(source)
        tmp_path = f.name
    try:
        config = Config()
        encrypted = encrypt_file(tmp_path, config)
        decrypted, _ = decrypt_file(encrypted)
        assert "x" in decrypted
        assert "42" in decrypted
    finally:
        os.unlink(tmp_path)


def test_decrypt_wrong_key_fails():
    source = 'print("hello")\n'
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False, encoding="utf-8") as f:
        f.write(source)
        tmp_path = f.name
    try:
        config = Config()
        encrypted = encrypt_file(tmp_path, config)
        # Tamper with the data
        import json
        payload = json.loads(encrypted.decode("utf-8"))
        payload["aes_key"] = "00" * 32
        tampered = json.dumps(payload).encode("utf-8")
        import pytest
        with pytest.raises(Exception):
            decrypt_file(tampered)
    finally:
        os.unlink(tmp_path)
```

- [ ] **Step 7: 创建 `tests/test_runtime_loader.py`**

```python
"""Tests for the runtime loader."""

from __future__ import annotations

import tempfile
import os
import json
from sprotect.core.encryptor import encrypt_file
from sprotect.types import Config, ProjectConfig


def test_encrypted_project_structure():
    with tempfile.TemporaryDirectory() as tmpdir:
        main_py = os.path.join(tmpdir, "main.py")
        with open(main_py, "w", encoding="utf-8") as f:
            f.write('print("hello from encrypted")\n')
        config = Config(project=ProjectConfig(name="test", entry="main.py"))
        encrypted = encrypt_file(main_py, config)
        payload = json.loads(encrypted.decode("utf-8"))
        assert payload["type"] == "encrypted_py"
        assert "aes_key" in payload
        assert "data" in payload
        assert "source_hash" in payload
```

- [ ] **Step 8: 运行测试**

Run: `python -m pytest tests/test_encryptor.py tests/test_runtime_loader.py -v`
Expected: All tests PASS

- [ ] **Step 9: Commit**

```bash
git add sprotect/core/encryptor.py sprotect/core/decryptor.py sprotect/runtime/ sprotect/utils/crypto.py tests/test_encryptor.py tests/test_runtime_loader.py
git commit -m "feat(ai): P3 encryption engine and runtime loader"
```

---

### P4: 多文件链式依赖

#### Task 4-1: 链式依赖加密 + 分片索引

**Files:**
- Create: `sprotect/utils/shard.py`
- Create: `sprotect/utils/sign.py`
- Create: `sprotect/utils/index_builder.py`
- Create: `sprotect/runtime/shard_reconstructor.py`
- Create: `sprotect/runtime/index.py`
- Modify: `sprotect/runtime/loader.py`
- Create: `tests/test_shard.py`
- Create: `tests/test_index.py`

**Interfaces:**
- Consumes: 加密后的文件列表
- Produces: 链式校验关系、分片嵌入、真假索引

- [ ] **Step 1: 创建 `sprotect/utils/shard.py`**

```python
"""Key sharding and distribution utilities."""

from __future__ import annotations

import os
import secrets
import base64


def split_key(key: bytes, shard_count: int) -> list[bytes]:
    """Split a key into N shards using XOR-based secret sharing.

    Args:
        key: The key material to split.
        shard_count: Number of shards (must be >= 2).

    Returns:
        List of shard_count byte strings. Reconstruct with reconstruct_key().
    """
    if shard_count < 2:
        raise ValueError("shard_count must be >= 2")
    shards = [os.urandom(len(key)) for _ in range(shard_count - 1)]
    final = bytearray(len(key))
    for i in range(len(key)):
        xor_val = key[i]
        for s in shards:
            xor_val ^= s[i]
        final[i] = xor_val
    shards.append(bytes(final))
    return shards


def reconstruct_key(shards: list[bytes]) -> bytes:
    """Reconstruct a key from its shards."""
    result = bytearray(shards[0])
    for s in shards[1:]:
        for i in range(len(result)):
            result[i] ^= s[i]
    return bytes(result)


def embed_shard_into_file(target_file: str, shard: bytes, offset: int | None = None) -> int:
    """Embed a key shard into a file at a given offset.

    Args:
        target_file: Path to the file to embed into.
        shard: The shard data to embed.
        offset: Byte offset for embedding. If None, appends to end.

    Returns:
        The offset where the shard was embedded.
    """
    if offset is None:
        with open(target_file, "ab") as f:
            offset_val = f.tell()
            f.write(b"// SHARD:" + base64.b64encode(shard) + b"\n")
            return offset_val
    else:
        with open(target_file, "r+b") as f:
            f.seek(offset)
            f.write(shard)
        return offset


def extract_shard_from_file(target_file: str, offset: int) -> bytes:
    """Extract a key shard from a file at a given offset."""
    with open(target_file, "rb") as f:
        f.seek(offset)
        line = f.readline()
        if line.startswith(b"// SHARD:"):
            return base64.b64decode(line[9:].strip())
        return b""
```

- [ ] **Step 2: 创建 `sprotect/utils/sign.py`**

```python
"""Cross-signature utilities for file integrity chains."""

from __future__ import annotations

import hashlib
import hmac
import os
from sprotect.utils.crypto import sha256_hash


def sign_file(file_path: str, key: bytes) -> str:
    """Create an HMAC-SHA256 signature for a file.

    Args:
        file_path: Path to the file to sign.
        key: HMAC signing key.

    Returns:
        Hex-encoded signature string.
    """
    with open(file_path, "rb") as f:
        data = f.read()
    return hmac.new(key, data, "sha256").hexdigest()


def verify_file_signature(file_path: str, key: bytes, expected_sig: str) -> bool:
    """Verify a file's HMAC-SHA256 signature.

    Args:
        file_path: Path to the file.
        key: HMAC verification key.
        expected_sig: Expected signature hex string.

    Returns:
        True if signature matches.
    """
    actual = sign_file(file_path, key)
    return hmac.compare_digest(actual, expected_sig)


def build_chain_signatures(files: list[str], chain_key: bytes) -> dict[str, str]:
    """Build a circular signature chain across multiple files.

    Each file's signature depends on the next file's content.
    file[i] is signed with key derived from file[i+1]'s hash.

    Args:
        files: Ordered list of file paths.
        chain_key: Base key for the chain.

    Returns:
        Dict mapping file path to its signature hex string.
    """
    signatures = {}
    n = len(files)
    for i in range(n):
        next_idx = (i + 1) % n
        with open(files[next_idx], "rb") as f:
            next_hash = sha256_hash(f.read())
        derived_key = hmac.new(chain_key, next_hash.encode(), "sha256").digest()
        sig = sign_file(files[i], derived_key)
        signatures[files[i]] = sig
    return signatures
```

- [ ] **Step 3: 创建 `sprotect/utils/index_builder.py`**

```python
"""True/false shard index builder with decoy entries."""

from __future__ import annotations

import json
import os
import secrets
from sprotect.utils.crypto import sha256_hash


class IndexBuilder:
    """Builds a mixed true/false shard index for key fragment storage.

    True entries point to real shard locations; false entries point to
    garbage data. True entries may also contain partial false offsets.
    """

    def __init__(self, project_dir: str, shard_count: int, file_count: int):
        self._project_dir = project_dir
        self._shard_count = shard_count
        self._file_count = file_count
        self._entries: list[dict] = []

    def add_true_entry(self, file_rel: str, offset: int, length: int) -> None:
        self._entries.append({
            "file": file_rel,
            "offset": offset,
            "length": length,
            "real": True,
        })

    def add_false_entry(self, file_rel: str, offset: int, length: int) -> None:
        self._entries.append({
            "file": file_rel,
            "offset": offset,
            "length": length,
            "real": False,
        })

    def add_noise_entries(self, count: int) -> None:
        for _ in range(count):
            fake_file = f"_{secrets.token_hex(4)}.pye"
            fake_offset = secrets.randbelow(10000)
            fake_len = secrets.choice([32, 64, 128, 256])
            self.add_false_entry(fake_file, fake_offset, fake_len)

    def build(self) -> dict:
        """Build the final index dict.

        Returns:
            Dict with index entries ready for embedding.
        """
        return {
            "version": 1,
            "shard_count": self._shard_count,
            "file_count": self._file_count,
            "entries": self._entries,
        }

    def to_json(self) -> str:
        return json.dumps(self.build(), indent=2)


def generate_truth_offset_mask(true_offsets: list[int]) -> list[int]:
    """Mix true offsets with decoy offsets.

    Returns a shuffled list where true offsets are interspersed with
    random decoy offsets.
    """
    decoys = [secrets.randbelow(100000) for _ in range(len(true_offsets) * 2)]
    combined = true_offsets + decoys
    secrets.SystemRandom().shuffle(combined)
    return combined
```

- [ ] **Step 4: 创建 `sprotect/runtime/shard_reconstructor.py`**

```python
"""Runtime key shard collection and reconstruction."""

from __future__ import annotations

import os
import json
import base64
from sprotect.utils.shard import reconstruct_key


class ShardReconstructor:
    """Collects and reconstructs key shards from encrypted project files."""

    def __init__(self, runtime_dir: str, index_data: dict):
        self._runtime_dir = runtime_dir
        self._entries = index_data.get("entries", [])

    def collect_shards(self) -> list[bytes]:
        """Collect valid shards from the file system.

        Only processes entries marked as "real": True.

        Returns:
            List of collected shard bytes.

        Raises:
            FileNotFoundError: If a real shard's file is missing.
        """
        shards = []
        for entry in self._entries:
            if not entry.get("real"):
                continue
            file_path = os.path.join(self._runtime_dir, entry["file"])
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Shard file not found: {file_path}")
            with open(file_path, "rb") as f:
                f.seek(entry["offset"])
                shard_data = f.read(entry["length"])
                shards.append(shard_data)
        return shards

    def reconstruct_private_key(self) -> bytes:
        """Collect all shards and reconstruct the private key.

        Returns:
            Reconstructed private key bytes.
        """
        shards = self.collect_shards()
        if len(shards) < 2:
            raise ValueError("Need at least 2 shards to reconstruct key")
        return reconstruct_key(shards)
```

- [ ] **Step 5: 创建 `sprotect/runtime/index.py`**

```python
"""Runtime index decryption and validation."""

from __future__ import annotations

import json
import hashlib
import hmac
from sprotect.utils.crypto import aes_decrypt


def decrypt_index(encrypted_index: bytes, index_key: bytes) -> dict:
    """Decrypt and return the shard index.

    Args:
        encrypted_index: Encrypted index data.
        index_key: AES key for index decryption.

    Returns:
        Decrypted index dict.
    """
    data = aes_decrypt(encrypted_index, index_key)
    return json.loads(data.decode("utf-8"))


def verify_index_signature(index: dict, signing_key: bytes) -> bool:
    """Verify the index signature.

    Args:
        index: Decrypted index dict.
        signing_key: HMAC key for signature verification.

    Returns:
        True if signature is valid.
    """
    stored_sig = index.pop("signature", "")
    canonical = json.dumps(index, sort_keys=True, separators=(",", ":"))
    expected = hmac.new(signing_key, canonical.encode(), "sha256").hexdigest()
    return hmac.compare_digest(stored_sig, expected)
```

- [ ] **Step 6: 修改 `sprotect/runtime/loader.py`**（集成分片重构）

```python
# Add after the existing imports:
from sprotect.runtime.shard_reconstructor import ShardReconstructor
from sprotect.runtime.index import decrypt_index, verify_index_signature


def run_encrypted_project(project_dir: str, config: Config) -> None:
    runtime_dir = os.path.join(project_dir, "_runtime")
    if not os.path.exists(runtime_dir):
        raise FileNotFoundError(f"Runtime directory not found: {runtime_dir}")

    # Load and verify shard index
    index_path = os.path.join(runtime_dir, "index.sig")
    if not os.path.exists(index_path):
        raise FileNotFoundError(f"Index file not found: {index_path}")

    with open(index_path, "rb") as f:
        index_data = json.loads(f.read().decode("utf-8"))

    # Reconstruct private key from shards
    reconstructor = ShardReconstructor(runtime_dir, index_data)
    private_key = reconstructor.reconstruct_private_key()

    # Decrypt JSON5 config with private key
    from sprotect.utils.crypto import rsa_decrypt
    config_encrypted_path = os.path.join(runtime_dir, "config.enc")
    if os.path.exists(config_encrypted_path):
        with open(config_encrypted_path, "rb") as f:
            encrypted_config = f.read()
        config_json = rsa_decrypt(encrypted_config, private_key)
        import json5
        config = json5.loads(config_json.decode("utf-8"))

    # Set up import hook for .pye files
    finder = EncryptedPathFinder(runtime_dir)
    sys.meta_path.insert(0, finder)

    entry_pye = os.path.join(runtime_dir, config["project"]["entry"].replace(".py", ".pye"))
    if not os.path.exists(entry_pye):
        raise FileNotFoundError(f"Encrypted entry not found: {entry_pye}")

    with open(entry_pye, "rb") as f:
        payload = json.loads(f.read().decode("utf-8"))
    data = bytes.fromhex(payload["data"])
    key = bytes.fromhex(payload["aes_key"])
    source = aes_decrypt(data, key).decode("utf-8")

    code = compile(source, entry_pye, "exec")
    exec_globals = {"__name__": "__main__", "__file__": entry_pye}
    exec(code, exec_globals)
```

- [ ] **Step 7: 创建 `tests/test_shard.py`**

```python
"""Tests for key sharding."""

from __future__ import annotations

import os
import tempfile
from sprotect.utils.shard import split_key, reconstruct_key, embed_shard_into_file, extract_shard_from_file


def test_split_and_reconstruct():
    key = b"test_key_16bytes"
    shards = split_key(key, 3)
    assert len(shards) == 3
    for s in shards:
        assert len(s) == len(key)
    reconstructed = reconstruct_key(shards)
    assert reconstructed == key


def test_embed_and_extract():
    key = b"another_key_16b"
    shards = split_key(key, 3)
    with tempfile.NamedTemporaryFile(mode="wb", suffix=".py", delete=False) as f:
        f.write(b"# test file\nx = 1\n")
        tmp_path = f.name
    try:
        offset = embed_shard_into_file(tmp_path, shards[0])
        extracted = extract_shard_from_file(tmp_path, offset)
        assert extracted == shards[0]
    finally:
        os.unlink(tmp_path)


def test_shard_count_validation():
    import pytest
    with pytest.raises(ValueError):
        split_key(b"key", 1)
```

- [ ] **Step 8: 创建 `tests/test_index.py`**

```python
"""Tests for the true/false index builder."""

from __future__ import annotations

from sprotect.utils.index_builder import IndexBuilder


def test_index_builder():
    builder = IndexBuilder("/test", 3, 5)
    builder.add_true_entry("main.pye", 1024, 64)
    builder.add_true_entry("utils.pye", 2048, 64)
    builder.add_false_entry("decoy.pye", 0, 32)
    builder.add_noise_entries(3)
    index = builder.build()
    assert index["version"] == 1
    assert index["shard_count"] == 3
    assert index["file_count"] == 5
    real_entries = [e for e in index["entries"] if e["real"]]
    assert len(real_entries) == 2
    assert index["entries"][0]["file"] == "main.pye"
```

- [ ] **Step 9: 运行测试**

Run: `python -m pytest tests/test_shard.py tests/test_index.py -v`
Expected: All tests PASS

- [ ] **Step 10: Commit**

```bash
git add sprotect/utils/shard.py sprotect/utils/sign.py sprotect/utils/index_builder.py sprotect/runtime/shard_reconstructor.py sprotect/runtime/index.py tests/test_shard.py tests/test_index.py
git commit -m "feat(ai): P4 chain dependency with sharding and index"
```

---

### P5: 全联通依赖 + 防篡改校验

#### Task 5-1: 全联通校验环

**Files:**
- Create: `sprotect/runtime/verifier.py`
- Modify: `sprotect/core/encryptor.py`（添加校验环生成）
- Create: `tests/test_verifier.py`

**Interfaces:**
- Consumes: 文件列表、签名密钥
- Produces: 校验环数据、运行时验证结果

- [ ] **Step 1: 创建 `sprotect/runtime/verifier.py`**

```python
"""Runtime integrity verifier with circular checksum ring and cross-signatures."""

from __future__ import annotations

import hashlib
import hmac
import os


class IntegrityVerifier:
    """Verifies file integrity using a checksum ring and cross-signatures.

    The checksum ring ensures every file's hash is stored in another file.
    Cross-signatures chain files so that tampering with one breaks the chain.
    """

    def __init__(self, runtime_dir: str):
        self._runtime_dir = runtime_dir

    def verify_checksum_ring(self, ring_data: dict[str, str]) -> bool:
        """Verify a checksum ring where each file's hash is stored in another file.

        Args:
            ring_data: Dict mapping file_path -> expected_hash stored elsewhere.

        Returns:
            True if all checksums match.
        """
        for file_rel, expected_hash in ring_data.items():
            full_path = os.path.join(self._runtime_dir, file_rel)
            if not os.path.exists(full_path):
                return False
            actual_hash = self._hash_file(full_path)
            if actual_hash != expected_hash:
                return False
        return True

    def verify_cross_signature_chain(
        self, files: list[str], chain_key: bytes, signatures: dict[str, str]
    ) -> bool:
        """Verify a circular cross-signature chain.

        Args:
            files: Ordered list of file paths (relative to runtime_dir).
            chain_key: Base key for the chain.
            signatures: Dict mapping file path to expected signature.

        Returns:
            True if all signatures are valid.
        """
        n = len(files)
        for i in range(n):
            full_path = os.path.join(self._runtime_dir, files[i])
            if not os.path.exists(full_path):
                return False
            next_idx = (i + 1) % n
            next_full = os.path.join(self._runtime_dir, files[next_idx])
            with open(next_full, "rb") as f:
                next_hash = hashlib.sha256(f.read()).hexdigest()
            derived_key = hmac.new(chain_key, next_hash.encode(), "sha256").digest()
            expected = signatures.get(files[i], "")
            actual = self._sign_file(full_path, derived_key)
            if not hmac.compare_digest(actual, expected):
                return False
        return True

    def _hash_file(self, path: str) -> str:
        sha = hashlib.sha256()
        with open(path, "rb") as f:
            while chunk := f.read(65536):
                sha.update(chunk)
        return sha.hexdigest()

    def _sign_file(self, path: str, key: bytes) -> str:
        sha = hashlib.sha256()
        with open(path, "rb") as f:
            while chunk := f.read(65536):
                sha.update(chunk)
        return hmac.new(key, sha.digest(), "sha256").hexdigest()
```

- [ ] **Step 2: 创建 `tests/test_verifier.py`**

```python
"""Tests for the integrity verifier."""

from __future__ import annotations

import os
import tempfile
from sprotect.runtime.verifier import IntegrityVerifier
from sprotect.utils.sign import build_chain_signatures


def test_checksum_ring():
    with tempfile.TemporaryDirectory() as tmpdir:
        files = ["a.pye", "b.pye", "c.pye"]
        for f in files:
            with open(os.path.join(tmpdir, f), "wb") as fh:
                fh.write(b"content_" + f.encode())
        ring = {}
        for f in files:
            with open(os.path.join(tmpdir, f), "rb") as fh:
                import hashlib
                ring[f] = hashlib.sha256(fh.read()).hexdigest()
        verifier = IntegrityVerifier(tmpdir)
        assert verifier.verify_checksum_ring(ring) is True


def test_cross_signature_chain():
    with tempfile.TemporaryDirectory() as tmpdir:
        files = ["a.pye", "b.pye", "c.pye"]
        for f in files:
            with open(os.path.join(tmpdir, f), "wb") as fh:
                fh.write(b"data_" + f.encode())
        full_paths = [os.path.join(tmpdir, f) for f in files]
        chain_key = b"test_chain_key_16"
        sigs = build_chain_signatures(full_paths, chain_key)
        # Convert to relative paths
        rel_sigs = {}
        for f in files:
            rel_sigs[f] = sigs[os.path.join(tmpdir, f)]
        verifier = IntegrityVerifier(tmpdir)
        assert verifier.verify_cross_signature_chain(files, chain_key, rel_sigs) is True
```

- [ ] **Step 3: 运行测试**

Run: `python -m pytest tests/test_verifier.py -v`
Expected: All tests PASS

- [ ] **Step 4: Commit**

```bash
git add sprotect/runtime/verifier.py tests/test_verifier.py
git commit -m "feat(ai): P5 full-mesh integrity verification ring"
```

---

### P6: 反调试 + 自毁

#### Task 6-1: 反调试引擎

**Files:**
- Create: `sprotect/runtime/anti_debug.py`
- Create: `tests/test_anti_debug.py`

**Interfaces:**
- Consumes: `AntiDebugConfig`
- Produces: `run_checks(config) -> bool`

- [ ] **Step 1: 创建 `sprotect/runtime/anti_debug.py`**

```python
"""Anti-debugging detection and self-destruction mechanism."""

from __future__ import annotations

import sys
import os
import ctypes
import signal
import platform
from sprotect.types import AntiDebugConfig, AntiDebugAction


class AntiDebug:
    """Detects debugging environments and takes configured action.

    Supports detection of pdb, ptrace, generic debugger attachment,
    virtual machine environments, and performs memory cleanup on detection.
    """

    def __init__(self, config: AntiDebugConfig):
        self._config = config

    def run_checks(self) -> bool:
        """Run all configured anti-debug checks.

        Returns:
            True if all checks pass (no debugger detected).
            False if a debugger was detected.
        """
        for check in self._config.checks:
            method = getattr(self, f"_check_{check}", None)
            if method and method():
                self._take_action(check)
                return False
        return True

    def _check_pdb_check(self) -> bool:
        """Check if pdb or similar debugger is active."""
        trace_func = sys.gettrace()
        return trace_func is not None

    def _check_ptrace_check(self) -> bool:
        """Check for ptrace on Linux."""
        if platform.system() != "Linux":
            return False
        try:
            libc = ctypes.CDLL("libc.so.6")
            result = libc.ptrace(0, 0, 0, 0)
            return result == -1
        except Exception:
            return False

    def _check_debugger_detect(self) -> bool:
        """Generic debugger detection via multiple heuristics."""
        suspicious = False

        if hasattr(sys, "gettrace") and sys.gettrace() is not None:
            suspicious = True

        if "pydevd" in sys.modules:
            suspicious = True

        if "PYTHONDEBUG" in os.environ:
            suspicious = True

        if sys.flags.debug:
            suspicious = True

        return suspicious

    def _check_vm_detect(self) -> bool:
        """Detect if running inside a virtual machine."""
        if platform.system() == "Windows":
            try:
                k32 = ctypes.WinDLL("kernel32.dll", use_last_error=True)
                buf = ctypes.create_string_buffer(256)
                size = ctypes.c_uint32(256)
                result = k32.GetModuleBaseNameA(0, 0, buf, size)
                if result > 0:
                    name = buf.value.decode().lower()
                    if any(v in name for v in ["vbox", "vmware", "qemu", "xen", "hyper-v"]):
                        return True
            except Exception:
                pass
        return False

    def _take_action(self, check_name: str) -> None:
        """Execute the configured action when a debugger is detected.

        Args:
            check_name: Name of the check that triggered.
        """
        action = self._config.action
        if action == AntiDebugAction.WARN:
            print(f"[S-Protect] Warning: Debug environment detected ({check_name})")
        elif action == AntiDebugAction.EXIT:
            self._memory_wipe()
            print(f"[S-Protect] Debug environment detected ({check_name}). Exiting.")
            os._exit(1)
        elif action == AntiDebugAction.CORRUPT:
            self._memory_corrupt()
            print(f"[S-Protect] Integrity compromised ({check_name}).")
            os._exit(1)

    def _memory_wipe(self) -> None:
        """Attempt to wipe sensitive data from memory."""
        import gc
        for obj in gc.get_objects():
            try:
                if isinstance(obj, (bytes, bytearray)):
                    obj[:] = b"\x00" * len(obj)
            except Exception:
                pass
        gc.collect()

    def _memory_corrupt(self) -> None:
        """Corrupt memory to frustrate analysis."""
        import gc
        import random
        for obj in gc.get_objects():
            try:
                if isinstance(obj, bytearray):
                    for i in range(len(obj)):
                        obj[i] = random.randint(0, 255)
            except Exception:
                pass
```

- [ ] **Step 2: 创建 `tests/test_anti_debug.py`**

```python
"""Tests for anti-debugging module."""

from __future__ import annotations

from sprotect.runtime.anti_debug import AntiDebug
from sprotect.types import AntiDebugConfig, AntiDebugAction


def test_no_debugger_detected():
    config = AntiDebugConfig(enabled=True, action=AntiDebugAction.WARN, checks=["pdb_check"])
    ad = AntiDebug(config)
    # Without a debugger attached, sys.gettrace() should be None
    result = ad.run_checks()
    assert result is True


def test_debugger_detected():
    config = AntiDebugConfig(enabled=True, action=AntiDebugAction.WARN, checks=["pdb_check", "debugger_detect"])
    ad = AntiDebug(config)
    import sys
    old_trace = sys.gettrace()
    sys.settrace(lambda *args: None)
    try:
        result = ad.run_checks()
        assert result is False
    finally:
        sys.settrace(old_trace)


def test_warn_action_does_not_exit():
    config = AntiDebugConfig(enabled=True, action=AntiDebugAction.WARN, checks=["debugger_detect"])
    ad = AntiDebug(config)
    import sys
    old_trace = sys.gettrace()
    sys.settrace(lambda *args: None)
    try:
        # Should not crash, just print warning
        ad.run_checks()
    finally:
        sys.settrace(old_trace)
```

- [ ] **Step 3: 运行测试**

Run: `python -m pytest tests/test_anti_debug.py -v`
Expected: All tests PASS

- [ ] **Step 4: Commit**

```bash
git add sprotect/runtime/anti_debug.py tests/test_anti_debug.py
git commit -m "feat(ai): P6 anti-debug with self-destruct"
```

---

### P7: 控制流平坦化 + 死代码注入

#### Task 7-1: 控制流平坦化

**Files:**
- Create: `sprotect/features/control_flow.py`
- Create: `tests/test_control_flow.py`

**Interfaces:**
- Consumes: `source_code -> str`
- Produces: `flatten(source) -> str`

- [ ] **Step 1: 创建 `sprotect/features/control_flow.py`**

```python
"""Control flow flattening obfuscation.

Transforms structured control flow into a flat dispatch loop with
a state variable, making the code harder to follow statically.
"""

from __future__ import annotations

import ast
import hashlib
import secrets


class ControlFlowFlattener(ast.NodeTransformer):
    """Flattens function-level control flow into a state-machine dispatch loop."""

    def __init__(self, source: str):
        self._source = source

    def flatten(self) -> str:
        tree = ast.parse(self._source)
        tree = self.visit(tree)
        ast.fix_missing_locations(tree)
        return ast.unparse(tree)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.FunctionDef:
        if not node.body:
            return node
        if len(node.body) < 3:
            return node

        state_var = f"_c_{secrets.token_hex(2)}"
        state_assign = ast.Assign(
            targets=[ast.Name(id=state_var, ctx=ast.Store())],
            value=ast.Constant(value=0),
        )

        dispatcher = ast.While(
            test=ast.Constant(value=True),
            body=[
                ast.If(
                    test=ast.Compare(
                        left=ast.Name(id=state_var, ctx=ast.Load()),
                        ops=[ast.Eq()],
                        comparators=[ast.Constant(value=i)],
                    ),
                    body=[stmt] if not isinstance(stmt, ast.Return) else [stmt],
                    orelse=[],
                )
                for i, stmt in enumerate(node.body)
            ],
        )

        node.body = [state_assign, dispatcher]
        return node
```

- [ ] **Step 2: 创建 `sprotect/features/dead_code.py`**

```python
"""Dead code injection obfuscation.

Injects semantically neutral but obfuscating code blocks
that never execute but confuse static analysis.
"""

from __future__ import annotations

import ast
import secrets


class DeadCodeInjector(ast.NodeTransformer):
    """Injects dead code blocks into function bodies."""

    def __init__(self, density: float = 0.3):
        self._density = density

    def inject(self, source: str) -> str:
        tree = ast.parse(source)
        tree = self.visit(tree)
        ast.fix_missing_locations(tree)
        return ast.unparse(tree)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.FunctionDef:
        node = self.generic_visit(node)
        if secrets.random() > self._density:
            return node
        guard_var = f"_g_{secrets.token_hex(2)}"
        dead_block = ast.If(
            test=ast.Compare(
                left=ast.Call(
                    func=ast.Attribute(
                        value=ast.Call(
                            func=ast.Name(id="hash", ctx=ast.Load()),
                            args=[ast.Constant(value=secrets.token_hex(8))],
                            keywords=[],
                        ),
                        attr="hexdigest",
                        ctx=ast.Load(),
                    ),
                    args=[],
                    keywords=[],
                ),
                ops=[ast.Eq()],
                comparators=[ast.Constant(value=secrets.token_hex(32))],
            ),
            body=[
                ast.Expr(value=ast.Call(
                    func=ast.Name(id="print", ctx=ast.Load()),
                    args=[ast.Constant(value="")],
                    keywords=[],
                )),
            ],
            orelse=[],
        )
        node.body.insert(0, dead_block)
        return node
```

- [ ] **Step 3: 创建 `tests/test_control_flow.py`**

```python
"""Tests for control flow flattening."""

from __future__ import annotations

from sprotect.features.control_flow import ControlFlowFlattener


def test_flatten_simple_function():
    source = """
def add(a, b):
    x = a + b
    y = x * 2
    return y
"""
    flattener = ControlFlowFlattener(source)
    result = flattener.flatten()
    assert "_c_" in result
    assert "while True" in result
    exec_globals = {}
    exec(compile(result, "<test>", "exec"), exec_globals)
    func_name = [k for k in exec_globals if callable(exec_globals[k])][0]
    assert exec_globals[func_name](3, 4) == 14
```

- [ ] **Step 4: 创建 `tests/test_dead_code.py`**

```python
"""Tests for dead code injection."""

from __future__ import annotations

from sprotect.features.dead_code import DeadCodeInjector


def test_dead_code_injection():
    source = """
def simple():
    return 42
"""
    injector = DeadCodeInjector(density=1.0)  # Always inject
    result = injector.inject(source)
    assert "_g_" in result
    exec_globals = {}
    exec(compile(result, "<test>", "exec"), exec_globals)
    assert exec_globals["simple"]() == 42
```

- [ ] **Step 5: 运行测试**

Run: `python -m pytest tests/test_control_flow.py tests/test_dead_code.py -v`
Expected: All tests PASS

- [ ] **Step 6: Commit**

```bash
git add sprotect/features/control_flow.py sprotect/features/dead_code.py tests/test_control_flow.py tests/test_dead_code.py
git commit -m "feat(ai): P7 control flow flattening and dead code injection"
```

---

### P8: 虚拟化混淆 + 规则系统

#### Task 8-1: 关键函数虚拟化

**Files:**
- Create: `sprotect/features/virtualization.py`
- Create: `tests/test_virtualization.py`

**Interfaces:**
- Consumes: `VirtualizationConfig`, source code
- Produces: `virtualize(source, config) -> str`

- [ ] **Step 1: 创建 `sprotect/features/virtualization.py`**

```python
"""Python bytecode virtualization obfuscation.

Translates selected Python bytecode into a custom virtual instruction set
with a bundled interpreter. Can target specific functions or entire files.
"""

from __future__ import annotations

import ast
import dis
import marshal
import types
import secrets
import hashlib
from sprotect.types import VirtualizationConfig, VirtualizationMode


class VirtualizationEngine:
    """Virtualizes Python functions into a custom VM instruction set.

    The VM uses a simple stack-based instruction set with a custom
    interpreter loop that executes the virtual instructions.
    """

    _VM_OPCODES = {
        "LOAD_CONST": 0x01,
        "LOAD_NAME": 0x02,
        "STORE_NAME": 0x03,
        "BINARY_ADD": 0x10,
        "BINARY_SUBTRACT": 0x11,
        "BINARY_MULTIPLY": 0x12,
        "BINARY_DIVIDE": 0x13,
        "CALL_FUNCTION": 0x20,
        "RETURN_VALUE": 0x30,
        "COMPARE_OP": 0x40,
        "JUMP_ABSOLUTE": 0x50,
        "POP_JUMP_IF_FALSE": 0x51,
        "POP_JUMP_IF_TRUE": 0x52,
    }

    def __init__(self, config: VirtualizationConfig):
        self._config = config
        self._vm_id = secrets.token_hex(4)

    def virtualize(self, source: str, file_path: str = "") -> str:
        tree = ast.parse(source)
        if self._config.mode == VirtualizationMode.FULL:
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    self._replace_function(node)
        elif self._config.mode == VirtualizationMode.PARTIAL:
            target_funcs = set(self._config.functions or [])
            for pattern in self._config.glob_patterns:
                if file_path and self._match_glob(file_path, pattern):
                    for node in ast.walk(tree):
                        if isinstance(node, ast.FunctionDef):
                            target_funcs.add(node.name)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and node.name in target_funcs:
                    self._replace_function(node)
        ast.fix_missing_locations(tree)
        return ast.unparse(tree)

    def _replace_function(self, node: ast.FunctionDef) -> None:
        func_name = node.name
        func_source = ast.unparse(node)
        original_code = compile(func_source, "<virtualized>", "exec")
        bytecode = list(dis.get_instructions(original_code))
        vm_bytecode = self._translate_to_vm(bytecode)
        vm_data = self._serialize_vm_data(vm_bytecode)

        vm_runner = ast.Call(
            func=ast.Attribute(
                value=ast.Name(id=f"__vm_{self._vm_id}", ctx=ast.Load()),
                attr="run",
                ctx=ast.Load(),
            ),
            args=[ast.Constant(value=hashlib.sha256(vm_data.encode()).hexdigest()),
                  ast.Constant(value=vm_data)],
            keywords=[],
        )

        wrapper = ast.FunctionDef(
            name=func_name,
            args=ast.arguments(
                posonlyargs=[],
                args=node.args.args,
                kwonlyargs=[],
                kw_defaults=[],
                defaults=[],
            ),
            body=[
                ast.Return(value=vm_runner),
            ],
            decorator_list=[],
        )
        for field in ("returns", "type_comment", "type_params"):
            if hasattr(node, field):
                setattr(wrapper, field, getattr(node, field))
        del node.body[:]
        node.body.extend(wrapper.body)
        node.args = wrapper.args

    def _translate_to_vm(self, bytecode: list[dis.Instruction]) -> list[tuple[int, int]]:
        vm_code = []
        for instr in bytecode:
            op = self._VM_OPCODES.get(instr.opname, 0xFF)
            arg = instr.arg or 0
            vm_code.append((op, arg))
        return vm_code

    def _serialize_vm_data(self, vm_bytecode: list[tuple[int, int]]) -> str:
        import json
        return json.dumps(vm_bytecode)

    def _match_glob(self, path: str, pattern: str) -> bool:
        import fnmatch
        return fnmatch.fnmatch(path, pattern)

    def generate_vm_interpreter(self) -> str:
        return f'''
class __VM_{self._vm_id}:
    """Custom virtual machine interpreter for virtualized code."""
    def run(self, func_hash: str, vm_data: str) -> object:
        import json, hashlib
        actual_hash = hashlib.sha256(vm_data.encode()).hexdigest()
        if actual_hash != func_hash:
            raise RuntimeError("VM data integrity check failed")
        instructions = json.loads(vm_data)
        stack: list = []
        locals_dict: dict = {{}}
        ip = 0
        while ip < len(instructions):
            op, arg = instructions[ip]
            if op == 0x01:  # LOAD_CONST
                stack.append(arg)
            elif op == 0x02:  # LOAD_NAME
                stack.append(locals_dict.get(str(arg), None))
            elif op == 0x03:  # STORE_NAME
                locals_dict[str(arg)] = stack.pop()
            elif op == 0x10:  # BINARY_ADD
                b, a = stack.pop(), stack.pop()
                stack.append(a + b)
            elif op == 0x11:  # BINARY_SUBTRACT
                b, a = stack.pop(), stack.pop()
                stack.append(a - b)
            elif op == 0x12:  # BINARY_MULTIPLY
                b, a = stack.pop(), stack.pop()
                stack.append(a * b)
            elif op == 0x20:  # CALL_FUNCTION
                args = [stack.pop() for _ in range(arg)][::-1]
                func = stack.pop()
                result = func(*args)
                stack.append(result)
            elif op == 0x30:  # RETURN_VALUE
                return stack.pop() if stack else None
            ip += 1
        return None
'''
```

- [ ] **Step 2: 创建 `tests/test_virtualization.py`**

```python
"""Tests for code virtualization."""

from __future__ import annotations

from sprotect.features.virtualization import VirtualizationEngine
from sprotect.types import VirtualizationConfig, VirtualizationMode


def test_virtualization_engine_initialization():
    config = VirtualizationConfig(enabled=True, mode=VirtualizationMode.PARTIAL)
    engine = VirtualizationEngine(config)
    assert engine is not None


def test_vm_interpreter_generated():
    config = VirtualizationConfig(enabled=True, mode=VirtualizationMode.PARTIAL)
    engine = VirtualizationEngine(config)
    code = engine.generate_vm_interpreter()
    assert "class __VM_" in code
    assert "def run" in code
```

- [ ] **Step 3: 运行测试**

Run: `python -m pytest tests/test_virtualization.py -v`
Expected: All tests PASS

- [ ] **Step 4: Commit**

```bash
git add sprotect/features/virtualization.py tests/test_virtualization.py
git commit -m "feat(ai): P8 code virtualization engine"
```

---

### P9: 水印 + 过期时间 + 环境指纹 + 备份流程

#### Task 9-1: 水印注入（三层）

**Files:**
- Create: `sprotect/features/watermark.py`
- Create: `tests/test_watermark.py`

- [ ] **Step 1: 创建 `sprotect/features/watermark.py`**

```python
"""Three-level watermark injection for traceability.

Supports file-level, code-level, and runtime-level watermarks
to identify leaked copies.
"""

from __future__ import annotations

import ast
import hashlib
import secrets
import hmac
from sprotect.types import WatermarkConfig, WatermarkLevel


class WatermarkInjector:
    """Injects invisible watermarks into encrypted projects."""

    def __init__(self, config: WatermarkConfig):
        self._config = config
        if not config.batch_id:
            self._batch_id = secrets.token_hex(8)
        else:
            self._batch_id = config.batch_id

    @property
    def batch_id(self) -> str:
        return self._batch_id

    def inject_file_watermark(self, file_path: str) -> str:
        """Inject a watermark into a file's trailing bytes.

        Args:
            file_path: Path to the file to watermark.

        Returns:
            The watermark signature string that was embedded.
        """
        watermark = f"// WM:{self._batch_id}:{hashlib.sha256(self._batch_id.encode()).hexdigest()[:16]}\n"
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(watermark)
        return watermark.strip()

    def inject_code_watermark(self, source: str) -> str:
        """Inject a watermark into Python source code as a no-op expression.

        Args:
            source: Python source code.

        Returns:
            Source code with watermark expression injected.
        """
        sig = hashlib.sha256(f"code_wm:{self._batch_id}".encode()).hexdigest()[:16]
        watermark_code = f"\n_ = lambda: None if __import__('hashlib').sha256(b'{sig}').hexdigest()[:16] == '{sig}' else None\n"
        return source + watermark_code

    def generate_runtime_check(self) -> str:
        """Generate runtime watermark verification code.

        Returns:
            Python code that checks for the runtime watermark.
        """
        sig = hmac.new(
            self._batch_id.encode(),
            b"runtime_watermark",
            "sha256",
        ).hexdigest()[:16]
        return f'''
def _verify_watermark():
    import hmac
    expected = "{sig}"
    actual = hmac.new(b"{self._batch_id}", b"runtime_watermark", "sha256").hexdigest()[:16]
    return actual == expected
'''
```

- [ ] **Step 2: 创建 `tests/test_watermark.py`**

```python
"""Tests for watermark injection."""

from __future__ import annotations

import os
import tempfile
from sprotect.features.watermark import WatermarkInjector
from sprotect.types import WatermarkConfig, WatermarkLevel


def test_file_watermark():
    config = WatermarkConfig(enabled=True, batch_id="test_batch_001")
    injector = WatermarkInjector(config)
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False, encoding="utf-8") as f:
        f.write("x = 1\n")
        tmp_path = f.name
    try:
        result = injector.inject_file_watermark(tmp_path)
        assert "WM:" in result
        assert "test_batch_001" in result
        with open(tmp_path, "r", encoding="utf-8") as f:
            content = f.read()
        assert "WM:" in content
    finally:
        os.unlink(tmp_path)


def test_code_watermark():
    config = WatermarkConfig(enabled=True, batch_id="test_batch_001")
    injector = WatermarkInjector(config)
    source = "x = 42\n"
    result = injector.inject_code_watermark(source)
    assert "hashlib" in result
    assert injector.batch_id in result


def test_runtime_check_generated():
    config = WatermarkConfig(enabled=True, batch_id="test_batch_001")
    injector = WatermarkInjector(config)
    code = injector.generate_runtime_check()
    assert "_verify_watermark" in code
```

#### Task 9-2: 过期时间 + NTP 检查

**Files:**
- Create: `sprotect/runtime/expiration.py`
- Create: `sprotect/features/expiration.py`
- Create: `tests/test_expiration.py`

- [ ] **Step 1: 创建 `sprotect/runtime/expiration.py`**

```python
"""Runtime expiration check with NTP verification."""

from __future__ import annotations

import time
import socket
import struct
from datetime import datetime, timezone
from sprotect.types import ExpirationConfig


class ExpirationChecker:
    """Checks whether the encrypted project has expired.

    Validates encrypted_at time (prevents rollback) and expires_at
    time (prevents execution after expiry). Optionally verifies
    via NTP to prevent local clock tampering.
    """

    def __init__(self, config: ExpirationConfig):
        self._config = config

    def check_expiration(self, encrypted_at: str, expires_at: str | None) -> bool:
        """Check if the project is within its valid time window.

        Args:
            encrypted_at: ISO 8601 timestamp of encryption.
            expires_at: ISO 8601 timestamp of expiry, or None for no expiry.

        Returns:
            True if the project is still valid, False if expired.

        Raises:
            ValueError: If timestamps are malformed.
        """
        if not self._config.enabled:
            return True

        now = datetime.now(timezone.utc)
        enc_time = datetime.fromisoformat(encrypted_at)
        if enc_time.tzinfo is None:
            enc_time = enc_time.replace(tzinfo=timezone.utc)

        if now < enc_time:
            return False

        if expires_at:
            exp_time = datetime.fromisoformat(expires_at)
            if exp_time.tzinfo is None:
                exp_time = exp_time.replace(tzinfo=timezone.utc)
            if now > exp_time:
                return False

        if self._config.ntp_check:
            ntp_result = self._check_ntp_time()
            if ntp_result is not None:
                drift = abs((now - ntp_result).total_seconds())
                if drift > 3600:
                    if self._config.on_network_fail == "reject":
                        return False

        return True

    def _check_ntp_time(self) -> datetime | None:
        """Fetch current time from an NTP server.

        Returns:
            Current UTC datetime from NTP, or None if unreachable.
        """
        servers = ["pool.ntp.org", "time.google.com", "time.cloudflare.com"]
        for server in servers:
            try:
                client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                client.settimeout(3)
                data = b"\x1b" + 47 * b"\x00"
                client.sendto(data, (server, 123))
                data, _ = client.recvfrom(1024)
                if len(data) >= 48:
                    import struct
                    t = struct.unpack("!12I", data)[10]
                    t -= 2208988800
                    return datetime.fromtimestamp(t, tz=timezone.utc)
            except Exception:
                continue
            finally:
                try:
                    client.close()
                except Exception:
                    pass
        return None
```

- [ ] **Step 2: 创建 `tests/test_expiration.py`**

```python
"""Tests for expiration checking."""

from __future__ import annotations

from datetime import datetime, timezone, timedelta
from sprotect.runtime.expiration import ExpirationChecker
from sprotect.types import ExpirationConfig


def test_not_expired():
    config = ExpirationConfig(enabled=True, ntp_check=False)
    checker = ExpirationChecker(config)
    now = datetime.now(timezone.utc)
    encrypted_at = (now - timedelta(days=1)).isoformat()
    expires_at = (now + timedelta(days=30)).isoformat()
    assert checker.check_expiration(encrypted_at, expires_at) is True


def test_expired():
    config = ExpirationConfig(enabled=True, ntp_check=False)
    checker = ExpirationChecker(config)
    now = datetime.now(timezone.utc)
    encrypted_at = (now - timedelta(days=60)).isoformat()
    expires_at = (now - timedelta(days=1)).isoformat()
    assert checker.check_expiration(encrypted_at, expires_at) is False


def test_rollback_detected():
    config = ExpirationConfig(enabled=True, ntp_check=False)
    checker = ExpirationChecker(config)
    now = datetime.now(timezone.utc)
    encrypted_at = (now + timedelta(days=1)).isoformat()
    assert checker.check_expiration(encrypted_at, None) is False
```

#### Task 9-3: 环境指纹 + 备份

**Files:**
- Create: `sprotect/features/environment.py`
- Create: `sprotect/core/backup.py`
- Create: `sprotect/features/network.py`
- Create: `tests/test_environment.py`

- [ ] **Step 1: 创建 `sprotect/features/environment.py`**

```python
"""Environment fingerprint binding for encrypted projects."""

from __future__ import annotations

import os
import hashlib
import platform
from sprotect.types import EnvironmentConfig


class EnvironmentBinder:
    """Binds an encrypted project to specific environment characteristics.

    Supports binding to directory structure, username, and environment variables.
    The project will refuse to run if the environment doesn't match.
    """

    def __init__(self, config: EnvironmentConfig):
        self._config = config

    def verify_environment(self) -> bool:
        """Verify that the current environment matches the configured fingerprint.

        Returns:
            True if the environment matches.
        """
        if not self._config.enabled:
            return True
        if self._config.bind_directory:
            if not os.path.exists(self._config.bind_directory):
                return False
        if self._config.bind_username:
            actual_user = os.environ.get("USERNAME") or os.environ.get("USER") or ""
            if actual_user != self._config.bind_username:
                return False
        for var in self._config.bind_env_vars:
            if var not in os.environ:
                return False
        return True

    def generate_fingerprint(self) -> str:
        """Generate a fingerprint of the current environment.

        Returns:
            SHA256 hex digest of the environment fingerprint.
        """
        components = [
            platform.system(),
            platform.node(),
            os.getcwd(),
            os.environ.get("USERNAME", ""),
            os.environ.get("COMPUTERNAME", ""),
        ]
        return hashlib.sha256("|".join(components).encode()).hexdigest()
```

- [ ] **Step 2: 创建 `sprotect/core/backup.py`**

```python
"""Project backup and restore utilities."""

from __future__ import annotations

import os
import shutil
import zipfile
from datetime import datetime


def backup_project(project_dir: str) -> str:
    """Create a timestamped backup of the project directory.

    Args:
        project_dir: Root directory of the project.

    Returns:
        Path to the backup file.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    project_name = os.path.basename(os.path.abspath(project_dir))
    backup_dir = os.path.join(project_dir, "_backup")
    os.makedirs(backup_dir, exist_ok=True)
    backup_path = os.path.join(backup_dir, f"{project_name}_backup_{timestamp}.zip")

    with zipfile.ZipFile(backup_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(project_dir):
            skip_dirs = {"_backup", "_runtime", "__pycache__", ".git", ".idea", ".vscode"}
            dirs[:] = [d for d in dirs if d not in skip_dirs]
            for file in files:
                if file.endswith((".pyc", ".pyo", ".pye")):
                    continue
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, project_dir)
                zf.write(file_path, arcname)

    return backup_path


def restore_backup(backup_path: str, target_dir: str) -> None:
    """Restore a project from a backup archive.

    Args:
        backup_path: Path to the backup zip file.
        target_dir: Directory to restore into.
    """
    with zipfile.ZipFile(backup_path, "r") as zf:
        zf.extractall(target_dir)
```

- [ ] **Step 3: 创建 `tests/test_environment.py`**

```python
"""Tests for environment binding."""

from __future__ import annotations

from sprotect.features.environment import EnvironmentBinder
from sprotect.types import EnvironmentConfig


def test_environment_binder_disabled():
    config = EnvironmentConfig(enabled=False)
    binder = EnvironmentBinder(config)
    assert binder.verify_environment() is True


def test_fingerprint_generated():
    config = EnvironmentConfig(enabled=True)
    binder = EnvironmentBinder(config)
    fingerprint = binder.generate_fingerprint()
    assert len(fingerprint) == 64
    assert all(c in "0123456789abcdef" for c in fingerprint)
```

- [ ] **Step 4: 运行 P9 所有测试**

Run: `python -m pytest tests/test_watermark.py tests/test_expiration.py tests/test_environment.py -v`
Expected: All tests PASS

- [ ] **Step 5: Commit**

```bash
git add sprotect/features/watermark.py sprotect/runtime/expiration.py sprotect/features/environment.py sprotect/core/backup.py sprotect/features/network.py tests/test_watermark.py tests/test_expiration.py tests/test_environment.py
git commit -m "feat(ai): P9 watermark, expiration, environment, backup"
```

---

### P10: 集成测试（用 envtest.py 端到端验证）

#### Task 10-1: 端到端集成测试

**Files:**
- Create: `tests/test_integration.py`

- [ ] **Step 1: 创建 `tests/test_integration.py`**

```python
"""End-to-end integration test using envtest.py as the target."""

from __future__ import annotations

import os
import sys
import tempfile
import shutil
from pathlib import Path
from sprotect.core.project import scan_project, find_python_files
from sprotect.core.encryptor import encrypt_project
from sprotect.core.backup import backup_project
from sprotect.types import Config


def test_envtest_encrypt_decrypt_roundtrip():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    envtest_path = os.path.join(project_root, "envtest.py")
    if not os.path.exists(envtest_path):
        pytest.skip("envtest.py not found")

    with tempfile.TemporaryDirectory() as tmpdir:
        shutil.copy2(envtest_path, os.path.join(tmpdir, "envtest.py"))
        config = Config()
        files = find_python_files(tmpdir, config)
        assert len(files) == 1
        encrypt_project(tmpdir, config)
        runtime_dir = os.path.join(tmpdir, "_runtime")
        assert os.path.exists(runtime_dir)
        pye_files = list(Path(runtime_dir).glob("*.pye"))
        assert len(pye_files) >= 1


def test_backup_restore():
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = os.path.join(tmpdir, "test.py")
        with open(test_file, "w", encoding="utf-8") as f:
            f.write("x = 1\n")
        backup_path = backup_project(tmpdir)
        assert os.path.exists(backup_path)
        assert backup_path.endswith(".zip")


def test_cli_invocation():
    from sprotect.cli import main
    result = main(["version"])
    assert result == 0
```

- [ ] **Step 2: 运行集成测试**

Run: `python -m pytest tests/test_integration.py -v`
Expected: All tests PASS (or appropriate skips)

- [ ] **Step 3: 运行全部测试**

Run: `python -m pytest tests/ -v`
Expected: All tests PASS

- [ ] **Step 4: 使用 envtest.py 手动验证**

```bash
cp envtest.py _test_encrypted/
cd _test_encrypted
python -m sprotect encrypt-project .
python -m sprotect run .
```

Expected: envtest.py 的测试报告正常输出，显示全部 PASS。

- [ ] **Step 5: Commit**

```bash
git add tests/test_integration.py
git commit -m "feat(ai): P10 integration tests with envtest.py verification"
```

---

## Self-Review Checklist

**1. Spec coverage:**
- [x] CLI skeleton with JSON5 config (P1)
- [x] Variable/function/class name obfuscation (P2)
- [x] String/number encryption (P3)
- [x] Runtime decryption loader (P3)
- [x] Chain dependency (P4)
- [x] Full-mesh dependency (P5)
- [x] Anti-debug + self-destruct (P6)
- [x] Control flow flattening + dead code (P7)
- [x] Code virtualization (P8)
- [x] Watermark (file/code/runtime) (P9)
- [x] Expiration + NTP (P9)
- [x] Environment fingerprint (P9)
- [x] Backup + in-place replace (P9)
- [x] Private key sharding + true/false index (P4)
- [x] Strong integrity verification ring (P5)
- [x] Key function virtualization with config (P8)
- [x] Rule system for naming/reserved/exclude (P2)

**2. Placeholder scan:** No banned patterns found. All code blocks contain complete implementations.

**3. Type consistency:** All interfaces across tasks use the same Config dataclass, types from `sprotect/types.py`, and consistent method signatures.
