# Python 包分析与解密报告

## 1. 结论

压缩包中的 `main.py` 是一个经过 S-Protect 风格封装和大量噪声代码混淆的 Python 启动器。实际业务源码存放在 `_runtime/*.pye` JSON 容器中。

最终恢复出的有效功能是：

1. 遍历当前工作目录。
2. 筛选扩展名为 `.md` 的普通文件，扩展名匹配不区分大小写。
3. 以 8192 字节为一块计算文件 SHA-256。
4. 输出文件名、文件大小和 SHA-256，字段之间使用制表符分隔。

整理后的脚本位于 `final.py`，解密后未经人工整理的源码位于 `final_extracted.py`。

## 2. 文件结构

解压后的主要结构如下：

```text
output_unpacked/
|-- main.py
|-- text.md
|-- _runtime/
|   |-- loader.pye
|   |-- ad6365473630.pye
|   |-- 29af4a2d774e.pye
|   |-- 6a3403a5b03f.pye
|   |-- 830c688b8982.pye
|   |-- 4450ba10/
|-- extract_source.py
|-- final_extracted.py
|-- final.py
|-- _sprotect_helper.py
`-- analysis_and_decryption.md
```

与最终入口直接相关的文件：

| 文件 | 作用 |
|---|---|
| `main.py` | 外层混淆启动器，包含加载器解密代码和大量干扰函数 |
| `_runtime/loader.pye` | 加密的真实模块加载器 |
| `_runtime/ad6365473630.pye` | 模块映射中的 `main` |
| `_runtime/29af4a2d774e.pye` | 模块映射中的 `_sprotect_helper` |
| `text.md` | 用于验证最终脚本的 Markdown 文件 |

## 3. 第一层：定位真实入口

`main.py` 前部定义了 12 个十六进制字符串分片：

```python
_d23861319 = '1e72129574'
_k6c7116db = '87624b0a474'
_n69c0e293 = '1a038c1e0ca'
_ydff420fe = '2d8e1f2fda'
_0x8e785cc261 = 'c73e197327f'
_r095e6fd7 = '9fb017291f1'
```

有效加载路径将前 6 个分片按顺序拼接：

```python
key = bytes.fromhex(
    _d23861319
    + _k6c7116db
    + _n69c0e293
    + _ydff420fe
    + _0x8e785cc261
    + _r095e6fd7
)
```

得到 32 字节入口密钥：

```text
1e7212957487624b0a4741a038c1e0ca2d8e1f2fdac73e197327f9fb017291f1
```

随后入口执行：

```python
exec(compile(decrypt_loader(), "", "exec"))
run("main", base_directory)
```

这说明分析重点是先恢复 `_runtime/loader.pye`，再调用其中的模块加载逻辑。

## 4. 解密 `loader.pye`

`loader.pye` 是 JSON 对象，关键字段如下：

| 字段 | 含义 |
|---|---|
| `v` | 容器版本，此处为 7 |
| `d` | 十六进制编码的密文 |
| `k1` 至 `k5` | 候选密钥或干扰分片 |
| `f1`、`f2`、`f3` | 密钥选择校验值 |

该文件的 `f1`、`f2`、`f3` 均为空字符串，因此 `_fe()` 不会选出候选密钥，加载器回退到 `main.py` 内拼出的固定入口密钥。

解密流程为：

1. 将 `d` 从十六进制转换为字节。
2. 前 12 字节作为 AES-GCM nonce，其余部分作为密文和认证标签。
3. 使用入口密钥执行 AES-GCM 解密。
4. 生成 SHA-256 计数器流。
5. 将 AES-GCM 明文与计数器流逐字节异或。
6. 尝试将结果按 `nonce || ciphertext || tag` 执行 ChaCha20-Poly1305 解密。
7. 使用 zlib 解压并按 UTF-8 解码。

入口层计数器流定义为：

```python
def hash_stream(length, key):
    output = bytearray()
    counter = 0
    while len(output) < length:
        output.extend(
            hashlib.sha256(key + counter.to_bytes(4, "big")).digest()
        )
        counter += 1
    return bytes(output[:length])
