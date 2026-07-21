# S-Protect-PY

Python 代码保护工具：混淆 + 加密 + 反调试 + 代码虚拟化 + 水印 + 过期控制。

## 快速开始

```bash
# 查看版本
python -m sprotect version

# 加密当前目录下的整个项目
python -m sprotect encrypt-project .

# 运行加密后的项目
python -m sprotect run .
```

---

## 安装

```bash
# 安装依赖
pip install json5 cryptography tqdm colorama

# 验证安装
python -m sprotect version
# 输出: S-Protect-PY v0.1.0
```

---

## 完整使用教程

### 1. 加密单个文件

```bash
python -m sprotect encrypt myfile.py
```

- 原文件不变
- 同级生成 `myfile.pye`（加密后的文件）

### 2. 加密多个文件

```bash
python -m sprotect encrypt a.py b.py c.py
```

### 3. 加密整个项目

```bash
cd myproject
python -m sprotect encrypt-project .
```

执行流程：
1. **备份项目** → 自动创建 `_backup/项目名_backup_时间.zip`
2. **扫描 .py 文件** → 自动发现所有 Python 源码
3. **混淆代码** → 重命名变量/函数/类名，加密字符串和数字
4. **加密** → AES-256-GCM 加密每一份源码
5. **输出到 `_runtime/`** → 加密后的文件以 `.pye` 后缀存放

### 4. 运行加密项目

```bash
cd myproject
python -m sprotect run .
```

运行时会：
1. 查找 `_runtime/` 目录下的加密文件
2. 安装自定义 import hook，拦截 `.pye` 模块的导入
3. 在内存中解密入口文件并执行（磁盘始终为加密态）

### 5. 检查文件

```bash
python -m sprotect check myfile.py
```

检查文件是否存在、Python 语法是否正确。

### 6. 配置管理

```bash
# 生成默认配置文件
python -m sprotect config init

# 查看当前配置
python -m sprotect config show
```

---

## 配置文件详解

`sprotect.json5` 使用 JSON5 格式（支持注释、不加引号的 key）。

```json5
{
  // ========== 项目信息 ==========
  project: {
    name: "myapp",          // 项目名称
    version: "1.0.0",       // 版本号
    entry: "main.py",       // 入口文件（sprotect run 时执行这个）
  },

  // ========== 混淆设置 ==========
  obfuscate: {
    level: 3,               // 混淆等级 1-5（越高越强）
    rename_variables: true,  // 重命名局部变量
    rename_functions: true,  // 重命名函数名
    rename_classes: true,    // 重命名类名
    rename_rules: {
      style: "hex",          // 命名风格: hex | chinese | invisible | math-symbols
      reserved: ["__init__", "main"],  // 保留名称（不混淆）
    },
    encrypt_strings: true,   // 加密字符串字面量
    encrypt_numbers: false,  // 加密数字字面量
    control_flow_flattening: true,  // 控制流平坦化
    dead_code_injection: false,     // 死代码注入
  },

  // ========== 加密设置 ==========
  encrypt: {
    algorithm: "aes-256-gcm",   // 加密算法
    key_source: "auto",         // 密钥来源
    interdependency: "chain",   // 文件依赖模式: chain | full-mesh | hybrid
    backup: true,               // 加密前自动备份
    replace_originals: false,   // 加密后替换原文件
    shard_count: 3,             // 密钥分片数量
  },

  // ========== 反调试设置 ==========
  anti_debug: {
    enabled: true,
    action: "exit",            // exit | warn | corrupt
    checks: ["ptrace", "debugger", "breakpoint", "timing"],
  },

  // ========== 代码虚拟化 ==========
  virtualization: {
    enabled: false,            // 是否启用
    mode: "partial",           // partial | full
    functions: [],             // 要虚拟化的函数名列表
    glob_patterns: [],         // 文件通配符模式
  },

  // ========== 水印 ==========
  watermark: {
    enabled: true,
    levels: ["file", "code"],  // file | code | runtime
    batch_id: "",              // 批次 ID（留空自动生成）
  },

  // ========== 过期时间 ==========
  expiration: {
    enabled: false,
    expires_at: null,          // 过期时间 ISO 8601, 如 "2027-12-31T23:59:59Z"
    ntp_check: true,           // 联网校验时间
    on_network_fail: "reject", // 网络不通时: reject | allow
  },

  // ========== 环境指纹 ==========
  environment: {
    enabled: false,
    bind_directory: null,      // 绑定到特定目录
    bind_username: null,       // 绑定到特定用户名
    bind_env_vars: [],         // 绑定到环境变量
  },

  // ========== 沙箱检测 ==========
  sandbox: {
    enabled: true,
  },

  // ========== 输出设置 ==========
  output: {
    dir: "./dist",
    keep_source_map: false,
  },
}
```

---

## 完整示例：加密并运行 envtest.py

