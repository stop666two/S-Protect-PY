"""KeyVault integration test: build with vault enabled and verify output."""
import os, sys, json, subprocess, tempfile, shutil, glob
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sprotect.encrypt import build
from sprotect.config import load_config
from sprotect.keyvault import (
    KeyVaultConfig, generate_vault, resolve_vault_key_from_loader,
)


def test_keyvault_module_unit():
    real_key = os.urandom(32)
    cfg = KeyVaultConfig(enabled=True, pool_size=64, pid_binding=True)
    vault = generate_vault(real_key, cfg, "test-fingerprint")
    assert len(vault.key_pool) == 64
    assert vault.key_pool[vault.real_position] == real_key


def test_keyvault_pid_binding():
    real_key = os.urandom(32)
    cfg = KeyVaultConfig(enabled=True, pool_size=16, pid_binding=True)
    vault = generate_vault(real_key, cfg, "pid-test")
    pool_hex = [k.hex() for k in vault.key_pool]

    k1 = resolve_vault_key_from_loader(
        pool_hex, vault.real_position, vault.xor_mask.hex(),
        "pid-test", True, "0xDEADBEEF", 12345,
    )
    k2 = resolve_vault_key_from_loader(
        pool_hex, vault.real_position, vault.xor_mask.hex(),
        "pid-test", True, "0xDEADBEEF", 67890,
    )
    assert k1 != k2, "Different PIDs must produce different keys"


def test_keyvault_no_pid():
    real_key = os.urandom(32)
    cfg = KeyVaultConfig(enabled=True, pool_size=16, pid_binding=False)
    vault = generate_vault(real_key, cfg, "no-pid-test")
    pool_hex = [k.hex() for k in vault.key_pool]
    resolved = resolve_vault_key_from_loader(
        pool_hex, vault.real_position, vault.xor_mask.hex(),
        "no-pid-test", False, "", 0,
    )
    expected = bytes(real_key[i] ^ vault.xor_mask[i % len(vault.xor_mask)]
                     for i in range(32))
    assert resolved == expected, "No-PID mode should return XOR-unmasked real key"


def test_build_and_run_with_vault():
    tmp = tempfile.mkdtemp()
    try:
        proj = os.path.join(tmp, "project")
        out = os.path.join(tmp, "output")
        os.makedirs(proj)
        open(os.path.join(proj, "main.py"), "w").write('print("VAULT_OK")')
        open(os.path.join(proj, "mod.py"), "w").write("x = 42")
        cfg = {
            "project": {"name": "vtest", "version": "1.0", "entry": "main.py"},
            "encrypt": {"extra_layers": [], "hybrid": {"enabled": False}},
            "watermark": {"enabled": False},
            "expiration": {"enabled": False},
            "keyvault": {"enabled": True, "pool_size": 128, "pid_binding": True},
        }
        open(os.path.join(proj, "sprotect.json5"), "w").write(json.dumps(cfg))
        build(proj, out, load_config(os.path.join(proj, "sprotect.json5")))
        r = subprocess.run(
            [sys.executable, os.path.join(out, "main.py")],
            capture_output=True, text=True, cwd=out, timeout=15,
        )
        assert r.returncode == 0, f"RC={r.returncode}\nSTDERR={r.stderr[:500]}"
        assert "VAULT_OK" in r.stdout, f"Unexpected output: {r.stdout}"
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