```

入口层可概括为：

```text
loader_source = UTF8(
    ZLIB_DECOMPRESS(
        CHACHA20_POLY1305_DECRYPT(
            AES_GCM_DECRYPT(hex(d), entry_key)
            XOR HASH_STREAM(entry_key)
        )
    )
)
```

其中原加载器对 ChaCha20-Poly1305 使用了异常回退：该层不存在或解密失败时，会直接尝试 zlib 解压异或后的数据。

## 5. 恢复模块映射

解出的加载器包含以下映射：

```json
{
  "main": "ad6365473630",
  "_sprotect_helper": "29af4a2d774e"
}
```

因此：

```text
main               -> _runtime/ad6365473630.pye
_sprotect_helper   -> _runtime/29af4a2d774e.pye
```

另外，加载器要求至少从两个模块容器中各选出一个有效分片，再将这些分片异或形成模块主密钥。

## 6. 候选分片校验

每个模块容器包含 `k1` 至 `k5`。加载器使用三种校验确定真正的分片。

### 6.1 组合校验 `f1`

先将同一容器内的五个候选分片逐字节异或：

```python
combined = bytearray(32)
for shard in shards:
    for i, value in enumerate(shard[:32]):
        combined[i] ^= value
```

然后验证：

```python
hashlib.sha256(combined).hexdigest()[5:13] == record["f1"]
```

`f1` 校验整个候选分片集合，不负责区分具体是哪一个分片。

### 6.2 单项校验 `f2`

对每个候选分片计算 BLAKE3：

```python
blake3.blake3(shard).hexdigest()[3:11] == record["f2"]
```

### 6.3 单项校验 `f3`

使用固定域字符串计算 HMAC-SHA256：

```python
hmac.new(
    shard,
    b"S-Protect-v6-key-verify",
    hashlib.sha256,
).hexdigest()[:8] == record["f3"]
```

同时满足 `f1`、`f2` 和 `f3` 的候选分片即为该模块的有效分片。

## 7. 选中的分片与模块主密钥

实际计算结果如下。

### 7.1 `main` 模块

选中 `ad6365473630.pye` 的 `k3`：

```text
0233e1076f37d4fe5ffa3e51cd63f502066a14c65692a63952ae5bb9e75f9c4a
```

### 7.2 `_sprotect_helper` 模块

选中 `29af4a2d774e.pye` 的 `k5`：

```text
4e88d873f5d1cac6abce30c007ce6c68a0cd549c5a56120f669f299875416d78
```

### 7.3 异或生成主密钥

加载器将两个有效分片逐字节异或：

```python
master_key = bytes(a ^ b for a, b in zip(main_k3, helper_k5))
```

得到模块主密钥：

```text
4cbb39749ae61e38f4340e91caad996aa6a7405a0cc4b43634317221921ef132
```

## 8. 解密模块容器

模块容器与入口加载器使用相似但不完全相同的流程。

模块解密步骤：

1. 读取模块 JSON 的 `d` 字段并进行十六进制解码。
2. 如果 `h` 是包含 `extra_layers` 的 JSON，则逆序解除附加 Salsa20 或 AES-CBC 层。
3. 使用模块主密钥执行 AES-GCM 解密。
4. 对模块主密钥先计算一次 SHA-256，以该摘要作为计数器流种子。
5. 将 AES-GCM 明文与计数器流异或。
6. 使用模块主密钥执行 ChaCha20-Poly1305 解密。
7. 使用 zlib 解压并按 UTF-8 解码。

本样本的 `h` 是普通十六进制摘要，不是带有 `extra_layers` 的 JSON，所以附加层处理直接跳过。

模块层计数器流的种子是：

```python
seed = hashlib.sha256(master_key).digest()
```

完整核心代码：

```python
def decrypt(record, master_key):
    encrypted = bytes.fromhex(record["d"])

    data = AESGCM(master_key).decrypt(
        encrypted[:12], encrypted[12:], b""
    )

    seed = hashlib.sha256(master_key).digest()
    stream = hash_stream(len(data), seed)
    data = bytes(a ^ b for a, b in zip(data, stream))

    data = ChaCha20Poly1305(master_key).decrypt(
        data[:12], data[12:], b""
    )

    return zlib.decompress(data).decode("utf-8")
```

注意入口层直接使用入口密钥作为哈希流种子，而模块层使用 `SHA256(master_key)` 作为种子。这是两层解密之间最容易混淆的差异。

## 9. 解密得到的源码

### 9.1 `main` 原始源码

`ad6365473630.pye` 解密后得到 1589 个字符，对应 `final_extracted.py`。

它包含以下有效操作：

```python
hashlib.sha256()
open(file_path, "rb")
file.read(8192)
os.listdir(".")
os.path.isfile(entry)
entry.lower().endswith(".md")
os.path.getsize(entry)
```

其余内容包括：

- Base64 动态导入和字符串还原。
- 无实际作用的 lambda 包装。
- 恒真条件和空操作。
- 未被调用的伪校验函数。
- 不影响执行结果的哈希表达式。

这些内容属于控制流和可读性混淆，不参与最终业务结果。

### 9.2 Helper 模块

`29af4a2d774e.pye` 解密后得到 364 个字符，对应 `_sprotect_helper.py`。

它包含一个调用 `os._exit(0)` 的函数和一个恒定数据伪校验函数。`main` 的恢复源码没有导入或调用该模块；它在本样本中的主要实际作用是提供第二个有效密钥分片，使加载器能够合成模块主密钥。

## 10. 去混淆后的等价脚本

整理后的 `final.py`：

```python
import hashlib
from pathlib import Path


