"""License key generation and verification system."""

from __future__ import annotations
import os, json, base64, hashlib, hmac, secrets, time
from datetime import datetime, timezone
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class LicenseConfig:
    """许可配置"""
    enabled: bool = False
    public_key_path: str = "license_pub.pem"
    bind_hardware: bool = False
    grace_period_days: int = 7


@dataclass
class LicenseData:
    """许可证数据"""
    issued_to: str = ""
    expires_at: str = ""
    features: list[str] = field(default_factory=list)
    machine_id: str = ""
    issued_at: str = ""
    signature: str = ""


def _machine_id() -> str:
    """Generate machine fingerprint for binding."""
    import platform, uuid
    raw = f"{platform.processor()}|{uuid.uuid4().hex[:8]}|{platform.node()}"
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


def generate(signing_key_pem: bytes | None = None) -> tuple[bytes, bytes]:
    """Generate RSA signing keypair. Returns (public_key, private_key)."""
    from Cryptodome.PublicKey import RSA
    key = RSA.generate(2048)
    return key.publickey().export_key(), key.export_key()


def create_license(data: dict, private_key_pem: bytes) -> str:
    """Create a signed license JSON string.

    Args:
        data: dict with keys: issued_to, expires_at (ISO date), features (list)
        private_key_pem: RSA private key for signing
    Returns:
        Signed license string (base64 encoded JSON + signature)
    """
    from Cryptodome.PublicKey import RSA
    from Cryptodome.Signature import pkcs1_15
    from Cryptodome.Hash import SHA256

    payload = {
        "issued_to": data.get("issued_to", "unknown"),
        "expires_at": data.get("expires_at", ""),
        "features": data.get("features", []),
        "machine_id": data.get("machine_id", ""),
        "issued_at": datetime.now(timezone.utc).isoformat(),
    }
    payload_json = json.dumps(payload, separators=(",", ":"), sort_keys=True)
    payload_bytes = payload_json.encode()

    key = RSA.import_key(private_key_pem)
    h = SHA256.new(payload_bytes)
    signature = pkcs1_15.new(key).sign(h)

    result = {
        "payload": base64.b64encode(payload_bytes).decode(),
        "sig": base64.b64encode(signature).decode(),
    }
    return json.dumps(result, separators=(",", ":"))


def verify_license(license_str: str, public_key_pem: bytes) -> LicenseData | None:
    """Verify a signed license and return LicenseData if valid, None if invalid."""
    from Cryptodome.PublicKey import RSA
    from Cryptodome.Signature import pkcs1_15
    from Cryptodome.Hash import SHA256

    try:
        data = json.loads(license_str)
        payload_bytes = base64.b64decode(data["payload"])
        signature = base64.b64decode(data["sig"])

        key = RSA.import_key(public_key_pem)
        h = SHA256.new(payload_bytes)
        pkcs1_15.new(key).verify(h, signature)

        payload = json.loads(payload_bytes.decode())
        return LicenseData(
            issued_to=payload.get("issued_to", ""),
            expires_at=payload.get("expires_at", ""),
            features=payload.get("features", []),
            machine_id=payload.get("machine_id", ""),
            issued_at=payload.get("issued_at", ""),
            signature=data["sig"][:16],
        )
    except (ValueError, KeyError, json.JSONDecodeError, Exception):
        return None


def check_license(license_str: str, public_key_pem: bytes,
                  bind_hardware: bool = False,
                  grace_period_days: int = 7) -> tuple[bool, str]:
    """Full license check: verify signature + expiry + hardware binding.

    Returns: (is_valid, message)
    """
    lic = verify_license(license_str, public_key_pem)
    if lic is None:
        return False, "Invalid license signature"

    if lic.expires_at:
        try:
            expiry = datetime.fromisoformat(lic.expires_at)
            if expiry.tzinfo is None:
                expiry = expiry.replace(tzinfo=timezone.utc)
            now = datetime.now(timezone.utc)
            if now > expiry:
                remaining = (now - expiry).days
                if remaining > grace_period_days:
                    return False, f"License expired {remaining} days ago"
                return True, f"License expired, {grace_period_days - remaining} days grace remaining"
        except ValueError:
            return False, "Invalid expiry date in license"

    if bind_hardware and lic.machine_id:
        current_id = _machine_id()
        if lic.machine_id != current_id:
            return False, "License bound to different machine"

    return True, f"Valid license for {lic.issued_to}"
