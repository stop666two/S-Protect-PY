"""Encryption engine: AES-256-GCM primary, HMAC-XOR fallback."""

from __future__ import annotations
import os, hashlib, hmac, json
from sprotect.types import Config
from sprotect.config import merge_file_config
from sprotect.obfuscate import Obfuscator, collect_defs
from sprotect.project import find_py_files
from sprotect.crypto import encrypt_payload as _enc_payload
from sprotect.loader import gen_boot, gen_loader
from sprotect.backup import backup

def build(project_dir: str, output_dir: str, config: Config) -> None:
    py_files = find_py_files(project_dir, config)
    rd = os.path.join(output_dir, "_runtime"); os.makedirs(rd, exist_ok=True)

    shared_map: dict[str, str] = {}
    for fp in py_files:
        try:
            collect_defs(open(fp, encoding="utf-8").read(), config.obfuscate, shared_map)
        except: pass

    per_file_configs: dict[str, str] = {}
    for fp in py_files:
        fc = merge_file_config(config, fp)
        rel = os.path.relpath(fp, project_dir)
        pye = os.path.join(rd, rel.replace(".py", ".pye"))
        os.makedirs(os.path.dirname(pye), exist_ok=True)

        try:
            src = open(fp, encoding="utf-8-sig").read()
            if fc.obfuscate.level.value >= 1:
                src = Obfuscator(fc.obfuscate, shared_map).obfuscate(src)
            payload = _enc_payload(src.encode(), fc.encrypt.algorithm)
            open(pye, "wb").write(payload)
        except Exception as e:
            print(f"  WARN: {rel} - {e}")
            continue

        pfc = fp + ".sprotect.json5"
        if os.path.isfile(pfc):
            dst = os.path.join(os.path.dirname(pye), os.path.basename(pfc))
            per_file_configs[pfc] = dst

    gen_loader(output_dir)
    entry_mod = config.project.entry.replace(".py", "")
    gen_boot(output_dir, entry_mod, per_file_configs)

    for f in ["run.bat", "requirements.txt"]:
        s = os.path.join(project_dir, f)
        if os.path.isfile(s):
            import shutil
            shutil.copy2(s, os.path.join(output_dir, f))
