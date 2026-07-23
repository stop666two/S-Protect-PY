# BUILD ENGINE: project compilation pipeline
# STAGES: collect->obfuscate->encrypt->assemble->deploy
"""Encryption: integrated watermark, expiration, anti-tamper."""
from __future__ import annotations
import os, json, secrets, hashlib, hmac, zlib
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from sprotect.types import Config
from sprotect.config import merge_file_config
from sprotect.obfuscate import Obfuscator, collect_defs
from sprotect.project import find_py_files, copy_non_py_files
from sprotect.virtualize import virtualize_source
from sprotect.crypto import aes_key, split_key, shamir_split, chain_hash, encrypt_payload, encrypt_payload_v2, generate_decoy_payload, rsa_generate_keypair, rsa_encrypt_master_key, ecc_generate_keypair, ecc_encrypt_master_key
from sprotect.loader import gen_boot, gen_loader_source
from sprotect.backup import backup
from sprotect.minify import minify_source
from sprotect.keyvault import generate_vault, KeyVaultConfig, VaultData
from sprotect.compressor import compress as _compress


def _parse_watermark_dict(_pye_bytes: bytes) -> tuple[str, dict]:
    try:
        _pkg_data = json.loads(_pye_bytes.decode())
        return _pkg_data.get("d", ""), _pkg_data
    except (json.JSONDecodeError, UnicodeDecodeError):
        return "", {}


def _generate_decoy_file() -> str:
    """Generate a valid Python file with real-looking code for decoy purposes."""
    import random
    rng = random.Random(secrets.randbits(32))
    funcs = []
    for _ in range(rng.randint(2, 5)):
        fn = f"_d{secrets.token_hex(4)}"
        ops = [
            f"    return sum(range({rng.randint(10, 100)}))",
            f"    x = hashlib.sha256(b'{secrets.token_hex(8)}').hexdigest()\n    return x[:{rng.randint(4, 12)}]",
            f"    return [{rng.randint(1, 99)} * i for i in range({rng.randint(3, 10)})]",
            f"    return os.path.basename(__file__) if os.path.isfile(__file__) else '{secrets.token_hex(4)}'",
        ]
        body = rng.choice(ops)
        funcs.append(f"def {fn}({rng.choice(['x', 'n', 'val', 'data', 'key'])}):\n{body}")
    src = "import hashlib, os, sys, json, base64\n\n"
    src += "\n\n".join(funcs)
    src += f"\n\n# {secrets.token_hex(16)}\n# TODO: {secrets.token_hex(8)}\n"
    if rng.random() < 0.3:
        src += f"\ndef main():\n    return {rng.randint(1, 9)} * {rng.randint(1, 9)}\n"
    if rng.random() < 0.3:
        src += f"\nif __name__ == '__main__':\n    main()\n"
    return src


def _build_layers(final_source: str | bytes, master_key: bytes, layer_count: int = 6) -> bytes:
    """Wrap source in N encrypted layers with post-layer obfuscation.
    Each layer's decryption code has variables renamed and comments stripped.
    Master key is used as the outermost layer key; inner layers use random keys.
    Accepts str or bytes; if str, encodes to UTF-8 first."""
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    import secrets, json, zlib, base64

    current = final_source.encode() if isinstance(final_source, str) else final_source

    for i in range(layer_count):
        key = secrets.token_bytes(32) if i < layer_count - 1 else master_key
        nonce = secrets.token_bytes(12)
        ct = nonce + AESGCM(key).encrypt(nonce, current, b"")

        if i < layer_count - 1:
            _lk = key.hex()
            _ld = ct.hex()
            raw_json = json.dumps({"k": _lk, "d": _ld}, separators=(",", ":"))
            _b64 = base64.urlsafe_b64encode(raw_json.encode()).decode().rstrip("=")
            _fake_var = "_" + secrets.token_hex(4)
            layer_code = f"{_fake_var}='{_b64}'"
            current = layer_code.encode()
        else:
            current = ct

    return current


