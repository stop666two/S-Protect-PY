import os
import tempfile
import hashlib
import base64
import json
import threading
import queue
import gzip
import zlib
import io
import tarfile
import contextlib
from contextlib import contextmanager

_HASH_PREFIX_LEN = 16
_THREAD_TIMEOUT = 5


def _run_in_thread(q):
    q.put("thread_ok")


def run_runtime_checks():
    tmp_path = None
    try:
        tmp_dir = tempfile.gettempdir()
        tmp_path = os.path.join(tmp_dir, "_py_env_test.tmp")
        data = "Hello, Python 环境测试!"
        with open(tmp_path, "w", encoding="utf-8") as f:
            f.write(data)
        with open(tmp_path, "r", encoding="utf-8") as f:
            read_back = f.read()
        ok = read_back == data
        yield {
            "name": "文件读写",
            "status": ok,
            "detail": "成功" if ok else "数据不一致",
        }
    except Exception as e:
        yield {
            "name": "文件读写",
            "status": False,
            "detail": str(e),
        }
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)

    try:
        h = hashlib.sha256(b"test").hexdigest()
        yield {
            "name": "HASH (SHA256)",
            "status": True,
            "detail": h[:_HASH_PREFIX_LEN] + "...",
        }
    except Exception as e:
        yield {
            "name": "HASH (SHA256)",
            "status": False,
            "detail": str(e),
        }

    try:
        encoded = base64.b64encode(b"test data").decode()
        decoded = base64.b64decode(encoded).decode()
        ok = decoded == "test data"
        yield {
            "name": "Base64 编解码",
            "status": ok,
            "detail": "成功" if ok else "数据不一致",
        }
    except Exception as e:
        yield {
            "name": "Base64 编解码",
            "status": False,
            "detail": str(e),
        }

    try:
        d = {"key": "value", "num": 42}
        serialized = json.dumps(d)
        deserialized = json.loads(serialized)
        ok = deserialized == d
        yield {
            "name": "JSON 序列化",
            "status": ok,
            "detail": "成功" if ok else "数据不一致",
        }
    except Exception as e:
        yield {
            "name": "JSON 序列化",
            "status": False,
            "detail": str(e),
        }

    try:
        q = queue.Queue()
        t = threading.Thread(target=_run_in_thread, args=(q,), daemon=True)
        t.start()
        t.join(timeout=_THREAD_TIMEOUT)
        result = q.get_nowait()
        ok = result == "thread_ok"
        yield {
            "name": "多线程",
            "status": ok,
            "detail": "成功" if ok else "线程返回值异常",
        }
    except Exception as e:
        yield {
            "name": "多线程",
            "status": False,
            "detail": str(e),
        }

    try:
        import socket
        hostname = socket.gethostname()
        yield {
            "name": "Socket (主机名)",
            "status": True,
            "detail": hostname,
        }
    except Exception as e:
        yield {
            "name": "Socket (主机名)",
            "status": False,
            "detail": str(e),
        }

    try:
        original = b"gzip compression test data " * 100
        compressed = gzip.compress(original)
        decompressed = gzip.decompress(compressed)
        ok = original == decompressed
        ratio = len(compressed) / len(original)
        yield {
            "name": "GZip 压缩",
            "status": ok,
            "detail": f"{'成功' if ok else '失败'} (压缩比 {ratio:.1%})",
        }
    except Exception as e:
        yield {
            "name": "GZip 压缩",
            "status": False,
            "detail": str(e),
        }

    try:
        text = "你好, Unicode 世界! \u4e2d\u6587"
        encoded = text.encode("utf-8")
        decoded = encoded.decode("utf-8")
        ok = decoded == text
        yield {
            "name": "UTF-8 编解码",
            "status": ok,
            "detail": "成功" if ok else "数据不一致",
        }
    except Exception as e:
        yield {
            "name": "UTF-8 编解码",
            "status": False,
            "detail": str(e),
        }

    try:
        import requests
        r = requests.get("https://httpbin.org/get", timeout=5)
        ok = r.status_code == 200
        yield {
            "name": "HTTP 网络请求",
            "status": ok,
            "detail": f"状态码 {r.status_code}" if ok else f"异常状态码 {r.status_code}",
        }
    except ImportError:
        yield {
            "name": "HTTP 网络请求",
            "status": False,
            "detail": "requests 未安装，跳过",
        }
    except Exception as e:
        yield {
            "name": "HTTP 网络请求",
            "status": False,
            "detail": str(e),
        }

    try:
        import pickle
        data = {"key": "value", "list": [1, 2, 3]}
        serialized = pickle.dumps(data)
        deserialized = pickle.loads(serialized)
        ok = deserialized == data
        yield {
            "name": "pickle 序列化",
            "status": ok,
            "detail": f"{len(serialized)} bytes, 还原{'成功' if ok else '失败'}",
        }
    except Exception as e:
        yield {
            "name": "pickle 序列化",
            "status": False,
            "detail": str(e),
        }

    try:
        import struct
        values = (42, 3.14, b"\x01\x02")
        packed = struct.pack("!I d 2s", *values)
        unpacked = struct.unpack("!I d 2s", packed)
        ok = unpacked == values
        yield {
            "name": "struct 二进制打包",
            "status": ok,
            "detail": f"packed={len(packed)} bytes, 还原{'成功' if ok else '失败'}",
        }
    except Exception as e:
        yield {
            "name": "struct 二进制打包",
            "status": False,
            "detail": str(e),
        }

    try:
        data = b"hello base32 and base85"
        b32 = base64.b32encode(data)
        back = base64.b32decode(b32)
        ok1 = back == data
        b85 = base64.b85encode(data)
        back = base64.b85decode(b85)
        ok2 = back == data
        yield {
            "name": "base32 / base85 编码",
            "status": ok1 and ok2,
            "detail": f"base32={'成功' if ok1 else '失败'}, base85={'成功' if ok2 else '失败'}",
        }
    except Exception as e:
        yield {
            "name": "base32 / base85 编码",
            "status": False,
            "detail": str(e),
        }

    try:
        encoded = base64.b64encode(b"res = 21 + 21").decode()
        decoded = base64.b64decode(encoded).decode()
        ns = {}
        exec(decoded, ns)
        ok = ns.get("res") == 42
        yield {
            "name": "Base64+exec 动态代码",
            "status": ok,
            "detail": "动态执行成功" if ok else "执行失败",
        }
    except Exception as e:
        yield {
            "name": "Base64+exec 动态代码",
            "status": False,
            "detail": str(e),
        }

    try:
        fn = getattr(json, "dumps")
        result = fn({"a": 1})
        ok = result == '{"a": 1}'
        yield {
            "name": "getattr 动态属性访问",
            "status": ok,
            "detail": f"json.dumps via getattr={'成功' if ok else '失败'}",
        }
    except Exception as e:
        yield {
            "name": "getattr 动态属性访问",
            "status": False,
            "detail": str(e),
        }

    try:
        c1 = zlib.crc32(b"hello")
        c2 = zlib.adler32(b"hello")
        ok = c1 != 0 and c2 != 0
        yield {
            "name": "zlib crc32/adler32",
            "status": ok,
            "detail": f"crc32=0x{c1:08x}, adler32=0x{c2:08x}",
        }
    except Exception as e:
        yield {
            "name": "zlib crc32/adler32",
            "status": False,
            "detail": str(e),
        }

    try:
        buf = io.BytesIO()
        buf.write(b"hello bytesio")
        buf.seek(0)
        result = buf.read()
        ok = result == b"hello bytesio"
        sbuf = io.StringIO()
        sbuf.write("hello stringio")
        sbuf.seek(0)
        sresult = sbuf.read()
        ok2 = sresult == "hello stringio"
        yield {
            "name": "io.BytesIO / StringIO",
            "status": ok and ok2,
            "detail": f"BytesIO={'成功' if ok else '失败'}, StringIO={'成功' if ok2 else '失败'}",
        }
    except Exception as e:
        yield {
            "name": "io.BytesIO / StringIO",
            "status": False,
            "detail": str(e),
        }

    try:
        lock = threading.Lock()
        ok1 = lock.acquire(timeout=1)
        lock.release()
        rlock = threading.RLock()
        ok2 = rlock.acquire(timeout=1)
        rlock.release()
        yield {
            "name": "threading.Lock / RLock",
            "status": ok1 and ok2,
            "detail": f"Lock={'成功' if ok1 else '失败'}, RLock={'成功' if ok2 else '失败'}",
        }
    except Exception as e:
        yield {
            "name": "threading.Lock / RLock",
            "status": False,
            "detail": str(e),
        }

    try:
        import codecs
        text = "你好世界"
        encoded = codecs.encode(text, "utf-16-le")
        decoded = codecs.decode(encoded, "utf-16-le")
        ok = decoded == text
        yield {
            "name": "codecs 编码转换 (UTF-16)",
            "status": ok,
            "detail": f"{len(text)} chars -> {len(encoded)} bytes, 还原{'成功' if ok else '失败'}",
        }
    except Exception as e:
        yield {
            "name": "codecs 编码转换 (UTF-16)",
            "status": False,
            "detail": str(e),
        }

    tmp_tar = None
    try:
        tmp_tar = os.path.join(tempfile.gettempdir(), "_py_tar_test.tar")
        with tarfile.open(tmp_tar, "w") as tf:
            info = tarfile.TarInfo(name="test.txt")
            content = b"tar file content test"
            info.size = len(content)
            tf.addfile(info, io.BytesIO(content))
        with tarfile.open(tmp_tar, "r") as tf:
            extracted = tf.extractfile("test.txt")
            result = extracted.read() if extracted else b""
        ok = result == content
        yield {
            "name": "tarfile 打包解包",
            "status": ok,
            "detail": f"{len(content)} bytes, 还原{'成功' if ok else '失败'}",
        }
    except Exception as e:
        yield {
            "name": "tarfile 打包解包",
            "status": False,
            "detail": str(e),
        }
    finally:
        if tmp_tar and os.path.exists(tmp_tar):
            os.remove(tmp_tar)

    try:
        @contextmanager
        def sample_ctx(msg):
            yield f"ctx:{msg}"
        with sample_ctx("test") as val:
            ok = val == "ctx:test"
        with contextlib.ExitStack() as stack:
            stack.enter_context(sample_ctx("stack"))
            ok2 = True
        yield {
            "name": "contextlib (ExitStack + contextmanager)",
            "status": ok and ok2,
            "detail": f"contextmanager={'成功' if ok else '失败'}, ExitStack={'成功' if ok2 else '失败'}",
        }
    except Exception as e:
        yield {
            "name": "contextlib (ExitStack + contextmanager)",
            "status": False,
            "detail": str(e),
        }
