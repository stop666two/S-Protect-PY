# S-Protect-PY

**Python 代码保护工具** — 6层加密 · 多态变异 · 密钥雷区2048 · Shamir门限 · 双进程架构 · AST混淆 · 反调试 · 反篡改 · 水印 · 过期控制 · 代码虚拟化 · 字节码保护

---

## 目录

- [原理](#原理)
- [快速开始](#快速开始)
- [安装](#安装)
- [CLI 命令](#cli-命令)
- [保护功能](#保护功能)
- [防御矩阵](#防御矩阵)
- [构建输出](#构建输出)
- [测试](#测试)
- [常见问题](#常见问题)

---

## 原理

```
project/                          output/
┌──────────┐                    ┌──────────────────┐
│ main.py  │──┐                 │  main.py         │ ← HMAC派生加载器
│ mod_a.py │  │  ╔═══════════╗  │  _meta/          │ ← 完整性报告/水印报告
│ mod_b.py │  ├──╢ sprotect  ╠──┤  _runtime/       │ ← 加密模块(.pye)
│ mod_c.py │  │  ║ build     ║  │  ├── loader.pye  │ ← 6层加密加载器
└──────────┘  │  ╚═══════════╝  │  ├── *.pye       │ ← Shamir分片+密文
sprotect.json5 │                 │  ├── decoy*      │ ← 诱饵文件(≥10个)
┌──────────┐  │                 └──────────────────┘
│ 配置     │──┘                       ↓
└──────────┘                   python main.py 即可运行
                               python main.py --dual (双进程模式)
```

### 运行时解密链

```
main.py 启动
    │
    ├── 15个HEX变量交织 → HMAC推导 → 解密loader.pye
    │
    ├── 6层加密逐层剥解（每层后多态变异器改写代码）
    │
    ├── 扫描.pye → k1-k5指纹(60%通过率) + Shamir M-of-N重构主密钥
    │
    ├── 链式哈希校验 + 完整性清单验证
    │
    ├── 动态密钥(HMAC-SHA256(base, floor(time/60)))
    │
    └── 反调试检测 + VM环境强制 + 时间墙(60min自动擦除)
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
| L5 | + 全开 + 蜜罐函数 | 注入假解密函数混淆分析 |

每层混淆后额外执行多态变异器（变量重命名+垃圾注入+三元组混淆+字符串分裂）。

### 2. 6层加密体系

```
源码 → Layer6 → Layer5 → Layer4 → Layer3 → Layer2 → Layer1
每层：AES-GCM加密 + 密钥指向下层
      每层解密后→多态变异器改写代码→提取下层密钥→继续解密
```

每层密钥完全独立，第 N 层被破解只暴露第 N-1 层的入口，不波及其他层。

### 3. 双轨密钥系统

- **Shamir Secret Sharing**（主）：M-of-N 门限，M-1 个分片信息量为零
- **XOR + k1-k5指纹**（备）：60%假密钥可通过 f1/f2/f3 验证，但解密到某层会断裂
- **动态密钥**：HMAC-SHA256(base_key, floor(time/60))，每分钟变化

### 4. 密钥雷区 2048

```
2048个32字节密钥（1真+2047假）→ XOR掩码混淆 → PID绑定派生
每个假密钥对应可解密的诱饵密文
Loader通过确定性位置提取真密钥
```

### 5. 反调试 / 反VM / 反沙箱

10 项检测：`pdb`、`ptrace`、`debugger`、`vm`、`sandbox`、`timing`、`cuckoo`、`ida`、`procmon`、`gpu`
+ 时序检测（循环耗时超过 1.0s 判断为调试器）
+ 反植入检测（检查可疑模块，发现后故意用错密钥解密）

### 6. 双进程架构（实验性）

```
父进程：持有全部密钥 → IPC → 发送解密后源码
子进程：接收源码 → exec() 执行业务代码
攻击者dump子进程内存→拿不到任何密钥
```

通过 `sprotect.json5` 中 `dual_process.enabled` 控制，默认关闭。

### 7. 运行时保护

| 措施 | 说明 |
|------|------|
| 时间墙 | 启动后 60 分钟自动擦除密钥退出 |
| 完整性自检 | 每 30 秒 SHA256 自检自身 EXE |
| 内存 TTL | 解密后 60 秒自动回收 |
| 内存擦除 | 用完后立即覆写解密缓冲区 |
| 6层加密 | 层层相扣，断开一层全断 |

### 8. 反篡改 / 完整性白名单

- 链式哈希校验
- **integrity\_manifest.json** — 记录所有 .pye 的 SHA256，运行时检测缺失/篡改/新增文件
- 内存完整性 + 反 Hook + 反 Dump + 周期自检

### 9. 水印溯源

三层水印（文件/代码/运行时），支持热补丁（无需重加密即可更新）：

```python
from sprotect.watermark import patch_watermark_batch
patch_watermark_batch("output/_runtime/", "CUSTOMER-ABC", "mysecret")
```

### 10. 其他

- **Shamir门限**：GF(256) Lagrange 插值，N-1 个分片不泄露任何信息
- **多态变异器**：AST 级重命名+垃圾注入+三元组混淆，每次加载产出不同代码
- **混合加密**：ECC P-521 公钥包装 master_key
- **过期控制**：NTP 联网校验 + 时间漂移检测，支持 IPv4+IPv6
- **环境绑定**：目录/用户名/环境变量/MAC/硬件 ID
- **诱饵模块**：文件数不足 10 时自动生成有效 Python 假模块
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
# 运行所有测试（63 项）
python -m pytest tests/ -v

# 混淆引擎测试（36项）
python -m pytest tests/test_obfuscate.py -v

# 密钥+加密测试
python -m pytest tests/test_crypto_extra.py -v

# 密钥雷区测试
python -m pytest tests/test_keyvault.py -v

# 集成测试（含实际运行加密输出）
python -m pytest tests/test_integration.py -v

# AntiDebug / Expiration 测试
python -m pytest tests/test_anti_debug.py -v
```

测试覆盖：AST混淆全组件、Shamir门限、密钥雷区、6层加密、多态变异器、双进程架构、RSA/ECC混合加密、完整构建流程、反调试/过期控制逻辑。

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
