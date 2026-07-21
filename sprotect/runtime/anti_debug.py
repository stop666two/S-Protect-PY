"""Runtime anti-debugging and self-destruction module.

Detects debuggers, tracing, and virtual machine environments at
runtime, then takes configurable action (warn / exit / corrupt).

P6 Task 6-1: Anti-debug detection + self-destruction.

Author: S-Protect Team
Version: 0.1.0
"""

from __future__ import annotations

import gc
import os
import random
import sys
from typing import Any

from sprotect.types import AntiDebugAction, AntiDebugConfig


class AntiDebug:
    """Runtime anti-debugging detection and response.

    Performs multiple detection checks based on the configuration
    and executes the configured action on detection.

    Args:
        config: Anti-debug configuration.
    """

    def __init__(self, config: AntiDebugConfig) -> None:
        self.config = config
        self._detected: list[str] = []

    def run_checks(self) -> bool:
        """Run all enabled detection checks.

        Returns:
            True if environment is safe, False if detection triggered.
        """
        if not self.config.enabled:
            return True

        self._detected.clear()

        check_map: dict[str, Any] = {
            "pdb": self._check_pdb_check,
            "ptrace": self._check_ptrace_check,
            "debugger": self._check_debugger_detect,
            "vm": self._check_vm_detect,
        }

        for check_name in self.config.checks:
            checker = check_map.get(check_name)
            if checker is None:
                continue
            if checker():
                self._detected.append(check_name)

        if self._detected:
            for name in self._detected:
                self._take_action(name)
            return False

        return True

    def _check_pdb_check(self) -> bool:
        """Detect Python-level tracer via ``sys.gettrace()``.

        Returns:
            True if a trace function is set.
        """
        return sys.gettrace() is not None

    def _check_ptrace_check(self) -> bool:
        """Detect ptrace-based debugger on Linux.

        Calls ``PTRACE_TRACEME``; returns True if a tracer is
        already attached (EPERM).

        Returns:
            True if ptrace indicates a debugger is attached.
        """
        if sys.platform != "linux":
            return False
        try:
            import ctypes
            libc = ctypes.CDLL(ctypes.util.find_library("c"), use_errno=True)
            result = libc.ptrace(0, 0, 0, 0)  # PTRACE_TRACEME = 0
            if result == -1 and ctypes.get_errno() == 1:  # EPERM
                return True
        except Exception:
            pass
        return False

    def _check_debugger_detect(self) -> bool:
        """Detect common debugger indicators.

        Checks for pydevd (PyCharm), PYTHONDEBUG env, and
        ``sys.flags.debug``.

        Returns:
            True if any debugger indicator is found.
        """
        if "pydevd" in sys.modules:
            return True
        if os.environ.get("PYTHONDEBUG"):
            return True
        if sys.flags.debug:
            return True
        return False

    def _check_vm_detect(self) -> bool:
        """Detect virtual machine environments.

        Cross-platform check using CPU info, DMI tables (Linux),
        and common VM artifacts.

        Returns:
            True if a VM is detected.
        """
        try:
            if sys.platform == "linux":
                if os.path.exists("/proc/cpuinfo"):
                    with open("/proc/cpuinfo") as f:
                        for line in f:
                            if "hypervisor" in line and "flags" in line:
                                return True

                for dmi_path, keywords in [
                    ("/sys/class/dmi/id/product_name", [
                        "VirtualBox", "VMware", "KVM", "QEMU",
                        "Virtual Machine", "Bochs", "Xen",
                    ]),
                    ("/sys/class/dmi/id/sys_vendor", [
                        "QEMU", "innotek", "Oracle Corporation", "VMware",
                    ]),
                    ("/sys/class/dmi/id/product_version", [
                        "VirtualBox", "VMware", "KVM",
                    ]),
                ]:
                    if os.path.exists(dmi_path):
                        with open(dmi_path) as f:
                            val = f.read().strip()
                        if any(k in val for k in keywords):
                            return True

            elif sys.platform == "win32":
                import platform
                if platform.processor() and platform.processor().lower() in (
                    "virtual", "vmware", "qemu",
                ):
                    return True

        except Exception:
            pass

        return False

    def _take_action(self, check_name: str) -> None:
        """Execute the configured response action.

        Args:
            check_name: Name of the check that triggered detection.
        """
        action = self.config.action
        if action == AntiDebugAction.WARN:
            print(f"[AntiDebug] WARNING: Debugger detected ({check_name})", file=sys.stderr)
        elif action == AntiDebugAction.CORRUPT:
            self._memory_corrupt()
            self._memory_wipe()
            print(f"[AntiDebug] Memory corrupted ({check_name})", file=sys.stderr)
        elif action == AntiDebugAction.EXIT:
            self._memory_wipe()
            print(f"[AntiDebug] Debugger detected ({check_name}) - exiting", file=sys.stderr)
            sys.exit(1)

    def _memory_wipe(self) -> None:
        """Zero-fill mutable memory objects tracked by GC.

        Note: ``bytearray`` objects are not GC-tracked in Python
        3.12+, so this primarily clears containers (list, dict)
        that held references to sensitive data.
        """
        for obj in gc.get_objects():
            if isinstance(obj, bytearray):
                try:
                    obj[:] = b"\x00" * len(obj)
                except Exception:
                    pass

    def _memory_corrupt(self) -> None:
        """Randomly overwrite portions of GC-tracked mutable memory."""
        for obj in gc.get_objects():
            if isinstance(obj, bytearray):
                try:
                    length = len(obj)
                    if length == 0:
                        continue
                    for _ in range(min(max(1, length // 4), 64)):
                        obj[random.randint(0, length - 1)] = random.randint(0, 255)
                except Exception:
                    pass
