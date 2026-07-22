"""Anti-debug: debugger detection, anti-VM, anti-sandbox, trace blocking, anti-Cuckoo."""

from __future__ import annotations
import sys, os, platform, ctypes, gc, signal, struct, time

class AntiDebug:
    """Multi-layer anti-debugging and environment detection.

    Detection layers:
    - Debugger: pdb, pydevd, sys.gettrace, ptrace, IDA/Ghidra remote
    - VM: VirtualBox, VMware, QEMU, KVM, Hyper-V, Xen
    - Sandbox: Cuckoo, JoeSandbox, VMRay, debugging VMs
    - Trace blocking: prevent sys.settrace/sys.setprofile from being used
    - Timing: detect slow execution (sign of sandbox stepping)
    """

    def __init__(self, cfg):
        self.cfg = cfg
        self._block_trace = False

    def run(self) -> bool:
        for c in self.cfg.checks:
            fn = getattr(self, f"_chk_{c}", None)
            if fn and fn(): self._act(c); return False
        return True

    def block_tracing(self):
        """Block sys.settrace and sys.setprofile to prevent debugging."""
        self._block_trace = True
        try:
            import __builtins__
            if hasattr(sys, "settrace"):
                sys.settrace(None)
            if hasattr(sys, "setprofile"):
                sys.setprofile(None)
        except: pass

    def _chk_pdb(self):
        return sys.gettrace() is not None

    def _chk_ptrace(self):
        if platform.system() == "Linux":
            try: return ctypes.CDLL("libc.so.6", use_errno=True).ptrace(0, 0, 0, 0) == -1
            except: return False
        if platform.system() == "Windows":
            try:
                ntdll = ctypes.WinDLL("ntdll.dll", use_last_error=True)
                info = ctypes.c_ulong()
                h = ctypes.windll.kernel32.GetCurrentProcess()
                STATUS_INFO_LEN_MISMATCH = 0xC0000004
                ret = ntdll.NtQueryInformationProcess(h, 7, ctypes.byref(info), ctypes.sizeof(info), None)
                return ret != STATUS_INFO_LEN_MISMATCH and info.value != 0
            except: pass
            try:
                k32 = ctypes.WinDLL("kernel32.dll", use_last_error=True)
                is_dbg = ctypes.c_bool()
                k32.CheckRemoteDebuggerPresent(k32.GetCurrentProcess(), ctypes.byref(is_dbg))
                return is_dbg.value
            except: pass
        return False

    def _chk_debugger(self):
        if sys.gettrace() is not None: return True
        if "pydevd" in sys.modules: return True
        if "PYTHONDEBUG" in os.environ or sys.flags.debug: return True
        if "_PYTEST_RAISE" in os.environ: return True
        return False

    def _chk_vm(self):
        if platform.system() == "Windows":
            try:
                k32 = ctypes.WinDLL("kernel32.dll", use_last_error=True)
                buf = ctypes.create_string_buffer(256); sz = ctypes.c_uint32(256)
                if k32.GetModuleBaseNameA(0, 0, buf, sz) > 0:
                    n = buf.value.decode().lower()
                    if any(v in n for v in ["vbox","vmware","qemu","xen","hyper","kvm"]): return True
            except: pass
        for d in ["/sys/class/dmi/id/product_name","/sys/class/dmi/id/sys_vendor",
                   "/proc/sys/kernel/ostype"]:
            if os.path.isfile(d):
                try:
                    v = open(d).read().lower()
                    if any(x in v for x in ["virtualbox","vmware","qemu","kvm",
                                              "microsoft","xen","hyper-v"]): return True
                except: pass
        return False

    def _chk_sandbox(self):
        """Detect common malware analysis sandboxes."""
        if platform.system() == "Windows":
            for ind in ["analysis", "sandbox", "malware"]:
                p = os.path.join(os.environ.get("SYSTEMDRIVE", "C:") + "\\", ind)
                if os.path.isdir(p): return True
            ud = os.environ.get("USERPROFILE", "")
            if ud:
                for ind in ["Desktop\\analysis", "Sandbox", "Malware"]:
                    if os.path.isdir(os.path.join(ud, ind)): return True
        if os.path.isfile("/proc/sys/kernel/ostype"):
            try:
                with open("/proc/sys/kernel/ostype") as f:
                    if "bsd" in f.read().lower(): return True
            except: pass
        return False

    def _chk_timing(self):
        """Detect if execution is unusually slow (sandbox stepping)."""
        t = time.time()
        _ = [i * i for i in range(100000)]
        elapsed = time.time() - t
        return elapsed > 2.0

    def _chk_cuckoo(self):
        """Detect Cuckoo sandbox specific artifacts."""
        for ind in ["/tmp/cuckoo", "/tmp/analysis"]:
            if os.path.isdir(ind): return True
        sd = os.environ.get("SYSTEMDRIVE", "C:")
        for ind in ["cuckoo", "analysis", "sandbox"]:
            if os.path.isdir(os.path.join(sd + "\\", ind)): return True
        cuckoo_procs = ["cuckoo", "sandboxie", "joe"]
        if platform.system() == "Windows":
            try:
                k32 = ctypes.WinDLL("kernel32.dll", use_last_error=True)
                buf = ctypes.create_string_buffer(256); sz = ctypes.c_uint32(256)
                if k32.GetModuleBaseNameA(0, 0, buf, sz) > 0:
                    n = buf.value.decode().lower() if buf.value else ""
                    if any(c in n for c in cuckoo_procs): return True
            except: pass
        return False

    def _chk_ida(self):
        """Detect IDA Pro / Ghidra remote debugging connections."""
        import socket
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.1)
            for port in [23946, 23947, 8000, 8001, 31337, 31338]:
                try:
                    if s.connect_ex(("127.0.0.1", port)) == 0:
                        s.close()
                        return True
                except: pass
            s.close()
        except: pass
        return False

    def _chk_procmon(self):
        """Detect process monitoring tools."""
        proc_indicators = ["procmon", "processhacker", "wireshark",
                           "tcpview", "apimonitor", "regmon", "filemon"]
        if platform.system() == "Windows":
            try:
                k32 = ctypes.WinDLL("kernel32.dll", use_last_error=True)
                buf = ctypes.create_string_buffer(256); sz = ctypes.c_uint32(256)
                if k32.GetModuleBaseNameA(0, 0, buf, sz) > 0:
                    n = buf.value.decode().lower() if buf.value else ""
                    if any(p in n for p in proc_indicators): return True
            except: pass
        return False

    def _act(self, c: str):
        if not hasattr(self, "cfg") or self.cfg.action.value == "exit":
            self._wipe(); os._exit(1)
        elif self.cfg.action.value == "warn":
            print(f"[S-Protect] Warning: {c}")
        elif self.cfg.action.value == "corrupt":
            self._corrupt(); os._exit(1)

    def _wipe(self):
        for o in gc.get_objects():
            try:
                if isinstance(o, (bytes, bytearray)) and len(o) < 100000:
                    try: o[:] = b"\x00" * len(o)
                    except: pass
            except: pass
        gc.collect()

    def _corrupt(self):
        import random
        for o in gc.get_objects():
            try:
                if isinstance(o, bytearray) and len(o) < 100000:
                    for i in range(len(o)): o[i] = random.randint(0, 255)
            except: pass
