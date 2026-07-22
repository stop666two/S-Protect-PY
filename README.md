# S-Protect-PY

**Python 代码保护工具** — 混淆 · 多层加密 · 反调试 · 反篡改 · 水印 · 过期控制 · 混合加密 · 代码虚拟化 · 字节码保护

将你的 Python 项目加密为独立可运行的输出，保护源码不被逆向。

---

## 目录

- [原理](#原理)
- [快速开始](#快速开始)
- [安装](#安装)
- [CLI 命令](#cli-命令)
- [保护功能](#保护功能)
- [构建输出](#构建输出)
- [测试](#测试)
- [常见问题](#常见问题)

---

## 原理

```
project/                          output/
┌──────────┐                    ┌──────────────────┐
│ main.py  │──┐                 │  main.py         │ ← 自举启动器
│ utils.py │  │  ╔═══════════╗  │  integrity_manifest.json  ← 文件完整性白名单
│ models.py│  ├──╢ sprotect  ╠──┤  watermark_report.json    ← 水印报告
└──────────┘  │  ║ build     ║  │  _runtime/               ← 加密后的模块
              │  ╚═══════════╝  │  ├── loader.pye           ← 加密加载器
sprotect.json5 │                 │  ├── a1b2c3.pye           ← main.py
┌──────────┐  │                 │  ├── d4e5f6.pye           ← utils.py
│ 配置     │──┘                 │  ├── ...decoy*            ← 诱饵文件
└──────────┘                    └──────────────────┘
                                      ↓
                               python main.py 即可运行
                               (或 sprotect run)
```

### 运行时解密

```
output/main.py 启动
    │
    ├──→ 验证 integrity_manifest.json（防文件篡改/增删）
    │
    ├──→ 解密 loader.pye → 加载解密引擎
    │
    ├──→ 扫描 .pye 文件，三层指纹（f1/f2/f3）识别真实分片
    │
    ├──→ XOR 重构 master_key
    │
    ├──→ 链式哈希校验
    │
    ├──→ 逐文件解密：反向额外层 → AES-GCM → XOR → ChaCha20 → zlib
    │
    └──→ 注入 import hook，按需延迟加载模块
```

---

## 快速开始

```bash
# 1. 安装
pip install json5 cryptography tqdm colorama

# 2. 准备源码
mkdir -p project
echo 'print("Hello World!")' > project/main.py

# 3. 初始化
python -m sprotect config init

# 4. 构建加密项目
python -m sprotect build

# 5. 运行加密后的项目
python -m sprotect run
```

**输出目录 `output/` 可以拷贝到任何有 Python 3.10+ 的机器上运行**，不需要 S-Protect-PY 本体。

---

## 安装

```bash
# 基础依赖（必须）
pip install json5 cryptography tqdm colorama

# 额外加密层支持（可选）
pip install pycryptodome

# exe 打包（可选）
pip install pyinstaller

# 验证
python -m sprotect version
# S-Protect-PY v1.0.0
```

---

## CLI 命令

| 命令 | 用途 |
|------|------|
| `sprotect build` | 构建加密项目（project/ → output/） |
| `sprotect run` | 运行加密项目（自动加载 .env） |
| `sprotect encrypt <file>` | 加密单个文件 |
| `sprotect config init\|show` | 配置管理 |
| `sprotect init` | 初始化项目骨架 |
| `sprotect watermark extract\|verify\|list` | 水印操作 |
| `sprotect pack` | PyInstaller 打包为 exe |
| `sprotect version` | 版本信息 |

### build 选项

```bash
sprotect build                          # 默认 project/ → output/
sprotect build --project ./src          # 指定源码目录
sprotect build --output ./dist          # 指定输出目录
sprotect build -c myconfig.json5        # 自定义配置
sprotect build --clean                  # 自动清空输出目录
sprotect build --watch                  # 监控文件变化自动重构建
```

### run

```bash
sprotect run                            # 运行 ./output/
sprotect run --dir ./dist               # 指定目录
```

自动加载 `output/.env` 文件到环境变量。hybrid 模式下可通过 `.env` 配置密钥路径：

```bash
# output/.env
KEY_PATH=/secure/path/key.pem
```

---

## 保护功能

### 1. AST 混淆（L1-L5）

| 等级 | 变换 | 效果 |
|------|------|------|
| L1 | 变量/函数/类重命名 | `user_count` → `_0xa1b2c3` |
| L2 | + 字符串加密 | base64/XOR 运行时解码 |
| L3 | + 控制流平坦化 | 顺序代码 → while+switch 分派器 |
| L4 | + 数字加密 + 死代码注入 | `4096` → `struct.unpack(...)` |
| L5 | + 全开 + 属性访问重命名 | `obj.CONST` → `obj._0x...`（跨模块一致） |

### 2. 多层加密管道

```
源码 → zlib → ChaCha20-Poly1305 → XOR → AES-256-GCM → [额外层] → .pye
```

每层使用 HKDF-SHA256 域分离派生独立密钥。额外层统一使用 AES-256-CBC + 独立 HKDF 密钥。

### 3. 密钥系统

- master_key XOR 分片为 N 份，每份一个 .pye 文件
- 每个文件 5 个密钥槽（1 真 + 4 诱饵）
- 三层指纹验证：f1=XOR+SHA256, f2=blake3/SHA256, f3=HMAC

### 4. 反调试 / 反VM / 反沙箱

10 项检测：`pdb`、`ptrace`、`debugger`、`vm`、`sandbox`、`timing`、`cuckoo`、`ida`、`procmon`、**`gpu`**

检测到异常后的动作：`exit`（清内存退出）、`warn`（打印警告）、`corrupt`（破坏内存）

### 5. 反篡改 / 完整性白名单

- 链式哈希校验
- **integrity\_manifest.json** — 记录所有 .pye 的 SHA256，运行时检测缺失/篡改/新增文件
- 内存完整性 + 反 Hook + 反 Dump + 周期自检

### 6. 水印溯源

三层水印，支持**热补丁**（无需重加密即可更新）：

```python
from sprotect.watermark import patch_watermark_batch
patch_watermark_batch("output/_runtime/", "CUSTOMER-ABC", "mysecret")
```

### 7. 代码虚拟化

将 Python 函数编译为自定义 VM 指令集执行（20+ opcode），支持算术/比较/分支/循环/函数调用：

```json5
virtualization: { enabled: true, functions: ["validate_license"] }
```

### 8. 字节码保护（.pyc 级别）

marshal + AES-GCM 加密代码对象，`SecureImporter` import hook 透明解密：

```python
from sprotect.bytecode_protect import protect_code, SecureImporter
ct = protect_code(compile(source, "mod", "exec"), key)
sys.meta_path.insert(0, SecureImporter(runtime_dir, key))
```

### 9. 自定义打包器

替代 PyInstaller，生成自解压单文件：

```python
from sprotect.pack_custom import pack_to_single_file
pack_to_single_file("./output", "./bundle.py", loader_key)
```

### 10. 其他

- **混合加密**：RSA-4096 / ECC P-256 公钥包装 master_key
- **过期控制**：NTP 联网校验 + 时间漂移检测，支持 IPv4+IPv6
- **环境绑定**：目录/用户名/环境变量/MAC/硬件 ID
- **诱饵文件**：自动生成 N+2 个结构相同的假文件
- **.env 支持**：output/.env 自动加载到运行环境

---

## 构建输出结构

```
output/
├── main.py                    ← 自举启动器
├── integrity_manifest.json    ← 文件完整性白名单
├── watermark_report.json      ← 水印报告
├── .env                       ← 环境变量（可选）
├── key.pem                    ← 私钥（hybrid 模式）
├── requirements.txt
└── _runtime/
    ├── loader.pye             ← 加密加载器
    ├── a1b2c3.pye             ← main.py
    ├── d4e5f6.pye             ← utils.py
    ├── decoy_xxxx.pye         ← 诱饵文件
    └── random_subdir/
        └── decoy_yyyy.pye
```

`output/` 目录可拷贝到任何 Python 3.10+ 环境运行，仅需目标机器安装项目本身的第三方依赖。

---

## 测试

```bash
# 运行所有测试（23 项）
python -m pytest tests/ -v

# 仅加密功能测试
python -m pytest tests/test_crypto_extra.py -v

# 集成测试（含实际运行加密输出）
python -m pytest tests/test_integration.py -v

# AntiDebug / Expiration 测试
python -m pytest tests/test_anti_debug.py -v
```

测试覆盖：密钥派生、Serpent/Twofish/Camellia/Salsa20 加解密、RSA/ECC 混合加密、完整构建流程、加密输出运行、反调试/过期控制逻辑。

---

## 常见问题

**Q: 加密后无法启动 "No valid key found"？**
A: `.pye` 文件损坏或 `shard_count > 项目文件数`。检查配置。

**Q: extra\_layers 报错 "module 'Cryptodome' has no attribute"？**
A: 目标机器缺少 pycryptodome。`pip install pycryptodome`。

**Q: Hybrid 模式 "Private key not found"？**
A: 私钥需要与加密程序一同分发。可通过 `.env` 配置 `KEY_PATH`。

**Q: 每次 build 输出都不一样？**
A: 正常。多态填充、随机密钥、随机诱饵文件名共同导致。

**Q: 加密后需要什么依赖运行？**
A: 运行只需要 Python 标准库（hmac/hashlib/zlib/json）。`cryptography` 仅 build 阶段使用。额外加密层需要 pycryptodome。

**Q: --clean 和 --watch 可以同时用吗？**
A: 可以。`--clean` 在首次 build 前清空，`--watch` 在后续 rebuild 时不会再次清空。

**Q: importlib.reload() 对加密模块不起作用？**
A: 是的。`importlib.reload()` 会重新执行模块代码，但 AST 混淆后的重命名变量与内存中已有的名称不一致。这是 AST 级别混淆的固有局限。如需热重载支持，建议对目标模块降低混淆等级或排除重命名。
