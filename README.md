# S-Protect-PY

**Python 代码保护工具** — 混淆 · 多层加密 · 反调试 · 反篡改 · 水印 · 过期控制 · 混合加密

将你的 Python 项目加密为独立可运行的输出，保护源码不被逆向。

---

## 目录

- [工作原理](#工作原理)
- [快速开始](#快速开始)
- [安装](#安装)
- [CLI 命令](#cli-命令)
- [保护功能详解](#保护功能详解)
  - [AST 混淆](#1-ast-混淆)
  - [多层加密管道](#2-多层加密管道)
  - [额外加密层（Serpent/Twofish/Camellia/Salsa20）](#3-额外加密层)
  - [混合加密（RSA/ECC 密钥包装）](#4-混合加密)
  - [密钥系统（k1-k5 + 诱饵）](#5-密钥系统)
  - [反调试 / 反VM / 反沙箱](#6-反调试--反vm--反沙箱)
  - [反篡改 / 完整性校验](#7-反篡改--完整性校验)
  - [水印溯源](#8-水印溯源)
  - [过期控制](#9-过期控制)
  - [环境指纹绑定](#10-环境指纹绑定)
  - [诱饵文件系统](#11-诱饵文件系统)
  - [代码虚拟化](#12-代码虚拟化)
- [配置文件](#配置文件)
- [构建输出结构](#构建输出结构)
- [测试](#测试)
- [常见问题](#常见问题)

---

## 工作原理

```
                        S-Protect-PY 构建流程
═══════════════════════════════════════════════════════════════

  project/                          output/
  ┌──────────┐                    ┌──────────────────┐
  │ main.py  │──┐                 │  main.py         │ ← 自举启动器
  │ utils.py │  │  ╔═══════════╗  │  requirements.txt│     (极简 stub)
  │ models.py│  ├──╢ sprotect  ╠──┤  _runtime/       │
  └──────────┘  │  ║ build     ║  │  ├── loader.pye  │ ← 加密后的加载器
                │  ╚═══════════╝  │  ├── a1b2c3.pye  │ ← main.py 加密
  sprotect.json5 │                 │  ├── d4e5f6.pye  │ ← utils.py 加密
  ┌──────────┐  │                 │  ├── g7h8i9.pye  │ ← models.py 加密
  │ 配置     │──┘                 │  ├── ...decoy*   │ ← 诱饵文件
  └──────────┘                    │  └── ...decoy*   │
                                  └──────────────────┘
                                      ↓
                               python main.py 即可运行
                               (纯 stdlib 解密，零外部依赖)
```

### 运行时的解密流程

```
output/main.py 启动
    │
    ├──→ 读取 _runtime/loader.pye，解密出 loader.py
    │
    ├──→ loader 扫描 _runtime/ 下所有 .pye 文件
    │      │
    │      ├──→ 对每个 .pye 提取 k1-k5，做三层指纹验证（f1/f2/f3）
    │      │    找到真实的密钥分片（诱饵文件会在某层验证失败）
    │      │
    │      ├──→ 收集所有真实分片，XOR 重构 master_key
    │      │
    │      ├──→ 链式哈希校验（interdependency chain）
    │      │
    │      ├──→ 逐文件解密：反向额外层 → AES-GCM → XOR → ChaCha20 → zlib
    │      │
    │      └──→ 注入 import hook，按需延迟加载模块
    │
    ├──→ 执行入口模块的 __main__
```

---

## 快速开始

```bash
# 1. 克隆仓库
git clone <repo>
cd S-Protect-PY

# 2. 安装依赖
pip install -r requirements.txt

# 3. 把源码放入 project/
mkdir -p project
cp myapp.py project/main.py
# （多文件项目照此放入）

# 4. 构建加密项目
python -m sprotect build

# 5. 运行加密后的项目
cd output
python main.py
```

**输出目录 `output/` 可以拷贝到任何有 Python 3.10+ 的机器上运行**，不需要 S-Protect-PY 本体。

---

## 安装

```bash
# 基础依赖（必须）
pip install json5 cryptography tqdm colorama

# 额外加密层支持（可选）
# 如需 serpent/twofish/camellia/salsa20 算法
pip install pycryptodome

# 验证安装
python -m sprotect version
# S-Protect-PY v0.2.0
```

---

## CLI 命令

| 命令 | 用途 |
|------|------|
| `sprotect build` | 构建加密项目（project/ → output/） |
| `sprotect encrypt <file>` | 加密单个文件 |
| `sprotect config init` | 生成默认 `sprotect.json5` |
| `sprotect config show` | 查看当前配置 |
| `sprotect init` | 初始化项目骨架 |
| `sprotect version` | 查看版本 |
| `sprotect watermark extract <file> [--key]` | 从 .pye 提取水印 |
| `sprotect watermark verify <file> [--key]` | 验证水印真实性 |
| `sprotect watermark list <dir>` | 扫描目录下所有水印 |

### build 命令选项

```bash
python -m sprotect build                          # 默认 project/ → output/
python -m sprotect build --project ./src           # 指定源码目录
python -m sprotect build --output ./dist           # 指定输出目录
python -m sprotect build -c myconfig.json5         # 使用自定义配置
```

---

## 保护功能详解

### 1. AST 混淆

在 **抽象语法树** 层面对源码进行变换，分为 5 个等级：

| 等级 | 变换 | 效果 |
|------|------|------|
| L1 | 变量/函数/类名重命名 | `user_count` → `_0xa1b2c3` |
| L2 | + 字符串加密 | `"secret"` → base64 编码运行时解码 |
| L3 | + 控制流平坦化 | 顺序代码转为 while + if 分派器，破坏控制流图 |
| L4 | + 数字加密 | `4096` → `(0x1000 ^ 0x0) + struct.unpack(...)` |
| L5 | + 死代码注入 + 不透明谓词 | 注入永不为真的 if 块迷惑静态分析 |

**20 种变量名前缀模式**：`_0x`, `_a`, `_b`, `_c`, ..., `_n` 随机选取，防止相邻文件使用相邻前缀导致名称冲突。

**5 种命名风格**：`hex`（十六进制）、`chinese`（中文字符）、`invisible`（零宽字符）、`math-symbols`（数学符号）、`custom`（自定义前缀/后缀）。

### 2. 多层加密管道

每个文件的加密管道（按顺序执行）：

```
源码 → zlib 压缩 → ChaCha20-Poly1305 → XOR 流混淆
      → AES-256-GCM → [额外层 1] → [额外层 2] → ... → .pye
```

- 每层使用从 master_key 通过 HKDF-SHA256 **域分离** 派生的独立子密钥
- 每层使用独立的随机 nonce/IV（不重用）
- 多态填充：每次 build 在末尾填充随机字节（0-N 字节），即使源码相同输出也不同

### 3. 额外加密层

可选的叠加层，在 AES-GCM 之后加密（需要通过 `pip install pycryptodome` 安装）：

| 算法 | 类型 | 块大小 | 密钥 | 模式 | 标准 |
|------|------|--------|------|------|------|
| **Serpent** | 块密码 | 128 bit | 256 bit | CBC+PKCS7 | AES 决赛算法 |
| **Twofish** | 块密码 | 128 bit | 256 bit | CBC+PKCS7 | Bruce Schneier 设计 |
| **Camellia** | 块密码 | 128 bit | 256 bit | CBC+PKCS7 | 日本标准 ISO/IEC 18033-3 |
| **Salsa20** | 流密码 | — | 256 bit | — | ChaCha20 前身 |

配置：
```json5
encrypt: {
  extra_layers: ["serpent", "twofish"],  // 按顺序叠加
}
```

**注意**：
- 改变顺序后旧文件无法解密
- salsa20 的 nonce 是 8 字节（其他是 16 字节）
- 每增加一层，运行时解密时间 +5%~15%
- 推荐组合：`["serpent", "twofish"]` 兼顾强度与性能

### 4. 混合加密

当 `hybrid.enabled: true` 时，build 流程自动：

1. 生成 RSA 或 ECC 密钥对
2. 用公钥加密 master_key
3. 私钥保存到文件（用户自行保管）
4. 加密后的 master_key 嵌入启动器

运行时：
1. 启动器提示用户输入私钥路径
2. 可选输入私钥密码（passphrase）
3. 用私钥解密 master_key
4. 后续解密流程不变

**支持的算法**：

| 算法 | 密钥生成 | 加密方式 | 密钥尺寸 |
|------|----------|----------|----------|
| RSA | `rsa_generate_keypair()` | OAEP + SHA-256 | 2048 / 3072 / **4096** / 8192 |
| ECC | `ecc_generate_keypair()` | ECIES (ECDH + HKDF + AES-256-GCM) | P-**256** / P-384 / P-521 |

配置：
```json5
encrypt: {
  hybrid: {
    enabled: true,
    algorithm: "RSA",      // RSA | ECC
    key_size: 4096,         // RSA 位长 / ECC 曲线
    key_file: "key.pem",    // 私钥保存路径
  },
}
```

**安全提示**：私钥即生命线，丢失私钥 = 加密文件永久无法解密。build 后立即将私钥移到安全位置。

### 5. 密钥系统

master_key（32 字节）被 **XOR 分片** 为 N 份，每份存入一个 `.pye` 文件：

```
master_key    = shard_1 ⊕ shard_2 ⊕ ... ⊕ shard_N
```

**5 槽位伪装**：每个 `.pye` 包含 k1~k5 共 5 个密钥槽，其中只有 1 个是真实分片，其余 4 个是随机诱饵。真实分片的顺序随机。

**三层指纹验证**（f1/f2/f3）：

```
f1 = SHA256(XOR(所有 k1~k5))[5:13]    ← 依赖所有密钥的 XOR 结果
f2 = blake3(real_shard)[3:11]          ← 只有真实分片能通过
f3 = HMAC-SHA256(real_shard, context)  ← 只有真实分片能通过
```

诱饵文件在至少一层指纹验证中失败，确保运行时能正确识别真实文件。

### 6. 反调试 / 反VM / 反沙箱

启动器加载后立即执行 9 项检测：

| 检测 | 目标 | 方法 |
|------|------|------|
| `pdb` | Python 调试器 | `sys.gettrace() != None` |
| `ptrace` | Linux 调试器 | ptrace 系统调用 |
| `debugger` | IDE 调试器 | `pydevd` 模块、`PYTHONDEBUG` 环境变量 |
| `vm` | 虚拟机 | VirtualBox/VMware/QEMU/Hyper-V/KVM/Xen 特征 |
| `sandbox` | 沙箱 | 沙箱目录特征 |
| `timing` | 调试/模拟 | 代码执行时间超过阈值 |
| `cuckoo` | Cuckoo 沙箱 | 特定文件/进程 |
| `ida` | 反编译工具 | IDA Pro/Ghidra 远程调试端口 |
| `procmon` | 监控工具 | Process Monitor/Process Hacker/Wireshark |

检测到异常后的动作：
- **`exit`**：清空内存后退出（推荐）
- **`warn`**：打印警告后继续（调试用）
- **`corrupt`**：破坏内存数据后退出（最激进）

支持 **逐检测项覆盖动作**，例如：VM 中只警告不退出，其他直接退出。

### 7. 反篡改 / 完整性校验

| 机制 | 说明 |
|------|------|
| 链式哈希 | 文件 N 的签名依赖文件 N+1 的哈希，形成闭环 |
| 文件完整性 | 启动时对所有 .pye 做 SHA256 校验 |
| 内存完整性 | 检测文件 mtime 与加载时间是否一致 |
| 反 Hook | 检测模块是否被 patch/hook |
| 反 Dump | 检测内存 dump 工具 |
| 周期自检 | 后台线程每隔 N 秒检查一次（默认 5 秒） |

### 8. 水印溯源

三层水印，用于追踪泄露来源：

| 层级 | 位置 | 内容 |
|------|------|------|
| **File** | .pye 元数据 `wm` 字段 | batch_id + ISO 时间戳 + SHA256 签名 + HMAC 认证码 |
| **Code** | 源码末尾 | 哈希校验 lambda（注入到每段源码） |
| **Runtime** | loader 启动时 | 运行时水印校验函数 |

水印报告在 build 后生成 `output/watermark_report.json`：

```json
{
  "generated": "2026-07-21T12:00:00+00:00",
  "project": "myapp",
  "total": 12,
  "batch_id": "a1b2c3d4-e5f6-...",
  "records": [
    {"file": "a1b2c3.pye", "bid": "...", "ts": "2026-07-21T12:00:00", "sig": "...", "auth": "..."},
    ...
  ]
}
```

CLI 操作：
```bash
# 提取水印
sprotect watermark extract _runtime/a1b2c3.pye --key mykey

# 验证水印真实性
sprotect watermark verify _runtime/a1b2c3.pye --key mykey

# 扫描整个目录
sprotect watermark list output/
```

### 9. 过期控制

| 功能 | 说明 |
|------|------|
| `expires_at` | 过期时间（ISO8601），到达后拒绝运行 |
| `grace_period_hours` | 过期后宽限期（小时） |
| NTP 校验 | 从 pool.ntp.org 等服务器校准时间，防系统时间篡改 |
| 漂移检测 | 本地时间与 NTP 时间偏差超过阈值（默认 1 小时）则拒绝 |
| 网络不通策略 | `reject`（拒绝运行）/ `allow`（允许）/ `grace`（记录日志） |
| 定期检查 | 运行时每隔 N 小时重新检查过期状态 |

### 10. 环境指纹绑定

将程序绑定到特定运行环境：

| 绑定类型 | 示例 |
|----------|------|
| 目录 | `bind_directory: "C:\\Program Files\\MyApp"` |
| 用户名 | `bind_username: "john"` |
| 环境变量 | `bind_env_vars: ["MYAPP_LICENSE=pro"]` |
| 文件哈希 | `bind_file_hash: "sha256:abc123..."` |
| MAC 地址 | `bind_mac_address: "AA:BB:CC:DD:EE:FF"` |
| 硬件 ID | `bind_hardware_id: "CPU-ID-..."` |

### 11. 诱饵文件系统

每次 build 自动生成 **N+2** 个诱饵 `.pye` 文件：

- 与真实文件使用相同的加密流程（minify → compress → encrypt）
- 密钥分片在指纹验证层不匹配，运行时被 `f_extract()` 过滤
- 诱饵代码使用 `decoy.py` 生成，包含真实的 import/class/function/asyncio/decorator 等 Python 语法结构
- 部分诱饵放在随机子目录中，模仿真实项目结构
- 部分诱饵是陷阱代码（死循环、异常），在运行时被 loader 识别跳过

### 12. 代码虚拟化

> ⚠️ 此功能当前为预留状态，尚未完整实现。

将 Python 函数翻译为自定义 VM 指令集执行，使反汇编结果完全不可读。支持 PARTIAL（指定函数）和 FULL（全部函数）模式。

---

## 配置文件

主配置文件 `sprotect.json5` 包含 **12 个配置段**，每个字段都有详细中文注释：

```
sprotect.json5
├── project          # 项目信息（name/version/entry）
├── files            # 文件过滤（include/exclude/exclude_dirs）
├── obfuscate        # AST 混淆（level 1-5 / 命名规则 / 字符串加密 / 控制流平坦化）
├── encrypt          # 加密（算法 / extra_layers / hybrid / 分片 / 压缩）
├── anti_debug       # 反调试（9 种检测 / 动作 / 逐项覆盖）
├── virtualization   # 代码虚拟化（预留）
├── watermark        # 水印（file/code/runtime 三层 / batch_id）
├── expiration       # 过期控制（expires_at / NTP / 漂移检测）
├── environment      # 环境指纹（目录/用户/环境变量/MAC/硬件ID）
├── sandbox          # 沙箱检测（Cuckoo / Sandboxie / Docker / CI）
├── bootloader       # 启动器（防 dump / 周期检查 / 控制台隐藏）
└── output           # 输出（目录 / runtime_dir / 日志等级）
```

**每个模块还可以有独立的 `.sprotect.json5` 覆盖配置**，放在 `sprotect/` 对应文件旁。例如 `sprotect/encrypt.py.sprotect.json5` 可以覆盖 encrypt.py 模块的混淆和反调试设置。

完整的配置参考见 `sprotect.json5` 文件本身（662 行含详细中文注释）。

---

## 构建输出结构

```
output/
├── main.py                  ← 自举启动器（可直接 python main.py）
├── requirements.txt         ← 项目依赖清单
├── watermark_report.json    ← 水印报告
├── key.pem                  ← 私钥（hybrid 模式开启时生成）
└── _runtime/
    ├── loader.pye           ← 加密后的运行时加载器
    ├── a1b2c3.pye           ← main.py 加密文件
    ├── d4e5f6.pye           ← utils.py 加密文件
    ├── g7h8i9.pye           ← models.py 加密文件
    ├── decoy_xxxx.pye       ← 诱饵文件（结构与真实文件完全相同）
    └── random_subdir/       ← 诱饵子目录
        ├── decoy_yyyy.pye
        └── decoy_zzzz.pye
```

`output/` 目录可以 **拷贝到任何有 Python 3.10+ 的机器运行**，仅需：
- Python 3.10+
- 如果开启了额外加密层（serpent 等）：`pip install pycryptodome`
- 如果是 hybrid 混合加密模式：需要私钥文件
- 项目本身依赖的第三方库

---

## 测试

```bash
# 运行所有测试
python -m pytest tests/ -v

# 仅加密功能测试（15 项）
python -m pytest tests/test_crypto_extra.py -v

# 集成构建测试
python -m pytest tests/test_integration.py -v
```

**测试覆盖**：
- `test_crypto_extra.py` — 15 项单元测试（HKDF 派生 / Serpent / Twofish / Camellia / Salsa20 加解密 / encrypt_payload_v2 / .pye v2 头 / RSA 加密 / ECC 加密）
- `test_integration.py` — 完整 build 流程集成测试

---

## 常见问题

**Q: 加密后的程序启动报错 "No valid key found"？**
A: `.pye` 文件可能被损坏，或者 project 中 `.py` 文件数少于 `shard_count`。检查配置确保 `shard_count <= 项目文件数`。

**Q: 开启了 extra_layers 但程序启动报错 "module 'Cryptodome' has no attribute..."?**
A: 目标机器缺少 `pycryptodome` 库。运行 `pip install pycryptodome`。

**Q: Hybrid 模式启动时提示 "Private key not found"?**
A: 私钥文件需要与加密后的程序一同分发。确保 `key.pem` 在输出目录中（或运行时输入正确的路径）。

**Q: 每次 build 输出都不一样？**
A: 这是正常现象。多态填充、随机密钥、随机诱饵文件名共同导致每次构建的产物不同。

**Q: 支持哪些 Python 版本？**
A: 构建工具需要 Python 3.10+。加密后的输出可在 Python 3.10+ 上运行。

**Q: 加密后的文件需要 cryptography 库吗？**
A: 运行时解密只需要 Python 标准库（hmac/hashlib/zlib/json）。`cryptography` 仅在 build 阶段使用。

**Q: 诱饵文件会影响运行吗？**
A: 不会。loader 通过三层指纹验证（f1/f2/f3）自动过滤诱饵文件，只有通过全部验证的密钥分片才会被用于解密。
