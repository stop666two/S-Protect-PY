# 快速开始

## 安装

```bash
pip install -r requirements.txt
```

依赖: `cryptography`, `json5`, `pycryptodome`, `blake3`, `msgpack`

## 最小示例

项目结构:
```
my_project/
  main.py              # 入口文件
  utils.py             # 业务模块
  sprotect.json5       # 保护配置
```

### 1. 生成默认配置

```bash
cd my_project
python -m sprotect config --generate
```

### 2. 构建加密输出

```bash
python -m sprotect build --clean
```

输出在 `./output/` 目录:
```
output/
  main.py                # 自解密启动器
  _runtime/              # 加密的 .pye 模块
    loader.pye           # 运行时加载器(加密)
    *.pye                # 加密的业务模块
    _key_store.json      # 远程密钥分片(可选部署)
  _meta/                 # 构建元数据
```

### 3. 运行加密程序

```bash
python -m sprotect run
# 或直接:
python output/main.py
```

### 4. (可选)部署远程密钥分片

```json5
// sprotect.json5
encrypt: {
    key_server: "https://your-server.com/api/shares",
}
```

将 `output/_runtime/_key_store.json` 部署到 HTTPS 服务器。
运行时自动拉取远程分片，离线不可解。

## 配置速查

```json5
obfuscate: {
    level: 5,                // 最高混淆
    opaque_expr: true,       // 不透明表达式(抗AI)
    match_dispatch: true,    // match/case 调度(抗AI)
    control_flow_flattening: true,
    dead_code_injection: true,
    string_split: true,
},
runtime: {
    memory_check_enabled: true,
    time_anomaly_check: true,
    stack_obfuscation: true,
    file_decoy_enabled: true,
},
```
