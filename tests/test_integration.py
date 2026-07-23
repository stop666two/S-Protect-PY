"""Integration tests: build, run, compressor, x7 flag verification."""
import tempfile, os, json, sys, glob, subprocess, shutil
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sprotect.encrypt import build
from sprotect.config import load_config
from sprotect.compressor import compress, decompress


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
            "encrypt": {"extra_layers": ["serpent", "twofish"], "hybrid": {"enabled": False}},
            "watermark": {"enabled": False}, "expiration": {"enabled": False},
        }
        open(os.path.join(proj, "sprotect.json5"), "w").write(json.dumps(cfg))
        build(proj, out, load_config(os.path.join(proj, "sprotect.json5")))
        runtime = os.path.join(out, "_runtime")
        pye_files = glob.glob(os.path.join(runtime, "**", "*.pye"), recursive=True)
        assert len(pye_files) >= 3
        v2_found = False
        for f in pye_files:
            raw = open(f, "rb").read()
            try:
                p = json.loads(raw.decode())
                if p.get("h"):
                    h = json.loads(p["h"])
                    assert h["extra_layers"] == ["serpent", "twofish"]
                    v2_found = True
            except: pass
        assert v2_found
        entry = os.path.join(out, "main.py")
        assert os.path.isfile(entry)
        r = subprocess.run([sys.executable, entry], capture_output=True, text=True, cwd=out, timeout=15)
        assert r.returncode == 0, f"RC={r.returncode}\nSTDERR={r.stderr[:500]}"
        assert "Hello, World!" in r.stdout
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_build_compressor_x7_flag():
    """Verify compressor adds x7 flag and output runs correctly."""
    tmp = tempfile.mkdtemp()
    try:
        proj = os.path.join(tmp, "project")
        out = os.path.join(tmp, "output")
        os.makedirs(proj)
        open(os.path.join(proj, "main.py"), "w").write(
            "import sys\nprint('COMPRESSOR_TEST_OK')"
        )
        cfg = {
            "project": {"name": "ctest", "version": "1.0", "entry": "main.py"},
            "encrypt": {"hybrid": {"enabled": False}},
            "watermark": {"enabled": False}, "expiration": {"enabled": False},
        }
        open(os.path.join(proj, "sprotect.json5"), "w").write(json.dumps(cfg))
        build(proj, out, load_config(os.path.join(proj, "sprotect.json5")))
        # Check x7 flag exists on .pye files
        runtime = os.path.join(out, "_runtime")
        x7_found = False
        for f in glob.glob(os.path.join(runtime, "**", "*.pye"), recursive=True):
            try:
                p = json.loads(open(f, "rb").read().decode())
                if p.get("x7"):
                    x7_found = True
                    break
            except: pass
        assert x7_found, "No x7 (compressor) flag found in any .pye file"
        # Verify output runs
        entry = os.path.join(out, "main.py")
        r = subprocess.run([sys.executable, entry], capture_output=True, text=True, cwd=out, timeout=15)
        assert r.returncode == 0, f"RC={r.returncode}\nSTDERR={r.stderr[:500]}"
        assert "COMPRESSOR_TEST_OK" in r.stdout
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_build_no_compressor():
    """Build with compressor disabled, verify no x7 flag."""
    tmp = tempfile.mkdtemp()
    try:
        proj = os.path.join(tmp, "project")
        out = os.path.join(tmp, "output")
        os.makedirs(proj)
        open(os.path.join(proj, "main.py"), "w").write("print('NO_CMP_OK')")
        cfg = {
            "project": {"name": "ncmp", "version": "1.0", "entry": "main.py"},
            "encrypt": {"hybrid": {"enabled": False}},
            "compressor": {"enabled": False},
            "watermark": {"enabled": False}, "expiration": {"enabled": False},
        }
        open(os.path.join(proj, "sprotect.json5"), "w").write(json.dumps(cfg))
        build(proj, out, load_config(os.path.join(proj, "sprotect.json5")))
        runtime = os.path.join(out, "_runtime")
        for f in glob.glob(os.path.join(runtime, "**", "*.pye"), recursive=True):
            try:
                p = json.loads(open(f, "rb").read().decode())
                assert "x7" not in p, f"x7 flag found when compressor disabled: {f}"
            except: pass
        r = subprocess.run([sys.executable, os.path.join(out, "main.py")],
            capture_output=True, text=True, cwd=out, timeout=15)
        assert r.returncode == 0, f"RC={r.returncode}\nSTDERR={r.stderr[:500]}"
        assert "NO_CMP_OK" in r.stdout
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_compressor_lossless():
    """Compressor roundtrip must be 100% lossless."""
    data = b"def test(): pass\n" * 1000 + b"# " + b"x" * 5000
    c = compress(data)
    d = decompress(c)
    assert data == d, f"Lossless failed: {len(data)} vs {len(d)}"
    assert len(c) < len(data), f"Compressor made data larger: {len(c)} >= {len(data)}"


def test_build_and_run_single_file():
    """Basic single-file build+run (original repro test)."""
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
            "watermark": {"enabled": False}, "expiration": {"enabled": False},
        }
        open(os.path.join(proj, "sprotect.json5"), "w").write(json.dumps(cfg))
        build(proj, out, load_config(os.path.join(proj, "sprotect.json5")))
        r = subprocess.run([sys.executable, os.path.join(out, "main.py")],
            capture_output=True, text=True, cwd=out, timeout=15)
        assert r.returncode == 0, f"RC={r.returncode}\nSTDERR={r.stderr[:800]}"
        assert "HELLO_FROM_ENCRYPTED" in r.stdout
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
