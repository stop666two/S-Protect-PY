# CLI 命令参考

## 全局选项

```bash
python -m sprotect <command> [options]
```

## build — 构建加密项目

```bash
sprotect build                          # 默认 project/ → output/
sprotect build --project ./src          # 指定源码目录
sprotect build --output ./dist          # 指定输出目录
sprotect build -c myconfig.json5        # 使用自定义配置
sprotect build --clean                  # 自动清空输出目录（无需手动删除）
sprotect build --watch                  # 监控源码变化自动重构建
```

构建流程：
1. 若 `--clean`，自动清空 output 目录
2. 备份 project/ → \_backup/
3. 扫描所有 .py 文件
4. 第一遍：收集跨文件命名映射（含属性名）
5. 逐文件：混淆 → 虚拟化（若配置）→ 加密 → 写入 .pye
6. 链式哈希校验
7. 生成诱饵文件
8. 生成 loader + boot stub
9. 完整性白名单（integrity\_manifest.json）
10. 水印报告
11. 若 `--watch`，进入监控模式等待文件变更

## run — 运行加密项目

```bash
sprotect run                            # 运行 ./output/
sprotect run --dir ./dist               # 运行指定目录
```

- 自动加载 output/.env 到环境变量（支持 hybrid 密钥路径配置）
- 透传子进程退出码

## pack — 打包为 exe

```bash
sprotect pack                           # 打包 output/ 为 exe（需 PyInstaller）
sprotect pack --onedir                  # 目录模式（启动更快）
sprotect pack --noconsole               # 隐藏控制台（GUI 程序）
sprotect pack --icon myapp.ico          # 自定义图标
```

## encrypt — 加密单个文件

```bash
sprotect encrypt file.py                # 加密 file.py → file.pye
```

## watermark — 水印操作

```bash
sprotect watermark extract file.pye              # 提取水印
sprotect watermark verify file.pye               # 验证水印
sprotect watermark list output/_runtime/         # 扫描目录
sprotect watermark extract file.pye --key mykey  # 带密钥验证
```

## config — 配置管理

```bash
sprotect config init     # 生成默认 sprotect.json5
sprotect config show     # 显示当前配置
```

## init — 初始化项目

```bash
sprotect init            # 创建 project/ output/ + 默认配置
```

## version — 查看版本

```bash
sprotect version
```
