"""Expiration control with NTP verification."""
from __future__ import annotations
from datetime import datetime, timezone
import socket, struct
from sprotect.types import ExpirationConfig

class Expiration:
    def __init__(self, cfg: ExpirationConfig): self.cfg = cfg
    def check(self, encrypted_at: str, expires_at: str | None) -> bool:
        if not self.cfg.enabled: return True
        now = datetime.now(timezone.utc)
        enc = datetime.fromisoformat(encrypted_at)
        if enc.tzinfo is None: enc = enc.replace(tzinfo=timezone.utc)
        if now < enc: return False
        if expires_at:
            exp = datetime.fromisoformat(expires_at)
            if exp.tzinfo is None: exp = exp.replace(tzinfo=timezone.utc)
            if now > exp: return False
        if self.cfg.ntp_check:
            nt = self._ntp()
            if nt and abs((now - nt).total_seconds()) > 3600:
                return self.cfg.on_network_fail != "reject"
        return True
    def _ntp(self):
        for srv in ["pool.ntp.org", "time.google.com", "time.cloudflare.com"]:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM); s.settimeout(3)
                s.sendto(b"\x1b" + 47 * b"\x00", (srv, 123))
                d, _ = s.recvfrom(1024); s.close()
                if len(d) >= 48:
                    t = struct.unpack("!12I", d)[10] - 2208988800
                    return datetime.fromtimestamp(t, tz=timezone.utc)
            except: pass
        return None
