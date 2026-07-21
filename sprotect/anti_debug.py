"""Anti-debug detection and anti-VM."""

from __future__ import annotations
import sys, os, platform, ctypes, gc
from sprotect.types import AntiDebugConfig, AntiDebugAction

class AntiDebug:
    def __init__(self, cfg: AntiDebugConfig): self.cfg = cfg

    def run(self) -> bool:
        for c in self.cfg.checks:
            fn = getattr(self, f"_chk_{c}", None)
            if fn and fn(): self._act(c); return False
        return True

    def _chk_pdb(self): return sys.gettrace() is not None
    def _chk_ptrace(self):
        if platform.system() != "Linux": return False
        try: return ctypes.CDLL("libc.so.6").ptrace(0, 0, 0, 0) == -1
        except: return False
    def _chk_debugger(self):
        return (sys.gettrace() is not None or "pydevd" in sys.modules
                or "PYTHONDEBUG" in os.environ or sys.flags.debug)
    def _chk_vm(self):
        if platform.system() == "Windows":
            try:
                k32 = ctypes.WinDLL("kernel32.dll", use_last_error=True)
                b = ctypes.create_string_buffer(256); s = ctypes.c_uint32(256)
                if k32.GetModuleBaseNameA(0, 0, b, s) > 0:
                    n = b.value.decode().lower()
                    if any(v in n for v in ["vbox","vmware","qemu","xen","hyper"]): return True
            except: pass
        try:
            for d in ["/sys/class/dmi/id/product_name", "/sys/class/dmi/id/sys_vendor"]:
                if os.path.isfile(d):
                    v = open(d).read().lower()
                    if any(x in v for x in ["virtualbox","vmware","qemu","kvm"]): return True
        except: pass
        return False

    def _act(self, c: str):
        a = self.cfg.action
        if a == AntiDebugAction.WARN: print(f"[S-Protect] Warning: {c}")
        elif a == AntiDebugAction.EXIT: self._wipe(); os._exit(1)
        elif a == AntiDebugAction.CORRUPT: self._corrupt(); os._exit(1)

    def _wipe(self):
        for o in gc.get_objects():
            try:
                if isinstance(o, (bytes, bytearray)): o[:] = b"\x00" * len(o)
            except: pass
        gc.collect()

    def _corrupt(self):
        import random
        for o in gc.get_objects():
            try:
                if isinstance(o, bytearray):
                    for i in range(len(o)): o[i] = random.randint(0, 255)
            except: pass
