# S-Protect-PY

**Python 代码保护工具** — AI 抗性 · 6层加密 · 远程密钥分片 · 反调试/反模拟器 · AST混淆(L5) · Shamir门限 · 双进程架构

---

## 目录

- [原理](#原理)
- [对抗 AI 逆向](#对抗-ai-逆向)
- [防御矩阵](#防御矩阵)
- [快速开始](#快速开始)
- [CLI 命令](#cli-命令)
- [保护功能](#保护功能)
- [测试](#测试)
- [常见问题](#常见问题)

---

## 原理

```
project/                          output/
┌──────────┐                    ┌──────────────────┐
│ main.py  │──┐                 │  main.py         │ ← 25个HEX变量交织 + 3路径多态 HMAC
│ mod_a.py │  │  ╔═══════════╗  │  _meta/          │ ← 完整性报告/水印报告
│ mod_b.py │  ├──╢ sprotect  ╠──┤  _runtime/       │ ← 加密模块(.pye)
│ mod_c.py │  │  ║ build     ║  │  ├── loader.pye  │ ← 6层HKDF/AES-GCM
└──────────┘  │  ╚═══════════╝  │  ├── *.pye       │ ← Shamir分片+密文+层间哈希
sprotect.json5 │                 │  ├── _key_store  │ ← 远程分片(可选部署)
┌──────────┐  │                 │  └── _decoy/     │ ← 诱饵文件(5个)
│ 配置     │──┘                 └──────────────────┘
└──────────┘                       ↓
                            python main.py 即可运行
```

### 运行时解密链

```
main.py 启动
  │
  ├── 25个HEX变量 → 3路径多态选择 → HMAC派生loader_key
  │
  ├── [可选] HTTP拉取远程Shamir分片
  │
  ├── AES-GCM + XOR流 + ChaCha20 + zlib → 解密loader.pye
  │
  ├── 200-300诱饵函数中定位6个真实执行段
  │
  ├── 收集本地+远程Shamir分片 → GF(256) Lagrange插值 → master_key
  │
  ├── 层间哈希链验证 → 6层HKDF/AES-GCM逐层剥解 → 源码
  │
  ├── 反调试/反模拟器/进程枚举/时间戳反演 → 异常则exit(1)
  │
  └── 模块加载后.pye自动删除 + 内存校验+栈混淆
```

---

## 对抗 AI 逆向

S-Protect-PY 专门设计了针对 AI 大模型逆向的防御层。核心策略：**让 AI 的上下文窗口和模式匹配失效**。

| 防御 | 原理 | 效果 |
|------|------|------|
| 语义噪声 5x | 200-300 诱饵函数淹没 6 个真实执行段 | ⭐⭐⭐⭐⭐ |
| 上下文污染 | 垃圾代码块填充 AI 注意力窗口 | ⭐⭐⭐⭐ |
| 假加密库导入 | cryptography 假导入误导 AI 模式判断 | ⭐⭐⭐ |
| 不透明表达式 | a+b→(a^b)+2*(a&b)，AI 不擅长代数简化 | ⭐⭐⭐ |
| 隐式数据流 | 常量化身 if-else 分支，AI 数据/控制流独立分析 | ⭐⭐⭐⭐ |
| 字符串分散 | 字符串切碎散落，AI 无法在单一位置看到完整值 | ⭐⭐ |
| match/case 调度 | 50%概率用 match 替代 if/elif，LLM 难静态推断 | ⭐⭐⭐ |

---

## 防御矩阵

| 攻击方式 | 对应防御 | 绕过难度 |
|---------|---------|---------|
| 静态分析提取 salt | 25 个 HEX_VARS + 3 路径多态 | 中 |
| 逐层剥离加密 | 层间哈希链验证 | 高 |
| 离线提取密钥 | 远程 HTTP 分片部署 | 极高 |
| AI 大模型分析代码 | 语义噪声 + 上下文污染 | 极高 |
| 调试器动态跟踪 | 反调试 10 项 + 调用栈混淆 | 高 |
| 内存 dump | 双进程架构(父进程持密钥) | 高 |
| 模拟器分析 | QEMU/VMware/KVM 检测 | 中 |
| 沙箱分析 | Cuckoo/Docker/Sandboxie 检测 | 高 |

---

## 快速开始

```bash
# 1. 安装
pip install -r requirements.txt

# 2. 准备项目
mkdir my_project
echo 'print("Hello World!")' > my_project/main.py

# 3. 构建加密
cd my_project
python -m sprotect build --clean

# 4. 运行
python -m sprotect run
```

### 启用远程密钥分片(推荐)

```json5
// sprotect.json5
encrypt: {
    key_server: "https://your-server.com/api/shares",
}
```

将 `output/_runtime/_key_store.json` 部署到 HTTPS 服务器。

---

## CLI 命令

| 命令 | 用途 |
|------|------|
| `sprotect build` | 构建加密项目 |
| `sprotect run` | 运行加密项目 |
| `sprotect config` | 配置管理 |
| `sprotect watermark` | 水印操作 |
| `sprotect pack` | PyInstaller 打包 |

---

## 保护功能

### AST 混淆 L5

8 道传递：命名重命名 → 字符串加密/分散 → 数字加密 → import 混淆 → 调用混淆 → 算术/布尔混淆 → 不透明表达式 → 控制流平坦化(match/case + if/elif) → 死代码注入 + 隐式数据流

### 6 层加密体系

每层 `HKDF(master_key, "layer:{i}")` → AES-GCM，层间 SHA256 哈希链验证。

### 远程密钥分片

支持 HTTPS 远程拉取部分 Shamir 分片。缺失则阈值不满足，master_key 恢复失败。

### 双轨密钥系统

- **Shamir**(主)：GF(256) Lagrange 插值
- **XOR + k1-k5 指纹**(备)：60% 假密钥可通过 f1/f2/f3 验证

### 反调试 / 反模拟器

10 项检测 + 进程枚举(20+工具) + 时间戳反演 + 模拟器检测(QEMU/VMware/KVM/VirtualBox)

### 运行时保护

内存校验和、调用栈混淆、文件系统饵雷、内存 TTL、时间墙自动擦除

---

## 测试

```bash
# 全部测试(177 项)
python -m pytest tests/ -v

# 按模块
python -m pytest tests/test_obfuscate.py -v   # 混淆引擎
python -m pytest tests/test_compressor.py -v  # 压缩器
python -m pytest tests/test_anti_tamper.py -v # 反篡改
python -m pytest tests/test_integration.py -v # 集成测试
```

---

## 常见问题

**Q: 加密后需要什么依赖运行？**
A: 运行只需要 Python 标准库。cryptography 仅在 build 阶段使用。

**Q: 远程密钥服务器怎么部署？**
A: 将 `_key_store.json` 部署到 HTTPS 服务器，返回 JSON 数组 `[[sid, sv], ...]`。

**Q: 每次 build 输出都不一样？**
A: 正常。多态填充、随机盐值、随机诱饵共同导致。
