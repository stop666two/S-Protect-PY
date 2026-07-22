# 使用示例

## 基础保护

```bash
sprotect build
sprotect run
```

## 最大保护

```json5
// sprotect.json5
{
  obfuscate: { level: 5, encrypt_numbers: true, dead_code_injection: true },
  encrypt: { extra_layers: ["serpent", "twofish", "camellia"], shard_count: 5 },
  bootloader: { periodic_check_interval: 3.0 },
}
```

```bash
sprotect build --clean
```

## 混合加密（RSA/ECC）

```json5
encrypt: { hybrid: { enabled: true, algorithm: "ECC", key_size: 256 } }
```

```bash
sprotect build
# build 后私钥保存在 output/key.pem，需妥善保管
```

## 代码虚拟化

```json5
virtualization: { enabled: true, functions: ["validate_license", "decrypt_core"] }
```

## 持续开发（watch 模式）

```bash
# 启动监控，修改源码后自动重构建
sprotect build --watch
```

## 水印溯源 + 热补丁

```bash
# 查看构建时水印
sprotect watermark list output/_runtime/

# 分发后追踪泄露来源
python -c "
from sprotect.watermark import patch_watermark_batch
patch_watermark_batch('output/_runtime/', 'CUSTOMER-ABC', 'mysecret', append=True)
"
```

## 字节码保护

```python
from sprotect.bytecode_protect import protect_code, SecureImporter
key = os.urandom(32)
with open("app.py") as f:
    code = compile(f.read(), "app.py", "exec")
ct = protect_code(code, key)
open("app.pye", "wb").write(ct)

# 加载时
sys.meta_path.insert(0, SecureImporter(".", key))
import app  # 透明解密
```

## 自定义打包

```python
from sprotect.pack_custom import pack_to_single_file
pack_to_single_file("./output", "./dist/bundle.py", loader_key)
# 生成单个 bundle.py，复制到任意 Python 3.10+ 环境即可运行
```

## 完整性校验

```bash
# build 自动生成 integrity_manifest.json
# 运行时自动校验文件完整性，检测到篡改或新增文件立即拒绝启动
```

## .env + hybrid 模式

```bash
# output/.env
KEY_PATH=/etc/myapp/key.pem

sprotect run
# 自动加载 .env，无需手动输入私钥路径
```
