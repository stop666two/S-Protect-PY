# 快速开始

## 安装

```bash
pip install json5 cryptography tqdm colorama
pip install pycryptodome      # 可选：Salsa20 额外加密层
pip install pyinstaller       # 可选：exe 打包
```

## 最小示例

```bash
# 1. 创建项目
mkdir -p project
echo 'print("Hello World!")' > project/main.py

# 2. 初始化配置
sprotect config init

# 3. 编辑 sprotect.json5，确保 entry = "main.py"

# 4. 构建
sprotect build

# 5. 运行加密后的项目
sprotect run
```

## 典型工作流

```bash
# 准备源码
cp -r myapp/* project/

# 构建加密项目（所有功能默认开启）
sprotect build --clean

# 分发 output/ 目录即可，运行时不需要 S-Protect-PY
```

## 新功能速览

```bash
# 自动监控重构建
sprotect build --watch

# 运行 + 自动加载 .env
echo "KEY_PATH=./key.pem" > output/.env
sprotect run

# 产品发布后追踪泄露
sprotect watermark list output/_runtime/
python -c "from sprotect.watermark import patch_watermark_batch; patch_watermark_batch('output/_runtime/', 'CUSTOMER-ABC', 'mysecret')"
```

## 下一步

- [CLI 命令详解](cli.md)
- [配置完整参考](config.md)
- [保护功能详解](features.md)
- [使用示例大全](examples.md)
