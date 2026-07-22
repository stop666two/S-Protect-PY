# 保护功能说明

## AST 混淆

| 变换 | 说明 | 配置 |
|------|------|------|
| 变量重命名 | `user_count` → `_0xa1b2c3` | `rename_variables: true` |
| 函数重命名 | `def validate()` → `def _0x...()` | `rename_functions: true` |
| 类重命名 | `class User()` → `class _0x...()` | `rename_classes: true` |
| **属性访问重命名** | `obj.CONST` → `obj._0x...`（跨模块一致） | 自动启用 |
| 字符串加密 | `"secret"` → base64/XOR 运行时解码 | `encrypt_strings: true` |
| 数字加密 | `4096` → `struct.unpack(...)` | `encrypt_numbers: true` |
| 字符串分割 | `"hello"` → `"hel" + "lo"` | `string_split: true` |
| 控制流平坦化 | 顺序代码 → while+switch 分派器 | `control_flow_flattening: true` |
| 死代码注入 | 插入永不执行的条件分支 | `dead_code_injection: true` |
| import 混淆 | `from X import Y` → `Y = __import__("X").Y`（属性名同步重命名） | `obfuscate_imports: true` |
| 调用混淆 | `func(a)` → `(lambda _a: func(_a))(a)` | `obfuscate_calls: true` |
| 算术混淆 | `a+b` → `a-(-b)` | `obfuscate_arithmetic: true` |
| 布尔混淆 | `True/False` → `1==1` / `1!=0` | `obfuscate_booleans: true` |

## 多层加密管道

```
源码 → zlib → ChaCha20-Poly1305 → XOR → AES-256-GCM → [额外层] → .pye
```

每层使用 HKDF-SHA256 从 master_key 派生独立子密钥。额外层支持：

| 层名 | 实现 | 类型 |
|------|------|------|
| `serpent` | AES-256-CBC (cryptography) | 块密码 |
| `twofish` | AES-256-CBC (cryptography) | 块密码 |
| `camellia` | AES-256-CBC (cryptography) | 块密码 |
| `salsa20` | Salsa20 (pycryptodome) | 流密码 |

> 注意：所有块密码层统一使用 AES-256-CBC，但每层通过 HKDF 域分离使用独立密钥。
> 加密管道顺序：serpent → twofish → camellia → salsa20，解密时反向执行。

## 密钥系统

- master_key XOR 分片为 N 份，每份存入一个 .pye 文件
- 每个文件含 5 个密钥槽（1 真 + 4 假诱饵）
- 三层指纹验证（f1=XOR+SHA256, f2=blake3, f3=HMAC）

## 反调试 / 反VM / 反沙箱

10 项检测：

| 检测 | 目标 | 方法 |
|------|------|------|
| pdb | Python 调试器 | sys.gettrace() |
| ptrace | Linux 调试器 | ptrace 系统调用 |
| debugger | IDE 调试器 | pydevd 模块/环境变量 |
| vm | 虚拟机 | VirtualBox/VMware/QEMU/Hyper-V 特征 |
| sandbox | 沙箱 | 目录/进程特征 |
| timing | 调试/模拟 | 代码执行时间阈值 |
| cuckoo | Cuckoo 沙箱 | 特定文件/进程 |
| ida | 反编译工具 | IDA Pro/Ghidra 远程端口 |
| procmon | 监控工具 | Process Hacker/Wireshark 等 |
| **gpu** | **GPU 调试** | **CUDA 环境变量/Nsight/cuda-gdb** |

检测到异常后的动作：exit / warn / corrupt，支持逐检测项覆盖。

## 反篡改

| 机制 | 说明 |
|------|------|
| 链式哈希 | 文件 N 的签名依赖文件 N+1 的哈希 |
| 文件完整性 | 启动时对所有 .pye 做 SHA256 校验 |
| **完整性白名单** | **integrity\_manifest.json 记录所有文件哈希，运行时检测缺失/篡改/新增** |
| 反 Hook | 检测模块是否被 patch/hook |
| 反 Dump | 检测内存 dump 工具 |
| 周期自检 | 后台线程定期检查 |

## 水印溯源

三层水印：

| 层级 | 位置 | 内容 |
|------|------|------|
| File | .pye 元数据 wm 字段 | batch_id + ISO 时间戳 + SHA256 + HMAC |
| Code | 源码末尾 | 哈希校验 lambda |
| Runtime | loader 启动时 | 运行时校验函数 |

**热补丁水印：** 无需重新加密即可更新 .pye 文件的水印。使用场景：

```python
from sprotect.watermark import patch_watermark, patch_watermark_batch

# 单个文件打补丁（保留原始 bid 在 prev 字段）
patch_watermark("output/_runtime/a1b2c3.pye", "CUSTOMER-ABC", "mysecret", append=True)

# 批量更新整个目录
patch_watermark_batch("output/_runtime/", "BATCH-V2", "mysecret")
```

## 代码虚拟化

将 Python 函数编译为自定义 VM 指令集执行：

```json5
virtualization: {
  enabled: true,
  mode: "partial",          // partial | full
  functions: ["validate_license", "decrypt_core"],
}
```

支持的 VM 指令：LOAD\_CONST / LOAD\_NAME / STORE\_NAME / BINARY\_ADD / SUB / MUL / DIV /
COMPARE\_EQ / NE / LT / GT / JUMP\_IF\_FALSE / CALL\_FUNCTION / RETURN\_VALUE 等 20+。

## 字节码保护（.pyc 级别）

marshal + zlib + AES-GCM 加密代码对象，运行时通过 import hook 透明解密：

```python
from sprotect.bytecode_protect import protect_code, SecureImporter

key = os.urandom(32)
ct = protect_code(compile("def f(): return 42", "test", "exec"), key)
# ct 可分发到目标机器

# 目标机器上透明加载
sys.meta_path.insert(0, SecureImporter(runtime_dir, key))
```

## 自定义打包器

替代 PyInstaller，生成自包含可执行文件：

```python
from sprotect.pack_custom import pack_to_single_file

pack_to_single_file("./output", "./bundle.py", loader_key)
# 生成单个 .py 文件，内嵌所有加密数据
```

## 环境绑定

将程序绑定到特定运行环境：

```json5
environment: {
  bind_directory: "C:\\Program Files\\MyApp",
  bind_username: "john",
  bind_mac_address: "AA:BB:CC:DD:EE:FF",
}
```

## 过期控制

```json5
expiration: {
  enabled: true,
  expires_at: "2027-12-31T23:59:59Z",
  ntp_check: true,           // 联网校准防止时间篡改
  max_drift_seconds: 3600,   // 时间偏差阈值
}
```

## .env 支持

`output/.env` 文件自动加载到运行环境：

```bash
# output/.env
KEY_PATH=/secure/path/key.pem
MYAPP_LICENSE=pro
```

`sprotect run` 自动加载；hybrid 模式下可通过 `KEY_PATH` 环境变量指定私钥路径。
