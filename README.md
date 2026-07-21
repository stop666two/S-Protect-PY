# S-Protect-PY

Python 代码保护工具：混淆 + 加密 + 反调试 + 代码虚拟化 + 水印 + 过期控制。

## 核心流程

```
project/          output/
  main.py    →     main.py         ← 自举启动器（零外部依赖）
  utils.py         _runtime/
  models.py          main.pye      ← HMAC-SHA256 加密后的源码
                     utils.pye
                     models.pye
                     loader.py     ← 解密加载器（纯 Python stdlib）
                   requirements.txt
```

1. 把你的 Python 项目放进 `project/` 目录
2. 运行 `sprotect build` → 加密到 `output/` 目录
3. 把 `output/` 拷到任何有 Python 的机器上运行

---

## 快速开始

```bash
# 1. 把源码放入 project/ 目录
mkdir project
copy myapp.py project\main.py

# 2. 构建加密项目
sprotect build

# 3. 运行加密后的项目
cd output
python main.py
```

---

## 安装

```bash
pip install json5 cryptography tqdm colorama
python -m sprotect version
# 输出: S-Protect-PY v0.1.0
```

---

## 完整用法

### 构建加密项目

```bash
# 默认: project/ → output/
sprotect build

# 指定目录
sprotect build --project ./src --output ./dist

# 使用指定配置文件
sprotect build -c myconfig.json5
```

执行流程：
1. **备份** `project/` → `_backup/项目名_时间.zip`
2. **扫描** 所有 `.py` 文件（排除 `_runtime/`、`_backup/` 等）
3. **混淆** 变量/函数/类名重命名 + 字符串/数字加密
4. **加密** HMAC-SHA256 流密码加密每一份源码
5. **生成启动器** `output/main.py` + `output/_runtime/loader.py`
6. **输出** 完整可独立运行的加密项目

### 运行加密项目

```bash
cd output
python main.py
```

无需安装 S-Protect，无需 `cryptography` 库，纯 Python stdlib 即可解密运行。

### 加密单个文件

```bash
sprotect encrypt myfile.py
# 生成 myfile.pye
```

### 检查文件

```bash
sprotect check myfile.py
# 检查语法是否正确
```

### 配置管理

```bash
sprotect config init       # 生成默认 sprotect.json5
sprotect config show       # 查看当前配置
```

---

## output/ 目录结构

```
output/
├── main.py                ← 自举启动器（可直接 python main.py）
├── requirements.txt       ← 项目依赖清单（自行补充）
└── _runtime/
    ├── loader.py          ← 解密加载器（纯 Python stdlib）
    ├── main.pye           ← main.py 加密后的文件
    ├── utils.pye          ← 其他模块加密后
    └── models.pye
```

**output/ 可以拷到任何机器运行**，只需要：
- Python 3.10+
- 项目本身用到的第三方库（在 requirements.txt 中列出）

---

## 配置文件参考

`sprotect.json5`（放在项目根目录）：

```json5
{
  project: {
    name: "myapp",          // 项目名称
    version: "1.0.0",       // 版本号
    entry: "main.py",       // 入口文件（对应 project/main.py）
  },
  obfuscate: {
    level: 3,               // 混淆等级 1-5
    rename_variables: true,  // 重命名变量
    rename_functions: true,  // 重命名函数
    rename_classes: true,    // 重命名类
    rename_rules: {
      style: "hex",          // 命名风格: hex | chinese | invisible | math-symbols
      reserved: ["__init__", "main"],  // 保留名称
    },
    encrypt_strings: true,   // 加密字符串字面量
    encrypt_numbers: false,  // 加密数字字面量
    control_flow_flattening: true,  // 控制流平坦化
    dead_code_injection: false,     // 死代码注入
  },
  encrypt: {
    algorithm: "hmac-sha256-xor",
    backup: true,            // 构建前自动备份
    shard_count: 3,          // 密钥分片数
  },
  anti_debug: {
    enabled: true,
    action: "exit",          // exit | warn | corrupt
  },
  virtualization: {
    enabled: false,
    mode: "partial",         // partial | full
    functions: [],
  },
  watermark: {
    enabled: true,
    levels: ["file", "code"],
  },
  expiration: {
    enabled: false,
    expires_at: null,
    ntp_check: true,
  },
  environment: {
    enabled: false,
  },
}
```

---

## 各功能说明

### 混淆 (Obfuscation)
| 功能 | 效果 |
|------|------|
| 变量重命名 | `user_count` → `_0x1a2b3c4d` |
| 字符串加密 | `"secret"` → `base64.b64decode("...").decode()` |
| 控制流平坦化 | 顺序代码 → while+if 分派器 |
| 死代码注入 | 插入永不为真的 if 块 |

### 加密
- **算法**: HMAC-SHA256 流密码（XOR + HMAC 完整性校验）
- **运行时零依赖**: 仅使用 `hmac`、`hashlib`、`json` 等 Python 标准库
- **自举启动器**: `output/main.py` 自带解密和 import hook，无需 S-Protect 本体

### 反调试
| 检测 | 说明 |
|------|------|
| pdb 检测 | `sys.gettrace()` |
| 调试器检测 | `pydevd` 模块、`PYTHONDEBUG` |
| ptrace 检测 | Linux ptrace 系统调用 |
| VM 检测 | VirtualBox/VMware/QEMU |

检测到调试器后：`exit`(清内存退出) / `warn`(警告) / `corrupt`(破坏内存)

### 代码虚拟化
将 Python 函数翻译为自定义 VM 指令集：
```
LOAD_CONST(0x01) → 压入常量
CALL_FUNC(0x20)  → 调用函数
RETURN_VAL(0x30) → 返回值
```
支持 PARTIAL（指定函数）和 FULL（全部函数）模式。

### 水印 (Watermark)
- **文件级**: 文件末尾追加 `// WM:batch_id:hash`
- **代码级**: 插入带水印校验的 no-op lambda
- **运行时**: 运行时验证水印完整性

### 过期时间
- 内嵌 `encrypted_at` 和 `expires_at`
- NTP 联网校验（可选）
- 防回滚：系统时间早于加密时间则拒绝运行

---

## CLI 命令参考

```bash
sprotect build                   # project/ → output/
sprotect build --project ./src   # 指定源码目录
sprotect encrypt file.py         # 加密单个文件
sprotect config init             # 生成默认配置
sprotect config show             # 查看配置
sprotect check file.py           # 检查文件
sprotect version                 # 查看版本
```

---

## 完整示例

```bash
# 1. 准备源码
mkdir myproject
cd myproject
echo "print('Hello from encrypted project!')" > main.py

# 2. 初始化配置
sprotect config init

# 3. 编辑 sprotect.json5，确保 entry = "main.py"

# 4. 构建加密项目
sprotect build

# 5. 查看输出
dir output
#    main.py  _runtime/

# 6. 运行加密项目
python output/main.py
# 输出: Hello from encrypted project!
```

---

## 测试

```bash
python -m pytest tests -v      # 运行全部 64+ 测试
python -m pytest tests/test_obfuscator.py -v   # 单文件测试
```
