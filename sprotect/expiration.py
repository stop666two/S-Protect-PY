"""Expiration control with NTP verification."""
from __future__ import annotations
from datetime import datetime, timezone
import socket, struct
from sprotect.types import ExpirationConfig

class Expiration:
    def __init__(self, cfg: ExpirationConfig): self.cfg = cfg
    def check(self, encrypted_at: str, expires_at: str | None) -> bool:
        if not self.cfg.enabled: return True
        nt = self._ntp() if self.cfg.ntp_check else None
        if nt is not None:
            ref = nt
            local = datetime.now(timezone.utc)
            drift = abs((local - nt).total_seconds())
            if drift > self.cfg.max_drift_seconds:
                return self.cfg.on_network_fail != "reject"
        else:
            ref = datetime.now(timezone.utc)
            if self.cfg.ntp_check:
                if self.cfg.on_network_fail == "reject":
                    return False
        enc = datetime.fromisoformat(encrypted_at)
        if enc.tzinfo is None: enc = enc.replace(tzinfo=timezone.utc)
        if ref < enc: return False
        if expires_at:
            exp = datetime.fromisoformat(expires_at)
            if exp.tzinfo is None: exp = exp.replace(tzinfo=timezone.utc)
            if ref > exp: return False
        return True
    def _ntp(self):
        for srv in self.cfg.ntp_servers:
            for family in (socket.AF_INET, socket.AF_INET6):
                try:
                    addrs = socket.getaddrinfo(srv, 123, family, socket.SOCK_DGRAM)
                    if not addrs: continue
                    s = socket.socket(family, socket.SOCK_DGRAM); s.settimeout(self.cfg.ntp_timeout)
                    s.sendto(b"\x1b" + 47 * b"\x00", addrs[0][4])
                    d, _ = s.recvfrom(1024); s.close()
                    if len(d) >= 48:
                        t = struct.unpack("!12I", d)[10] - 2208988800
                        return datetime.fromtimestamp(t, tz=timezone.utc)
                except: pass
        return None
