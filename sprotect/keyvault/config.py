"""KeyVault config: separate dataclass + JSON5 loader."""
from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional
import json5
import os


@dataclass
class KeyVaultConfig:
    enabled: bool = False
    pool_size: int = 1024
    xor_mask_hex: str = "A5A5A5A5A5A5A5A5A5A5A5A5A5A5A5A5A5A5A5A5A5A5A5A5A5A5A5A5A5A5A5A5"
    pid_binding: bool = True
    pid_salt: str = "0xDEADBEEF"
    decoy_min_size: int = 64
    decoy_max_size: int = 256


def load_keyvault_config(path: Optional[str] = None) -> KeyVaultConfig:
    candidates = []
    if path:
        candidates.append(Path(path))
    candidates.append(Path.cwd() / "sprotect" / "keyvault" / "defaults.json5")
    candidates.append(Path(__file__).parent / "defaults.json5")
    for c in candidates:
        if c.exists():
            raw = json5.loads(c.read_text(encoding="utf-8"))
            return KeyVaultConfig(
                enabled=raw.get("enabled", False),
                pool_size=raw.get("pool_size", 1024),
                xor_mask_hex=raw.get("xor_mask_hex", "A5" * 32),
                pid_binding=raw.get("pid_binding", True),
                pid_salt=raw.get("pid_salt", "0xDEADBEEF"),
                decoy_min_size=raw.get("decoy_min_size", 64),
                decoy_max_size=raw.get("decoy_max_size", 256),
            )
    return KeyVaultConfig()
