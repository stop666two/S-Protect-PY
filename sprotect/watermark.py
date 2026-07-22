"""Three-level watermark: timestamp, authenticity verification, batch ID."""

from __future__ import annotations
import hashlib, hmac, secrets, json, time
from datetime import datetime, timezone


class Watermark:
    def __init__(self, cfg):
        self.cfg = cfg
        self.bid = cfg.batch_id or secrets.token_hex(8)
        self._key = cfg.watermark_key or secrets.token_hex(16)
    
    def file_payload(self) -> dict:
        """Watermark payload with timestamp + authenticity code.
        
        Fields:
        - bid: batch ID (identifies customer/build)
        - ts: ISO 8601 timestamp of build
        - sig: SHA256(bid)[:16] quick integrity check
        - auth: HMAC-SHA256(bid + ts, secret_key)[:16] authenticity proof
        """
        ts = datetime.now(timezone.utc).isoformat()
        sig = hashlib.sha256(self.bid.encode()).hexdigest()[:16]
        auth_data = f"{self.bid}|{ts}"
        auth = hmac.new(self._key.encode(), auth_data.encode(), "sha256").hexdigest()[:16]
        return {"bid": self.bid, "ts": ts, "sig": sig, "auth": auth, "t": "file"}
    
    def code(self, src: str) -> str:
        """Code-level watermark."""
        sig = hashlib.sha256(f"code_wm:{self.bid}".encode()).hexdigest()[:16]
        return src + f"\n_=lambda:None if __import__('hashlib').sha256(b'{sig}').hexdigest()[:16]=='{sig}' else None\n"
    
    def runtime(self) -> str:
        """Runtime watermark check code."""
        sig = hmac.new(self.bid.encode(), b"runtime_watermark", "sha256").hexdigest()[:16]
        return (
            f'def _verify_wm():\n'
            f' import hmac\n'
            f' return hmac.compare_digest(\n'
            f'  hmac.new(b"{self.bid}",b"runtime_watermark","sha256").hexdigest()[:16],\n'
            f'  "{sig}")\n'
        )


def extract_watermark(pye_path: str, secret_key: str = "") -> dict | None:
    """Extract watermark from a .pye file.
    
    If secret_key is provided, also validates the authenticity code.
    
    Returns dict with: bid, ts, sig, auth, t, valid (bool)
    """
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
        
        # Verify signature (quick integrity)
        expected_sig = hashlib.sha256(wm["bid"].encode()).hexdigest()[:16]
        result["sig_ok"] = wm.get("sig") == expected_sig
        
        # Verify authenticity (if key provided)
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
    """Verify watermark: signature check + optional authenticity check."""
    wm = extract_watermark(pye_path, secret_key)
    if not wm:
        return False
    if secret_key:
        return wm.get("sig_ok", False) and wm.get("auth_ok", False)
    return wm.get("sig_ok", False)


def patch_watermark(pye_path: str, new_bid: str, secret_key: str = "",
                    append: bool = False) -> dict | None:
    """Hot-patch watermark on an existing .pye file without re-encryption.

    Args:
        pye_path: Path to .pye file
        new_bid: New batch ID to set
        secret_key: Key for HMAC authenticity signing
        append: If True, keeps old bid in a 'prev' field

    Returns:
        Updated watermark dict, or None on failure
    """
    try:
        with open(pye_path, "rb") as f:
            raw = f.read()
        p = json.loads(raw.decode())
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None

    ts = datetime.now(timezone.utc).isoformat()
    sig = hashlib.sha256(new_bid.encode()).hexdigest()[:16]
    wm = {"bid": new_bid, "ts": ts, "sig": sig, "t": "patched"}

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
    """Patch watermark on all .pye files in a directory.

    Returns:
        Number of files successfully patched.
    """
    import os, glob
    count = 0
    for f in sorted(glob.glob(os.path.join(runtime_dir, "**", "*.pye"), recursive=True)):
        if patch_watermark(f, new_bid, secret_key, append):
            count += 1
    return count
