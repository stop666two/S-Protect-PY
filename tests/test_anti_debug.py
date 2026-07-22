"""Tests for anti_debug and expiration modules."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sprotect.anti_debug import AntiDebug
from sprotect.types import AntiDebugConfig, AntiDebugAction

def test_anti_debug_init():
    cfg = AntiDebugConfig(enabled=True, action=AntiDebugAction.WARN, checks=["pdb"])
    ad = AntiDebug(cfg)
    assert ad is not None
    assert ad.cfg.action == AntiDebugAction.WARN

def test_anti_debug_disabled():
    cfg = AntiDebugConfig(enabled=True, checks=["pdb"])
    ad = AntiDebug(cfg)
    ad.cfg.checks = []
    assert ad.run()


from sprotect.expiration import Expiration
from sprotect.types import ExpirationConfig

def test_expiration_disabled():
    cfg = ExpirationConfig(enabled=False)
    exp = Expiration(cfg)
    assert exp.check("2026-01-01T00:00:00+00:00", None)

def test_expiration_not_yet_expired():
    cfg = ExpirationConfig(enabled=True, ntp_check=False)
    exp = Expiration(cfg)
    assert exp.check("2026-01-01T00:00:00+00:00", "2099-12-31T23:59:59Z")

def test_expiration_expired():
    cfg = ExpirationConfig(enabled=True, ntp_check=False)
    exp = Expiration(cfg)
    assert not exp.check("2020-01-01T00:00:00+00:00", "2021-01-01T00:00:00Z")

def test_expiration_encrypted_in_future():
    cfg = ExpirationConfig(enabled=True, ntp_check=False)
    exp = Expiration(cfg)
    assert not exp.check("2099-12-31T23:59:59+00:00", None)
