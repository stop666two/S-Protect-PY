"""JSON5 config loader - full customization."""

from __future__ import annotations
import os, json, dataclasses
from typing import Any, Optional
from pathlib import Path
import json5
from sprotect.types import *

def _te(et, v):
    if isinstance(v, et): return v
    if isinstance(v, str):
        try: return et[v.upper()]
        except KeyError: return et(v)
    if isinstance(v, int): return et(v)
    raise ValueError(f"Invalid {et.__name__}: {v}")

def _rr(d): return RenameRules(
    style=_te(NamingStyle, d.get("style","hex")),
    reserved=d.get("reserved",["__init__","main"]),
    dictionary=d.get("dictionary"), prefix=d.get("prefix","_0x"),
    suffix=d.get("suffix",""), min_length=d.get("min_length",6),
    blacklist=d.get("blacklist",[]))

def _obf(d): return ObfuscateConfig(
    level=_te(ObfuscateLevel, d.get("level",3)),
    rename_variables=d.get("rename_variables",True),
    rename_functions=d.get("rename_functions",True),
    rename_classes=d.get("rename_classes",True),
    rename_rules=_rr(d.get("rename_rules",{})),
    encrypt_strings=d.get("encrypt_strings",True),
    encrypt_numbers=d.get("encrypt_numbers",False),
    string_min_length=d.get("string_min_length",3),
    string_encrypt_ratio=d.get("string_encrypt_ratio",1.0),
    control_flow_flattening=d.get("control_flow_flattening",True),
    dead_code_injection=d.get("dead_code_injection",False),
    dead_code_density=d.get("dead_code_density",0.3),
    opaque_predicate_count=d.get("opaque_predicate_count",2),
    remove_docstrings=d.get("remove_docstrings",False),
    remove_comments=d.get("remove_comments",True),
    strip_blank_lines=d.get("strip_blank_lines",False),
    max_line_length=d.get("max_line_length",0))

def _enc(d): return EncryptConfig(
    algorithm=_te(EncryptAlgorithm, d.get("algorithm","aes-256-gcm")).value,
    key_source=d.get("key_source","auto"),
    key_file=d.get("key_file"), key_env_var=d.get("key_env_var"),
    interdependency=_te(InterdependencyMode, d.get("interdependency","chain")),
    backup=d.get("backup",True), backup_max_count=d.get("backup_max_count",5),
    replace_originals=d.get("replace_originals",False),
    shard_count=d.get("shard_count",3), shard_min_files=d.get("shard_min_files",2),
    compress_level=d.get("compress_level",9),
    polymorphic_padding=d.get("polymorphic_padding",True),
    polymorphic_padding_max=d.get("polymorphic_padding_max",512),
    aad_context=d.get("aad_context","S-Protect-PY"),
    extra_layers=d.get("extra_layers",[]),
    hybrid=_extral_hybrid(d.get("hybrid",{})))

def _adbc(d): return AntiDebugCheckConfig(check=d.get("check",""), enabled=d.get("enabled",True), action=d.get("action"))

def _adb(d): return AntiDebugConfig(
    enabled=d.get("enabled",True),
    action=_te(AntiDebugAction, d.get("action","exit")),
    checks=d.get("checks",["pdb","ptrace","debugger","vm","sandbox","timing","cuckoo","ida","procmon"]),
    per_check_actions=[_adbc(c) for c in d.get("per_check_actions",[])],
    process_whitelist=d.get("process_whitelist",[]),
    block_tracing=d.get("block_tracing",True),
    timing_threshold=d.get("timing_threshold",2.0),
    exit_code=d.get("exit_code",1), wipe_memory=d.get("wipe_memory",True),
    corrupt_on_exit=d.get("corrupt_on_exit",False))

def _virt(d): return VirtualizationConfig(
    enabled=d.get("enabled",False),
    mode=_te(VirtualizationMode, d.get("mode","partial")),
    functions=d.get("functions",[]), glob_patterns=d.get("glob_patterns",[]),
    exclude_functions=d.get("exclude_functions",[]),
    inline_threshold=d.get("inline_threshold",50),
    interpreter_obfuscate=d.get("interpreter_obfuscate",True))

def _wm(d): return WatermarkConfig(
    enabled=d.get("enabled",True),
    levels=[_te(WatermarkLevel, l) for l in d.get("levels",["file","code","runtime"])],
    batch_id=d.get("batch_id",""), custom_template=d.get("custom_template"),
    multi_batch=d.get("multi_batch",[]), visible=d.get("visible",False),
    watermark_key=d.get("watermark_key",""))

def _exp(d): return ExpirationConfig(
    enabled=d.get("enabled",False), expires_at=d.get("expires_at"),
    encrypted_at=d.get("encrypted_at"),
    grace_period_hours=d.get("grace_period_hours",0),
    ntp_check=d.get("ntp_check",True),
    ntp_servers=d.get("ntp_servers",["pool.ntp.org","time.google.com","time.cloudflare.com","time.windows.com","time.apple.com"]),
    ntp_timeout=d.get("ntp_timeout",3.0),
    on_network_fail=d.get("on_network_fail","reject"),
    check_interval_hours=d.get("check_interval_hours",24),
    max_drift_seconds=d.get("max_drift_seconds",3600))

