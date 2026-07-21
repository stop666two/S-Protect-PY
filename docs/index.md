# S-Protect-PY 文档

Python 代码保护工具：混淆 · 多层加密 · 反调试 · 反篡改 · 水印 · 过期控制 · 混合加密

---

## 目录

- [快速开始](quickstart.md)
- [CLI 命令参考](cli.md)
- [配置文件参考](config.md)
- [保护功能说明](features.md)
- [使用示例](examples.md)
- [API 参考](api.md)

---

## 概述

S-Protect-PY 将你的 Python 项目加密为独立可运行的输出，保护源码不被逆向。

**核心能力：**
- **AST 混淆** — 变量/函数/类重命名、字符串/数字加密、控制流平坦化、死代码注入
- **多层加密** — zlib + ChaCha20 + XOR + AES-256-GCM + 可选额外层（Serpent/Twofish 等）
- **混合加密** — RSA-4096 / ECC P-256 公钥加密 master_key
- **反调试** — 9 种检测（pdb / ptrace / VM / 沙箱 / 时序 / IDA 等）
- **反篡改** — 哈希校验 + 热重载检测 + 周期自检
- **水印** — 三层（文件/代码/运行时）+ 提取/验证 CLI
- **过期控制** — NTP 联网校验 + 时间漂移检测
- **环境绑定** — 绑定到目录/用户/硬件/MAC
- **诱饵文件** — 自动生成假文件迷惑分析
- **Pack 打包** — PyInstaller 一键打包为 exe
