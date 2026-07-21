"""Expiration payload generation for S-Protect-PY.

Generates the timestamp payload that is embedded during encryption
and later checked at runtime.

Author: S-Protect Team
Version: 0.1.0
"""

from __future__ import annotations

from typing import Any


def generate_expiration_payload(expires_at: str, encrypted_at: str) -> dict[str, Any]:
    """Generate an expiration timestamp payload.

    Args:
        expires_at: ISO-8601 datetime string indicating when the
                    encrypted project should expire.
        encrypted_at: ISO-8601 datetime string indicating when the
                      encryption was performed (used for rollback
                      prevention).

    Returns:
        A dictionary with ``expires_at`` and ``encrypted_at`` keys.
    """
    return {
        "expires_at": expires_at,
        "encrypted_at": encrypted_at,
    }
