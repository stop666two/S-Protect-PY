import platform
import sys
import os
import shutil
import subprocess

_GB = 1024 ** 3


def run_basic_checks():
    py_version = sys.version
    yield {
        "name": "Python 版本",
        "status": True,
        "detail": py_version.split()[0],
    }

    py_impl = platform.python_implementation()
    yield {
        "name": "Python 实现",
        "status": True,
        "detail": py_impl,
    }

    os_name = platform.system()
    os_ver = platform.release()
    yield {
        "name": "操作系统",
        "status": True,
        "detail": f"{os_name} {os_ver}",
    }

    arch = platform.machine()
    yield {
        "name": "系统架构",
        "status": True,
        "detail": arch,
    }

    try:
        import psutil
        mem = psutil.virtual_memory()
        total_gb = mem.total / _GB
        yield {
            "name": "物理内存",
            "status": True,
            "detail": f"{total_gb:.1f} GB",
        }
        cpu_count = psutil.cpu_count(logical=True)
        yield {
            "name": "CPU 逻辑核心数",
            "status": True,
            "detail": str(cpu_count),
        }
    except ImportError:
        yield {
            "name": "物理内存",
            "status": False,
            "detail": "psutil 未安装，跳过",
        }
        yield {
            "name": "CPU 逻辑核心数",
            "status": False,
            "detail": "psutil 未安装，跳过",
        }

    total, used, free = shutil.disk_usage(os.path.abspath(os.sep))
    free_gb = free / _GB
    yield {
        "name": "磁盘剩余空间",
        "status": True,
        "detail": f"{free_gb:.1f} GB",
    }

    is_64bit = sys.maxsize > 2 ** 32
    yield {
        "name": "64 位解释器",
        "status": is_64bit,
        "detail": "是" if is_64bit else "否",
    }

    try:
        proc = subprocess.run(
            ["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader"],
            capture_output=True, text=True, timeout=10
        )
        if proc.returncode == 0:
            gpu_info = proc.stdout.strip()
            yield {
                "name": "NVIDIA GPU",
                "status": True,
                "detail": gpu_info,
            }
        else:
            yield {
                "name": "NVIDIA GPU",
                "status": False,
                "detail": "nvidia-smi 未检测到 GPU",
            }
    except FileNotFoundError:
        yield {
            "name": "NVIDIA GPU",
            "status": False,
            "detail": "nvidia-smi 未安装",
        }
    except Exception as e:
        yield {
            "name": "NVIDIA GPU",
            "status": False,
            "detail": str(e),
        }

    try:
        node = platform.node()
        yield {
            "name": "主机名",
            "status": True,
            "detail": node,
        }
    except Exception as e:
        yield {
            "name": "主机名",
            "status": False,
            "detail": str(e),
        }
