# CLI 命令参考

## 基本用法

```bash
python -m sprotect <command> [options]
```

## 命令

### build — 构建加密项目

```bash
python -m sprotect build [project_dir] [--config <path>] [--clean] [--output <dir>]
```

将项目加密为可独立运行的输出。

- `project_dir`: 项目目录(默认当前目录)
- `--config`: 指定配置文件路径
- `--clean`: 构建前清空输出目录
- `--output`: 指定输出目录

### run — 运行加密项目

```bash
python -m sprotect run [--output <dir>]
```

运行已加密的输出。

### config — 查看/生成配置

```bash
python -m sprotect config [--generate] [project_dir]
```

- `--generate`: 生成默认 sprotect.json5

### watermark — 水印管理

```bash
python -m sprotect watermark extract <pye_path> [--key <secret>]
python -m sprotect watermark verify <pye_path> [--key <secret>]
python -m sprotect watermark patch <pye_path> --bid <new_bid>
```

### pack — 打包为单文件

```bash
python -m sprotect pack [--onefile|--onedir] [--console|--noconsole] [--icon <path>]
```

使用 PyInstaller 打包为可执行文件。

## 环境变量

| 变量 | 说明 |
|------|------|
| `SP_KEY_SERVER` | (已废弃) 使用 sprotect.json5 的 encrypt.key_server 替代 |
