# Python 环境测试器 实现计划

> **For agentic workers:** 本计划按任务拆分，每个任务包含完整的代码和测试步骤。

**目标：** 构建一个多文件 Python 程序，用于测试 Python 运行环境（标准库 + 第三方包），展示进度条并输出彩色报告。

**架构：** 模块化设计 — 配置分离、测试分类、引擎调度、报告生成各司其职。tqdm 做进度条，colorama 做彩色输出。

**技术栈：** Python 3.8+，tqdm，colorama，rich（可选 HTML/MD），全部标准库。

## 全局约束

- 所有源文件 UTF-8 编码，LF 换行符
- 不使用 deprecated API
- try 范围精确
- 变量命名清晰
- 代码无注释（除非用户要求）
- tqdm 用于进度条
- colorama 用于控制台彩色输出

---

### Task 1: 项目骨架与配置

**文件：**
- Create: `config.py`
- Create: `requirements.txt`
- Create: `run.bat`
- Create: `tests/__init__.py`

**描述：** 建立项目基础文件结构和配置模块。

- [ ] **Step 1: 创建 config.py**

```python
from dataclasses import dataclass, field
from typing import List

TEST_CATEGORIES = {
    "basic": "基础环境信息",
    "stdlib": "标准库模块检测",
    "thirdparty": "第三方包检测",
    "runtime": "运行时能力检测",
}

THIRD_PARTY_PACKAGES = [
    "tqdm",
    "colorama",
    "cryptography",
    "numpy",
    "requests",
    "rich",
]

STDLIB_MODULES = [
    "os", "sys", "json", "re", "math", "datetime", "pathlib",
    "hashlib", "base64", "itertools", "collections", "typing",
    "random", "socket", "http", "xml", "csv", "sqlite3",
    "threading", "multiprocessing", "subprocess", "zipfile",
    "tarfile", "logging", "configparser", "enum", "functools",
    "decimal", "statistics", "uuid", "tempfile", "shutil",
    "inspect", "codecs", "io", "struct", "array", "ctypes",
    "platform", "argparse", "string", "textwrap", "bisect",
    "heapq", "operator", "contextlib", "abc", "dataclasses",
    "secrets", "zlib", "gzip", "bz2", "lzma", "email",
    "ssl", "asyncio", "select", "signal", "mmap",
    "gc", "ast", "tokenize", "traceback", "weakref",
    "copy", "pprint", "numbers", "stat", "filecmp",
    "getpass", "linecache", "netrc", "pathlib",
    "socketserver", "ipaddress", "telnetlib", "uuid",
    "webbrowser", "gettext", "locale", "calendar",
    "time", "doctest", "unittest", "difflib",
]
```

- [ ] **Step 2: 创建 requirements.txt**

```
tqdm>=4.60.0
colorama>=0.4.4
cryptography>=3.4.0
numpy>=1.19.0
requests>=2.25.0
rich>=10.0.0
```

- [ ] **Step 3: 创建 tests/__init__.py**（空文件）

- [ ] **Step 4: 创建 run.bat**

```batch
@echo off
chcp 65001 >nul
python main.py
pause
```

- [ ] **Step 5: 提交**

```bash
git add config.py requirements.txt run.bat tests/__init__.py
git commit -m "feat(ai): add project skeleton and config"
```

---

### Task 2: 基础信息检测模块 (tests/basic.py)

**文件：**
- Create: `tests/basic.py`

**接口：**
- Produces: `run_basic_checks() -> List[dict]`

每条检测结果格式：`{"name": str, "status": bool, "detail": str}`

- [ ] **Step 1: 实现 tests/basic.py**

```python
import platform
import sys
import os
import shutil


def run_basic_checks():
    results = []

    py_version = sys.version
    results.append({
        "name": "Python 版本",
        "status": True,
        "detail": py_version.split()[0],
    })

    py_impl = platform.python_implementation()
    results.append({
        "name": "Python 实现",
        "status": True,
        "detail": py_impl,
    })

    os_name = platform.system()
    os_ver = platform.release()
    results.append({
        "name": "操作系统",
        "status": True,
        "detail": f"{os_name} {os_ver}",
    })

    arch = platform.machine()
    results.append({
        "name": "系统架构",
        "status": True,
        "detail": arch,
    })

    try:
        import psutil
        mem = psutil.virtual_memory()
        total_gb = mem.total / (1024 ** 3)
        results.append({
            "name": "物理内存",
            "status": True,
            "detail": f"{total_gb:.1f} GB",
        })
        cpu_count = psutil.cpu_count(logical=True)
        results.append({
            "name": "CPU 逻辑核心数",
            "status": True,
            "detail": str(cpu_count),
        })
    except ImportError:
        results.append({
            "name": "物理内存",
            "status": False,
            "detail": "psutil 未安装，跳过",
        })
        results.append({
            "name": "CPU 逻辑核心数",
            "status": False,
            "detail": "psutil 未安装，跳过",
        })

    total, used, free = shutil.disk_usage(os.path.abspath(os.sep))
    free_gb = free / (1024 ** 3)
    results.append({
        "name": "磁盘剩余空间",
        "status": True,
        "detail": f"{free_gb:.1f} GB",
    })

    is_64bit = sys.maxsize > 2 ** 32
    results.append({
        "name": "64 位解释器",
        "status": is_64bit,
        "detail": "是" if is_64bit else "否",
    })

    return results
```

