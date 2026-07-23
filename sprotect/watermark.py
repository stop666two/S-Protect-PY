"""Three-level watermark: timestamp, authenticity verification, batch ID."""

from __future__ import annotations
import hashlib, hmac, secrets, json, time
from datetime import datetime, timezone


# WATERMARK INJECTOR: three-layer provenance tracking
# BATCH: auto-generated if empty

class Watermark:
    def __init__(self, cfg):
        self.cfg = cfg
        self.bid = cfg.batch_id or secrets.token_hex(8)
        self._wm_secret = cfg.watermark_key or secrets.token_hex(16)

    def file_payload(self) -> dict:
        ts = datetime.now(timezone.utc).isoformat()
        _digest = hashlib.sha256(self.bid.encode()).hexdigest()[:16]
        auth_data = f"{self.bid}|{ts}"
        auth = hmac.new(self._wm_secret.encode(), auth_data.encode(), "sha256").hexdigest()[:16]
        return {"bid": self.bid, "ts": ts, "sig": _digest, "auth": auth, "t": "file"}

    def code(self, src: str) -> str:
        _digest = hashlib.sha256(f"code_wm:{self.bid}".encode()).hexdigest()[:16]
        return src + f"\n_=lambda:None if __import__('hashlib').sha256(b'{_digest}').hexdigest()[:16]=='{_digest}' else None\n"

    def runtime(self) -> str:
        _digest = hmac.new(self.bid.encode(), b"runtime_watermark", "sha256").hexdigest()[:16]
        return (
            f'def _verify_wm():\n'
            f' import hmac\n'
            f' return hmac.compare_digest(\n'
            f'  hmac.new(b"{self.bid}",b"runtime_watermark","sha256").hexdigest()[:16],\n'
            f'  "{_digest}")\n'
        )


def extract_watermark(pye_path: str, secret_key: str = "") -> dict | None:
    try:
        raw = open(pye_path, "rb").read()
        try:
            p = json.loads(raw.decode())
        except:
            if raw[:3] == b"Sv7":
                import msgpack
                p = msgpack.unpackb(raw[3:], strict_map_key=False)
                p = {str(k) if isinstance(k, int) else k: v for k, v in p.items()}
            else:
                return None
        wm = p.get("wm") or p.get("WM")
        if not wm or not isinstance(wm, dict) or "bid" not in wm:
            return None

        result = dict(wm)
        result["valid"] = False

        expected_sig = hashlib.sha256(wm["bid"].encode()).hexdigest()[:16]
        result["sig_ok"] = wm.get("sig") == expected_sig

        if secret_key and "ts" in wm:
            auth_data = f"{wm['bid']}|{wm['ts']}"
            expected_auth = hmac.new(secret_key.encode(), auth_data.encode(), "sha256").hexdigest()[:16]
            result["auth_ok"] = wm.get("auth") == expected_auth
        else:
            result["auth_ok"] = False

        result["valid"] = result.get("sig_ok", False)
        return result
    except:
        return None


def verify_watermark(pye_path: str, secret_key: str = "") -> bool:
    wm = extract_watermark(pye_path, secret_key)
    if not wm:
        return False
    if secret_key:
        return wm.get("sig_ok", False) and wm.get("auth_ok", False)
    return wm.get("sig_ok", False)


def patch_watermark(pye_path: str, new_bid: str, secret_key: str = "",
                    append: bool = False) -> dict | None:
    try:
        with open(pye_path, "rb") as f:
            raw = f.read()
        p = json.loads(raw.decode())
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None

    ts = datetime.now(timezone.utc).isoformat()
    _digest = hashlib.sha256(new_bid.encode()).hexdigest()[:16]
    wm = {"bid": new_bid, "ts": ts, "sig": _digest, "t": "patched"}

    old_wm = p.get("wm") or p.get("WM")
    if append and old_wm and isinstance(old_wm, dict):
        wm["prev"] = old_wm.get("bid", "")

    if secret_key:
        auth_data = f"{new_bid}|{ts}"
        wm["auth"] = hmac.new(secret_key.encode(), auth_data.encode(), "sha256").hexdigest()[:16]

    p["wm"] = wm
    with open(pye_path, "wb") as f:
        f.write(json.dumps(p, separators=(",", ":")).encode())
    return wm


def patch_watermark_batch(runtime_dir: str, new_bid: str, secret_key: str = "",
                          append: bool = False) -> int:
    import os, glob
    count = 0
    for f in sorted(glob.glob(os.path.join(runtime_dir, "**", "*.pye"), recursive=True)):
        if patch_watermark(f, new_bid, secret_key, append):
            count += 1
    return count
