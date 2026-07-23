# 保护功能说明

## 一、AST 混淆 (8 道传递)

| 传递 | 说明 | 配置项 |
|------|------|--------|
| 命名重命名 | 变量/函数/类名改为随机 hex | `rename_variables/functions/classes` |
| 字符串加密 | Base64/XOR 编码 + 分散碎片化 | `encrypt_strings`, `string_split` |
| 数字加密 | struct.pack 运行时解码 | `encrypt_numbers` |
| 不透明表达式 | a+b → (a^b)+2*(a&b) 等恒等式 | `opaque_expr` |
| 控制流平坦化 | while+if/elif 状态机 或 match/case 调度 | `control_flow_flattening`, `match_dispatch` |
| 死代码注入 | 恒真不透明谓词 + 无效分支 | `dead_code_injection` |
| Import/Call 混淆 | import→__import__()、调用→lambda 包装 | `obfuscate_imports/calls` |
| 隐式数据流 | 常量化身 if-else 分支，LLM 无法静态判定 | `dead_code_injection` |

## 二、多层加密

```
源码 → marshal → 6层 HKDF/AES-GCM → 层间哈希链验证
  → zlib(9) → ChaCha20-Poly1305 → XOR 流 → AES-256-GCM
  → [可选 extra_layers: Serpent/Twofish/Camellia/Salsa20]
  → [可选 x7 堆叠压缩: LZMA→BZ2→Zlib→Base85]
```

每层加密存储链式哈希 `h`，运行时验证。单独提取任意一层都会被检测。

## 三、反 AI 逆向

| 防御 | 原理 | 效果 |
|------|------|------|
| 语义噪声 5x | 200-300 诱饵函数淹没 6 个真实执行段 | ⭐⭐⭐⭐⭐ |
| 上下文污染 | hashlib/os.urandom 垃圾块填充 AI 注意力窗口 | ⭐⭐⭐⭐ |
| 假加密导入 | from cryptography.hazmat... 导入误导 AI 判断 | ⭐⭐⭐ |
| 不透明表达式 | 数学恒等式替换，AI 不擅长代数简化 | ⭐⭐⭐ |
| 隐式数据流 | 数据编码在控制流分支中，AI 数据/控制流独立分析 | ⭐⭐⭐⭐ |

## 四、反调试/反分析

| 检测项 | 触发条件 | 响应 |
|--------|---------|------|
| pdb/ptrace | 调试器附着 | exit(1) |
| VM/沙箱 | Docker/Cuckoo/Sandboxie | exit(1) |
| 进程枚举 | x64dbg/IDA/Windbg 等 20+ 工具 | exit(1) |
| 时间戳反演 | time.time() vs time.monotonic() 偏差 >2s | exit(1) |
| 内存校验和 | 模块代码哈希与基线不匹配 | exit(1) |
| 模拟器 | QEMU/VMware/KVM/VirtualBox 检测 | exit(1) |
| 调用链验证 | _trace_verify HMAC 令牌不匹配 | exit(1) |
| 文件系统陷阱 | 误触诱饵 .pye | exit(1) |

## 五、密钥保护

| 机制 | 说明 |
|------|------|
| Shamir 分片 | master_key 切分为 N 片，需 T 片恢复(GF(256)) |
| 本地密钥分片 | 部分分片嵌入 .pye，部分写入 _key_store.json |
| 远程密钥分片 | 支持 HTTPS 直连远程服务器获取额外分片 |
| 多态密钥路径 | 4 种不同 salt 推导方式，运行时由 PID 随机选择 |
| 白盒混淆 | 25 个 HEX_VARS 中仅 1 个真 salt |
| 层无密钥化 | 每层不存储密钥，全部由 HKDF(master_key) 派生 |

## 六、运行时保护

| 保护 | 说明 |
|------|------|
| 执行时间墙 | 启动后 N 分钟自动退出 |
| 内存 TTL | 解密缓存超过 N 秒后回收 |
| 完整性自检 | 定时验证 .pye 哈希和模块内存 |
| 诱饵文件监控 | 45 秒间隔检查 _decoy/ 文件完整性 |
| 内存自删除 | 模块加载后 .pye 文件立即删除 |
| 栈混淆 | 关键函数通过 6 层深 lambda 调用 |

## 七、双进程架构(实验性)

父进程持有全部解密密钥，子进程执行业务代码。子进程被 dump 也拿不到密钥。
启动增加 0.5-2秒，内存翻倍。适用于高安全场景。
