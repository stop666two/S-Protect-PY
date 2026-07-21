"""Three-level watermark injection + extraction."""

from __future__ import annotations
import hashlib, hmac, secrets, json

class Watermark:
    def __init__(self, cfg):
        self.cfg = cfg
        self.bid = cfg.batch_id or secrets.token_hex(8)
    
    def file_payload(self) -> dict:
        """Return watermark dict to embed inside JSON/msgpack payload.
        Usage: payload["wm"] = Watermark(cfg).file_payload()"""
        sig = hashlib.sha256(self.bid.encode()).hexdigest()[:16]
        return {"bid": self.bid, "sig": sig, "t": "file"}
    
    def code(self, src: str) -> str:
        """Inject code-level watermark into source."""
        sig = hashlib.sha256(f"code_wm:{self.bid}".encode()).hexdigest()[:16]
        return src + f"\n_=lambda:None if __import__('hashlib').sha256(b'{sig}').hexdigest()[:16]=='{sig}' else None\n"
    
    def runtime(self) -> str:
        """Generate runtime watermark verification code."""
        sig = hmac.new(self.bid.encode(), b"runtime_watermark", "sha256").hexdigest()[:16]
        return (
            f'def _verify_wm():\n'
            f' import hmac\n'
            f' return hmac.compare_digest(\n'
            f'  hmac.new(b"{self.bid}",b"runtime_watermark","sha256").hexdigest()[:16],\n'
            f'  "{sig}")\n'
        )


def extract_watermark(pye_path: str) -> dict | None:
    """Extract watermark from an encrypted .pye file.
    
    Usage:
        wm = extract_watermark("output/_runtime/main.pye")
        if wm:
            print(f"Batch ID: {wm['bid']}")
            print(f"Signature: {wm['sig']}")
    """
    try:
        raw = open(pye_path, "rb").read()
        # Try JSON first
        try:
            p = json.loads(raw.decode())
        except:
            # Try msgpack
            if raw[:3] == b"Sv7":
                import msgpack
                p = msgpack.unpackb(raw[3:], strict_map_key=False)
                # Convert integer keys to strings if needed
                p = {str(k) if isinstance(k, int) else k: v for k, v in p.items()}
            else:
                return None
        wm = p.get("wm") or p.get("WM")
        if wm and isinstance(wm, dict) and "bid" in wm:
            return wm
        return None
    except:
        return None


def verify_watermark(pye_path: str) -> bool:
    """Verify a .pye file's watermark signature.
    
    Usage:
        if verify_watermark("output/_runtime/main.pye"):
            print("Watermark valid")
    """
    wm = extract_watermark(pye_path)
    if not wm:
        return False
    expected = hashlib.sha256(wm["bid"].encode()).hexdigest()[:16]
    return wm.get("sig") == expected
