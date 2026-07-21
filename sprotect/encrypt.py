"""Encryption: two-layer keys + cross-file sharding + encrypted loader."""

from __future__ import annotations
import os, json
from sprotect.types import Config
from sprotect.config import merge_file_config
from sprotect.obfuscate import Obfuscator, collect_defs
from sprotect.project import find_py_files
from sprotect.crypto import aes_key, split_key, chain_hash, encrypt_payload, encrypt_loader, sha256
from sprotect.loader import gen_boot, gen_loader_source
from sprotect.backup import backup


def build(project_dir: str, output_dir: str, config: Config) -> None:
    py_files = find_py_files(project_dir, config)
    if not py_files:
        print("  WARN: no Python files found"); return

    rd = os.path.join(output_dir, config.output.runtime_dir_name)
    os.makedirs(rd, exist_ok=True)

    # Shared rename map
    shared_map: dict[str, str] = {}
    for fp in py_files:
        try: collect_defs(open(fp, encoding="utf-8-sig").read(), config.obfuscate, shared_map)
        except: pass

    # Layer 1: Loader key (stored in bootloader, only decrypts loader.pye)
    loader_key = aes_key()
    # Layer 2: Master key (split across ALL .pye files, decrypts program code)
    master_key = aes_key()
    shards = split_key(master_key, len(py_files))

    file_data: list[tuple[str, bytes]] = []
    per_file_configs: dict[str, str] = {}

    for idx, fp in enumerate(py_files):
        fc = merge_file_config(config, fp)
        rel = os.path.relpath(fp, project_dir)
        pye = os.path.join(rd, rel.replace(".py", ".pye"))
        os.makedirs(os.path.dirname(pye), exist_ok=True)
        try:
            src = open(fp, encoding="utf-8-sig").read()
            if fc.obfuscate.level.value >= 1:
                src = Obfuscator(fc.obfuscate, shared_map).obfuscate(src)
            # Encrypt with MASTER KEY, but store ONE SHARD in payload
            # All shards needed to reconstruct master key
            payload = encrypt_payload(src.encode(), master_key, "",
                                       config.encrypt.compress_level,
                                       config.encrypt.polymorphic_padding_max)
            # Replace the key in payload with this file's shard
            p = json.loads(payload.decode())
            p["s"] = shards[idx].hex()
            payload = json.dumps(p, separators=(",", ":")).encode()
            open(pye, "wb").write(payload)
            file_data.append((rel, payload))
        except Exception as e:
            print(f"  WARN: {rel} - {e}"); continue
        pfc = fp + ".sprotect.json5"
        if os.path.isfile(pfc):
            dst = os.path.join(os.path.dirname(pye), os.path.basename(pfc))
            per_file_configs[pfc] = dst

    # Chain signatures (using master key, based on encrypted data "d" field)
    payloads = [json.loads(d.decode()) for _, d in file_data]
    sigs = chain_hash(payloads, master_key)
    for idx, (rel, _) in enumerate(file_data):
        pye_path = os.path.join(rd, rel.replace(".py", ".pye"))
        p = json.loads(open(pye_path, "rb").read().decode())
        p["c"] = sigs[idx]
        open(pye_path, "wb").write(json.dumps(p, separators=(",", ":")).encode())

    # Encrypt loader with loader_key (NOT master_key)
    loader_src = gen_loader_source()
    enc = encrypt_loader(loader_src, loader_key)
    open(os.path.join(rd, "loader.pye"), "wb").write(enc)

    # Generate bootloader (only has loader_key, NOT master_key)
    entry_mod = config.project.entry.replace(".py", "")
    gen_boot(output_dir, entry_mod, per_file_configs, loader_key)

    for f in ["run.bat", "requirements.txt"]:
        s = os.path.join(project_dir, f)
        if os.path.isfile(s):
            import shutil; shutil.copy2(s, os.path.join(output_dir, f))