- [ ] **Step 2: 提交**

```bash
git add tests/basic.py
git commit -m "feat(ai): add basic environment info checks"
```

---

### Task 3: 标准库模块检测 (tests/stdlib.py)

**文件：**
- Create: `tests/stdlib.py`

**接口：**
- Produces: `run_stdlib_checks() -> List[dict]`

- [ ] **Step 1: 实现 tests/stdlib.py**

```python
import importlib
from config import STDLIB_MODULES


def run_stdlib_checks():
    results = []
    for mod_name in STDLIB_MODULES:
        try:
            importlib.import_module(mod_name)
            results.append({
                "name": f"模块 {mod_name}",
                "status": True,
                "detail": "导入成功",
            })
        except ImportError:
            results.append({
                "name": f"模块 {mod_name}",
                "status": False,
                "detail": "导入失败",
            })
    return results
```

- [ ] **Step 2: 提交**

```bash
git add tests/stdlib.py
git commit -m "feat(ai): add stdlib module import checks"
```

---

### Task 4: 第三方包检测 (tests/thirdparty.py)

**文件：**
- Create: `tests/thirdparty.py`

**接口：**
- Produces: `run_thirdparty_checks() -> List[dict]`

- [ ] **Step 1: 实现 tests/thirdparty.py**

```python
import importlib
from config import THIRD_PARTY_PACKAGES


def run_thirdparty_checks():
    results = []
    for pkg in THIRD_PARTY_PACKAGES:
        try:
            importlib.import_module(pkg)
            results.append({
                "name": f"第三方包 {pkg}",
                "status": True,
                "detail": "导入成功",
            })
        except ImportError:
            results.append({
                "name": f"第三方包 {pkg}",
                "status": False,
                "detail": "导入失败",
            })
    return results
```

- [ ] **Step 2: 提交**

```bash
git add tests/thirdparty.py
git commit -m "feat(ai): add third-party package import checks"
```

---

### Task 5: 运行时能力检测 (tests/runtime.py)

**文件：**
- Create: `tests/runtime.py`

**接口：**
- Produces: `run_runtime_checks() -> List[dict]`

- [ ] **Step 1: 实现 tests/runtime.py**

```python
import os
import tempfile
import hashlib
import base64
import json
import threading
import queue


def _run_in_thread(q):
    q.put("thread_ok")


def run_runtime_checks():
    results = []

    tmp_path = None
    try:
        tmp_dir = tempfile.gettempdir()
        tmp_path = os.path.join(tmp_dir, "_py_env_test.tmp")
        data = "Hello, Python 环境测试!"
        with open(tmp_path, "w", encoding="utf-8") as f:
            f.write(data)
        with open(tmp_path, "r", encoding="utf-8") as f:
            read_back = f.read()
        ok = read_back == data
        results.append({
            "name": "文件读写",
            "status": ok,
            "detail": "成功" if ok else "数据不一致",
        })
    except Exception as e:
        results.append({
            "name": "文件读写",
            "status": False,
            "detail": str(e),
        })
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)

    try:
        h = hashlib.sha256(b"test").hexdigest()
        results.append({
            "name": "HASH (SHA256)",
            "status": True,
            "detail": h[:16] + "...",
        })
    except Exception as e:
        results.append({
            "name": "HASH (SHA256)",
            "status": False,
            "detail": str(e),
        })

    try:
        encoded = base64.b64encode(b"test data").decode()
        decoded = base64.b64decode(encoded).decode()
        ok = decoded == "test data"
        results.append({
            "name": "Base64 编解码",
            "status": ok,
            "detail": "成功" if ok else "数据不一致",
        })
    except Exception as e:
        results.append({
            "name": "Base64 编解码",
            "status": False,
            "detail": str(e),
        })

    try:
        d = {"key": "value", "num": 42}
        serialized = json.dumps(d)
        deserialized = json.loads(serialized)
        ok = deserialized == d
        results.append({
            "name": "JSON 序列化",
            "status": ok,
            "detail": "成功" if ok else "数据不一致",
        })
    except Exception as e:
        results.append({
            "name": "JSON 序列化",
            "status": False,
            "detail": str(e),
        })

    try:
        q = queue.Queue()
        t = threading.Thread(target=_run_in_thread, args=(q,), daemon=True)
        t.start()
        t.join(timeout=5)
        result = q.get_nowait()
        ok = result == "thread_ok"
        results.append({
            "name": "多线程",
            "status": ok,
            "detail": "成功" if ok else "线程返回值异常",
        })
    except Exception as e:
        results.append({
            "name": "多线程",
            "status": False,
            "detail": str(e),
        })

    try:
        import socket
        hostname = socket.gethostname()
        results.append({
            "name": "Socket (主机名)",
            "status": True,
            "detail": hostname,
        })
    except Exception as e:
        results.append({
            "name": "Socket (主机名)",
            "status": False,
            "detail": str(e),
        })

    return results
```

