"""KeyVault core: minefield key pool with PID-binding and decoy payloads."""
from __future__ import annotations
import os, hashlib, hmac, json, secrets, struct, zlib
from dataclasses import dataclass, field
from typing import Optional
from sprotect.keyvault.config import KeyVaultConfig
from sprotect.crypto import aes_encrypt


@dataclass
class VaultData:
    key_pool: list[bytes] = field(default_factory=list)
    real_position: int = 0
    xor_mask: bytes = b""
    index_seed: str = ""
    payloads: list[bytes] = field(default_factory=list)
    decoy_sources: list[str] = field(default_factory=list)


def _compute_key_position(project_fingerprint: str, pool_size: int) -> int:
    h = int(hashlib.sha256(project_fingerprint.encode()).hexdigest()[:8], 16)
    return h % pool_size


def _generate_decoy_source() -> str:
    """Generate valid-looking Python source that compiles but is harmless."""
    tmpl = secrets.choice([
        'def {f}():\n    return "{s}"\n',
        'x = "{s}"\nprint(x)\n',
        'import hashlib\nh = hashlib.sha256(b"{s}").hexdigest()\n',
        'import os\nprint(os.path.basename(__file__))\n',
        'def compute(n):\n    return n * {n} + {m}\n',
        'data = [{a}, {b}, {c}]\ntotal = sum(data)\n',
    ])
    return tmpl.format(
        f=secrets.token_hex(4),
        s=secrets.token_hex(16),
        n=secrets.randbelow(999),
        m=secrets.randbelow(999),
        a=secrets.randbelow(1000),
        b=secrets.randbelow(1000),
        c=secrets.randbelow(1000),
    )


def _generate_decoy_encrypted(decoy_source: str, decoy_key: bytes) -> bytes:
    """Encrypt a decoy source with a decoy key, producing valid ciphertext."""
    compressed = zlib.compress(decoy_source.encode(), 9)
    return aes_encrypt(compressed, decoy_key)


def generate_vault(real_key: bytes, cfg: KeyVaultConfig,
                   project_fingerprint: str) -> VaultData:
    if not cfg.enabled:
        return VaultData(key_pool=[real_key], real_position=0,
                         xor_mask=b"", index_seed="")
    pool_n = cfg.pool_size
    decoy_keys = [os.urandom(32) for _ in range(pool_n - 1)]
    real_pos = _compute_key_position(project_fingerprint, pool_n)
    all_keys = decoy_keys[:real_pos] + [real_key] + decoy_keys[real_pos:]
    mask = bytes.fromhex(cfg.xor_mask_hex.replace(" ", "")) if cfg.xor_mask_hex else b""
    # Generate decoy payloads for all DECOY keys
    decoy_sources = [_generate_decoy_source() for _ in range(pool_n - 1)]
    decoy_payloads = []
    for i, dk in enumerate(decoy_keys):
        decoy_payloads.append(_generate_decoy_encrypted(decoy_sources[i], dk))
    # Insert placeholder for real key payload (filled by caller)
    all_payloads = decoy_payloads[:real_pos] + [b"REAL"] + decoy_payloads[real_pos:]
    all_sources = decoy_sources[:real_pos] + [""] + decoy_sources[real_pos:]
    return VaultData(key_pool=all_keys, real_position=real_pos,
                     xor_mask=mask, payloads=all_payloads,
                     decoy_sources=all_sources)


def resolve_vault_key_from_loader(
    key_pool_hex: list[str], real_position: int, xor_mask_hex: str,
    index_seed: str, pid_binding: bool, pid_salt: str, current_pid: int,
) -> Optional[bytes]:
    key_hex = key_pool_hex[real_position]
    k = bytes.fromhex(key_hex)
    mask = bytes.fromhex(xor_mask_hex) if xor_mask_hex else b""
    if mask:
        k = bytes(k[i] ^ mask[i % len(mask)] for i in range(32))
    if pid_binding:
        deriver = hmac.new(k, digestmod="sha256")
        deriver.update(struct.pack("<I", current_pid))
        deriver.update(pid_salt.encode())
        k = deriver.digest()
    return k
