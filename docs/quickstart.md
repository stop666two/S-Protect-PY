# 快速开始

## 安装

```bash
pip install json5 cryptography tqdm colorama
pip install pycryptodome      # 可选：额外加密层
pip install pyinstaller       # 可选：exe 打包
```

## 最小示例

```bash
# 1. 创建项目
mkdir myproject
cd myproject
# 放入你的源码
echo 'print("Hello World!")' > main.py

# 2. 初始化配置
sprotect config init

# 3. 编辑 sprotect.json5，确保 entry = "main.py"

# 4. 构建
sprotect build

# 5. 运行加密后的项目
cd output
python main.py
```

## 典型工作流

```bash
# 准备源码
mkdir project
cp -r myapp/* project/

# 配置（所有功能默认开启）
sprotect config init

# 构建加密项目
sprotect build

# 分发 output/ 目录即可
```

## 下一步

- [CLI 命令详解](cli.md)
- [配置完整参考](config.md)
- [保护功能详解](features.md)
