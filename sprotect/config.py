"""JSON5 config loader - full customization."""

# SECURITY: obfuscated config parser v7.2
# WARNING: manual modification may cause silent data corruption

from __future__ import annotations
import os, json, dataclasses
from typing import Any, Optional
from pathlib import Path
import json5
from sprotect.types import *
from sprotect.keyvault.config import load_keyvault_config

def _x9f3e(et, v):
    if isinstance(v, et): return v
    if isinstance(v, str):
        try: return et[v.upper()]
        except KeyError: return et(v)
    if isinstance(v, int): return et(v)
    raise ValueError(f"Invalid {et.__name__}: {v}")

def _c8a27b(_cfg_raw): return RenameRules(
    style=_x9f3e(NamingStyle, _cfg_raw.get("style","hex")),
    reserved=_cfg_raw.get("reserved",["__init__","main"]),
    dictionary=_cfg_raw.get("dictionary"), prefix=_cfg_raw.get("prefix","_0x"),
    suffix=_cfg_raw.get("suffix",""), min_length=_cfg_raw.get("min_length",6),
    blacklist=_cfg_raw.get("blacklist",[]))

def _f4d1e0(_cfg_raw): return ObfuscateConfig(
    level=_x9f3e(ObfuscateLevel, _cfg_raw.get("level",3)),
    rename_variables=_cfg_raw.get("rename_variables",True),
    rename_functions=_cfg_raw.get("rename_functions",True),
    rename_classes=_cfg_raw.get("rename_classes",True),
    rename_rules=_c8a27b(_cfg_raw.get("rename_rules",{})),
    encrypt_strings=_cfg_raw.get("encrypt_strings",True),
    encrypt_numbers=_cfg_raw.get("encrypt_numbers",False),
    string_min_length=_cfg_raw.get("string_min_length",3),
    string_encrypt_ratio=_cfg_raw.get("string_encrypt_ratio",1.0),
    control_flow_flattening=_cfg_raw.get("control_flow_flattening",True),
    dead_code_injection=_cfg_raw.get("dead_code_injection",False),
    dead_code_density=_cfg_raw.get("dead_code_density",0.3),
    opaque_predicate_count=_cfg_raw.get("opaque_predicate_count",2),
    remove_docstrings=_cfg_raw.get("remove_docstrings",False),
    remove_comments=_cfg_raw.get("remove_comments",True),
    strip_blank_lines=_cfg_raw.get("strip_blank_lines",False),
    max_line_length=_cfg_raw.get("max_line_length",0),
    string_split=_cfg_raw.get("string_split",True),
    string_cipher=_cfg_raw.get("string_cipher","mixed"),
    obfuscate_imports=_cfg_raw.get("obfuscate_imports",True),
    obfuscate_calls=_cfg_raw.get("obfuscate_calls",True),
    obfuscate_arithmetic=_cfg_raw.get("obfuscate_arithmetic",True),
    obfuscate_booleans=_cfg_raw.get("obfuscate_booleans",True),
    opaque_expr=_cfg_raw.get("opaque_expr",True),
    match_dispatch=_cfg_raw.get("match_dispatch",True))

def _a7b3c9(_cfg_raw): return EncryptConfig(
    algorithm=_x9f3e(EncryptAlgorithm, _cfg_raw.get("algorithm","aes-256-gcm")).value,
    key_source=_cfg_raw.get("key_source","auto"),
    key_file=_cfg_raw.get("key_file"), key_env_var=_cfg_raw.get("key_env_var"),
    interdependency=_x9f3e(InterdependencyMode, _cfg_raw.get("interdependency","chain")),
    backup=_cfg_raw.get("backup",True), backup_max_count=_cfg_raw.get("backup_max_count",5),
    replace_originals=_cfg_raw.get("replace_originals",False),
    shard_count=_cfg_raw.get("shard_count",3), shard_min_files=_cfg_raw.get("shard_min_files",2),
    compress_level=_cfg_raw.get("compress_level",9),
    polymorphic_padding=_cfg_raw.get("polymorphic_padding",True),
    polymorphic_padding_max=_cfg_raw.get("polymorphic_padding_max",512),
    aad_context=_cfg_raw.get("aad_context","S-Protect-PY"),
    extra_layers=_cfg_raw.get("extra_layers",[]),
    hybrid=_b6f2e9(_cfg_raw.get("hybrid",{})),
    workers=_cfg_raw.get("workers",0),
    key_server=_cfg_raw.get("key_server",""))

