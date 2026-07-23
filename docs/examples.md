# 使用示例

## 基础保护

最简单的保护配置:

```json5
{
  project: { name: "myapp", entry: "main.py" },
  obfuscate: { level: 5 },
  encrypt: { extra_layers: [] },
}
```

```bash
python -m sprotect build --clean
python -m sprotect run
```

## 最高安全级(抗 AI + 远程密钥 + 双进程)

```json5
{
  encrypt: {
    extra_layers: ["serpent","twofish","camellia","salsa20"],
    key_server: "https://your-server.com/api/shares",
    hybrid: { enabled: true, algorithm: "ECC", key_size: 521 },
  },
  obfuscate: {
    level: 5,
    opaque_expr: true,
    match_dispatch: true,
    string_split: true,
    control_flow_flattening: true,
    dead_code_injection: true,
  },
  dual_process: { enabled: true },
  runtime: {
    memory_check_enabled: true,
    time_anomaly_check: true,
    stack_obfuscation: true,
    file_decoy_enabled: true,
  },
}
```

此配置下：
- 200-300 诱饵函数淹没真实逻辑(抗 AI)
- 远程密钥分片使离线提取不可行
- 双进程分离密钥与业务
- 6 层加密 + 4 层额外加密 + 6 层 HKDF
- 全部运行时保护开启

## 最小体积(移动端/嵌入式)

```json5
{
  obfuscate: { level: 3 },
  encrypt: { extra_layers: [], hybrid: { enabled: false } },
  compressor: { enabled: true, pass_count: 1 },
  runtime: { memory_check_enabled: false, time_anomaly_check: false },
}
```
