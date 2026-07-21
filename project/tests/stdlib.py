import importlib
from config import STDLIB_MODULES, DEPRECATED_MODULES


def _check_modules(module_list, prefix=""):
    results = []
    for mod_name in module_list:
        try:
            importlib.import_module(mod_name)
            results.append({
                "name": f"{prefix}{mod_name}",
                "status": True,
                "detail": "导入成功",
            })
        except ImportError:
            results.append({
                "name": f"{prefix}{mod_name}",
                "status": False,
                "detail": "导入失败",
            })
    return results


def run_stdlib_checks():
    yield from _check_modules(STDLIB_MODULES, prefix="模块 ")
    for r in _check_modules(DEPRECATED_MODULES, prefix="已弃用模块 "):
        r["expect"] = "fail"
        yield r
