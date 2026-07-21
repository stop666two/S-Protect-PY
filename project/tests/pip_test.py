import subprocess
import sys
import importlib
from config import PIP_TEST_PACKAGE


def _clear_cache(pkg_name):
    keys = [k for k in sys.modules if k == pkg_name or k.startswith(pkg_name + ".")]
    for k in keys:
        del sys.modules[k]


def run_pip_tests():
    _clear_cache(PIP_TEST_PACKAGE)
    try:
        importlib.import_module(PIP_TEST_PACKAGE)
        was_preinstalled = True
        yield {
            "name": f"预安装检查 ({PIP_TEST_PACKAGE})",
            "status": True,
            "detail": f"{PIP_TEST_PACKAGE} 已预安装",
            "expect": "pass",
        }
    except ImportError:
        was_preinstalled = False
        yield {
            "name": f"预安装检查 ({PIP_TEST_PACKAGE})",
            "status": True,
            "detail": f"{PIP_TEST_PACKAGE} 未预安装，将进行安装测试",
            "expect": "pass",
        }

    try:
        proc = subprocess.run(
            [sys.executable, "-m", "pip", "install", PIP_TEST_PACKAGE],
            capture_output=True, text=True, timeout=120
        )
        install_ok = proc.returncode == 0
        yield {
            "name": f"pip 安装 ({PIP_TEST_PACKAGE})",
            "status": install_ok,
            "detail": "安装成功" if install_ok else proc.stderr.strip()[-100:],
            "expect": "pass",
        }
    except Exception as e:
        yield {
            "name": f"pip 安装 ({PIP_TEST_PACKAGE})",
            "status": False,
            "detail": str(e),
            "expect": "pass",
        }
        return

    _clear_cache(PIP_TEST_PACKAGE)
    try:
        importlib.import_module(PIP_TEST_PACKAGE)
        yield {
            "name": f"安装后导入 ({PIP_TEST_PACKAGE})",
            "status": True,
            "detail": f"{PIP_TEST_PACKAGE} 导入成功 (含 C 扩展)",
            "expect": "pass",
        }
    except ImportError as e:
        yield {
            "name": f"安装后导入 ({PIP_TEST_PACKAGE})",
            "status": False,
            "detail": str(e),
            "expect": "pass",
        }

    try:
        proc = subprocess.run(
            [sys.executable, "-m", "pip", "uninstall", "-y", PIP_TEST_PACKAGE],
            capture_output=True, text=True, timeout=60
        )
        uninstall_ok = proc.returncode == 0
        yield {
            "name": f"pip 卸载 ({PIP_TEST_PACKAGE})",
            "status": uninstall_ok,
            "detail": "卸载成功" if uninstall_ok else proc.stderr.strip()[-100:],
            "expect": "pass",
        }
    except Exception as e:
        yield {
            "name": f"pip 卸载 ({PIP_TEST_PACKAGE})",
            "status": False,
            "detail": str(e),
            "expect": "pass",
        }

    _clear_cache(PIP_TEST_PACKAGE)
    try:
        importlib.import_module(PIP_TEST_PACKAGE)
        yield {
            "name": f"卸载后导入 ({PIP_TEST_PACKAGE})",
            "status": True,
            "detail": "不应存在但可导入",
            "expect": "fail",
        }
    except ImportError:
        yield {
            "name": f"卸载后导入 ({PIP_TEST_PACKAGE})",
            "status": False,
            "detail": "导入失败 - 符合预期",
            "expect": "fail",
        }

    if was_preinstalled:
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", PIP_TEST_PACKAGE],
                capture_output=True, text=True, timeout=120
            )
        except Exception:
            pass
