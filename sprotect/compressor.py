"""极致压缩器 — 多算法堆叠压缩引擎。
独立的压缩模块，负责对加密后的载荷进行极致压缩。
支持多轮堆叠压缩（Token替换→LZMA→BZ2→Zlib→Base85）。
"""

from __future__ import annotations
import os, zlib, bz2, lzma, base64, re, struct, json, secrets
from typing import Optional


# ─── 默认配置（可通过 compressor.json5 覆盖） ─────────────────────────

DEFAULT_CONFIG = {
    "enabled": True,
    "pass_count": 3,
    "use_lzma": True,
    "use_bz2": True,
    "use_zlib": True,
    "use_base85": True,
    "token_replace": True,
    "shorten_identifiers": True,
    "remove_dead_strings": True,
    "dictionary_size": 4096,
    "max_chunk_size": 1048576,
}


def load_config(path: Optional[str] = None) -> dict:
    """从 JSON5 文件加载压缩器配置。"""
    import json5 as _j5
    candidates = []
    if path:
        candidates.append(path)
    candidates.append(os.path.join(os.path.dirname(__file__), "compressor.json5"))
    for c in candidates:
        if os.path.isfile(c):
            try:
                raw = _j5.loads(open(c, encoding="utf-8").read())
                cfg = dict(DEFAULT_CONFIG)
                cfg.update(raw)
                return cfg
            except:
                pass
    return dict(DEFAULT_CONFIG)


# ─── 核心压缩/解压函数 ────────────────────────────────────────────────

def _build_token_dict(data: bytes, dict_size: int = 4096) -> dict[bytes, int]:
    """从数据中提取高频重复模式建立 Token 字典。"""
    from collections import Counter
    patterns = Counter()
    for length in [4, 8, 16, 32]:
        for i in range(len(data) - length + 1):
            patterns[data[i:i + length]] += 1
    # 取最高频的模式
    top = [p for p, _ in patterns.most_common(256) if _ > 2]
    return {p: i for i, p in enumerate(top[:255])}


def _token_replace(data: bytes, token_dict: dict[bytes, int]) -> bytes:
    """用 Token ID 替换高频模式。"""
    if not token_dict:
        return data
    result = bytearray()
    i = 0
    while i < len(data):
        matched = False
        for pattern in sorted(token_dict.keys(), key=len, reverse=True):
            if data[i:i + len(pattern)] == pattern:
                result.append(0xFF)  # escape marker
                result.append(token_dict[pattern])
                i += len(pattern)
                matched = True
                break
        if not matched:
            result.append(data[i])
            i += 1
    return bytes(result)


def _token_restore(data: bytes, token_dict: dict[bytes, int]) -> bytes:
    """从 Token ID 还原原始模式。"""
    rev = {v: k for k, v in token_dict.items()}
    result = bytearray()
    i = 0
    while i < len(data):
        if data[i] == 0xFF and i + 1 < len(data):
            token_id = data[i + 1]
            if token_id in rev:
                result.extend(rev[token_id])
                i += 2
                continue
        result.append(data[i])
        i += 1
    return bytes(result)


def _shorten_identifiers(data: bytes) -> tuple[bytes, dict[str, str]]:
    """将长标识符替换为短标识符，返回映射表。"""
    try:
        text = data.decode("utf-8")
    except:
        return data, {}
    # 匹配 Python 标识符
    id_map = {}
    counter = 0
    def _replace(m):
        nonlocal counter
        name = m.group(0)
        if name not in id_map and len(name) > 3:
            short = f"_x{counter:02x}"
            id_map[name] = short
            counter += 1
            return short
        return name
    text = re.sub(r'\b[a-zA-Z_][a-zA-Z0-9_]{3,}\b', _replace, text)
    return text.encode("utf-8"), id_map


def _restore_identifiers(data: bytes, id_map: dict[str, str]) -> bytes:
    """从短标识符还原（逆转映射）。"""
    rev = {v: k for k, v in id_map.items()}
    try:
        text = data.decode("utf-8")
    except:
        return data
    def _restore(m):
        name = m.group(0)
        return rev.get(name, name)
    text = re.sub(r'\b_x[a-f0-9]{2}\b', _restore, text)
    return text.encode("utf-8")


