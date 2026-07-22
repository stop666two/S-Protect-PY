# 快速开始

## 安装

```bash
pip install json5 cryptography tqdm colorama
pip install pycryptodome      # 可选：Salsa20 额外加密层
pip install pyinstaller       # 可选：exe 打包
```

## 最小示例

```bash
# 1. 准备项目
mkdir -p project
echo 'print("Hello World!")' > project/main.py

# 2. 初始化配置
sprotect config init

# 3. 构建加密项目
sprotect build

# 4. 运行
sprotect run
```

## 新功能速览

```bash
# 自动清空输出目录
sprotect build --clean

# 监控重构建
sprotect build --watch

# 查看构建信息
cat output/_meta/build.spec

# 运行时加载 .env
echo "KEY_PATH=./key.pem" > output/.env
sprotect run
```

## 下一步

- [CLI 命令详解](cli.md)
- [配置完整参考](config.md)
- [保护功能详解](features.md)
- [使用示例大全](examples.md)