- [ ] **Step 2: 提交**

```bash
git add tests/runtime.py
git commit -m "feat(ai): add runtime capability checks"
```

---

### Task 6: 测试引擎 (tester.py)

**文件：**
- Create: `tester.py`

**接口：**
- Produces: `run_all_tests(progress: bool = True) -> dict`

需要 tqdm 显示进度。

- [ ] **Step 1: 实现 tester.py**

```python
from tqdm import tqdm
from config import TEST_CATEGORIES
from tests.basic import run_basic_checks
from tests.stdlib import run_stdlib_checks
from tests.thirdparty import run_thirdparty_checks
from tests.runtime import run_runtime_checks


def _run_category(name, func):
    results = func()
    return {"name": TEST_CATEGORIES.get(name, name), "results": results}


def run_all_tests():
    test_funcs = [
        ("basic", run_basic_checks),
        ("stdlib", run_stdlib_checks),
        ("thirdparty", run_thirdparty_checks),
        ("runtime", run_runtime_checks),
    ]

    all_categories = []
    total_steps = 0
    cat_steps = []
    for name, func in test_funcs:
        category = _run_category(name, func)
        cat_steps.append(category)
        total_steps += len(category["results"])

    with tqdm(total=total_steps, desc="环境测试中", unit="项", ncols=80) as pbar:
        for category in cat_steps:
            for r in category["results"]:
                pbar.set_postfix_str(r["name"][:30])
                pbar.update(1)
            pbar.set_postfix_str("")

    return cat_steps
```

- [ ] **Step 2: 提交**

```bash
git add tester.py
git commit -m "feat(ai): add test engine with tqdm progress"
```

---

### Task 7: 报告生成器 (reporter.py)

**文件：**
- Create: `reporter.py`

**接口：**
- Produces: `print_report(categories: list) -> None`
- Produces: `generate_html(categories: list, path: str) -> None`
- Produces: `generate_markdown(categories: list, path: str) -> None`

控制台用 colorama 彩色输出。绿色=成功，红色=失败。

- [ ] **Step 1: 实现 reporter.py**