def sha256_file(file_path):
    digest = hashlib.sha256()
    with file_path.open("rb") as file:
        for chunk in iter(lambda: file.read(8192), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    for file_path in Path(".").iterdir():
        if file_path.is_file() and file_path.suffix.lower() == ".md":
            print(
                f"{file_path.name}\t"
                f"{file_path.stat().st_size}\t"
                f"{sha256_file(file_path)}"
            )


if __name__ == "__main__":
    main()
```

这里将 `os.listdir` 和 `os.path` 改写为 `pathlib.Path`，行为保持一致。目录遍历顺序仍沿用文件系统返回顺序，没有额外排序。

## 11. 自动提取脚本

完整自动提取过程已写入 `extract_source.py`。它执行以下工作：

1. 读取两个映射模块的 `.pye` JSON。
2. 验证并选择每个模块的真实分片。
3. 异或生成模块主密钥。
4. 解密 `main` 和 `_sprotect_helper`。
5. 输出 `final.py` 与 `_sprotect_helper.py`。
6. 使用 `compile()` 对解密源码进行语法校验。

依赖：

```bash
python -m pip install cryptography blake3
```

重新提取：

```bash
cd /storage/emulated/0/Download/Operit/cleanOnExit/output_unpacked
python extract_source.py
```

预期输出：

```text
wrote final.py: 1589 chars
wrote _sprotect_helper.py: 364 chars
```

`extract_source.py` 会将 `final.py` 重新生成成原始解密版本。如需保留清晰整理版，应先备份当前 `final.py`，或将提取器中的目标文件名调整为 `final_extracted.py`。

## 12. 运行与验证

在解压目录运行整理后的脚本：

```bash
python final.py
```

输出：

```text
text.md\t62\t36e191fcdc2dc8e4c5e08c9143d596c37c3be4ab3d2f29d34da702eb49575f05
```

使用系统工具独立计算：

```bash
sha256sum text.md
```

结果：

```text
36e191fcdc2dc8e4c5e08c9143d596c37c3be4ab3d2f29d34da702eb49575f05  text.md
```

两者完全一致。所有恢复脚本也已通过 Python `py_compile` 语法检查。

## 13. 文件哈希

为便于复核，相关文件的 SHA-256 如下：

| 文件 | SHA-256 |
|---|---|
| `main.py` | `68c4c9b690d18621f2c02b6561bae36874814aa0c34c79c5df92a79c63b4d535` |
| `_runtime/loader.pye` | `cc1b602bb434085dbef072f233f70e259e14880dc4edc792a7a057186245afc1` |
| `_runtime/ad6365473630.pye` | `51b6c00e0a5ee8a2dd944fc64708b680917da277c13ced99ca6f77b129f2c9e4` |
| `_runtime/29af4a2d774e.pye` | `fe32c58474ea1806d1bc11b038b578c771cf62cb1873aa6255283e929faf0692` |
| `final_extracted.py` | `4cc6b5430bba584046724572053f6b532b33fbaf9fbd57e4915df45d538d7104` |
| `final.py` | `5e8fe9470a1e23aa05cfe83eef544c5329d2732335a3760fc5f3e73d29db34ec` |
| `extract_source.py` | `7813717d5fd56b4ba88a3068c7fe627a22805b15245e4ef823c4e20c1b17b8ef` |
| `text.md` | `36e191fcdc2dc8e4c5e08c9143d596c37c3be4ab3d2f29d34da702eb49575f05` |

## 14. 最终产物说明

| 产物 | 说明 |
|---|---|
| `analysis_and_decryption.md` | 本分析与解密报告 |
| `extract_source.py` | 可复现的模块解密器 |
| `final_extracted.py` | 解密所得原始混淆源码 |
| `final.py` | 人工去混淆后的清晰等价实现 |
| `_sprotect_helper.py` | 解密所得辅助模块源码 |

最终业务逻辑已恢复，原始解密版本、可读版本、自动提取器和独立验证结果均已保留。