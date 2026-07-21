"""Encryption: multi-key payloads, decoy files, sharded master key, encrypted loader."""

from __future__ import annotations
import os, json, secrets
from sprotect.types import Config
from sprotect.config import merge_file_config
from sprotect.obfuscate import Obfuscator, collect_defs
from sprotect.project import find_py_files
from sprotect.crypto import aes_key, split_key, chain_hash, encrypt_payload, generate_decoy_payload, sha256, xor_stream, xof_stream
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

    # Two-layer keys
    loader_key = aes_key()
    master_key = aes_key()
    shards = split_key(master_key, len(py_files))
    decoy_count = 2  # 2 decoy keys per payload (k2, k3)

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
            payload_bytes = encrypt_payload(src.encode(), master_key,
                                       config.encrypt.compress_level,
                                       config.encrypt.polymorphic_padding_max, decoy_count)
            p = json.loads(payload_bytes.decode())
            p["k1"] = shards[idx].hex()  # Replace with this file's shard
            # Recompute mixing hash with actual k1
            import hashlib as _hl
            _m = _hl.sha256(bytes.fromhex(p["k1"])).digest()
            for _ki in ["k2","k3"]:
                if _ki in p:
                    _m = bytes(a^b for a,b in zip(_m, _hl.sha256(bytes.fromhex(p[_ki])).digest()))
            p["m"] = _m.hex()
            payload = json.dumps(p, separators=(",", ":")).encode()
            open(pye, "wb").write(payload)
            file_data.append((rel, payload))
        except Exception as e:
            print(f"  WARN: {rel} - {e}"); continue
        pfc = fp + ".sprotect.json5"
        if os.path.isfile(pfc):
            dst = os.path.join(os.path.dirname(pye), os.path.basename(pfc))
            per_file_configs[pfc] = dst

    # Chain signatures
    payloads = [json.loads(d.decode()) for _, d in file_data]
    sigs = chain_hash(payloads, master_key)
    for idx, (rel, _) in enumerate(file_data):
        pye_path = os.path.join(rd, rel.replace(".py", ".pye"))
        p = json.loads(open(pye_path, "rb").read().decode())
        p["c"] = sigs[idx]
        open(pye_path, "wb").write(json.dumps(p, separators=(",", ":")).encode())

    # Inject decoy files (20-50% extra files that look real)
    decoy_count_files = max(1, len(py_files) // 3)
    for i in range(decoy_count_files):
        decoy = generate_decoy_payload(master_key, decoy_count + 1)
        decoy_name = f"_decoy_{secrets.token_hex(4)}.pye"
        with open(os.path.join(rd, decoy_name), "wb") as f:
            f.write(decoy)

    # Encrypt loader
    loader_src = gen_loader_source()
    from sprotect.crypto import encrypt_payload as _ep
    compressed = __import__("zlib").compress(loader_src.encode(), level=9)
    from sprotect.crypto import xor_stream as _xs
    xored = _xs(compressed, loader_key)
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    nonce = os.urandom(12)
    ct = nonce + AESGCM(loader_key).encrypt(nonce, xored, b"")
    from sprotect.crypto import sha256 as _sh
    import hashlib as _hl
    lk1 = loader_key; lk2 = os.urandom(32); lk3 = os.urandom(32)
    lm = _hl.sha256(lk1).digest()
    lm = bytes(a^b for a,b in zip(lm, _hl.sha256(lk2).digest()))
    lm = bytes(a^b for a,b in zip(lm, _hl.sha256(lk3).digest()))
    loader_payload = json.dumps({"v":4,"d":ct.hex(),"h":_sh(loader_src.encode()),
                                  "k1":lk1.hex(),"k2":lk2.hex(),
                                  "k3":lk3.hex(),"m":lm.hex()},
                                 separators=(",",":")).encode()
    open(os.path.join(rd, "loader.pye"), "wb").write(loader_payload)

    # Generate bootloader
    entry_mod = config.project.entry.replace(".py", "")
    gen_boot(output_dir, entry_mod, per_file_configs, loader_key)

    for f in ["run.bat", "requirements.txt"]:
        s = os.path.join(project_dir, f)
        if os.path.isfile(s):
            import shutil; shutil.copy2(s, os.path.join(output_dir, f))
