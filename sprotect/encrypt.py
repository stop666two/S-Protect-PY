"""Encryption: random hex names, module map, mixed real/decoy keys."""

from __future__ import annotations
import os, json, secrets, hashlib, zlib
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from sprotect.types import Config
from sprotect.config import merge_file_config
from sprotect.obfuscate import Obfuscator, collect_defs
from sprotect.project import find_py_files
from sprotect.crypto import aes_key, split_key, chain_hash, encrypt_payload, generate_decoy_payload, fp as key_fingerprint
from sprotect.loader import gen_boot, gen_loader_source
from sprotect.backup import backup


def encrypt_loader(loader_src: str, loader_key: bytes) -> str:
    """Encrypt loader source and return encoded module map + encrypted payload."""
    compressed = zlib.compress(loader_src.encode(), level=9)
    from sprotect.crypto import xor_stream as _xs
    xored = _xs(compressed, loader_key)
    nonce = os.urandom(12)
    ct = nonce + AESGCM(loader_key).encrypt(nonce, xored, b"")
    return json.dumps({"v":6,"d":ct.hex(),"k1":loader_key.hex(),"k2":os.urandom(32).hex(),
                        "k3":os.urandom(32).hex(),"f1":key_fingerprint(loader_key),
                        "f2":key_fingerprint(os.urandom(32)),"f3":key_fingerprint(os.urandom(32))},
                       separators=(",",":"))


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

    # Build module map: module_name -> random hex filename
    module_map: dict[str, str] = {}
    file_data: list[tuple[str, bytes]] = []
    per_file_configs: dict[str, str] = {}

    for idx, fp in enumerate(py_files):
        fc = merge_file_config(config, fp)
        rel = os.path.relpath(fp, project_dir)
        mod_name = rel.replace(".py", "").replace("\\", "/").replace("/", ".")
        if mod_name.endswith(".__init__"):
            mod_name = mod_name[:-9]  # helpers.__init__ -> helpers
        hex_name = secrets.token_hex(6)  # 12-char random name

        try:
            src = open(fp, encoding="utf-8-sig").read()
            if fc.obfuscate.level.value >= 1:
                src = Obfuscator(fc.obfuscate, shared_map).obfuscate(src)

            payload_bytes = encrypt_payload(src.encode(), master_key,
                                       config.encrypt.compress_level,
                                       config.encrypt.polymorphic_padding_max)
            p = json.loads(payload_bytes.decode())
            p["k1"] = shards[idx].hex()
            # Recompute fingerprints to match this file's k1
            f1 = key_fingerprint(shards[idx])
            f2 = key_fingerprint(os.urandom(32))
            f3 = key_fingerprint(os.urandom(32))
            pos = secrets.randbelow(3)
            fps = [f1, f2, f3]
            fps[0], fps[pos] = fps[pos], fps[0]
            p["f1"], p["f2"], p["f3"] = fps
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

    # Chain signatures
    payloads = [json.loads(d.decode()) for _, d in file_data]
    sigs = chain_hash(payloads, master_key)
    for idx, (rel, _) in enumerate(file_data):
        mod_name = rel.replace(".py", "").replace("\\", "/").replace("/", ".")
        if mod_name.endswith(".__init__"):
            mod_name = mod_name[:-9]
        hex_n = module_map[mod_name]
        pye_path = os.path.join(rd, hex_n + ".pye")
        p = json.loads(open(pye_path, "rb").read().decode())
        p["c"] = sigs[idx]
        open(pye_path, "wb").write(json.dumps(p, separators=(",", ":")).encode())

    # Inject decoy files (SAME random hex format)
    from sprotect.crypto import generate_decoy_payload as _gdp
    import secrets as _sec
    decoy_count = max(1, len(py_files) // 3)
    for i in range(decoy_count):
        decoy = _gdp()
        # Give decoys random chain sigs that look real but won't verify
        d_p = json.loads(decoy.decode())
        d_p["c"] = os.urandom(32).hex()
        decoy = json.dumps(d_p, separators=(",", ":")).encode()
        dn = _sec.token_hex(6) + ".pye"
        with open(os.path.join(rd, dn), "wb") as f: f.write(decoy)
        # Subdirectory decoys
        if i % 2 == 0:
            sub = _sec.token_hex(4)
            os.makedirs(os.path.join(rd, sub), exist_ok=True)
            for _ in range(2):
                sn = _sec.token_hex(6) + ".pye"
                with open(os.path.join(rd, sub, sn), "wb") as f:
                    f.write(_gdp())

    # Encrypt module map and embed in loader
    map_json = json.dumps(module_map, separators=(",", ":"))
    map_encrypted = encrypt_loader(map_json, loader_key)
    # Embed map into loader source
    loader_src = gen_loader_source()
    import json as _json
    escaped = _json.dumps(map_encrypted)  # JSON string properly escaped for Python
    loader_src = loader_src.replace('_MAP_ENCRYPTED = ""', f"_MAP_ENCRYPTED = {escaped}")

    # Encrypt loader
    encrypted_loader = encrypt_loader(loader_src, loader_key)
    open(os.path.join(rd, "loader.pye"), "wb").write(encrypted_loader.encode())

    # Bootloader
    entry_mod = config.project.entry.replace(".py", "")
    entry_hex = module_map.get(entry_mod, "")
    gen_boot(output_dir, entry_mod, entry_hex, per_file_configs, loader_key)

    for f in ["run.bat", "requirements.txt"]:
        s = os.path.join(project_dir, f)
        if os.path.isfile(s):
            import shutil; shutil.copy2(s, os.path.join(output_dir, f))
