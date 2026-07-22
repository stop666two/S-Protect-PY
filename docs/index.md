# S-Protect-PY 文档

Python 代码保护工具：混淆 · 多层加密 · 反调试 · 反篡改 · 水印 · 过期控制 · 混合加密 · 代码虚拟化 · 字节码保护

---

## 目录

- [快速开始](quickstart.md)
- [CLI 命令参考](cli.md)
- [配置文件参考](config.md)
- [保护功能说明](features.md)
- [使用示例](examples.md)

---

## 概述

S-Protect-PY 将你的 Python 项目加密为独立可运行的输出，保护源码不被逆向。

**核心能力：**
- **AST 混淆** — 变量/函数/类重命名、字符串/数字加密、控制流平坦化、死代码注入、**属性访问重命名**
- **多层加密** — zlib + ChaCha20 + XOR + AES-256-GCM + 可选额外层（AES-CBC 域分离密钥）
- **混合加密** — RSA-4096 / ECC P-256 公钥加密 master\_key
- **反调试** — 10 种检测（pdb / ptrace / VM / 沙箱 / 时序 / IDA / GPU 等）
- **反篡改** — 哈希校验 + 热重载检测 + 周期自检 + **完整性白名单**
- **水印** — 三层（文件/代码/运行时）+ **热补丁水印** + 提取/验证 CLI
- **过期控制** — NTP 联网校验 + 时间漂移检测
- **环境绑定** — 绑定到目录/用户/硬件/MAC
- **诱饵文件** — 自动生成假文件迷惑分析
- **代码虚拟化** — 自定义栈式 VM 编译 Python 函数为 bytecode 执行
- **字节码保护** — .pyc 级别加密 + 透明 import hook 运行时解密
- **自定义打包** — 自解压单文件打包替代 PyInstaller

**新增 CLI：** `sprotect run` · `sprotect build --clean` · `sprotect build --watch`