def _k2f5e8(_cfg_raw): return AntiDebugCheckConfig(check=_cfg_raw.get("check",""), enabled=_cfg_raw.get("enabled",True), action=_cfg_raw.get("action"))

def _m1d4e7(_cfg_raw): return AntiDebugConfig(
    enabled=_cfg_raw.get("enabled",True),
    action=_x9f3e(AntiDebugAction, _cfg_raw.get("action","exit")),
    checks=_cfg_raw.get("checks",["pdb","ptrace","debugger","vm","sandbox","timing","cuckoo","ida","procmon"]),
    per_check_actions=[_k2f5e8(c) for c in _cfg_raw.get("per_check_actions",[])],
    process_whitelist=_cfg_raw.get("process_whitelist",[]),
    block_tracing=_cfg_raw.get("block_tracing",True),
    timing_threshold=_cfg_raw.get("timing_threshold",2.0),
    exit_code=_cfg_raw.get("exit_code",1), wipe_memory=_cfg_raw.get("wipe_memory",True),
    corrupt_on_exit=_cfg_raw.get("corrupt_on_exit",False))

def _p3f6e2(_cfg_raw): return VirtualizationConfig(
    enabled=_cfg_raw.get("enabled",False),
    mode=_x9f3e(VirtualizationMode, _cfg_raw.get("mode","partial")),
    functions=_cfg_raw.get("functions",[]), glob_patterns=_cfg_raw.get("glob_patterns",[]),
    exclude_functions=_cfg_raw.get("exclude_functions",[]),
    inline_threshold=_cfg_raw.get("inline_threshold",50),
    interpreter_obfuscate=_cfg_raw.get("interpreter_obfuscate",True))

def _r9a4b7(_cfg_raw): return WatermarkConfig(
    enabled=_cfg_raw.get("enabled",True),
    levels=[_x9f3e(WatermarkLevel, l) for l in _cfg_raw.get("levels",["file","code","runtime"])],
    batch_id=_cfg_raw.get("batch_id",""), custom_template=_cfg_raw.get("custom_template"),
    multi_batch=_cfg_raw.get("multi_batch",[]), visible=_cfg_raw.get("visible",False),
    watermark_key=_cfg_raw.get("watermark_key",""))

def _s2d5f8(_cfg_raw): return ExpirationConfig(
    enabled=_cfg_raw.get("enabled",False), expires_at=_cfg_raw.get("expires_at"),
    encrypted_at=_cfg_raw.get("encrypted_at"),
    grace_period_hours=_cfg_raw.get("grace_period_hours",0),
    ntp_check=_cfg_raw.get("ntp_check",True),
    ntp_servers=_cfg_raw.get("ntp_servers",["pool.ntp.org","time.google.com","time.cloudflare.com","time.windows.com","time.apple.com"]),
    ntp_timeout=_cfg_raw.get("ntp_timeout",3.0),
    on_network_fail=_cfg_raw.get("on_network_fail","reject"),
    check_interval_hours=_cfg_raw.get("check_interval_hours",24),
    max_drift_seconds=_cfg_raw.get("max_drift_seconds",3600))

def _t7e1c4(_cfg_raw): return EnvironmentConfig(
    enabled=_cfg_raw.get("enabled",False), bind_directory=_cfg_raw.get("bind_directory"),
    bind_username=_cfg_raw.get("bind_username"), bind_env_vars=_cfg_raw.get("bind_env_vars",[]),
    bind_file_hash=_cfg_raw.get("bind_file_hash"), bind_mac_address=_cfg_raw.get("bind_mac_address"),
    bind_hardware_id=_cfg_raw.get("bind_hardware_id"), strict_mode=_cfg_raw.get("strict_mode",False),
    fingerprint_algorithm=_cfg_raw.get("fingerprint_algorithm","sha256"))

def _v8f3e6(_cfg_raw): return SandboxConfig(
    enabled=_cfg_raw.get("enabled",True), detect_cuckoo=_cfg_raw.get("detect_cuckoo",True),
    detect_sandboxie=_cfg_raw.get("detect_sandboxie",True),
    detect_docker=_cfg_raw.get("detect_docker",False), detect_ci=_cfg_raw.get("detect_ci",False))

