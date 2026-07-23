from sprotect.compressor import compress, decompress, load_config, compress_file, decompress_file, DEFAULT_CONFIG
import os, json, tempfile


def test_compress_decompress_roundtrip():
    data = b"hello world " * 100
    packed = compress(data)
    assert isinstance(packed, bytes)
    restored = decompress(packed)
    assert restored == data


def test_compress_empty():
    assert decompress(compress(b"")) == b""


def test_compress_small():
    data = b"a" * 10
    packed = compress(data)
    restored = decompress(packed)
    assert restored == data


def test_compress_twice():
    data = b"hello world " * 50
    c1 = compress(data)
    c2 = compress(c1)
    assert decompress(decompress(c2)) == data


def test_compress_lossless_binary():
    data = bytes(range(256)) * 50
    packed = compress(data)
    restored = decompress(packed)
    assert restored == data


def test_compress_repeated_pattern():
    data = b"The quick brown fox jumps over the lazy dog " * 200
    packed = compress(data)
    ratio = len(packed) / len(data)
    assert ratio < 0.4
    restored = decompress(packed)
    assert restored == data


def test_compress_random_hard():
    data = os.urandom(5000)
    packed = compress(data)
    restored = decompress(packed)
    assert restored == data


def test_decompress_invalid_returns_asis():
    result = decompress(b"\n\ninvalid")
    assert result == b"\n\ninvalid"


def test_decompress_truncated_falls_back():
    data = b"hello " * 200
    packed = compress(data)
    truncated = packed.split(b"\n\n", 1)[0] + b"\n\ntruncated"
    result = decompress(truncated)
    assert result == b"truncated"


def test_compress_unicode():
    data = "你好世界 🌍"
    packed = compress(data.encode("utf-8"))
    restored = decompress(packed).decode("utf-8")
    assert restored == data


def test_compress_with_base85():
    cfg = dict(DEFAULT_CONFIG)
    cfg["use_base85"] = True
    packed = compress(b"test " * 50, cfg)
    assert b"b85" in packed.split(b"\n\n", 1)[0]
    restored = decompress(packed)
    assert restored == b"test " * 50


def test_compress_disabled():
    cfg = dict(DEFAULT_CONFIG)
    cfg["enabled"] = False
    data = b"hello " * 100
    packed = compress(data, cfg)
    assert packed == data


def test_compress_single_pass():
    cfg = dict(DEFAULT_CONFIG)
    cfg["pass_count"] = 1
    data = b"test " * 200
    packed = compress(data, cfg)
    ratio = len(packed) / len(data)
    assert ratio < 0.5
    restored = decompress(packed)
    assert restored == data


def test_compress_five_pass():
    cfg = dict(DEFAULT_CONFIG)
    cfg["pass_count"] = 5
    data = b"test " * 200
    packed = compress(data, cfg)
    restored = decompress(packed)
    assert restored == data


def test_decompress_non_compressed():
    data = b"plain text without compression header"
    assert decompress(data) == data


def test_compress_decompress_file_roundtrip():
    data = b"file test data " * 500
    with tempfile.NamedTemporaryFile(suffix=".bin", delete=False) as src:
        src.write(data)
        src_path = src.name
    out_path = src_path + ".cmp"
    restored_path = src_path + ".res"
    try:
        saved = compress_file(src_path, out_path)
        assert saved > 0
        result_size = decompress_file(out_path, restored_path)
        assert result_size == len(data)
        with open(restored_path, "rb") as f:
            assert f.read() == data
    finally:
        for p in [src_path, out_path, restored_path]:
            if os.path.isfile(p):
                os.unlink(p)


def test_load_config_defaults():
    cfg = load_config("nonexistent.json5")
    assert cfg["enabled"] is True
    assert cfg["pass_count"] == 3


def test_load_config_from_file():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json5", delete=False, encoding="utf-8") as f:
        f.write('{enabled:false, pass_count:1}')
        cfg_path = f.name
    try:
        cfg = load_config(cfg_path)
        assert cfg["enabled"] is False
        assert cfg["pass_count"] == 1
    finally:
        if os.path.isfile(cfg_path):
            os.unlink(cfg_path)


def test_compress_preserves_header():
    packed = compress(b"test " * 100)
    assert b"\n\n" in packed
    header, body = packed.split(b"\n\n", 1)
    meta = json.loads(header.decode())
    assert "v" in meta
    assert "seq" in meta
    assert len(meta["seq"]) > 0


def test_compress_b85_flag_in_header():
    cfg = dict(DEFAULT_CONFIG)
    cfg["use_base85"] = True
    packed = compress(b"test " * 50, cfg)
    header = packed.split(b"\n\n", 1)[0]
    meta = json.loads(header.decode())
    assert meta.get("b85") is True


def test_compress_very_large():
    data = b"abcdefghij " * 50000
    packed = compress(data)
    ratio = len(packed) / len(data)
    assert ratio < 0.3
    restored = decompress(packed)
    assert restored == data
