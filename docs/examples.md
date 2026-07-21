# 使用示例

## 基础保护

```bash
sprotect build
python output/main.py
```

## 最大保护

在 `sprotect.json5` 中（已默认开启全部功能）：

```json5
obfuscate: { level: 5, ... },
encrypt: { extra_layers: ["serpent", "twofish"] },
```

## 混合加密（RSA）

```json5
encrypt: {
  hybrid: {
    enabled: true,
    algorithm: "RSA",
    key_size: 4096,
  }
}
```

构建后私钥保存在 `output/key.pem`，运行时需提供私钥路径。

## 打包为 exe

```bash
pip install pyinstaller
sprotect pack                    # 打包 output/
# 或启用自动打包：
# sprotect.json5 → pack.enabled: true
# sprotect build  # 自动 build + pack
```

## 过期保护

```json5
expiration: {
  enabled: true,
  expires_at: "2027-12-31T23:59:59Z",
  ntp_check: true,
}
```
