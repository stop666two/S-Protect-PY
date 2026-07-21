"""Tests for expiration payload generation and runtime checking.

All test artifacts are created inside the project's _test_temp directory.

Author: S-Protect Team
Version: 0.1.0
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from sprotect.features.expiration import generate_expiration_payload
from sprotect.runtime.expiration import ExpirationChecker
from sprotect.types import ExpirationConfig


def _checker(ntp_check: bool = False, on_network_fail: str = "allow") -> ExpirationChecker:
    return ExpirationChecker(ExpirationConfig(
        enabled=True,
        expires_at=None,
        ntp_check=ntp_check,
        on_network_fail=on_network_fail,
    ))


def test_not_expired() -> None:
    """Current time within valid window passes check."""
    now = datetime.now(timezone.utc)
    encrypted_at = (now - timedelta(days=1)).isoformat()
    expires_at = (now + timedelta(days=7)).isoformat()

    checker = _checker()
    assert checker.check_expiration(encrypted_at, expires_at)


def test_expired() -> None:
    """Current time past expiration returns False."""
    now = datetime.now(timezone.utc)
    encrypted_at = (now - timedelta(days=14)).isoformat()
    expires_at = (now - timedelta(days=7)).isoformat()

    checker = _checker()
    assert not checker.check_expiration(encrypted_at, expires_at)


def test_anti_rollback() -> None:
    """Current time before encrypted_at (rollback) returns False."""
    now = datetime.now(timezone.utc)
    encrypted_at = (now + timedelta(days=1)).isoformat()
    expires_at = (now + timedelta(days=7)).isoformat()

    checker = _checker()
    assert not checker.check_expiration(encrypted_at, expires_at)


def test_generate_expiration_payload_returns_dict() -> None:
    """Payload generation returns correct dict structure."""
    payload = generate_expiration_payload(
        expires_at="2026-12-31T23:59:59",
        encrypted_at="2026-01-01T00:00:00",
    )
    assert payload["expires_at"] == "2026-12-31T23:59:59"
    assert payload["encrypted_at"] == "2026-01-01T00:00:00"
