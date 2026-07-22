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
- **AST 混淆 L5** — 变量/函数/类重命名、字符串/数字加密、控制流平坦化、死代码注入、import 混淆、调用混淆、蜜罐函数注入
- **多层加密** — zlib + ChaCha20 + XOR + AES-256-GCM + 可选 AES-CBC 额外层
- **混合加密** — RSA-4096 / ECC P-256 公钥加密 master\_key
- **反调试** — 10 种检测（pdb / ptrace / VM / 沙箱 / 时序 / IDA / GPU 等）
- **反篡改** — 哈希校验 + 完整性白名单 + 内存反 dump + 周期自检
- **水印** — 三层（文件/代码/运行时）+ 热补丁水印 + 提取/验证 CLI
- **过期控制** — NTP 联网校验 + IPv4/IPv6 双栈
- **环境绑定** — 绑定到目录/用户/硬件/MAC
- **诱饵文件系统** — 自动生成假文件 + 蜜罐函数迷惑分析
- **代码虚拟化** — 自定义栈式 VM（20+ 指令），编译 Python 函数为 bytecode 执行
- **字节码保护** — .pyc 级别 marshal + AES-GCM 加密 + import hook
- **数字指纹** — 文件哈希校验 + 远程上报 + 后台定时检测
- **内存保护** — secure\_zero 清零 + GC 遍历 + VirtualProtect
- **自定义打包** — 自解压单文件 / .pyz zip 包