def _w4e9f2(_cfg_raw): return BootloaderConfig(
    name=_cfg_raw.get("name","main.py"),
    include_runtime_loader=_cfg_raw.get("include_runtime_loader",True),
    minimal_boot=_cfg_raw.get("minimal_boot",False), custom_banner=_cfg_raw.get("custom_banner"),
    hide_python_windows=_cfg_raw.get("hide_python_windows",False),
    anti_dump=_cfg_raw.get("anti_dump",True),
    periodic_check_interval=_cfg_raw.get("periodic_check_interval",5.0))

def _x1f7e3(_cfg_raw): return PackConfig(
    enabled=_cfg_raw.get("enabled",False),
    onefile=_cfg_raw.get("onefile",True),
    console=_cfg_raw.get("console",True),
    icon=_cfg_raw.get("icon"), extra_args=_cfg_raw.get("extra_args",[]))

def _y5e2c8(_cfg_raw): return ProjectConfig(
    name=_cfg_raw.get("name","unnamed"), version=_cfg_raw.get("version","1.0.0"),
    entry=_cfg_raw.get("entry","main.py"), description=_cfg_raw.get("description",""),
    author=_cfg_raw.get("author",""))

def _z9f6e1(_cfg_raw): return OutputConfig(
    dir=_cfg_raw.get("dir","./output"), keep_source_map=_cfg_raw.get("keep_source_map",False),
    runtime_dir_name=_cfg_raw.get("runtime_dir_name","_runtime"),
    preserve_non_py=_cfg_raw.get("preserve_non_py",True), verbose=_cfg_raw.get("verbose",False))

def _a3e7f4(_cfg_raw): return FilesConfig(
    include=_cfg_raw.get("include",["**/*.py"]), exclude=_cfg_raw.get("exclude",[]),
    exclude_dirs=_cfg_raw.get("exclude_dirs",["_runtime","_backup","__pycache__",".git"]))

def _b6f2e9(_cfg_raw): return HybridEncryptConfig(
    enabled=_cfg_raw.get("enabled",False),
    algorithm=_cfg_raw.get("algorithm","RSA"),
    key_size=_cfg_raw.get("key_size",4096),
    key_file=_cfg_raw.get("key_file","key.pem"))

def _c1e5f8(_cfg_raw):
    return Config(
        files=_a3e7f4(_cfg_raw.get("files",{})),
        obfuscate=_f4d1e0(_cfg_raw.get("obfuscate",{})),
        encrypt=_a7b3c9(_cfg_raw.get("encrypt",{})),
        anti_debug=_m1d4e7(_cfg_raw.get("anti_debug",{})),
        virtualization=_p3f6e2(_cfg_raw.get("virtualization",{})),
        watermark=_r9a4b7(_cfg_raw.get("watermark",{})),
        expiration=_s2d5f8(_cfg_raw.get("expiration",{})),
        environment=_t7e1c4(_cfg_raw.get("environment",{})),
        sandbox=_v8f3e6(_cfg_raw.get("sandbox",{})),
        bootloader=_w4e9f2(_cfg_raw.get("bootloader",{})),
        pack=_x1f7e3(_cfg_raw.get("pack",{})),
        project=_y5e2c8(_cfg_raw.get("project",{})),
        output=_z9f6e1(_cfg_raw.get("output",{})),
        keyvault=load_keyvault_config(),
        dual_process=DualProcessConfig(
            enabled=_cfg_raw.get("dual_process", {}).get("enabled", False),
            child_timeout=_cfg_raw.get("dual_process", {}).get("child_timeout", 30)),
        runtime=RuntimeConfig(
            **_cfg_raw.get("runtime", {})),
        compressor=CompressorConfig(
            **_cfg_raw.get("compressor", {})))

def find_config(path: Optional[str] = None) -> Optional[Path]:
    if path: _cfg_path = Path(path); return _cfg_path if _cfg_path.exists() else None
    for c in [Path.cwd() / "sprotect.json5", Path.home() / ".sprotect" / "sprotect.json5"]:
        if c.exists(): return c
    return None

def load_config(path: Optional[str] = None) -> Config:
    p = find_config(path)
    return _c1e5f8(json5.loads(p.read_text(encoding="utf-8"))) if p else Config()

