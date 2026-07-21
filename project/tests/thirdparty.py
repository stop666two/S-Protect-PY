import importlib
import sys
from config import THIRD_PARTY_PACKAGES

_CORE_PACKAGES = {"tqdm", "colorama", "cryptography", "numpy", "requests", "rich"}


def _pre_scan():
    available = set()
    for pkg in THIRD_PARTY_PACKAGES:
        try:
            importlib.import_module(pkg)
            available.add(pkg)
        except ImportError:
            pass
    for pkg in list(sys.modules.keys()):
        name = pkg.split(".")[0]
        if name in THIRD_PARTY_PACKAGES:
            available.add(name)
    return available


def run_thirdparty_checks():
    available = _pre_scan()
    for pkg in THIRD_PARTY_PACKAGES:
        is_core = pkg in _CORE_PACKAGES
        is_available = pkg in available

        if is_available:
            yield {
                "name": f"第三方包 {pkg}",
                "status": True,
                "detail": "导入成功",
                "expect": "pass",
            }
        elif is_core:
            yield {
                "name": f"第三方包 {pkg}",
                "status": False,
                "detail": "导入失败 (核心依赖缺失)",
                "expect": "pass",
            }
        else:
            yield {
                "name": f"第三方包 {pkg}",
                "status": False,
                "detail": "导入失败 (可选包未安装)",
                "expect": "fail",
            }