```bash
# 1. 创建测试项目
mkdir demo
copy envtest.py demo\main.py
cd demo

# 2. 生成默认配置
python -m sprotect config init

# 3. 查看配置
python -m sprotect config show

# 4. 配置入口文件（编辑 sprotect.json5）
#    确保 project.entry = "main.py"

# 5. 加密项目（自动备份 + 混淆 + 加密）
python -m sprotect encrypt-project .

# 6. 查看加密产物
dir _runtime
#    main.pye  ← 加密后的文件（乱码）

# 7. 运行加密项目（内存解密执行）
python -m sprotect run .
```

---

## 各功能说明

### 混淆 (Obfuscation)

| 功能 | 说明 |
|------|------|
| 变量重命名 | 将 `user_count` → `_0x1a2b3c4d` |
| 函数重命名 | 将 `calculate_total` → `_0x4d3c2b1a` |
| 类重命名 | 将 `UserManager` → `_0x7e8f9a0b` |
| 字符串加密 | `"secret"` → `base64.b64decode("c2VjcmV0").decode()` |
| 数字加密 | `42` → `struct.unpack("d", base64.b64decode("..."))[0]` |
| 控制流平坦化 | 将顺序执行的代码转为 while+if 分派器 |
| 死代码注入 | 插入永不为真的 if 块迷惑静态分析 |

### 加密 (Encryption)

- 算法: AES-256-GCM（带认证标签，防篡改）
- 密钥: 每次随机生成
- 载荷格式: JSON `{type, algorithm, aes_key, data, source_hash}`
- 运行时: 在内存中解密，磁盘始终为密文

### 反调试 (Anti-Debug)

| 检测项 | 说明 |
|--------|------|
| pdb 检测 | `sys.gettrace() != None` |
| 调试器检测 | `pydevd` 模块、`PYTHONDEBUG` 环境变量 |
| ptrace 检测 | Linux 平台 ptrace 系统调用 |
| VM 检测 | 检测 VirtualBox/VMware/QEMU 等虚拟机 |

检测到调试器后的动作：
- `exit`: 清空内存并退出
- `warn`: 打印警告但不退出
- `corrupt`: 随机破坏内存数据后退出

### 代码虚拟化

将 Python 函数翻译为自定义 VM 指令集，用内置的解释器执行：

```
LOAD_CONST → 0x01   # 压入常量
LOAD_NAME  → 0x02   # 压入变量
STORE_NAME → 0x03   # 存储变量
BINARY_ADD → 0x10   # 加法
CALL_FUNC  → 0x20   # 函数调用
RETURN_VAL → 0x30   # 返回值
```

支持 PARTIAL（仅虚拟化指定函数）和 FULL（虚拟化所有函数）两种模式。

### 水印

三层水印用于追踪泄露源：
- **文件级**: 在文件末尾追加不可见注释行 `// WM:batch_id:hash`
- **代码级**: 在源码中插入带水印校验的 no-op lambda
- **运行时**: 运行时验证水印完整性

### 过期时间

- 加密时写入 `encrypted_at` 和 `expires_at`
- 运行时检测系统时间是否在有效窗口内
- 可选 NTP 联网校验防止本地时钟篡改
- 网络不通时可按配置放行或拒绝

---

## CLI 命令参考

```
sprotect encrypt <files...>      加密指定文件
sprotect encrypt-project [dir]   加密整个项目目录
sprotect run [dir]               运行加密项目
sprotect config init             生成默认配置文件
sprotect config show             查看当前配置
sprotect check <files...>        检查文件状态
sprotect version                 查看版本
```

---

## 测试

```bash
# 运行所有测试
python -m pytest tests -v

# 运行单个测试文件
python -m pytest tests/test_obfuscator.py -v
```

---

## 项目结构

```
├── sprotect/                  主包
│   ├── __init__.py            版本信息
│   ├── __main__.py            python -m sprotect 入口
│   ├── cli.py                 CLI 参数解析与分发
│   ├── config.py              JSON5 配置加载
│   ├── types.py               类型定义 (dataclasses + enums)
│   ├── core/                  核心引擎
│   │   ├── encryptor.py       加密
│   │   ├── decryptor.py       解密
│   │   ├── obfuscator.py      AST 混淆
│   │   ├── project.py         项目扫描
│   │   └── backup.py          备份
│   ├── runtime/               运行时
│   │   ├── loader.py          解密加载器
│   │   ├── verifier.py        完整性校验
│   │   ├── anti_debug.py      反调试
│   │   ├── shard_reconstructor.py  密钥重构
│   │   ├── index.py           运行时索引
│   │   └── expiration.py      过期检查
│   ├── features/              可选功能
│   │   ├── control_flow.py    控制流平坦化
│   │   ├── dead_code.py       死代码注入
│   │   ├── virtualization.py  代码虚拟化
│   │   ├── watermark.py       水印
│   │   ├── environment.py     环境指纹
│   │   └── network.py         NTP
│   └── utils/                 工具
│       ├── crypto.py          密码学
│       ├── shard.py           密钥分片
│       ├── sign.py            签名
│       ├── index_builder.py   索引构建
│       └── random_gen.py      随机名生成
├── tests/                     测试 (66 个测试用例)
├── sprotect.bat               Windows 启动脚本
├── run_tests.bat              测试启动脚本
└── sprotect.json5             默认配置
```
