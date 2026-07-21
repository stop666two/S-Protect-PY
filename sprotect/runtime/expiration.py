"""Runtime expiration checking for S-Protect-PY.

Checks system time against encrypted-at and expires-at timestamps
with optional NTP verification to prevent local clock tampering.

Author: S-Protect Team
Version: 0.1.0
"""

from __future__ import annotations

import socket
import struct
from datetime import datetime, timezone
from typing import Optional

from sprotect.types import ExpirationConfig

_NTP_SERVERS = ["pool.ntp.org", "time.google.com", "time.cloudflare.com"]
_NTP_PORT = 123
_NTP_TIMEOUT = 3
_NTP_EPOCH_OFFSET = 2208988800


class ExpirationChecker:
    """Runtime expiration checker.

    Validates that the current system time falls within the allowed
    window defined by ``encrypted_at`` (earliest) and ``expires_at``
    (latest).  Optionally cross-checks against NTP time.
    """

    def __init__(self, config: ExpirationConfig) -> None:
        """Initialize the checker with expiration configuration.

        Args:
            config: Expiration configuration.
        """
        self.config = config

    def check_expiration(
        self,
        encrypted_at: str,
        expires_at: Optional[str] = None,
    ) -> bool:
        """Check whether the current time is within the valid window.

        The system time must be >= ``encrypted_at`` (prevents rollback)
        and, if ``expires_at`` is set, <= ``expires_at``.

        If ``ntp_check`` is enabled in config, the system time is also
        validated against an NTP server.  On NTP failure the behaviour
        depends on ``on_network_fail`` in the config.

        Args:
            encrypted_at: ISO-8601 datetime of encryption.
            expires_at: Optional ISO-8601 datetime of expiration.

        Returns:
            True if the current time is valid, False otherwise.
        """
        now = datetime.now(timezone.utc)

        try:
            encrypted_dt = datetime.fromisoformat(encrypted_at)
            if encrypted_dt.tzinfo is None:
                encrypted_dt = encrypted_dt.replace(tzinfo=timezone.utc)
        except ValueError:
            return False

        if now < encrypted_dt:
            return False

        if expires_at is not None:
            try:
                expires_dt = datetime.fromisoformat(expires_at)
                if expires_dt.tzinfo is None:
                    expires_dt = expires_dt.replace(tzinfo=timezone.utc)
            except ValueError:
                return False
            if now > expires_dt:
                return False

        if self.config.ntp_check:
            ntp_time = self._check_ntp_time()
            if ntp_time is not None:
                diff = abs((now - ntp_time).total_seconds())
                if diff > 60:
                    return False
            elif self.config.on_network_fail == "reject":
                return False

        return True

    def _check_ntp_time(self) -> Optional[datetime]:
        """Fetch the current time from public NTP servers.

        Tries ``pool.ntp.org``, ``time.google.com``, and
        ``time.cloudflare.com`` with a 3-second timeout per server.
        Returns the first successful response or ``None``.

        Returns:
            A timezone-aware UTC datetime, or None on failure.
        """
        request_data = b"\x1b" + 47 * b"\x00"

        for server in _NTP_SERVERS:
            sock: Optional[socket.socket] = None
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.settimeout(_NTP_TIMEOUT)
                sock.sendto(request_data, (server, _NTP_PORT))
                response, _ = sock.recvfrom(1024)

                if len(response) < 40:
                    continue

                unpacked = struct.unpack("!12I", response)
                timestamp = unpacked[10] + float(unpacked[11]) / 2**32
                utc_time = datetime.fromtimestamp(
                    timestamp - _NTP_EPOCH_OFFSET, tz=timezone.utc
                )
                return utc_time
            except (socket.timeout, OSError, struct.error):
                continue
            finally:
                if sock is not None:
                    try:
                        sock.close()
                    except Exception:
                        pass

        return None