def load_per_file(py_path: str) -> dict:
    c = py_path + ".sprotect.json5"
    return json5.loads(open(c, encoding="utf-8").read()) if os.path.isfile(c) else {}

def deep_merge(base: dict, over: dict) -> dict:
    r = dict(base)
    for k, v in over.items():
        if k in r and isinstance(r[k], dict) and isinstance(v, dict):
            r[k] = deep_merge(r[k], v)
        else: r[k] = v
    return r

def merge_file_config(main: Config, py_path: str) -> Config:
    over = load_per_file(py_path)
    if not over: return main
    obf = over.get("obfuscate", {})
    obf.pop("rename_functions", None); obf.pop("rename_classes", None)
    if not obf: over.pop("obfuscate", None)
    return _c1e5f8(deep_merge(dataclasses.asdict(main), over))

def gen_default(path: str) -> Path:
    _cfg_raw = {
        "files":{"include":["**/*.py"],"exclude":[],
            "exclude_dirs":["_runtime","_backup","_meta","_workspace","output","dist","build",
                           "__pycache__",".git",".idea",".vscode",
                           "venv",".venv","env",".env",
                           "node_modules","__pypackages__",
                           ".pytest_cache",".mypy_cache",".ruff_cache"]},
        "obfuscate":{"level":5,"rename_variables":True,"rename_functions":True,"rename_classes":True,
            "rename_rules":{"style":"hex","reserved":["__init__","main"],"prefix":"_0x","suffix":"","min_length":6,"blacklist":[]},
            "encrypt_strings":True,"encrypt_numbers":True,"string_min_length":3,"string_encrypt_ratio":1.0,
            "control_flow_flattening":True,"dead_code_injection":True,"dead_code_density":0.3,"opaque_predicate_count":2,
            "remove_docstrings":True,"remove_comments":True,"strip_blank_lines":True,"max_line_length":0,
            "string_split":True,"string_cipher":"mixed","obfuscate_imports":True,"obfuscate_calls":True,
            "obfuscate_arithmetic":True,"obfuscate_booleans":True},
        "encrypt":{"algorithm":"aes-256-gcm","key_source":"auto","interdependency":"chain",
            "backup":True,"backup_max_count":5,"replace_originals":False,
            "shard_count":3,"shard_min_files":2,"compress_level":9,
            "polymorphic_padding":True,"polymorphic_padding_max":512,"aad_context":"S-Protect-PY",
            "extra_layers":[],"hybrid":{},"workers":0},
        "anti_debug":{"enabled":True,"action":"exit",
            "checks":["pdb","ptrace","debugger","vm","sandbox","timing","cuckoo","ida","procmon","gpu"],
            "per_check_actions":[],"process_whitelist":[],"block_tracing":True,
            "timing_threshold":2.0,"exit_code":1,"wipe_memory":True,"corrupt_on_exit":False},
        "virtualization":{"enabled":False,"mode":"partial","functions":[],"glob_patterns":[],
            "exclude_functions":[],"inline_threshold":50,"interpreter_obfuscate":True},
        "watermark":{"enabled":True,"levels":["file","code","runtime"],"batch_id":"",
            "multi_batch":[],"visible":False,"watermark_key":""},
        "expiration":{"enabled":False,"expires_at":None,"grace_period_hours":0,
            "ntp_check":True,"ntp_servers":["pool.ntp.org","time.google.com","time.cloudflare.com","time.windows.com","time.apple.com"],
            "ntp_timeout":3.0,"on_network_fail":"reject","check_interval_hours":24,"max_drift_seconds":3600},
        "environment":{"enabled":False,"bind_env_vars":[],"strict_mode":False,"fingerprint_algorithm":"sha256"},
        "sandbox":{"enabled":True,"detect_cuckoo":True,"detect_sandboxie":True,"detect_docker":False,"detect_ci":False},
        "bootloader":{"name":"main.py","include_runtime_loader":True,"minimal_boot":False,
            "hide_python_windows":False,"anti_dump":True,"periodic_check_interval":5.0},
        "pack":{"enabled":False,"onefile":True,"console":True,"icon":None,"extra_args":[]},
        "project":{"name":"unnamed","version":"1.0.0","entry":"main.py","description":"","author":""},
        "output":{"dir":"./output","keep_source_map":False,"runtime_dir_name":"_runtime","verbose":False}
    }
    p = Path(path); p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(_cfg_raw, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return p