def compress(data: bytes, cfg: dict | None = None) -> bytes:
    """对数据进行极致压缩，返回压缩后的 bytes。
    
    压缩流程（可配置轮数）：
    1. Token 替换（高频模式 → 单字节 ID）
    2. 标识符缩短（长名 → _x00 格式）
    3. LZMA 压缩（最高压缩率）
    4. BZ2 压缩（中等压缩率）
    5. Zlib 压缩（level 9，最大压缩）
    6. Base85 编码（减少文本膨胀）
    """
    if cfg is None:
        cfg = DEFAULT_CONFIG
    if not cfg.get("enabled", True):
        return data

    current = data
    meta = {}

    for _pass in range(cfg.get("pass_count", 3)):
        # Token 替换
        if cfg.get("token_replace"):
            token_dict = _build_token_dict(current, cfg.get("dictionary_size", 4096))
            if token_dict:
                current = _token_replace(current, token_dict)
                meta["token_dict"] = {k.hex(): v for k, v in token_dict.items()}

        # 标识符缩短
        if cfg.get("shorten_identifiers"):
            current, id_map = _shorten_identifiers(current)
            if id_map:
                meta["id_map"] = id_map

        # LZMA
        if cfg.get("use_lzma"):
            try:
                _prev = len(current)
                current = lzma.compress(current)
                meta.setdefault("lzma_count", 0)
                meta["lzma_count"] += 1
            except:
                pass

        # BZ2
        if cfg.get("use_bz2"):
            try:
                current = bz2.compress(current)
                meta["bz2"] = True
            except:
                pass

        # Zlib
        if cfg.get("use_zlib"):
            try:
                current = zlib.compress(current, level=9)
                meta["zlib"] = True
            except:
                pass

    # Base85 编码（最终输出文本安全）
    if cfg.get("use_base85"):
        try:
            current = base64.a85encode(current)
            meta["base85"] = True
        except:
            pass

    # 包装元数据头
    header = json.dumps(meta, separators=(",", ":")).encode() + b"\n\n"
    return header + current


def decompress(data: bytes) -> bytes:
    """解压由 compress() 压缩的数据。"""
    # 分离元数据头和数据
    parts = data.split(b"\n\n", 1)
    if len(parts) < 2:
        return data
    try:
        meta = json.loads(parts[0].decode())
    except:
        return data
    current = parts[1]

    # 逆向解压
    if meta.get("base85"):
        try:
            current = base64.a85decode(current)
        except:
            pass
    if meta.get("zlib"):
        try:
            current = zlib.decompress(current)
        except:
            pass
    if meta.get("bz2"):
        try:
            current = bz2.decompress(current)
        except:
            pass
    for _ in range(meta.get("lzma_count", 0)):
        try:
            current = lzma.decompress(current)
        except:
            break
    if meta.get("id_map"):
        try:
            current = _restore_identifiers(current, meta["id_map"])
        except:
            pass
    if meta.get("token_dict"):
        try:
            td = {bytes.fromhex(k): v for k, v in meta["token_dict"].items()}
            current = _token_restore(current, td)
        except:
            pass

    return current


def compress_file(input_path: str, output_path: str, cfg: dict | None = None) -> int:
    """压缩文件，返回节省的字节数。"""
    with open(input_path, "rb") as f:
        original = f.read()
    compressed = compress(original, cfg)
    with open(output_path, "wb") as f:
        f.write(compressed)
    saved = len(original) - len(compressed)
    return saved


def decompress_file(input_path: str, output_path: str) -> int:
    """解压文件，返回恢复的字节数。"""
    with open(input_path, "rb") as f:
        data = f.read()
    decompressed = decompress(data)
    with open(output_path, "wb") as f:
        f.write(decompressed)
    return len(decompressed)


if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 3 and sys.argv[1] == "--compress":
        saved = compress_file(sys.argv[2], sys.argv[3])
        print(f"Compressed: {sys.argv[2]} -> {sys.argv[3]} ({saved} bytes saved)")
    elif len(sys.argv) >= 3 and sys.argv[1] == "--decompress":
        size = decompress_file(sys.argv[2], sys.argv[3])
        print(f"Decompressed: {sys.argv[2]} -> {sys.argv[3]} ({size} bytes)")
    else:
        print("Usage: compressor.py --compress <input> <output>")
        print("       compressor.py --decompress <input> <output>")
