# 保护功能说明

## AST 混淆

| 变换 | 说明 | 配置 |
|------|------|------|
| 变量重命名 | `user_count` → `_0xa1b2c3` | `rename_variables: true` |
| 函数重命名 | `def validate()` → `def _0x...()` | `rename_functions: true` |
| 类重命名 | `class User()` → `class _0x...()` | `rename_classes: true` |
| 字符串加密 | `"secret"` → `base64.b64decode('...').decode()` | `encrypt_strings: true` |
| 数字加密 | `4096` → `struct.unpack('i', b64decode('...'))` | `encrypt_numbers: true` |
| 字符串分割 | `"hello"` → `"hel" + "lo"` | `string_split: true` |
| 控制流平坦化 | 顺序代码 → while+switch 分派器 | `control_flow_flattening: true` |
| 死代码注入 | 插入永不执行的条件分支 | `dead_code_injection: true` |
| import 混淆 | `import os` → `os = __import__(...)` | `obfuscate_imports: true` |
| 调用混淆 | `func(a)` → `(lambda _a: func(_a))(a)` | `obfuscate_calls: true` |

## 多层加密管道

```
源码 → zlib → ChaCha20-Poly1305 → XOR → AES-256-GCM → [Serpent] → [Twofish] → .pye
```

每层使用 HKDF-SHA256 从 master_key 派生独立子密钥。

## 密钥系统

- master_key XOR 分片为 N 份，每份存入一个 .pye 文件
- 每个文件含 5 个密钥槽（1 真 + 4 假）
- 三层指纹验证（f1=XOR+SHA256, f2=blake3, f3=HMAC）

## 其他功能

- 反调试：9 种检测 + 可逐项覆盖动作
- 反篡改：文件哈希 + 热重载检测 + 周期自检
- 水印：文件级 + 代码级 + 运行时
- 过期控制：时间 + NTP + 漂移检测
- 环境绑定：目录/用户/硬件/MAC
- 诱饵文件：伪随机生成假 .pye 文件
- Pack 打包：PyInstaller → 单文件 exe
