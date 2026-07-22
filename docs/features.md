# 保护功能说明

## AST 混淆（L1-L5，全部模块全开）

所有 22 个模块的 `.sprotect.json5` 配置均使用 **L5 全开**。

| 变换 | 说明 |
|------|------|
| 变量/函数/类重命名 | `user_count` → `_0xa1b2c3` |
| 属性访问重命名 | `mymodule.CONST` → `mymodule._0x...`（仅对象名也在 rename map 中时） |
| 字符串加密 | `"secret"` → `base64.b64decode(...)` 或 `(lambda k,d: ...)(KEY, bytes)` |
| 数字加密 | `4096` → `struct.unpack('i', b64decode('...'))` |
| 控制流平坦化 | 函数体转为 `while + if-elif` 链式状态机（跳过含 yield/async 的函数） |
| 死代码注入 + 蜜罐函数 | 注入永不执行的分支 + 虚假解密/验证函数（含死循环/`os._exit` 陷阱） |
| import 混淆 | `from X import Y` → `Y = __import__("X").Y`（fromlist 保持原名） |
| 调用混淆 | `func(a)` → `(lambda _a0,_a1: _a0(_a1))(func, a)`（跳过 `*args` 解包） |
| 算术混淆 | `a+b` → `a-(-b)`，`a*2^n` → `a<<n`（仅数值类型） |
| 布尔混淆 | `True/False` → `1==1` / `1!=0` |

## 多层加密管道

```
源码 → zlib → ChaCha20-Poly1305 → XOR → AES-256-GCM → [额外层] → .pye
```

额外层统一使用 AES-256-CBC（cryptography 库），每层通过 HKDF-SHA256 域分离派生独立密钥。

## 密钥系统

- master_key XOR 分片为 N 份，每份一个 .pye 文件
- 每个文件含 5 个密钥槽（1 真 + 4 诱饵）
- 三层指纹验证：f1=XOR+SHA256, f2=blake3/SHA256, f3=HMAC

## 反调试

10 项检测：pdb、ptrace（Win/Linux）、debugger、vm、sandbox、timing、cuckoo、ida、procmon、**gpu**

GPU 检测：CUDA 环境变量（11 个）、GPU 调试工具进程（nsight/cuda-gdb 等 8 个）、Linux CUDA 工具包文件。

## 反篡改

- 链式哈希校验
- **integrity\_manifest.json**（`output/_meta/`）— 所有 .pye 的 SHA256，运行时检测缺失/篡改/新增
- **secure\_zero** — ctypes 方式清零敏感 bytearray
- **wipe\_sensitive** — GC 遍历清零缓存对象
- 周期自检 + 反 Hook + 反 Dump

## 水印溯源

三层 + 热补丁：

```python
from sprotect.watermark import patch_watermark_batch
patch_watermark_batch("output/_runtime/", "CUSTOMER-ABC", "mysecret", append=True)
```

## 代码虚拟化

自定义栈式 VM，20+ 指令：

| 类别 | 指令 |
|------|------|
| 数据 | LOAD\_CONST, LOAD\_NAME, STORE\_NAME |
| 运算 | ADD, SUB, MUL, DIV, MOD, POW, AND, OR, XOR, LSHIFT, RSHIFT |
| 比较 | EQ, NE, LT, GT, LE, GE |
| 控制 | JUMP\_FORWARD, JUMP\_IF\_FALSE, JUMP\_ABSOLUTE |
| 复合 | BUILD\_LIST/TUPLE/SET/DICT, FOR\_ITER, SETUP\_EXCEPT |
| 调用 | CALL\_FUNCTION, YIELD\_VALUE, LOAD\_ATTR, LOAD\_SUBSCR |

## 字节码保护

marshal + zlib + AES-GCM 加密代码对象，`SecureImporter` import hook 透明解密：

```python
from sprotect.bytecode_protect import SecureImporter
sys.meta_path.insert(0, SecureImporter(runtime_dir, key))
```

## 数字指纹

```python
from sprotect.fingerprint import compute_fingerprint, report_fingerprint, check_integrity
fp = compute_fingerprint("output/_runtime/")
report_fingerprint("https://your-server.com/api", batch_id, "output/_runtime/")
```

## 自定义打包

```python
from sprotect.pack_custom import pack_to_single_file, pack_to_onefile
pack_to_single_file("./output", "./bundle.py", loader_key)
```

## 输出结构

```
output/
├── main.py                    ← 自举启动器
├── .env                       ← 环境变量（可选）
├── key.pem                    ← 私钥（hybrid 模式）
├── requirements.txt
├── _runtime/                  ← 加密模块
│   ├── loader.pye
│   ├── a1b2c3.pye
│   └── ...
└── _meta/                     ← 元数据（构建信息）
    ├── integrity_manifest.json
    ├── build.spec
    ├── protection_report.html
    └── watermark_report.json
```

## 已知限制

- `importlib.reload()` 对加密模块不兼容（AST 混淆的固有局限）
- `sys._getframe()` / `inspect.getsource()` 在加密模块中不可用（无源码）
- 控制流平坦化跳过含 `yield`/`yield from`/推导式的函数
- `CallObfuscator` 跳过 `*args` 解包参数
