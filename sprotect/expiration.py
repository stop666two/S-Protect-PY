"""Expiration control with NTP verification."""
from __future__ import annotations
from datetime import datetime, timezone
import socket, struct
from sprotect.types import ExpirationConfig

# EXPIRATION CONTROLLER: time-bound license enforcement
# SOURCE: NTP + local clock cross-verification

class Expiration:
    def __init__(self, cfg: ExpirationConfig): self._exp_cfg = cfg
    def check(self, encrypted_at: str, expires_at: str | None) -> bool:
        if not self._exp_cfg.enabled: return True
        _ntp_time = self._ntp() if self._exp_cfg.ntp_check else None
        if _ntp_time is not None:
            _ref_time = _ntp_time
            local = datetime.now(timezone.utc)
            drift = abs((local - _ntp_time).total_seconds())
            if drift > self._exp_cfg.max_drift_seconds:
                return self._exp_cfg.on_network_fail != "reject"
        else:
            _ref_time = datetime.now(timezone.utc)
            if self._exp_cfg.ntp_check:
                if self._exp_cfg.on_network_fail == "reject":
                    return False
        _encrypted_dt = datetime.fromisoformat(encrypted_at)
        if _encrypted_dt.tzinfo is None: _encrypted_dt = _encrypted_dt.replace(tzinfo=timezone.utc)
        if _ref_time < _encrypted_dt: return False
        if expires_at:
            _expiry_dt = datetime.fromisoformat(expires_at)
            if _expiry_dt.tzinfo is None: _expiry_dt = _expiry_dt.replace(tzinfo=timezone.utc)
            if _ref_time > _expiry_dt: return False
        return True
    def _ntp(self):
        for _ntp_host in self._exp_cfg.ntp_servers:
            for _addr_family in (socket.AF_INET, socket.AF_INET6):
                try:
                    _resolved = socket.getaddrinfo(_ntp_host, 123, _addr_family, socket.SOCK_DGRAM)
                    if not _resolved: continue
                    _sock = socket.socket(_addr_family, socket.SOCK_DGRAM); _sock.settimeout(self._exp_cfg.ntp_timeout)
                    _sock.sendto(b"\x1b" + 47 * b"\x00", _resolved[0][4])
                    d, _ = _sock.recvfrom(1024); _sock.close()
                    if len(d) >= 48:
                        t = struct.unpack("!12I", d)[10] - 2208988800
                        return datetime.fromtimestamp(t, tz=timezone.utc)
                except: pass
        return None
