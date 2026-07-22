"""Encryption: integrated watermark, expiration, anti-tamper."""
from __future__ import annotations
import os, json, secrets, hashlib, hmac, zlib
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from sprotect.types import Config
from sprotect.config import merge_file_config
from sprotect.obfuscate import Obfuscator, collect_defs
from sprotect.project import find_py_files
from sprotect.crypto import aes_key, split_key, chain_hash, encrypt_payload, encrypt_payload_v2, generate_decoy_payload, rsa_generate_keypair, rsa_encrypt_master_key, ecc_generate_keypair, ecc_encrypt_master_key
from sprotect.loader import gen_boot, gen_loader_source
from sprotect.backup import backup
from sprotect.minify import minify_source


def _extract_d(pye_bytes: bytes) -> tuple[str, dict]:
    try:
        p = json.loads(pye_bytes.decode())
        return p.get("d", ""), p
    except (json.JSONDecodeError, UnicodeDecodeError):
        return "", {}


def build(project_dir, output_dir, config):
    """Build encrypted project: obfuscate, encrypt, generate boot loader."""
    if os.path.isdir(output_dir) and os.listdir(output_dir):
        print(f"  ERROR: 输出目录不为空: {os.path.abspath(output_dir)}")
        print(f"  请先清理该目录再构建:")
        print(f"    Remove-Item -Recurse -Force '{os.path.abspath(output_dir)}'")
        print(f"  或手动删除 {output_dir} 下的所有文件")
        return
    py_files = find_py_files(project_dir, config)
    if not py_files:
        print("  WARN: no Python files found"); return
    helper_created = False
    if len(py_files) < 2:
        print("  WARN: only 1 file found, creating companion module for sharding")
        helper = os.path.join(project_dir, "_sprotect_helper.py")
        with open(helper, "w") as f: f.write("# S-Protect shard helper\n")
        py_files.append(helper)
        helper_created = True

    helper_created = False
    rd = os.path.join(output_dir, "_runtime")
    os.makedirs(rd, exist_ok=True)

    shared_map = {}
    shared_params: set[str] = set()
    for fp in py_files:
        try:
            collect_defs(open(fp, encoding="utf-8-sig").read(), config.obfuscate,
                         shared_map, shared_params)
        except: pass

    from sprotect.watermark import Watermark
    wm = Watermark(config.watermark) if config.watermark.enabled else None

    loader_key = aes_key()
    master_key = aes_key()
    hybrid_key = None
    if config.encrypt.hybrid.enabled:
        hc = config.encrypt.hybrid
        if hc.algorithm == "RSA":
            pub, priv = rsa_generate_keypair(hc.key_size)
        elif hc.algorithm == "ECC":
            curve = f"P-{hc.key_size}" if hc.key_size <= 521 else "P-256"
            pub, priv = ecc_generate_keypair(curve)
        else:
            pub, priv = rsa_generate_keypair(hc.key_size)
        key_path = os.path.join(output_dir, hc.key_file)
        with open(key_path, "wb") as f:
            f.write(priv)
        print(f"  Private key saved: {key_path}")
        if hc.algorithm == "RSA":
            hybrid_key = rsa_encrypt_master_key(master_key, pub)
        else:
            hybrid_key = ecc_encrypt_master_key(master_key, pub)
    shards = split_key(master_key, len(py_files))

    module_map: dict[str, str] = {}
    raw_payloads: list[bytes] = []
    results: list[tuple[str, str, bytes] | None] = [None] * len(py_files)

    def _process_one(idx: int, fp: str) -> tuple[str, str, bytes] | None:
        """Process a single file: obfuscate, encrypt, write .pye."""
        fc = merge_file_config(config, fp)
        rel = os.path.relpath(fp, project_dir).replace("\\", "/")
        mod_name = rel.replace(".py", "").replace("/", ".")
        if mod_name.endswith(".__init__"): mod_name = mod_name[:-9]
        hex_name = secrets.token_hex(6)
        try:
            src = open(fp, encoding="utf-8-sig").read()
            if fc.obfuscate.level.value >= 1:
                src = Obfuscator(fc.obfuscate, shared_map, shared_params).obfuscate(src)
            if wm: src = wm.code(src)
            extra = fc.encrypt.extra_layers or []
            if extra:
                ct, hdr = encrypt_payload_v2(src.encode(), master_key, extra,
                                             config.encrypt.compress_level)
                hdr_json = json.dumps(hdr, separators=(",", ":"))
                payload_bytes = json.dumps({"v":2,"h":hdr_json,"d":ct.hex()},
                                           separators=(",", ":")).encode()
            else:
                payload_bytes = encrypt_payload(src.encode(), master_key,
                                           config.encrypt.compress_level,
                                           config.encrypt.polymorphic_padding_max)
            p = json.loads(payload_bytes.decode())
            from sprotect.crypto import make_keys_complex
            keys_dict, _ = make_keys_complex(shards[idx], 4)
            p.update(keys_dict)
            if wm: p["wm"] = wm.file_payload()
            payload = json.dumps(p, separators=(",", ":")).encode()
            pye_path = os.path.join(rd, hex_name + ".pye")
            with open(pye_path, "wb") as f: f.write(payload)
            return mod_name, hex_name, payload
        except Exception as e:
            print(f"  WARN: {rel} - {e}")
            return None

    workers = config.encrypt.workers or os.cpu_count() or 1
    if workers > 1 and len(py_files) > 1:
        with ThreadPoolExecutor(max_workers=workers) as pool:
            fut_map = {pool.submit(_process_one, i, fp): i for i, fp in enumerate(py_files)}
            for fut in as_completed(fut_map):
                i = fut_map[fut]
                results[i] = fut.result()
    else:
        for i, fp in enumerate(py_files):
            results[i] = _process_one(i, fp)

    failed = sum(1 for r in results if r is None)
    if failed:
        print(f"  ERROR: {failed}/{len(py_files)} files failed to encrypt")
        if failed == len(py_files):
            raise RuntimeError("All files failed to encrypt")
    for r in results:
        if r:
            mod_name, hex_name, payload = r
            module_map[mod_name] = hex_name
            raw_payloads.append(payload)

    sigs = chain_hash(raw_payloads, master_key)
    for idx, (rel, _) in enumerate([(fp, "") for fp in py_files]):
        mod_name = os.path.relpath(fp, project_dir).replace("\\", "/")
        mod_name = mod_name.replace(".py", "").replace("/", ".")
        if mod_name.endswith(".__init__"): mod_name = mod_name[:-9]
        hex_n = module_map.get(mod_name, "")
        if not hex_n: continue
        pye_path = os.path.join(rd, hex_n + ".pye")
        raw = open(pye_path, "rb").read()
        p2 = json.loads(raw.decode())
        p2["c"] = sigs[idx]
        open(pye_path, "wb").write(json.dumps(p2, separators=(",", ":")).encode())

    for i in range(max(2, len(py_files) // 2)):
        decoy = generate_decoy_payload()
        dn = secrets.token_hex(6) + ".pye"
        with open(os.path.join(rd, dn), "wb") as f: f.write(decoy)
        if i % 2 == 0:
            sub = secrets.token_hex(4)
            os.makedirs(os.path.join(rd, sub), exist_ok=True)
            for _ in range(2):
                sn = secrets.token_hex(6) + ".pye"
                with open(os.path.join(rd, sub, sn), "wb") as f:
                    f.write(generate_decoy_payload())

    map_json = json.dumps(module_map, separators=(",", ":"))
    loader_src = gen_loader_source()
    escaped = json.dumps(map_json)
    loader_src = loader_src.replace('_MAP = ""', f"_MAP = {escaped}")
    loader_src = minify_source(loader_src, add_garbage=True)

    compressed = zlib.compress(loader_src.encode(), 9)
    from sprotect.crypto import xor_stream as _xs
    xored = _xs(compressed, loader_key)
    nonce = os.urandom(12)
    ct = nonce + AESGCM(loader_key).encrypt(nonce, xored, b"")
    lkeys = [os.urandom(32) for _ in range(5)]
    lkpos = secrets.randbelow(5)
    lkeys[lkpos] = loader_key
    lflags = (lkpos << 3) | (secrets.randbelow(8) << 6)
    loader_payload = {"v":7,"d":ct.hex(),"l":lflags,"k1":lkeys[0].hex(),"k2":lkeys[1].hex(),
                       "k3":lkeys[2].hex(),"k4":lkeys[3].hex(),"k5":lkeys[4].hex(),
                       "f1":"","f2":"","f3":""}
    open(os.path.join(rd, "loader.pye"), "wb").write(
        json.dumps(loader_payload, separators=(",", ":")).encode())

    # Watermark report
    if wm:
        try:
            records = []
            for r, _, fs in os.walk(rd):
                for f in sorted(fs):
                    if f.endswith(".pye"):
                        fp = os.path.join(r, f)
                        try:
                            pp = json.loads(open(fp, "rb").read().decode())
                            w = pp.get("wm")
                            if w: records.append({"file": f, "bid": w.get("bid",""),
                                                   "ts": w.get("ts",""), "sig": w.get("sig",""),
                                                   "auth": w.get("auth","")})
                        except: pass
            report = {"generated": datetime.now(timezone.utc).isoformat(),
                       "project": config.project.name, "total": len(records),
                       "batch_id": wm.bid if wm else "",
                       "records": records}
            rpath = os.path.join(output_dir, "watermark_report.json")
            with open(rpath, "w", encoding="utf-8") as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            print(f"  Watermark report: {rpath}")
            print(f"  Batch ID: {wm.bid}")
        except Exception as e:
            print(f"  Watermark report: {e}")

    if helper_created:
        try: os.remove(helper)
        except OSError: pass

    entry_mod = config.project.entry.replace(".py", "")
    entry_hex = module_map.get(entry_mod, "")
    hc = config.encrypt.hybrid
    gen_boot(output_dir, entry_mod, entry_hex, {}, loader_key, hybrid_key, hc.algorithm if hybrid_key else "RSA")

    for f in ["run.bat", "requirements.txt"]:
        s = os.path.join(project_dir, f)
        if os.path.isfile(s):
            import shutil; shutil.copy2(s, os.path.join(output_dir, f))
