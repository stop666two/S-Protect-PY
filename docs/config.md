# 配置文件参考

`sprotect.json5` 是项目主配置文件，使用 JSON5 格式(支持注释、尾逗号)。

## 完整配置项

```json5
{
  project: {
    name: "myapp",              // 项目名称
    version: "1.0.0",           // 项目版本
    entry: "main.py",           // 入口文件
    description: "",            // 项目描述
    author: "",                 // 作者
  },

  files: {
    include: ["**/*.py"],       // 包含的文件模式
    exclude: [],                // 排除的文件
    exclude_dirs: ["_runtime","_backup","__pycache__",".git"],
  },

  obfuscate: {
    level: 5,                   // 混淆等级 1-5
    rename_variables: true,     // 变量重命名
    rename_functions: true,    // 函数重命名
    rename_classes: true,      // 类重命名
    rename_rules: { style: "hex", reserved: [...], prefix: "_0x", ... },
    encrypt_strings: true,     // 字符串加密
    encrypt_numbers: true,     // 数字加密
    control_flow_flattening: true,  // 控制流平坦化
    dead_code_injection: true, // 死代码注入 + 隐式数据流
    string_split: true,        // 字符串分散碎片化
    opaque_expr: true,         // 不透明表达式注入 (NEW)
    match_dispatch: true,      // match/case 调度 (NEW)
  },

  encrypt: {
    algorithm: "aes-256-gcm",
    extra_layers: ["serpent","twofish","camellia","salsa20"],
    key_server: "",             // HTTPS 远程密钥服务器 URL (NEW)
    hybrid: { enabled: true, algorithm: "ECC", key_size: 521, key_file: "key.pem" },
  },

  runtime: {
    layer_count: 6,             // 加密层数
    time_wall_minutes: 60,      // 执行时间墙(分钟)
    memory_check_enabled: true, // 运行时内存校验和 (NEW)
    time_anomaly_check: true,   // 时间戳反演检测 (NEW)
    stack_obfuscation: true,    // 调用栈混淆 (NEW)
    file_decoy_enabled: true,   // 文件系统饵雷 (NEW)
    decoy_watch_interval: 45,   // 饵雷校验间隔(秒) (NEW)
  },

  output: {
    dir: "./output",
    clean_before_build: false,  // 构建前清空输出 (NEW)
    backup_before_build: true,  // 构建前自动备份 (NEW)
  },
}
```

## 新功能配置详解

### opaque_expr (v1.1+)
控制**不透明表达式注入**——将 `a + b` 替换为 `(a ^ b) + 2 * (a & b)` 等恒等式。
AI 不擅长代数简化，此功能可有效增加 AI 逆向难度。
默认 `true`。

### match_dispatch (v1.1+)
控制 **match/case 调度**——50% 概率用 Python 3.10+ 的 match/case 替代传统 if/elif 状态机。
LLM 难以静态推断 match/case 的跳转目标。
默认 `true`。需要 Python 3.10+。

### key_server (v1.1+)
配置 **远程密钥服务器 URL**(HTTPS)。部分 Shamir 分片存储在服务器上，
运行时自动通过 HTTPS 拉取。缺失远程分片时无法恢复 master_key。
格式: `"https://your-server.com/api/shares"`
默认 `""`(禁用)。

### memory_check_enabled / time_anomaly_check / stack_obfuscation / file_decoy_enabled (v1.1+)
运行时保护开关，控制新增的 4 个运行时反分析功能。
默认全部 `true`。

## 每模块独立配置

每个 `.py` 文件可以有一个对应的 `.py.sprotect.json5` 配置文件，
覆盖主配置中的 `obfuscate` 设置。例如 `crypto.py.sprotect.json5`。

主要用途：
- 入口模块禁用函数重命名(保持外部可调用)
- 类型模块启用最低混淆(避免破坏 dataclass)
- 密码学模块保持最高混淆
- 模板/字符串密集型模块禁用字符串加密
