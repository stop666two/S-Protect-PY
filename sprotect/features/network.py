"""NTP network time utility for S-Protect-PY.

Provides NTP time fetching from public time servers with
configurable fallback and timeout handling.

Author: S-Protect Team
Version: 0.1.0
"""

from __future__ import annotations

import socket
import struct
import time
from datetime import datetime, timezone
from typing import Optional

_NTP_DEFAULT_SERVERS = [
    "pool.ntp.org",
    "time.google.com",
    "time.cloudflare.com",
]

_NTP_PORT = 123
_NTP_TIMEOUT = 3
_NTP_EPOCH_OFFSET = 2208988800


def fetch_ntp_time(servers: Optional[list[str]] = None) -> Optional[datetime]:
    """Fetch the current NTP time from one of the given servers.

    Iterates through the server list and returns the first successful
    response as a timezone-aware UTC datetime.  Returns ``None`` if
    all servers are unreachable or return invalid data.

    Args:
        servers: List of NTP server hostnames.  Defaults to
                 ``[pool.ntp.org, time.google.com, time.cloudflare.com]``.

    Returns:
        A timezone-aware UTC datetime, or None on failure.
    """
    if servers is None:
        servers = _NTP_DEFAULT_SERVERS

    request_data = b"\x1b" + 47 * b"\x00"

    for server in servers:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(_NTP_TIMEOUT)
            sock.sendto(request_data, (server, _NTP_PORT))
            response, _ = sock.recvfrom(1024)
            sock.close()

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
            try:
                sock.close()
            except Exception:
                pass

    return None
