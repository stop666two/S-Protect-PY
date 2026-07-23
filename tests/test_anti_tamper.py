from sprotect.anti_tamper import AntiTamper
import os, tempfile, threading, time, hashlib


def test_verify_files_empty_db():
    at = AntiTamper(tempfile.gettempdir(), {})
    assert at.verify_files() is True


def test_verify_files_missing_file():
    at = AntiTamper(tempfile.gettempdir(), {"nonexistent.pye": "abc123"})
    assert at.verify_files() is False


def test_verify_files_valid():
    with tempfile.TemporaryDirectory() as td:
        fp = os.path.join(td, "test.pye")
        with open(fp, "wb") as f:
            f.write(b"encrypted data")
        h = hashlib.sha256(b"encrypted data").hexdigest()
        at = AntiTamper(td, {"test.pye": h})
        assert at.verify_files() is True


def test_verify_files_tampered():
    with tempfile.TemporaryDirectory() as td:
        fp = os.path.join(td, "test.pye")
        with open(fp, "wb") as f:
            f.write(b"encrypted data")
        wrong_hash = "0" * 64
        at = AntiTamper(td, {"test.pye": wrong_hash})
        assert at.verify_files() is False


def test_verify_files_modified():
    with tempfile.TemporaryDirectory() as td:
        fp = os.path.join(td, "test.pye")
        with open(fp, "wb") as f:
            f.write(b"original")
        h = hashlib.sha256(b"original").hexdigest()
        at = AntiTamper(td, {"test.pye": h})
        assert at.verify_files() is True
        with open(fp, "wb") as f:
            f.write(b"modified")
        assert at.verify_files() is False


def test_check_memory_clean():
    at = AntiTamper(tempfile.gettempdir())
    assert at.check_memory() is True


def test_detect_hooks_clean():
    at = AntiTamper(tempfile.gettempdir())
    assert at.detect_hooks() is False


def test_detect_dump():
    at = AntiTamper(tempfile.gettempdir())
    result = at.detect_dump()
    assert isinstance(result, bool)


def test_start_stop_periodic_check():
    at = AntiTamper(tempfile.gettempdir(), {})
    t = at.start_periodic_check(interval=0.1)
    assert isinstance(t, threading.Thread)
    assert t.is_alive()
    time.sleep(0.3)
    at.stop()
    t.join(timeout=2)
    assert not t.is_alive()


def test_secure_zero():
    data = bytearray(b"secret data")
    AntiTamper.secure_zero(data)
    assert all(b == 0 for b in data)


def test_wipe_sensitive_runs_without_error():
    AntiTamper.wipe_sensitive()


def test_secure_zero_then_wipe():
    buf = bytearray(b"sensitive buffer")
    AntiTamper.secure_zero(buf)
    assert all(b == 0 for b in buf)


def test_virtual_protect():
    result = AntiTamper.virtual_protect()
    assert isinstance(result, bool)


def test_multi_file_integrity():
    with tempfile.TemporaryDirectory() as td:
        files = {}
        for name in ["mod1.pye", "mod2.pye", "mod3.pye"]:
            data = os.urandom(100)
            fp = os.path.join(td, name)
            with open(fp, "wb") as f:
                f.write(data)
            files[name] = hashlib.sha256(data).hexdigest()
        at = AntiTamper(td, files)
        assert at.verify_files() is True
        with open(os.path.join(td, "mod2.pye"), "wb") as f:
            f.write(os.urandom(100))
        assert at.verify_files() is False


def test_verify_files_large():
    with tempfile.TemporaryDirectory() as td:
        fp = os.path.join(td, "large.pye")
        data = os.urandom(10 * 1024 * 1024)
        with open(fp, "wb") as f:
            f.write(data)
        h = hashlib.sha256(data).hexdigest()
        at = AntiTamper(td, {"large.pye": h})
        assert at.verify_files() is True


def test_hooks_detection():
    at = AntiTamper(tempfile.gettempdir())
    import sys
    try:
        sys.modules["pydevd"] = type("mock", (), {})()
        assert at.detect_hooks() is True
    finally:
        sys.modules.pop("pydevd", None)
    assert at.detect_hooks() is False


def test_periodic_check_stops_cleanly():
    with tempfile.TemporaryDirectory() as td:
        fp = os.path.join(td, "safe.pye")
        with open(fp, "wb") as f:
            f.write(b"safe data")
        h = hashlib.sha256(b"safe data").hexdigest()
        at = AntiTamper(td, {"safe.pye": h})
        t = at.start_periodic_check(interval=0.05)
        time.sleep(0.2)
        assert t.is_alive()
        at.stop()
        t.join(timeout=3)
        assert not t.is_alive()


def test_secure_zero_empty():
    ba = bytearray()
    AntiTamper.secure_zero(ba)
    assert len(ba) == 0


def test_secure_zero_large():
    ba = bytearray(10000)
    AntiTamper.secure_zero(ba)
    assert all(b == 0 for b in ba)
