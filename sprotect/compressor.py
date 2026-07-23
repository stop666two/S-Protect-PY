"""极致压缩器 — 多算法堆叠压缩引擎。
独立模块，负责对载荷进行极致压缩。
支持 LZMA(9) + BZ2(9) + Zlib(9) 多轮堆叠 + Base85 编码。
"""

from __future__ import annotations
import os, zlib, bz2, lzma, base64, json
from typing import Optional

DEFAULT_CONFIG = {
    "enabled": True,
    "pass_count": 3,
    "use_lzma": True,
    "use_bz2": True,
    "use_zlib": True,
    "use_base85": False,
}


def load_config(path: Optional[str] = None) -> dict:
    import json5 as _j5
    candidates = [path] if path else []
    candidates.append(os.path.join(os.path.dirname(__file__), "compressor.json5"))
    for c in candidates:
        if c and os.path.isfile(c):
            try:
                cfg = dict(DEFAULT_CONFIG)
                cfg.update(_j5.loads(open(c, encoding="utf-8").read()))
                return cfg
            except: pass
    return dict(DEFAULT_CONFIG)


def compress(data: bytes, cfg: dict | None = None) -> bytes:
    if cfg is None: cfg = DEFAULT_CONFIG
    if not cfg.get("enabled", True): return data
    current = data
    meta = {"v": 2, "seq": []}
    for _pass in range(cfg.get("pass_count", 3)):
        _seq = []
        if cfg.get("use_lzma"):
            try: current = lzma.compress(current, preset=9 | lzma.PRESET_EXTREME); _seq.append("z")
            except: pass
        if cfg.get("use_bz2"):
            try: current = bz2.compress(current, compresslevel=9); _seq.append("b")
            except: pass
        if cfg.get("use_zlib"):
            try: current = zlib.compress(current, level=9); _seq.append("l")
            except: pass
        if _seq: meta["seq"].extend(_seq)
    if cfg.get("use_base85"):
        try: current = base64.a85encode(current); meta["b85"] = True
        except: pass
    hdr = json.dumps(meta, separators=(",",":")).encode() + b"\n\n"
    return hdr + current


def decompress(data: bytes) -> bytes:
    parts = data.split(b"\n\n", 1)
    if len(parts) < 2: return data
    try: meta = json.loads(parts[0].decode())
    except: return data
    current = parts[1]
    if meta.get("b85"):
        try: current = base64.a85decode(current)
        except: pass
    # Reverse sequence
    for code in reversed(meta.get("seq", [])):
        try:
            if code == "l": current = zlib.decompress(current)
            elif code == "b": current = bz2.decompress(current)
            elif code == "z": current = lzma.decompress(current)
        except: break
    return current


def compress_file(input_path: str, output_path: str, cfg: dict | None = None) -> int:
    with open(input_path, "rb") as f: original = f.read()
    c = compress(original, cfg)
    with open(output_path, "wb") as f: f.write(c)
    return len(original) - len(c)


def decompress_file(input_path: str, output_path: str) -> int:
    with open(input_path, "rb") as f: data = f.read()
    r = decompress(data)
    with open(output_path, "wb") as f: f.write(r)
    return len(r)


if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 3:
        if sys.argv[1] == "--compress":
            s = compress_file(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else sys.argv[2] + ".cmp")
            print(f"Saved: {s} bytes")
        elif sys.argv[1] == "--decompress":
            s = decompress_file(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else sys.argv[2].replace(".cmp",""))
            print(f"Decompressed: {s} bytes")
    else:
        print("Usage: compressor.py --compress <input> [output]")
        print("       compressor.py --decompress <input> [output]")
