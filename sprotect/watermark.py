"""Three-level watermark injection."""
from __future__ import annotations
import hashlib, hmac, secrets
from sprotect.types import WatermarkConfig, WatermarkLevel

class Watermark:
    def __init__(self, cfg: WatermarkConfig):
        self.cfg = cfg
        self.bid = cfg.batch_id or secrets.token_hex(8)
    def file(self, path: str) -> str:
        w = f"// WM:{self.bid}:{hashlib.sha256(self.bid.encode()).hexdigest()[:16]}\n"
        with open(path, "a", encoding="utf-8") as f: f.write(w)
        return w.strip()
    def code(self, src: str) -> str:
        sig = hashlib.sha256(f"code_wm:{self.bid}".encode()).hexdigest()[:16]
        return src + f"\n_=lambda:None if __import__('hashlib').sha256(b'{sig}').hexdigest()[:16]=='{sig}' else None\n"
    def runtime(self) -> str:
        sig = hmac.new(self.bid.encode(), b"runtime_watermark", "sha256").hexdigest()[:16]
        return f'def _verify_wm():\n import hmac\n return hmac.compare_digest(hmac.new(b"{self.bid}",b"runtime_watermark","sha256").hexdigest()[:16],"{sig}")\n'
