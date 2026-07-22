"""Verify build + run works (single module, no imports)."""
import os, sys, json, subprocess, tempfile, shutil
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sprotect.encrypt import build
from sprotect.config import load_config


def test_build_and_run_single_file():
    tmp = tempfile.mkdtemp()
    try:
        proj = os.path.join(tmp, "project")
        out = os.path.join(tmp, "output")
        os.makedirs(proj)
        open(os.path.join(proj, "main.py"), "w").write('print("HELLO_FROM_ENCRYPTED")')
        open(os.path.join(proj, "mod.py"), "w").write("x = 1")
        cfg = {
            "project": {"name": "t", "version": "1.0", "entry": "main.py"},
            "encrypt": {"extra_layers": [], "hybrid": {"enabled": False}},
            "watermark": {"enabled": False},
            "expiration": {"enabled": False},
        }
        open(os.path.join(proj, "sprotect.json5"), "w").write(json.dumps(cfg))
        build(proj, out, load_config(os.path.join(proj, "sprotect.json5")))

        r = subprocess.run(
            [sys.executable, os.path.join(out, "main.py")],
            capture_output=True, text=True, cwd=out, timeout=15,
        )
        assert r.returncode == 0, (
            f"RC={r.returncode}\nSTDERR: {r.stderr[:800]}\nSTDOUT: {r.stdout}"
        )
        assert "HELLO_FROM_ENCRYPTED" in r.stdout
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
