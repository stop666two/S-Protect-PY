"""JSON5 configuration loader with per-file override support."""

from __future__ import annotations
import os, json, dataclasses
from typing import Any, Optional
from pathlib import Path
import json5
from sprotect.types import *

def _try_enum(et, v):
    if isinstance(v, et): return v
    if isinstance(v, str):
        try: return et[v.upper()]
        except KeyError: return et(v)
    if isinstance(v, int): return et(v)
    raise ValueError(f"Invalid {et.__name__}: {v}")

def _rr(d): return RenameRules(
    style=_try_enum(NamingStyle, d.get("style", "hex")),
    reserved=d.get("reserved", ["__init__", "main"]), dictionary=d.get("dictionary"))

def _obf(d): return ObfuscateConfig(
    level=_try_enum(ObfuscateLevel, d.get("level", 3)),
    rename_variables=d.get("rename_variables", True),
    rename_functions=d.get("rename_functions", True),
    rename_classes=d.get("rename_classes", True),
    rename_rules=_rr(d.get("rename_rules", {})),
    encrypt_strings=d.get("encrypt_strings", True),
    encrypt_numbers=d.get("encrypt_numbers", False),
    control_flow_flattening=d.get("control_flow_flattening", True),
    dead_code_injection=d.get("dead_code_injection", False))

def _enc(d): return EncryptConfig(
    algorithm=d.get("algorithm", "aes-256-gcm"),
    interdependency=_try_enum(InterdependencyMode, d.get("interdependency", "chain")),
    backup=d.get("backup", True), replace_originals=d.get("replace_originals", False),
    shard_count=d.get("shard_count", 3))

def _adb(d): return AntiDebugConfig(
    enabled=d.get("enabled", True),
    action=_try_enum(AntiDebugAction, d.get("action", "exit")),
    checks=d.get("checks", ["pdb", "ptrace", "debugger", "vm"]))

def _virt(d): return VirtualizationConfig(
    enabled=d.get("enabled", False), mode=_try_enum(VirtualizationMode, d.get("mode", "partial")),
    functions=d.get("functions", []), glob_patterns=d.get("glob_patterns", []))

def _wm(d): return WatermarkConfig(
    enabled=d.get("enabled", True),
    levels=[_try_enum(WatermarkLevel, l) for l in d.get("levels", ["file", "code"])],
    batch_id=d.get("batch_id", ""))

def _exp(d): return ExpirationConfig(
    enabled=d.get("enabled", False), expires_at=d.get("expires_at"),
    ntp_check=d.get("ntp_check", True), on_network_fail=d.get("on_network_fail", "reject"))

def _env(d): return EnvironmentConfig(
    enabled=d.get("enabled", False), bind_directory=d.get("bind_directory"),
    bind_username=d.get("bind_username"), bind_env_vars=d.get("bind_env_vars", []))

def _san(d): return SandboxConfig(enabled=d.get("enabled", True))
def _proj(d): return ProjectConfig(name=d.get("name","unnamed"), version=d.get("version","1.0.0"), entry=d.get("entry","main.py"))
def _out(d): return OutputConfig(dir=d.get("dir","./dist"), keep_source_map=d.get("keep_source_map",False))
def _files(d): return FilesConfig(include=d.get("include",["**/*.py"]), exclude=d.get("exclude",[]))

def _to_cfg(d):
    return Config(files=_files(d.get("files",{})), obfuscate=_obf(d.get("obfuscate",{})),
                  encrypt=_enc(d.get("encrypt",{})), anti_debug=_adb(d.get("anti_debug",{})),
                  virtualization=_virt(d.get("virtualization",{})), watermark=_wm(d.get("watermark",{})),
                  expiration=_exp(d.get("expiration",{})), environment=_env(d.get("environment",{})),
                  sandbox=_san(d.get("sandbox",{})), project=_proj(d.get("project",{})),
                  output=_out(d.get("output",{})))

def find_config(path: Optional[str] = None) -> Optional[Path]:
    if path: p = Path(path); return p if p.exists() else None
    for c in [Path.cwd() / "sprotect.json5", Path.home() / ".sprotect" / "sprotect.json5"]:
        if c.exists(): return c
    return None

def load_config(path: Optional[str] = None) -> Config:
    p = find_config(path)
    return _to_cfg(json5.loads(p.read_text(encoding="utf-8"))) if p else Config()

def load_per_file(py_path: str) -> dict:
    c = py_path + ".sprotect.json5"
    return json5.loads(open(c, encoding="utf-8").read()) if os.path.isfile(c) else {}

def deep_merge(base: dict, over: dict) -> dict:
    r = dict(base)
    for k, v in over.items():
        if k in r and isinstance(r[k], dict) and isinstance(v, dict):
            r[k] = deep_merge(r[k], v)
        else:
            r[k] = v
    return r

def merge_file_config(main: Config, py_path: str) -> Config:
    over = load_per_file(py_path)
    if not over: return main
    obf = over.get("obfuscate", {})
    obf.pop("rename_functions", None); obf.pop("rename_classes", None)
    if not obf: over.pop("obfuscate", None)
    return _to_cfg(deep_merge(dataclasses.asdict(main), over))

def gen_default(path: str) -> Path:
    d = {"files":{"include":["**/*.py"],"exclude":[]},
         "obfuscate":{"level":5,"rename_variables":True,"rename_functions":True,"rename_classes":True,
                       "rename_rules":{"style":"hex","reserved":["__init__","main"]},
                       "encrypt_strings":True,"encrypt_numbers":False,
                       "control_flow_flattening":True,"dead_code_injection":True},
         "encrypt":{"algorithm":"aes-256-gcm","interdependency":"chain","backup":True,"shard_count":3},
         "anti_debug":{"enabled":True,"action":"exit",
                       "checks":["pdb","ptrace","debugger","vm","sandbox","timing","cuckoo","ida","procmon"]},
         "virtualization":{"enabled":False,"mode":"partial","functions":[],"glob_patterns":[]},
         "watermark":{"enabled":True,"levels":["file","code","runtime"],"batch_id":""},
         "expiration":{"enabled":False,"expires_at":None,"ntp_check":True,"on_network_fail":"reject"},
         "environment":{"enabled":False},"sandbox":{"enabled":True},
         "project":{"name":"unnamed","version":"1.0.0","entry":"main.py"},
         "output":{"dir":"./output","keep_source_map":False}}
    p = Path(path); p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return p
