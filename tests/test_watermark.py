from sprotect.watermark import Watermark, extract_watermark, verify_watermark, patch_watermark
from sprotect.types import WatermarkConfig
import tempfile, os, json


def _make_cfg(batch_id="", wm_key=""):
    return WatermarkConfig(
        enabled=True,
        levels=["file", "code", "runtime"],
        batch_id=batch_id,
        multi_batch=[],
        visible=False,
        watermark_key=wm_key,
    )


def test_file_payload_structure():
    wm = Watermark(_make_cfg("test_batch_001"))
    payload = wm.file_payload()
    assert isinstance(payload, dict)
    assert "bid" in payload
    assert "ts" in payload
    assert "sig" in payload
    assert "auth" in payload
    assert "t" in payload
    assert payload["bid"] == "test_batch_001"
    assert payload["t"] == "file"


def test_file_payload_auto_bid():
    wm = Watermark(_make_cfg())
    payload = wm.file_payload()
    assert len(payload["bid"]) == 16
    assert isinstance(payload["sig"], str)
    assert len(payload["sig"]) == 16


def test_code_watermark():
    wm = Watermark(_make_cfg("test_batch"))
    original = "print('hello')"
    marked = wm.code(original)
    assert marked.startswith(original)
    assert "hashlib" in marked
    assert "sha256" in marked
    compile(marked, "<test>", "exec")


def test_runtime_watermark():
    wm = Watermark(_make_cfg("test_batch"))
    code = wm.runtime()
    assert "def _verify_wm" in code
    assert "hmac" in code
    assert "compare_digest" in code
    compile(code, "<test>", "exec")


def test_different_batch_different_payload():
    wm1 = Watermark(_make_cfg("batch_a"))
    wm2 = Watermark(_make_cfg("batch_b"))
    assert wm1.file_payload() != wm2.file_payload()


def test_custom_secret_key():
    wm = Watermark(_make_cfg("batch", "my_secret_key_123"))
    payload = wm.file_payload()
    assert len(payload["auth"]) == 16


def test_extract_watermark_from_pye():
    wm = Watermark(_make_cfg("extract_test"))
    payload = {"wm": wm.file_payload()}
    with tempfile.NamedTemporaryFile(mode="w", suffix=".pye", delete=False, encoding="utf-8") as f:
        json.dump(payload, f)
        path = f.name
    try:
        result = extract_watermark(path)
        assert result is not None
        assert result["bid"] == "extract_test"
    finally:
        os.unlink(path)


def test_extract_watermark_invalid_file():
    assert extract_watermark("nonexistent.pye") is None


def test_verify_watermark_valid():
    wm = Watermark(_make_cfg("verify_test", "key123"))
    payload = {"wm": wm.file_payload()}
    with tempfile.NamedTemporaryFile(mode="w", suffix=".pye", delete=False, encoding="utf-8") as f:
        json.dump(payload, f)
        path = f.name
    try:
        assert verify_watermark(path, "key123") is True
    finally:
        os.unlink(path)


def test_verify_watermark_wrong_key():
    wm = Watermark(_make_cfg("verify_test", "key123"))
    payload = {"wm": wm.file_payload()}
    with tempfile.NamedTemporaryFile(mode="w", suffix=".pye", delete=False, encoding="utf-8") as f:
        json.dump(payload, f)
        path = f.name
    try:
        assert verify_watermark(path, "wrong_key") is False
    finally:
        os.unlink(path)


def test_patch_watermark():
    wm = Watermark(_make_cfg("patch_test"))
    payload = {"wm": wm.file_payload()}
    with tempfile.NamedTemporaryFile(mode="w", suffix=".pye", delete=False, encoding="utf-8") as f:
        json.dump(payload, f)
        path = f.name
    try:
        patch_watermark(path, new_bid="patched_bid")
        with open(path, encoding="utf-8") as f:
            updated = json.load(f)
        assert updated["wm"]["bid"] == "patched_bid"
    finally:
        os.unlink(path)


def test_code_watermark_is_valid():
    wm = Watermark(_make_cfg("code_test"))
    src = "x = 1"
    marked = wm.code(src)
    ns = {}
    exec(compile(marked, "<test>", "exec"), ns)
    assert ns.get("x") == 1
