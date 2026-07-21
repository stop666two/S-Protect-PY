# 配置文件参考

## sprotect.json5 结构

```json5
{
  project:   { name, version, entry },
  files:     { include, exclude, exclude_dirs },
  obfuscate: { level, rename_*, encrypt_*, control_flow_flattening, ... },
  encrypt:   { algorithm, extra_layers, hybrid, workers, ... },
  anti_debug:{ enabled, action, checks, ... },
  watermark: { enabled, levels, batch_id, ... },
  expiration:{ enabled, expires_at, ntp_check, ... },
  environment:{ enabled, bind_*, ... },
  sandbox:   { enabled, detect_*, ... },
  bootloader:{ name, anti_dump, periodic_check_interval, ... },
  pack:      { enabled, onefile, console, icon, ... },
  output:    { dir, keep_source_map, verbose },
}
```

详见 `sprotect.json5` 文件内完整注释（765 行中文详解）。

## Per-file 配置

每个模块可以有独立的 `.sprotect.json5`，覆盖全局配置。
例如 `sprotect/encrypt.py.sprotect.json5` 可单独控制 encrypt.py 模块的混淆和反调试设置。

配置优先级：per-file 配置 > 全局 sprotect.json5 > 代码默认值。