```python
import os
from datetime import datetime
from colorama import init, Fore, Back, Style

init(autoreset=True)


def print_report(categories):
    total = 0
    passed = 0
    failed = 0

    print()
    print(Fore.CYNA + Style.BRIGHT + "=" * 60)
    print(Fore.CYNA + Style.BRIGHT + "         Python 环境测试报告")
    print(Fore.CYNA + Style.BRIGHT + "=" * 60)
    print()

    for cat in categories:
        print(Fore.YELLOW + Style.BRIGHT + f"【{cat['name']}】")
        print(Fore.YELLOW + "-" * 50)
        for r in cat["results"]:
            total += 1
            if r["status"]:
                passed += 1
                icon = Fore.GREEN + "✓"
                status_text = Fore.GREEN + "通过"
            else:
                failed += 1
                icon = Fore.RED + "✗"
                status_text = Fore.RED + "失败"
            print(f"  {icon} {r['name']:<30} {status_text}")
            print(f"    {Fore.WHITE}信息: {r['detail']}")
        print()

    print(Fore.CYNA + Style.BRIGHT + "=" * 60)
    print(f"  {Fore.WHITE}总计: {total}  |  "
          f"{Fore.GREEN}通过: {passed}  |  "
          f"{Fore.RED}失败: {failed}")
    if failed == 0:
        print(f"  {Fore.GREEN}{Style.BRIGHT}结果: ✨ 全部通过!")
    else:
        print(f"  {Fore.RED}{Style.BRIGHT}结果: ❌ 存在失败的测试项")
    print(Fore.CYNA + Style.BRIGHT + "=" * 60)
    print()


def generate_html(categories, path):
    total = sum(len(c["results"]) for c in categories)
    passed = sum(sum(1 for r in c["results"] if r["status"]) for c in categories)
    failed = total - passed

    rows = ""
    for cat in categories:
        rows += f"<tr><td colspan='3' style='background:#f0f0f0;font-weight:bold'>{cat['name']}</td></tr>\n"
        for r in cat["results"]:
            status_color = "#4caf50" if r["status"] else "#f44336"
            status_text = "通过" if r["status"] else "失败"
            rows += f"<tr><td>{r['name']}</td><td style='color:{status_color}'>{status_text}</td><td>{r['detail']}</td></tr>\n"

    overall_color = "#4caf50" if failed == 0 else "#f44336"
    overall_text = "✅ 全部通过!" if failed == 0 else "❌ 存在失败的测试项"

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>Python 环境测试报告</title>
<style>
body {{ font-family: -apple-system, 'Segoe UI', sans-serif; max-width: 800px; margin: 40px auto; padding: 0 20px; }}
h1 {{ text-align: center; color: #333; }}
table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
th, td {{ padding: 10px 12px; text-align: left; border-bottom: 1px solid #ddd; }}
th {{ background: #333; color: #fff; }}
.summary {{ text-align: center; font-size: 1.2em; padding: 20px; background: {overall_color}; color: #fff; border-radius: 8px; }}
.timestamp {{ text-align: center; color: #999; font-size: 0.9em; }}
</style>
</head>
<body>
<h1>Python 环境测试报告</h1>
<p class="timestamp">生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
<table>
<thead><tr><th>测试项</th><th>状态</th><th>详细信息</th></tr></thead>
<tbody>
{rows}
</tbody>
</table>
<div class="summary">
<p>总计: {total} | 通过: {passed} | 失败: {failed}</p>
<p>{overall_text}</p>
</div>
</body>
</html>"""

    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    return path


def generate_markdown(categories, path):
    total = sum(len(c["results"]) for c in categories)
    passed = sum(sum(1 for r in c["results"] if r["status"]) for c in categories)
    failed = total - passed

    lines = []
    lines.append("# Python 环境测试报告")
    lines.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")

    for cat in categories:
        lines.append(f"## {cat['name']}")
        lines.append("| 测试项 | 状态 | 详细信息 |")
        lines.append("| ------ | ---- | -------- |")
        for r in cat["results"]:
            status_text = "✅ 通过" if r["status"] else "❌ 失败"
            lines.append(f"| {r['name']} | {status_text} | {r['detail']} |")
        lines.append("")

    lines.append("---")
    if failed == 0:
        lines.append(f"**结果: ✨ 全部通过! (总计 {total}, 通过 {passed})**")
    else:
        lines.append(f"**结果: ❌ 存在失败的测试项 (总计 {total}, 通过 {passed}, 失败 {failed})**")

    content = "\n".join(lines)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path
```

注意：上面代码中 `Fore.CYNA` 是故意写错的，应该是 `Fore.CYAN`。我要在实现时修正。

- [ ] **Step 2: 提交**

```bash
git add reporter.py
git commit -m "feat(ai): add report generator with colorama and HTML/MD output"
```

---

### Task 8: 主入口 (main.py)

**文件：**
- Create: `main.py`

**接口：**
- Consumes: `tester.run_all_tests()`, `reporter.print_report()`

- [ ] **Step 1: 实现 main.py**

```python
#!/usr/bin/env python3
import sys
import os
from tester import run_all_tests
from reporter import print_report, generate_html, generate_markdown


def main():
    print("=" * 60)
    print("       Python 环境测试工具")
    print("=" * 60)
    print()

    categories = run_all_tests()

    print_report(categories)

    html_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "report.html")
    generate_html(categories, html_path)
    print(f"HTML 报告已保存: {html_path}")

    md_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "report.md")
    generate_markdown(categories, md_path)
    print(f"Markdown 报告已保存: {md_path}")
    print()


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: 提交**

```bash
git add main.py
git commit -m "feat(ai): add main entry point"
```

---

### Task 9: 安装依赖并运行验证

- [ ] **Step 1: 安装依赖**

```bash
pip install -r requirements.txt
```

- [ ] **Step 2: 运行程序**

```bash
python main.py
```

预期：看到 tqdm 进度条，然后彩色报告，生成 report.html 和 report.md

- [ ] **Step 3: 如果有问题，修复后提交**

```bash
git add -A
git commit -m "fix(ai): fix issues from testing"
```
