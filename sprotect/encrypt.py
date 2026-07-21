"""Encryption: external libs (PyArmor/PyCryptodome/blake3), random build artifacts."""

from __future__ import annotations
import os, json, secrets, hashlib, hmac, zlib, subprocess, sys
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from sprotect.types import Config
from sprotect.config import merge_file_config
from sprotect.obfuscate import Obfuscator, collect_defs
from sprotect.project import find_py_files
from sprotect.crypto import aes_key, split_key, chain_hash, encrypt_payload, generate_decoy_payload
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

    # Keys
    loader_key = aes_key()
    master_key = aes_key()
    shards = split_key(master_key, len(py_files))

    # Build module map
    module_map: dict[str, str] = {}
    file_data: list[tuple[str, bytes]] = []
    per_file_configs: dict[str, str] = {}

    for idx, fp in enumerate(py_files):
        fc = merge_file_config(config, fp)
        rel = os.path.relpath(fp, project_dir)
        rel = rel.replace("\\", "/")
        mod_name = rel.replace(".py", "").replace("/", ".")
        if mod_name.endswith(".__init__"):
            mod_name = mod_name[:-9]
        hex_name = secrets.token_hex(6)

        try:
            src = open(fp, encoding="utf-8-sig").read()
            if fc.obfuscate.level.value >= 1:
                src = Obfuscator(fc.obfuscate, shared_map).obfuscate(src)

            payload_bytes = encrypt_payload(src.encode(), master_key,
                                       config.encrypt.compress_level,
                                       config.encrypt.polymorphic_padding_max)
            p = json.loads(payload_bytes.decode())
            # k1-k5: overwrite keys + fingerprints after encryption
            kpos = secrets.randbelow(5)
            keys = [os.urandom(32) for _ in range(5)]
            keys[kpos] = shards[idx]
            for i, kv in enumerate(keys):
                p[f"k{i+1}"] = kv.hex()
            xored = bytearray(32)
            for kb in keys:
                for i in range(min(32, len(kb))): xored[i] ^= kb[i]
            p["f1"] = hashlib.sha256(bytes(xored)).hexdigest()[5:13]
            try:
                import blake3; p["f2"] = blake3.blake3(shards[idx]).hexdigest()[3:11]
            except:
                p["f2"] = hashlib.sha256(shards[idx]).hexdigest()[3:11]
            try: p["f3"] = hmac.new(shards[idx], b"S-Protect-v6-key-verify", "sha256").hexdigest()[:8]
            except: p["f3"] = ""
            payload = json.dumps(p, separators=(",", ":")).encode()

            pye_path = os.path.join(rd, hex_name + ".pye")
            with open(pye_path, "wb") as f: f.write(payload)
            module_map[mod_name] = hex_name
            file_data.append((rel, payload))
        except Exception as e:
            print(f"  WARN: {rel} - {e}"); continue
        pfc = fp + ".sprotect.json5"
        if os.path.isfile(pfc):
            dst = os.path.join(rd, f"{hex_name}.sprotect.json5")
            import shutil; shutil.copy2(pfc, dst)

    # Build integrity database for anti-tamper
    integrity_db = {}
    for (rel, _) in [(fp, "") for fp in py_files]:
        mod_name = os.path.relpath(fp, project_dir).replace("\\", "/")
        mod_name = mod_name.replace(".py", "").replace("/", ".")
        if mod_name.endswith(".__init__"): mod_name = mod_name[:-9]
        hex_n = module_map.get(mod_name, "")
        if not hex_n: continue
        pye_path = os.path.join(rd, hex_n + ".pye")
        if os.path.isfile(pye_path):
            h = hashlib.sha256(open(pye_path, "rb").read()).hexdigest()
            integrity_db[hex_n + ".pye"] = h
    
    # Chain signatures
    payloads = [json.loads(d.decode()) for _, d in file_data]
    sigs = chain_hash(payloads, master_key)
    for idx, (rel, _) in enumerate(file_data):
        mod_name = rel.replace(".py", "").replace("/", ".")
        if mod_name.endswith(".__init__"): mod_name = mod_name[:-9]
        hex_n = module_map.get(mod_name, "")
        if not hex_n: continue
        pye_path = os.path.join(rd, hex_n + ".pye")
        p = json.loads(open(pye_path, "rb").read().decode())
        p["c"] = sigs[idx]
        open(pye_path, "wb").write(json.dumps(p, separators=(",", ":")).encode())

    # Decoy files
    from sprotect.crypto import generate_decoy_payload as _gdp
    dc = max(1, len(py_files) // 3)
    for i in range(dc):
        decoy = _gdp()
        dp = json.loads(decoy.decode())
        dp["c"] = os.urandom(32).hex()
        decoy = json.dumps(dp, separators=(",", ":")).encode()
        dn = secrets.token_hex(6) + ".pye"
        with open(os.path.join(rd, dn), "wb") as f: f.write(decoy)
        if i % 2 == 0:
            sub = secrets.token_hex(4)
            os.makedirs(os.path.join(rd, sub), exist_ok=True)
            for _ in range(2):
                sn = secrets.token_hex(6) + ".pye"
                with open(os.path.join(rd, sub, sn), "wb") as f:
                    f.write(_gdp())

    # Build loader with embedded module map
    map_json = json.dumps(module_map, separators=(",", ":"))
    loader_src = gen_loader_source()
    # Map is in JSON format, embedded via _MAP variable
    import json as _js
    escaped_map = _js.dumps(map_json)
    loader_src = loader_src.replace('_MAP = ""', f"_MAP = {escaped_map}")

    # Encrypt loader
    compressed = zlib.compress(loader_src.encode(), 9)
    from sprotect.crypto import xor_stream as _xs
    xored = _xs(compressed, loader_key)
    nonce = os.urandom(12)
    ct = nonce + AESGCM(loader_key).encrypt(nonce, xored, b"")
    # Use make_keys_complex for loader.pye too
    from sprotect.crypto import make_keys_complex as _mkc
    keys3, _ = _mkc(loader_key, 2)
    loader_payload = {"v": 7, "d": ct.hex(), "k1": loader_key.hex(),
                       "k2": os.urandom(32).hex(), "k3": os.urandom(32).hex(),
                       "f1": keys3["f1"], "f2": keys3["f2"], "f3": keys3["f3"]}
    open(os.path.join(rd, "loader.pye"), "wb").write(
        json.dumps(loader_payload, separators=(",", ":")).encode())

    # Bootloader
    entry_mod = config.project.entry.replace(".py", "")
    entry_hex = module_map.get(entry_mod, "")
    gen_boot(output_dir, entry_mod, entry_hex, per_file_configs, loader_key)

    # Copy non-py files
    for f in ["run.bat", "requirements.txt"]:
        s = os.path.join(project_dir, f)
        if os.path.isfile(s):
            import shutil; shutil.copy2(s, os.path.join(output_dir, f))

