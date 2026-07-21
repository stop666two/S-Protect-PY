# Python 环境测试工具

> 仓库地址: [github.com/stop666two/py-running-text](https://github.com/stop666two/py-running-text)

Python 运行环境兼容性测试工具。用于验证 Python 环境的标准库、第三方包、运行时能力等是否正常，后续可用于加密混淆兼容性验证。

## 快速开始

```bash
pip install -r requirements.txt
python main.py
```

Windows 也可双击 `run.bat`。

## 测试项总览

| 分类 | 文件 | 数量 | 说明 |
|------|------|------|------|
| 基础环境信息 | `tests/basic.py` | 10 | Python 版本、OS、CPU、内存、磁盘、GPU |
| 标准库模块 | `tests/stdlib.py` | 113 | 90 个当前模块(预期通过) + 23 个已弃用模块(预期失败) |
| 第三方包 | `tests/thirdparty.py` | 8 | tqdm/colorama/cryptography/numpy 等 |
| 运行时能力 | `tests/runtime.py` | 19 | 文件IO/HASH/GZip/HTTP/多线程/pickle/struct/tarfile 等 |
| 编译/加密核心 | `tests/compile_crypto.py` | 13 | compile/exec/marshal/zipimport/hashlib/PBKDF2/hmac/AES |
| 高级运行时 | `tests/advanced.py` | 14 | asyncio/subprocess/importlib/mmap/timeit/os/signal/typing |
| 系统压力/底层 | `tests/stress.py` | 9 | ctypes C/Windows API/sys._getframe/递归/ssl/secrets |
| 特殊/边缘功能 | `tests/special.py` | 13 | inspect/ast/type()/weakref/gc/heapq/unicodedata |
| 依赖安装卸载 | `tests/pip_test.py` | 5 | pip install/uninstall psutil (含 C 扩展) |
| 实际项目功能 | `tests/realworld.py` | 24 | ConfigParser/URL/CSV/XML/TOML/dataclasses/enum/logging 等 |

**总计: 222 项测试**

## 判定规则

每条测试结果包含 `expect` 字段标明预期：

- **预期通过 + 实际通过** → 正常
- **预期失败 + 实际失败** → 正常（如已弃用模块）
- **预期通过 + 实际失败** → **异常**（需要关注的真正问题）
- **预期失败 + 实际通过** → **异常**（预期外的兼容性变化）

最终判定：**正常**（全符合预期）或 **异常**（存在偏离项），异常项目会在报告末尾明细列出。

## 报告输出

- **控制台** — colorama 彩色输出，PASS/FAIL/SKIP/ALRT 四色标记
- **report.html** — HTML 表格报告
- **report.md** — Markdown 报告

三种报告均包含预期列和异常明细。

## 项目结构

```
py-running-text/
├── main.py                 # 启动入口
├── config.py               # 全局配置（测试列表、测试包等）
├── tester.py               # 测试引擎（生成器驱动 + tqdm 实时进度）
├── reporter.py             # 报告生成器（控制台/HTML/MD）
├── requirements.txt        # 依赖声明
├── run.bat                 # Windows 一键启动
├── tests/                  # 测试模块
│   ├── __init__.py
│   ├── basic.py            # 基础环境信息
│   ├── stdlib.py           # 标准库 + 已弃用模块
│   ├── thirdparty.py       # 第三方包检测
│   ├── runtime.py          # 运行时能力
│   ├── compile_crypto.py   # 编译/加密核心
│   ├── advanced.py         # 高级运行时
│   ├── stress.py           # 压力/底层测试
│   ├── special.py          # 特殊/边缘功能
│   ├── pip_test.py         # 依赖安装卸载
│   └── realworld.py        # 实际项目功能
├── _workspace/             # 测试工作目录（自动创建，已 gitignore）
├── docs/plans/             # 实现计划
└── README.md
```

## 添加新的测试

1. 在 `tests/` 下创建模块，函数使用 `yield` 返回结果字典：
   ```python
   def run_my_checks():
       try:
           result = do_something()
           yield {"name": "测试名称", "status": True, "detail": "成功", "expect": "pass"}
       except Exception as e:
           yield {"name": "测试名称", "status": False, "detail": str(e), "expect": "pass"}
   ```
2. 在 `config.py` 的 `TEST_CATEGORIES` 注册分类名
3. 在 `tester.py` 导入并加入 `test_funcs` 列表

结果字典字段：
| 字段 | 必填 | 说明 |
|------|------|------|
| `name` | 是 | 测试项名称 |
| `status` | 是 | True=通过, False=失败 |
| `detail` | 是 | 详细信息 |
| `expect` | 否 | 默认为 `"pass"`，设为 `"fail"` 表示预期失败 |

## 依赖

- tqdm — 进度条
- colorama — 控制台颜色
- cryptography — AES 加解密测试
- numpy — 数值计算
- requests — HTTP 请求测试
- rich — (仅导入检测)

所有依赖通过 `pip install -r requirements.txt` 安装。

## 输出文件

运行后会生成 `report.html` 和 `report.md`，已加入 `.gitignore`。
