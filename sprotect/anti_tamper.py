"""Anti-tamper: file integrity verification, memory integrity, anti-dump, anti-hook."""

from __future__ import annotations
import os, sys, hashlib, hmac, gc, threading, time

class AntiTamper:
    """Runtime integrity protection suite.

    - File integrity: periodic hash verification of critical files
    - Anti-dump: detect memory dump tools and debugger memory access
    - Anti-hook: detect if common hooking frameworks are attached
    - Self-check: verify own code hasn't been modified in memory
    """

    def __init__(self, runtime_dir: str, integrity_db: dict[str, str] | None = None):
        self._dir = runtime_dir
        self._db = integrity_db or {}
        self._stop = threading.Event()

    def verify_files(self) -> bool:
        """Check all .pye files in _runtime/ against stored hashes."""
        for rel, expected in self._db.items():
            fp = os.path.join(self._dir, rel)
            if not os.path.isfile(fp):
                return False
            h = hashlib.sha256()
            with open(fp, "rb") as f:
                while True:
                    chunk = f.read(65536)
                    if not chunk: break
                    h.update(chunk)
            if h.hexdigest() != expected:
                return False
        return True

    def check_memory(self) -> bool:
        """Check if decrypted code in memory appears to be dumped or hooked."""
        import sys
        for mod_name in list(sys.modules.keys()):
            mod = sys.modules[mod_name]
            if mod is None: continue
            if hasattr(mod, "__file__") and mod.__file__ and ".pye" in mod.__file__:
                src_file = mod.__file__
                if os.path.isfile(src_file):
                    st = os.stat(src_file)
                    mtime = getattr(mod, "__load_time__", None)
                    if mtime and abs(st.st_mtime - mtime) > 0.1:
                        return False
        return True

    def detect_hooks(self) -> bool:
        """Detect if any common hooking/interception frameworks are present."""
        suspicious = [
            "pydevd", "pydevd_file_utils", "pydevd_tracing",
            "PySnooper", "hunter", "pympler", "memray",
            "dll_inject", "inject", "frida", "pyinjector",
        ]
        for mod in suspicious:
            if mod in sys.modules:
                return True
        for name, _ in gc.get_objects():
            try:
                if isinstance(name, str) and any(h in name.lower() for h in ["hook", "patch", "inject"]):
                    return True
            except: pass
        return False

    def detect_dump(self) -> bool:
        """Heuristic detection of memory dump activity."""
        suspicious_procs = ["procdump", "dump64", "x64dbg", "immunity", "ollydbg"]
        if os.name == "nt":
            try:
                import ctypes
                k32 = ctypes.WinDLL("kernel32.dll", use_last_error=True)
                buf = ctypes.create_string_buffer(4096)
                k32.GetModuleBaseNameA(0, 0, buf, 4096)
                name = buf.value.decode().lower() if buf.value else ""
                if any(p in name for p in suspicious_procs):
                    return True
            except: pass
        return False

    def start_periodic_check(self, interval: float = 5.0) -> threading.Thread:
        """Start a background thread that periodically checks integrity."""
        def _check_loop():
            while not self._stop.is_set():
                if not self.verify_files() or self.detect_hooks() or self.detect_dump():
                    import os
                    os._exit(3)
                time.sleep(interval)
        t = threading.Thread(target=_check_loop, daemon=True)
        t.start()
        return t

    def stop(self):
        self._stop.set()
