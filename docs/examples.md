# 使用示例

## 基础保护

```bash
sprotect build
sprotect run
```

## 最大保护

```bash
sprotect build --clean
```

## 混合加密（ECC P-256）

```json5
encrypt: { hybrid: { enabled: true, algorithm: "ECC", key_size: 256 } }
```

## 持续开发（watch 模式）

```bash
sprotect build --watch
```

## 水印热补丁

```python
from sprotect.watermark import patch_watermark_batch
patch_watermark_batch("output/_runtime/", "CUSTOMER-ABC", "mysecret", append=True)
```

## 字节码保护

```python
from sprotect.bytecode_protect import protect_code, SecureImporter
key = os.urandom(32)
ct = protect_code(compile(open("app.py").read(), "app.py", "exec"), key)
open("app.pye", "wb").write(ct)
sys.meta_path.insert(0, SecureImporter(".", key))
import app  # 透明解密
```

## 自定义打包

```python
from sprotect.pack_custom import pack_to_single_file
pack_to_single_file("./output", "./dist/bundle.py", loader_key)
```

## 数字指纹上报

```python
from sprotect.fingerprint import compute_fingerprint, report_fingerprint
fp = compute_fingerprint("output/_runtime/")
report_fingerprint("https://api.example.com/fp", "BUILD-001", "output/_runtime/")
```

## 代码虚拟化

```json5
virtualization: { enabled: true, functions: ["validate_license", "decrypt_core"] }
```

## 查看构建元数据

```bash
cat output/_meta/build.spec
cat output/_meta/protection_report.html
```

## .env + hybrid 模式

```bash
echo "KEY_PATH=/etc/myapp/key.pem" > output/.env
sprotect run
```