def _env(d): return EnvironmentConfig(
    enabled=d.get("enabled",False), bind_directory=d.get("bind_directory"),
    bind_username=d.get("bind_username"), bind_env_vars=d.get("bind_env_vars",[]),
    bind_file_hash=d.get("bind_file_hash"), bind_mac_address=d.get("bind_mac_address"),
    bind_hardware_id=d.get("bind_hardware_id"), strict_mode=d.get("strict_mode",False),
    fingerprint_algorithm=d.get("fingerprint_algorithm","sha256"))

def _san(d): return SandboxConfig(
    enabled=d.get("enabled",True), detect_cuckoo=d.get("detect_cuckoo",True),
    detect_sandboxie=d.get("detect_sandboxie",True),
    detect_docker=d.get("detect_docker",False), detect_ci=d.get("detect_ci",False))

def _bl(d): return BootloaderConfig(
    name=d.get("name","main.py"),
    include_runtime_loader=d.get("include_runtime_loader",True),
    minimal_boot=d.get("minimal_boot",False), custom_banner=d.get("custom_banner"),
    hide_python_windows=d.get("hide_python_windows",False),
    anti_dump=d.get("anti_dump",True),
    periodic_check_interval=d.get("periodic_check_interval",5.0))

def _proj(d): return ProjectConfig(
    name=d.get("name","unnamed"), version=d.get("version","1.0.0"),
    entry=d.get("entry","main.py"), description=d.get("description",""),
    author=d.get("author",""))

def _out(d): return OutputConfig(
    dir=d.get("dir","./output"), keep_source_map=d.get("keep_source_map",False),
    runtime_dir_name=d.get("runtime_dir_name","_runtime"),
    preserve_non_py=d.get("preserve_non_py",True), verbose=d.get("verbose",False))

def _files(d): return FilesConfig(
    include=d.get("include",["**/*.py"]), exclude=d.get("exclude",[]),
    exclude_dirs=d.get("exclude_dirs",["_runtime","_backup","__pycache__",".git"]))

def _extral_hybrid(d): return HybridEncryptConfig(
    enabled=d.get("enabled",False),
    algorithm=d.get("algorithm","RSA"),
    key_size=d.get("key_size",4096),
    key_file=d.get("key_file","key.pem"))

def _to_cfg(d):
    return Config(
        files=_files(d.get("files",{})),
        obfuscate=_obf(d.get("obfuscate",{})),
        encrypt=_enc(d.get("encrypt",{})),
        anti_debug=_adb(d.get("anti_debug",{})),
        virtualization=_virt(d.get("virtualization",{})),
        watermark=_wm(d.get("watermark",{})),
        expiration=_exp(d.get("expiration",{})),
        environment=_env(d.get("environment",{})),
        sandbox=_san(d.get("sandbox",{})),
        bootloader=_bl(d.get("bootloader",{})),
        project=_proj(d.get("project",{})),
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
        else: r[k] = v
    return r

def merge_file_config(main: Config, py_path: str) -> Config:
    over = load_per_file(py_path)
    if not over: return main
    obf = over.get("obfuscate", {})
    obf.pop("rename_functions", None); obf.pop("rename_classes", None)
    if not obf: over.pop("obfuscate", None)
    return _to_cfg(deep_merge(dataclasses.asdict(main), over))

def gen_default(path: str) -> Path:
    d = {
        "files":{"include":["**/*.py"],"exclude":[],"exclude_dirs":["_runtime","_backup","__pycache__",".git"]},
        "obfuscate":{"level":5,"rename_variables":True,"rename_functions":True,"rename_classes":True,
            "rename_rules":{"style":"hex","reserved":["__init__","main"],"prefix":"_0x","suffix":"","min_length":6,"blacklist":[]},
            "encrypt_strings":True,"encrypt_numbers":False,"string_min_length":3,"string_encrypt_ratio":1.0,
            "control_flow_flattening":True,"dead_code_injection":True,"dead_code_density":0.3,"opaque_predicate_count":2,
            "remove_docstrings":False,"remove_comments":True,"strip_blank_lines":False,"max_line_length":0},
        "encrypt":{"algorithm":"aes-256-gcm","key_source":"auto","interdependency":"chain",
            "backup":True,"backup_max_count":5,"replace_originals":False,
            "shard_count":3,"shard_min_files":2,"compress_level":9,
            "polymorphic_padding":True,"polymorphic_padding_max":512,"aad_context":"S-Protect-PY",
            "extra_layers":[],"hybrid":{}},
        "anti_debug":{"enabled":True,"action":"exit",
            "checks":["pdb","ptrace","debugger","vm","sandbox","timing","cuckoo","ida","procmon"],
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
        "project":{"name":"unnamed","version":"1.0.0","entry":"main.py","description":"","author":""},
        "output":{"dir":"./output","keep_source_map":False,"runtime_dir_name":"_runtime","verbose":False}
    }
    p = Path(path); p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return p