def build(project_dir, output_dir, config):
    """Build encrypted project: obfuscate, encrypt, generate boot loader."""
    if os.path.isdir(output_dir) and os.listdir(output_dir):
        print(f"  WARN: 输出目录不为空，将覆盖现有文件: {os.path.abspath(output_dir)}")
    py_files = find_py_files(project_dir, config)
    if not py_files:
        print("  WARN: no Python files found"); return
    _decoy_count = 0
    _MIN_REAL_DECOYS = 10
    if len(py_files) < _MIN_REAL_DECOYS:
        _needed = _MIN_REAL_DECOYS - len(py_files) + secrets.randbelow(6)
        _decoy_dir = os.path.join(project_dir, "_decoy_modules")
        os.makedirs(_decoy_dir, exist_ok=True)
        for i in range(_needed):
            _dn = f"decoy_module_{secrets.token_hex(4)}.py"
            _df = _generate_decoy_file()
            with open(os.path.join(_decoy_dir, _dn), "w", encoding="utf-8") as _fh:
                _fh.write(_df)
            py_files.append(os.path.join(_decoy_dir, _dn))
            _decoy_count += 1
        py_files.sort()
        if _decoy_count:
            print(f"  Generated {_decoy_count} decoy modules (anti-crack defense)")
    _helper_generated = False
    if len(py_files) < 2:
        print("  WARN: only 1 file found, creating companion module for sharding")
        _shard_helper_path = os.path.join(project_dir, "_sprotect_helper.py")
        with open(_shard_helper_path, "w") as f: f.write("# S-Protect shard helper\n")
        py_files.append(_shard_helper_path)
        _helper_generated = True
    _runtime_dir = os.path.join(output_dir, "_runtime")
    os.makedirs(_runtime_dir, exist_ok=True)

    _global_rename_map = {}
    _global_param_set: set[str] = set()
    _global_import_set: set[str] = set()
    for fp in py_files:
        try:
            collect_defs(open(fp, encoding="utf-8-sig").read(), config.obfuscate,
                         _global_rename_map, _global_param_set, _global_import_set)
        except: pass

    from sprotect.watermark import Watermark
    _watermark_engine = Watermark(config.watermark) if config.watermark.enabled else None

    _loader_build_salt = secrets.token_hex(32)
    _loader_cipher_key = hmac.new(
        bytes.fromhex(_loader_build_salt),
        b"sprotect-loader-key-v1",
        hashlib.sha256
    ).digest()
    _master_cipher_key = aes_key()
    _hybrid_wrapped_key = None
    if config.encrypt.hybrid.enabled:
        _hybrid_cfg = config.encrypt.hybrid
        if _hybrid_cfg.algorithm == "RSA":
            _public_key, _private_key = rsa_generate_keypair(_hybrid_cfg.key_size)
        elif _hybrid_cfg.algorithm == "ECC":
            curve = f"P-{_hybrid_cfg.key_size}" if _hybrid_cfg.key_size <= 521 else "P-256"
            _public_key, _private_key = ecc_generate_keypair(curve)
        else:
            _public_key, _private_key = rsa_generate_keypair(_hybrid_cfg.key_size)
        _key_file_path = os.path.join(output_dir, _hybrid_cfg.key_file)
        with open(_key_file_path, "wb") as f:
            f.write(_private_key)
        # Split private key into hash-chained Shamir shards, random names/sizes
        _key_shard_dir = os.path.join(output_dir, "_ks" + secrets.token_hex(4))
        os.makedirs(_key_shard_dir, exist_ok=True)
        _key_data = _private_key
        _shard_n = 24
        _shard_t = 12
        _key_shards = shamir_split(_key_data, _shard_n, _shard_t)
        _ext_pool = [".dat", ".bin", ".cfg", ".tmp", ".log", ".idx", ".map",
                     ".sig", ".key", ".bak", ".old", ".res", ".enc", ".raw",
                     ".pyd", ".so", ".cache", ".blob", ".seg", ".part"]
        _real_shards = []
        _rng = __import__("random").Random(secrets.randbits(32))
        for (_sid, _sval) in _key_shards:
            _pad = os.urandom(_rng.randint(16, 256))
            _sval_padded = _sval + _pad
            _ext = _rng.choice(_ext_pool)
            _name = f"{secrets.token_hex(4)}{_ext}"
            _real_shards.append((_sid, _sval_padded, _name))
        # Build hash chain: each shard's SHA256 is included in the next
        _chain = []
        for i, (_sid, _data, _name) in enumerate(_real_shards):
            _h = hashlib.sha256(_data).hexdigest()
            _chain.append(_h)
        # Embed hash chain into each shard (last contains first)
        for i, (_sid, _data, _name) in enumerate(_real_shards):
            _prev_hash = _chain[i - 1].encode()
            _next_hash = _chain[(i + 1) % _shard_n].encode()
            _manifest = f"{_prev_hash.hex()}:{_next_hash.hex()}:{_shard_n}:{_shard_t}".encode()
            _final = _manifest + b"||" + _data
            with open(os.path.join(_key_shard_dir, _name), "wb") as _sf:
                _sf.write(_final)
        # Generate decoy files to blend in
        for _ in range(_rng.randint(15, 30)):
            _dummy = os.urandom(_rng.randint(32, 512))
            _dname = f"{secrets.token_hex(4)}{_rng.choice(_ext_pool)}"
            with open(os.path.join(_key_shard_dir, _dname), "wb") as _df:
                _df.write(_dummy)
        # Remove original unsplit key
        os.remove(_key_file_path)
        print(f"  Private key: {_shard_n} hash-chained shards (need {_shard_t})")
        print(f"  Location: {_key_shard_dir}/ ({len(os.listdir(_key_shard_dir))} files total)")
        if _hybrid_cfg.algorithm == "RSA":
            _hybrid_wrapped_key = rsa_encrypt_master_key(_master_cipher_key, _public_key)
        else:
            _hybrid_wrapped_key = ecc_encrypt_master_key(_master_cipher_key, _public_key)
    _vault = None
    if config.keyvault.enabled:
        fp_entries = sorted(hashlib.sha256(open(f, "rb").read()).hexdigest() for f in py_files[:5])
        _fingerprint = "|".join(fp_entries) + "|" + config.project.name
        _vault = generate_vault(_master_cipher_key, config.keyvault, _fingerprint)
        _master_cipher_key = _vault.key_pool[_vault.real_position]
    _threshold = max(2, len(py_files) // 3 + 1)
    _key_fragments = split_key(_master_cipher_key, len(py_files))
    _shamir_shares = shamir_split(_master_cipher_key, len(py_files), _threshold)

    _module_hex_map: dict[str, str] = {}
    _encrypted_blobs: list[bytes] = []
    _build_results: list[tuple[str, str, bytes] | None] = [None] * len(py_files)

    def _encrypt_single_file(idx: int, fp: str) -> tuple[str, str, bytes] | None:
        """Process a single file: obfuscate, encrypt, write .pye."""
        _file_config = merge_file_config(config, fp)
        _relative_path = os.path.relpath(fp, project_dir).replace("\\", "/")
        _module_dotted = _relative_path.replace(".py", "").replace("/", ".")
        if _module_dotted.endswith(".__init__"): _module_dotted = _module_dotted[:-9]
        _random_hex_alias = secrets.token_hex(6)
        try:
            _source_code = open(fp, encoding="utf-8-sig").read()
            if _file_config.obfuscate.level.value >= 1:
                _source_code = Obfuscator(_file_config.obfuscate, _global_rename_map, _global_param_set, _global_import_set).obfuscate(_source_code)
            if _file_config.virtualization.enabled and _file_config.virtualization.functions:
                _source_code = virtualize_source(_source_code, _file_config.virtualization)
            if _watermark_engine: _source_code = _watermark_engine.code(_source_code)
            _LAYER_COUNT = 6
            if config.compressor.enabled:
                from sprotect.compressor import compress as _cmp
                _ml_wrapped = _build_layers(_cmp(_source_code.encode()), _master_cipher_key, _LAYER_COUNT)
            else:
                _ml_wrapped = _build_layers(_source_code.encode(), _master_cipher_key, _LAYER_COUNT)
            _extra_layers = _file_config.encrypt.extra_layers or []
            if _extra_layers:
                _ciphertext, _enc_header = encrypt_payload_v2(_ml_wrapped, _master_cipher_key, _extra_layers,
                                             config.encrypt.compress_level)
                _header_json = json.dumps(_enc_header, separators=(",", ":"))
                _serialized_payload = json.dumps({"v":2,"h":_header_json,"d":_ciphertext.hex()},
                                           separators=(",", ":")).encode()
            else:
                _serialized_payload = encrypt_payload(_ml_wrapped, _master_cipher_key,
                                           config.encrypt.compress_level,
                                           config.encrypt.polymorphic_padding_max)
            _pkg_data = json.loads(_serialized_payload.decode())
            _pkg_data["ml"] = _LAYER_COUNT
            if config.compressor.enabled:
                # Fixed compression sequence: z=lzma, b=bz2, l=zlib (3 passes)
                _pkg_data["cmp"] = "zblzblzbl"
            _sid, _sval = _shamir_shares[idx]
            _pkg_data["sid"] = _sid
            _pkg_data["sv"] = _sval.hex()
            from sprotect.crypto import make_keys_complex
            _fingerprint_keys, _ = make_keys_complex(_key_fragments[idx], 4)
            _pkg_data.update(_fingerprint_keys)
            if config.encrypt.shard_count > 1 and "d" in _pkg_data:
                _raw_d = bytes.fromhex(_pkg_data["d"])
                _parts = []
                _base = len(_raw_d) // config.encrypt.shard_count
                _rem = len(_raw_d) % config.encrypt.shard_count
                _pos = 0
                for _si in range(config.encrypt.shard_count):
                    _sz = _base + (1 if _si < _rem else 0)
                    _parts.append(_raw_d[_pos:_pos+_sz].hex())
                    _pos += _sz
                _pkg_data["shards"] = {f"s{_si}": _parts[_si] for _si in range(config.encrypt.shard_count)}
                del _pkg_data["d"]
            if _watermark_engine: _pkg_data["wm"] = _watermark_engine.file_payload()
            _final_pkg = json.dumps(_pkg_data, separators=(",", ":")).encode()
            _pye_file_path = os.path.join(_runtime_dir, _random_hex_alias + ".pye")
            with open(_pye_file_path, "wb") as f: f.write(_final_pkg)
            return _module_dotted, _random_hex_alias, _final_pkg
        except Exception as e:
            print(f"  WARN: {_relative_path} - {e}")
            return None

    _thread_count = config.encrypt.workers or os.cpu_count() or 1
    if _thread_count > 1 and len(py_files) > 1:
        with ThreadPoolExecutor(max_workers=_thread_count) as pool:
            _future_index = {pool.submit(_encrypt_single_file, i, fp): i for i, fp in enumerate(py_files)}
            for fut in as_completed(_future_index):
                i = _future_index[fut]
                _build_results[i] = fut.result()
    else:
        for i, fp in enumerate(py_files):
            _build_results[i] = _encrypt_single_file(i, fp)

    _failure_count = sum(1 for r in _build_results if r is None)
    if _failure_count:
        print(f"  ERROR: {_failure_count}/{len(py_files)} files failed to encrypt")
        if _failure_count == len(py_files):
            raise RuntimeError("All files failed to encrypt")
    for r in _build_results:
        if r:
            _module_dotted, _random_hex_alias, _final_pkg = r
            _module_hex_map[_module_dotted] = _random_hex_alias
            _encrypted_blobs.append(_final_pkg)

    _chain_hashes = chain_hash(_encrypted_blobs, _master_cipher_key)
    for idx, (rel, _) in enumerate([(fp, "") for fp in py_files]):
        _module_dotted = os.path.relpath(fp, project_dir).replace("\\", "/")
        _module_dotted = _module_dotted.replace(".py", "").replace("/", ".")
        if _module_dotted.endswith(".__init__"): _module_dotted = _module_dotted[:-9]
        _hex_module = _module_hex_map.get(_module_dotted, "")
        if not _hex_module: continue
        _pye_file_path = os.path.join(_runtime_dir, _hex_module + ".pye")
        _raw_bytes = open(_pye_file_path, "rb").read()
        _payload_data = json.loads(_raw_bytes.decode())
        _payload_data["c"] = _chain_hashes[idx]
        open(_pye_file_path, "wb").write(json.dumps(_payload_data, separators=(",", ":")).encode())

    for i in range(max(2, len(py_files) // 2)):
        _garbage_payload = generate_decoy_payload()
        _decoy_name = secrets.token_hex(6) + ".pye"
        with open(os.path.join(_runtime_dir, _decoy_name), "wb") as f: f.write(_garbage_payload)
        if i % 2 == 0:
            _sub_dir = secrets.token_hex(4)
            os.makedirs(os.path.join(_runtime_dir, _sub_dir), exist_ok=True)
            for _ in range(2):
                _sub_file = secrets.token_hex(6) + ".pye"
                with open(os.path.join(_runtime_dir, _sub_dir, _sub_file), "wb") as f:
                    f.write(generate_decoy_payload())

    _module_map_json = json.dumps(_module_hex_map, separators=(",", ":"))
    _loader_source = gen_loader_source()
    _escaped_json = json.dumps(_module_map_json)
    _loader_source = _loader_source.replace('_MAP = ""', f"_MAP = {_escaped_json}")
    if _vault:
        _vault_pool_hex = [k.hex() for k in _vault.key_pool]
        _vault_payload = json.dumps({
            "pool": _vault_pool_hex,
            "pos": _vault.real_position,
            "mask": _vault.xor_mask.hex(),
            "seed": _vault.index_seed or config.project.name,
            "pay": [p.hex() for p in _vault.payloads],
        }, separators=(",", ":"))
        _vault_escaped = json.dumps(_vault_payload)
        _loader_source = _loader_source.replace('_VAULT = ""', f"_VAULT = {_vault_escaped}")
    _loader_source = minify_source(_loader_source, add_garbage=True)

    _zlib_compressed = zlib.compress(_loader_source.encode(), 9)
    from sprotect.crypto import xor_stream as _xs
    _xor_obfuscated = _xs(_zlib_compressed, _loader_cipher_key)
    _aes_nonce = os.urandom(12)
    _aes_ciphertext = _aes_nonce + AESGCM(_loader_cipher_key).encrypt(_aes_nonce, _xor_obfuscated, b"")
    _decoy_keys = [os.urandom(32) for _ in range(5)]
    _real_key_slot = secrets.randbelow(5)
    _decoy_keys[_real_key_slot] = _loader_cipher_key
    _key_flags = (_real_key_slot << 3) | (secrets.randbelow(8) << 6)
    loader_payload = {"v":7,"d":_aes_ciphertext.hex(),"l":_key_flags,"k1":_decoy_keys[0].hex(),"k2":_decoy_keys[1].hex(),
                       "k3":_decoy_keys[2].hex(),"k4":_decoy_keys[3].hex(),"k5":_decoy_keys[4].hex(),
                       "f1":"","f2":"","f3":""}
    open(os.path.join(_runtime_dir, "loader.pye"), "wb").write(
        json.dumps(loader_payload, separators=(",", ":")).encode())

    # Create _meta/ directory for metadata files
    meta_dir = os.path.join(output_dir, "_meta")
    os.makedirs(meta_dir, exist_ok=True)

    # Integrity manifest
    _integrity_db = {}
    for r, _, fs in os.walk(_runtime_dir):
        for f in sorted(fs):
            if f.endswith(".pye"):
                fp = os.path.join(r, f)
                _hash_obj = hashlib.sha256()
                with open(fp, "rb") as fh:
                    while True:
                        _read_buffer = fh.read(65536)
                        if not _read_buffer: break
                        _hash_obj.update(_read_buffer)
                _relative_path = os.path.relpath(fp, _runtime_dir).replace("\\", "/")
                _integrity_db[_relative_path] = _hash_obj.hexdigest()
    _manifest_path = os.path.join(meta_dir, "integrity_manifest.json")
    with open(_manifest_path, "w", encoding="utf-8") as f:
        json.dump(_integrity_db, f, separators=(",", ":"))
    print(f"  Integrity manifest: {_manifest_path} ({len(_integrity_db)} files)")

    # Build spec
    _build_metadata = {
        "project": config.project.name,
        "version": config.project.version,
        "entry": config.project.entry,
        "built_at": datetime.now(timezone.utc).isoformat(),
        "obfuscate_level": config.obfuscate.level.value,
        "encrypt_algorithm": config.encrypt.algorithm,
        "extra_layers": config.encrypt.extra_layers,
        "shard_count": config.encrypt.shard_count,
        "watermark_batch_id": _watermark_engine.bid if _watermark_engine else "",
        "hybrid_encryption": config.encrypt.hybrid.enabled,
        "file_count": len(py_files),
        "decoy_count": max(2, len(py_files) // 2),
    }
    _spec_save_path = os.path.join(meta_dir, "build.spec")
    with open(_spec_save_path, "w", encoding="utf-8") as f:
        json.dump(_build_metadata, f, indent=2, ensure_ascii=False)
    print(f"  Build spec: {_spec_save_path}")

    # Protection report
    _html_rows = []
    for _relative_path, _hash_obj in sorted(_integrity_db.items()):
        fsize = os.path.getsize(os.path.join(_runtime_dir, _relative_path))
        _html_rows.append(f"    <tr><td>{_relative_path}</td><td>{_hash_obj[:16]}...</td><td>{fsize}</td></tr>")
    _layers_display = ", ".join(config.encrypt.extra_layers) if config.encrypt.extra_layers else "none"
    _html_report = f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="UTF-8"><title>保护报告 - {_build_metadata['project']}</title>
<style>body{{font-family:sans-serif;max-width:800px;margin:40px auto;padding:0 20px}}
table{{width:100%;border-collapse:collapse;margin:10px 0}}
th,td{{padding:8px 12px;text-align:left;border-bottom:1px solid #ddd}}
th{{background:#333;color:#fff}}
.section{{background:#f5f5f5;padding:8px 12px;font-weight:bold;margin-top:20px}}
</style></head><body>
<h1>保护报告</h1>
<p>项目: {_build_metadata['project']} v{_build_metadata['version']} | 构建时间: {_build_metadata['built_at']}</p>
<div class="section">保护配置</div>
<table><tr><td>混淆等级</td><td>L{_build_metadata['obfuscate_level']}</td></tr>
<tr><td>加密算法</td><td>{_build_metadata['encrypt_algorithm']}</td></tr>
<tr><td>额外加密层</td><td>{_layers_display}</td></tr>
<tr><td>密钥分片数</td><td>{_build_metadata['shard_count']}</td></tr>
<tr><td>混合加密</td><td>{'是' if _build_metadata['hybrid_encryption'] else '否'}</td></tr>
<tr><td>水印批次</td><td>{_build_metadata['watermark_batch_id'] or '无'}</td></tr>
<tr><td>文件数</td><td>{_build_metadata['file_count']} 源码 + {_build_metadata['decoy_count']} 诱饵</td></tr></table>
<div class="section">文件清单 ({len(_integrity_db)} 个)</div>
<table><thead><tr><th>文件</th><th>哈希</th><th>大小</th></tr></thead><tbody>
{chr(10).join(_html_rows)}
</tbody></table></body></html>"""
    _report_path = os.path.join(meta_dir, "protection_report.html")
    with open(_report_path, "w", encoding="utf-8") as f:
        f.write(_html_report)
    print(f"  Protection report: {_report_path}")

    # Watermark report
    if _watermark_engine:
        try:
            _watermark_records = []
            for r, _, fs in os.walk(_runtime_dir):
                for f in sorted(fs):
                    if f.endswith(".pye"):
                        fp = os.path.join(r, f)
                        try:
                            pp = json.loads(open(fp, "rb").read().decode())
                            w = pp.get("wm")
                            if w: _watermark_records.append({"file": f, "bid": w.get("bid",""),
                                                   "ts": w.get("ts",""), "sig": w.get("sig",""),
                                                   "auth": w.get("auth","")})
                        except: pass
            _wm_report = {"generated": datetime.now(timezone.utc).isoformat(),
                       "project": config.project.name, "total": len(_watermark_records),
                       "batch_id": _watermark_engine.bid if _watermark_engine else "",
                       "records": _watermark_records}
            _wm_report_path = os.path.join(meta_dir, "watermark_report.json")
            with open(_wm_report_path, "w", encoding="utf-8") as f:
                json.dump(_wm_report, f, indent=2, ensure_ascii=False)
            print(f"  Watermark report: {_wm_report_path}")
            print(f"  Batch ID: {_watermark_engine.bid}")
        except Exception as e:
            print(f"  Watermark report: {e}")

    if _helper_generated:
        try: os.remove(_shard_helper_path)
        except OSError: pass

    _entry_module = config.project.entry.replace(".py", "")
    _entry_hex_alias = _module_hex_map.get(_entry_module, "")
    _hybrid_cfg = config.encrypt.hybrid
    gen_boot(output_dir, _entry_module, _entry_hex_alias, {}, _loader_cipher_key, _loader_build_salt, _hybrid_wrapped_key, _hybrid_cfg.algorithm if _hybrid_wrapped_key else "RSA", dual_process_enabled=config.dual_process.enabled)

    # Cleanup decoy modules
    _decoy_dir_path = os.path.join(project_dir, "_decoy_modules")
    if os.path.isdir(_decoy_dir_path):
        import shutil as _shu
        _shu.rmtree(_decoy_dir_path, ignore_errors=True)

    _copied = copy_non_py_files(project_dir, output_dir, config)
    if _copied:
        print(f"  Copied {_copied} non-Py files")
