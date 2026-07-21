import ctypes
import ctypes.wintypes
import sys
import os
import ssl
import secrets
import atexit
from config import WORKSPACE


def run_stress_checks():
    os.makedirs(WORKSPACE, exist_ok=True)

    try:
        libc = ctypes.CDLL("msvcrt.dll")
        libc.sqrt.argtypes = [ctypes.c_double]
        libc.sqrt.restype = ctypes.c_double
        result = libc.sqrt(ctypes.c_double(100.0))
        ok = abs(result - 10.0) < 0.001
        yield {
            "name": "ctypes 调用 C (msvcrt.sqrt)",
            "status": ok,
            "detail": f"sqrt(100)={result:.4f}" if ok else f"结果异常: {result}",
            "expect": "pass",
        }
    except Exception as e:
        yield {
            "name": "ctypes 调用 C (msvcrt.sqrt)",
            "status": False,
            "detail": str(e),
            "expect": "pass",
        }

    try:
        kernel32 = ctypes.WinDLL("kernel32.dll", use_last_error=True)
        class SYSTEM_INFO(ctypes.Structure):
            _fields_ = [
                ("wProcessorArchitecture", ctypes.c_uint16),
                ("wReserved", ctypes.c_uint16),
                ("dwPageSize", ctypes.c_uint32),
                ("lpMinimumApplicationAddress", ctypes.c_void_p),
                ("lpMaximumApplicationAddress", ctypes.c_void_p),
                ("dwActiveProcessorMask", ctypes.c_size_t),
                ("dwNumberOfProcessors", ctypes.c_uint32),
                ("dwProcessorType", ctypes.c_uint32),
                ("dwAllocationGranularity", ctypes.c_uint32),
                ("wProcessorLevel", ctypes.c_uint16),
                ("wProcessorRevision", ctypes.c_uint16),
            ]
        si = SYSTEM_INFO()
        kernel32.GetSystemInfo(ctypes.byref(si))
        ok = si.dwNumberOfProcessors > 0
        yield {
            "name": "ctypes Windows API (GetSystemInfo)",
            "status": ok,
            "detail": f"{si.dwNumberOfProcessors} 核, 页面大小 {si.dwPageSize}",
            "expect": "pass",
        }
    except Exception as e:
        yield {
            "name": "ctypes Windows API (GetSystemInfo)",
            "status": False,
            "detail": str(e),
            "expect": "pass",
        }

    try:
        frame = sys._getframe()
        ok = frame is not None and frame.f_code.co_name == "run_stress_checks"
        yield {
            "name": "sys._getframe() 栈帧获取",
            "status": ok,
            "detail": f"当前函数={frame.f_code.co_name}" if ok else "获取栈帧失败",
            "expect": "pass",
        }
    except Exception as e:
        yield {
            "name": "sys._getframe() 栈帧获取",
            "status": False,
            "detail": str(e),
            "expect": "pass",
        }

    try:
        depth = 0
        def recurse(n):
            nonlocal depth
            depth = n
            if n > 0:
                return recurse(n - 1)
            return "done"
        result = recurse(50)
        ok = result == "done" and depth == 0
        yield {
            "name": "递归深度 50 层",
            "status": ok,
            "detail": f"递归返回={result}, 底层深度={depth}" if ok else f"失败: {result}",
            "expect": "pass",
        }
    except Exception as e:
        yield {
            "name": "递归深度 50 层",
            "status": False,
            "detail": str(e),
            "expect": "pass",
        }

    try:
        count = 0
        for _ in range(100000):
            count += 1
        ok = count == 100000
        yield {
            "name": "大循环 10 万次",
            "status": ok,
            "detail": f"循环 {count} 次" if ok else f"计数异常: {count}",
            "expect": "pass",
        }
    except Exception as e:
        yield {
            "name": "大循环 10 万次",
            "status": False,
            "detail": str(e),
            "expect": "pass",
        }

    long_path = None
    try:
        long_name = "A" * 200 + "_end.txt"
        long_path = os.path.join(WORKSPACE, long_name)
        with open(long_path, "w", encoding="utf-8") as f:
            f.write("long path test")
        with open(long_path, "r", encoding="utf-8") as f:
            content = f.read()
        ok = content == "long path test"
        yield {
            "name": "超长路径 (200 字符)",
            "status": ok,
            "detail": f"路径长度={len(long_name)}, 读写{'成功' if ok else '失败'}",
            "expect": "pass",
        }
    except Exception as e:
        yield {
            "name": "超长路径 (200 字符)",
            "status": False,
            "detail": str(e),
            "expect": "pass",
        }
    finally:
        if long_path and os.path.exists(long_path):
            os.remove(long_path)

    try:
        ctx = ssl.create_default_context()
        ok = ctx.protocol >= ssl.PROTOCOL_TLS_CLIENT
        yield {
            "name": "ssl 默认 TLS 上下文",
            "status": ok,
            "detail": f"协议版本={ctx.protocol}",
            "expect": "pass",
        }
    except Exception as e:
        yield {
            "name": "ssl 默认 TLS 上下文",
            "status": False,
            "detail": str(e),
            "expect": "pass",
        }

    try:
        token = secrets.token_hex(16)
        ok = isinstance(token, str) and len(token) == 32
        yield {
            "name": "secrets 密码学随机数",
            "status": ok,
            "detail": f"token_hex(16)={token[:16]}... ({len(token)} chars)" if ok else "生成失败",
            "expect": "pass",
        }
    except Exception as e:
        yield {
            "name": "secrets 密码学随机数",
            "status": False,
            "detail": str(e),
            "expect": "pass",
        }

    atexit_called = []
    def _cleanup():
        atexit_called.append(True)
    atexit.register(_cleanup)
    yield {
        "name": "atexit 注册退出处理器",
        "status": True,
        "detail": "处理器已注册",
        "expect": "pass",
    }
