"""Integration test: build with extra_layers and verify output."""
import tempfile, os, json, sys, glob, subprocess, shutil
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sprotect.encrypt import build
from sprotect.config import load_config


def test_build_with_extra_layers():
    tmp = tempfile.mkdtemp()
    try:
        proj = os.path.join(tmp, "project")
        out = os.path.join(tmp, "output")
        os.makedirs(proj)

        open(os.path.join(proj, "main.py"), "w").write(
            "from helper import greet\nprint(greet(\"World\"))"
        )
        open(os.path.join(proj, "helper.py"), "w").write(
            "def greet(name):\n    return f\"Hello, {name}!\""
        )

        cfg = {
            "project": {"name": "test", "version": "1.0", "entry": "main.py"},
            "encrypt": {
                "algorithm": "aes-256-gcm",
                "extra_layers": ["serpent", "twofish"],
                "hybrid": {"enabled": False},
            },
            "watermark": {"enabled": False},
            "expiration": {"enabled": False},
        }
        open(os.path.join(proj, "sprotect.json5"), "w").write(json.dumps(cfg))
        build(proj, out, load_config(os.path.join(proj, "sprotect.json5")))

        runtime = os.path.join(out, "_runtime")
        pye_files = glob.glob(os.path.join(runtime, "**", "*.pye"), recursive=True)
        assert len(pye_files) >= 3, f"Expected >=3 .pye files, got {len(pye_files)}"

        v2_found = False
        for f in pye_files:
            raw = open(f, "rb").read()
            try:
                p = json.loads(raw.decode())
                if p.get("h"):
                    h = json.loads(p["h"])
                    assert h["extra_layers"] == ["serpent", "twofish"]
                    v2_found = True
            except (json.JSONDecodeError, UnicodeDecodeError):
                pass
        assert v2_found, "No v2 header found in any .pye file"

        entry = os.path.join(out, "main.py")
        assert os.path.isfile(entry), f"Entry file missing: {entry}"

        r = subprocess.run(
            [sys.executable, entry], capture_output=True, text=True, cwd=out, timeout=15,
        )
        assert r.returncode == 0, f"RC={r.returncode}\nSTDERR: {r.stderr[:500]}"
        assert "Hello, World!" in r.stdout, f"Unexpected output: {r.stdout}"
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
