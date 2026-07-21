import os
import tempfile
import configparser
import csv
import json
import re
import string
import zipfile
import shutil
import glob
import xml.etree.ElementTree as ET
import tomllib
import collections
import itertools
import dataclasses
import enum
import functools
import logging
import pathlib
from datetime import datetime
from urllib.parse import urlparse, urlencode
from config import WORKSPACE


def run_realworld_checks():
    try:
        cfg = configparser.ConfigParser()
        cfg.read_string("[app]\nhost = localhost\nport = 8080\n")
        host = cfg.get("app", "host")
        port = cfg.get("app", "port")
        ok = host == "localhost" and port == "8080"
        yield {
            "name": "配置文件解析 (ConfigParser)",
            "status": ok,
            "detail": f"host={host}, port={port}" if ok else "解析结果不符",
            "expect": "pass",
        }
    except Exception as e:
        yield {
            "name": "配置文件解析 (ConfigParser)",
            "status": False,
            "detail": str(e),
            "expect": "pass",
        }

    try:
        url = "https://user:pass@api.example.com:8443/path?key=val#sec"
        parsed = urlparse(url)
        ok = all([parsed.scheme == "https", parsed.netloc == "user:pass@api.example.com:8443",
                  parsed.path == "/path", parsed.query == "key=val"])
        yield {
            "name": "URL 解析 (urllib.parse)",
            "status": ok,
            "detail": f"scheme={parsed.scheme}, host={parsed.hostname}, port={parsed.port}",
            "expect": "pass",
        }
    except Exception as e:
        yield {
            "name": "URL 解析 (urllib.parse)",
            "status": False,
            "detail": str(e),
            "expect": "pass",
        }

    try:
        query = urlencode({"name": "张三", "age": 28})
        ok = query == "name=%E5%BC%A0%E4%B8%89&age=28"
        yield {
            "name": "URL 编码 (urlencode)",
            "status": ok,
            "detail": query if ok else "编码结果不符",
            "expect": "pass",
        }
    except Exception as e:
        yield {
            "name": "URL 编码 (urlencode)",
            "status": False,
            "detail": str(e),
            "expect": "pass",
        }

    tmpdir = None
    try:
        tmpdir = tempfile.mkdtemp()
        csv_path = os.path.join(tmpdir, "test.csv")
        rows = [{"name": "Alice", "score": "95"}, {"name": "Bob", "score": "87"}]
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["name", "score"])
            w.writeheader()
            w.writerows(rows)
        read_back = []
        with open(csv_path, "r", encoding="utf-8") as f:
            r = csv.DictReader(f)
            for row in r:
                read_back.append(row)
        ok = read_back == rows
        yield {
            "name": "CSV 读写",
            "status": ok,
            "detail": f"{'数据一致' if ok else '数据不一致'} ({len(rows)} 条)",
            "expect": "pass",
        }
    except Exception as e:
        yield {
            "name": "CSV 读写",
            "status": False,
            "detail": str(e),
            "expect": "pass",
        }
    finally:
        if tmpdir and os.path.exists(tmpdir):
            shutil.rmtree(tmpdir, ignore_errors=True)

    try:
        dt = datetime.now()
        formatted = dt.strftime("%Y-%m-%d %H:%M:%S")
        parsed_back = datetime.strptime(formatted, "%Y-%m-%d %H:%M:%S")
        ok = abs((parsed_back - dt).total_seconds()) < 1
        yield {
            "name": "日期时间格式化/解析",
            "status": ok,
            "detail": formatted if ok else "时间回解析不一致",
            "expect": "pass",
        }
    except Exception as e:
        yield {
            "name": "日期时间格式化/解析",
            "status": False,
            "detail": str(e),
            "expect": "pass",
        }

    try:
        os.environ["_PY_TEST_VAR"] = "test_value_123"
        val = os.environ.get("_PY_TEST_VAR", "")
        ok = val == "test_value_123"
        del os.environ["_PY_TEST_VAR"]
        gone = os.environ.get("_PY_TEST_VAR", "NOT_FOUND")
        yield {
            "name": "环境变量读写",
            "status": ok and gone == "NOT_FOUND",
            "detail": f"写入={val}, 删除后={gone}",
            "expect": "pass",
        }
    except Exception as e:
        yield {
            "name": "环境变量读写",
            "status": False,
            "detail": str(e),
            "expect": "pass",
        }

    try:
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        valid_emails = ["user@example.com", "a.b@c.co"]
        invalid_emails = ["not-email", "@no.com", "xxx@"]
        all_ok = all(re.match(email_pattern, e) for e in valid_emails)
        all_bad = not any(re.match(email_pattern, e) for e in invalid_emails)
        ok = all_ok and all_bad
        yield {
            "name": "正则表达式 (邮件验证)",
            "status": ok,
            "detail": f"正例通过={all_ok}, 反例拦截={all_bad}",
            "expect": "pass",
        }
    except Exception as e:
        yield {
            "name": "正则表达式 (邮件验证)",
            "status": False,
            "detail": str(e),
            "expect": "pass",
        }

    try:
        tmpl = string.Template("Hello, $name! You are $age.")
        rendered = tmpl.safe_substitute(name="测试", age=25)
        ok = rendered == "Hello, 测试! You are 25."
        yield {
            "name": "字符串模板 (string.Template)",
            "status": ok,
            "detail": rendered if ok else "渲染结果不符",
            "expect": "pass",
        }
    except Exception as e:
        yield {
            "name": "字符串模板 (string.Template)",
            "status": False,
            "detail": str(e),
            "expect": "pass",
        }

    tmp_zip = None
    try:
        import io
        tmp_zip = os.path.join(tempfile.gettempdir(), "_py_test_archive.zip")
        content = b"zip file content for testing"
        with zipfile.ZipFile(tmp_zip, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("test.txt", content)
        with zipfile.ZipFile(tmp_zip, "r") as zf:
            extracted = zf.read("test.txt")
        ok = extracted == content
        yield {
            "name": "ZIP 压缩/解压",
            "status": ok,
            "detail": f"{'数据一致' if ok else '数据不一致'} ({len(content)} bytes)",
            "expect": "pass",
        }
    except Exception as e:
        yield {
            "name": "ZIP 压缩/解压",
            "status": False,
            "detail": str(e),
            "expect": "pass",
        }
    finally:
        if tmp_zip and os.path.exists(tmp_zip):
            os.remove(tmp_zip)

    try:
        data = {"users": [{"id": 1, "name": "测试"}], "total": 1}
        serialized = json.dumps(data, ensure_ascii=False, indent=2)
        deserialized = json.loads(serialized)
        ok = deserialized == data
        yield {
            "name": "JSON 深度序列化",
            "status": ok,
            "detail": f"{len(serialized)} bytes, 中文保留={ok}",
            "expect": "pass",
        }
    except Exception as e:
        yield {
            "name": "JSON 深度序列化",
            "status": False,
            "detail": str(e),
            "expect": "pass",
        }

    os.makedirs(WORKSPACE, exist_ok=True)

    try:
        root = ET.Element("data")
        item = ET.SubElement(root, "item", id="1")
        ET.SubElement(item, "name").text = "测试"
        ET.SubElement(item, "value").text = "42"
        xml_str = ET.tostring(root, encoding="unicode")
        parsed = ET.fromstring(xml_str)
        name = parsed.find("item/name")
        ok = name is not None and name.text == "测试"
        yield {
            "name": "XML 解析 (ElementTree)",
            "status": ok,
            "detail": f"XML={xml_str[:50]}..., 解析={'成功' if ok else '失败'}",
        }
    except Exception as e:
        yield {
            "name": "XML 解析 (ElementTree)",
            "status": False,
            "detail": str(e),
        }

    try:
        import tomllib
        toml_str = """
[server]
host = "localhost"
port = 8080

[log]
level = "info"
"""
        data = tomllib.loads(toml_str)
        ok = data["server"]["host"] == "localhost" and data["server"]["port"] == 8080
        yield {
            "name": "TOML 解析 (tomllib)",
            "status": ok,
            "detail": f"host={data['server']['host']}, port={data['server']['port']}" if ok else "解析失败",
        }
    except Exception as e:
        yield {
            "name": "TOML 解析 (tomllib)",
            "status": False,
            "detail": str(e),
        }

    try:
        dq = collections.deque([1, 2, 3], maxlen=5)
        dq.appendleft(0)
        dq.append(4)
        ok1 = list(dq) == [0, 1, 2, 3, 4]
        cnt = collections.Counter("aabbc")
        ok2 = cnt["a"] == 2 and cnt["c"] == 1
        yield {
            "name": "deque / Counter",
            "status": ok1 and ok2,
            "detail": f"deque={list(dq)}, Counter(a)={cnt['a']}" if ok1 and ok2 else f"deque={'成功' if ok1 else '失败'}, Counter={'成功' if ok2 else '失败'}",
        }
    except Exception as e:
        yield {
            "name": "deque / Counter",
            "status": False,
            "detail": str(e),
        }

    try:
        chained = list(itertools.chain([1, 2], [3, 4]))
        ok1 = chained == [1, 2, 3, 4]
        grouped = {k: list(g) for k, g in itertools.groupby("AAABBCC", lambda x: x)}
        ok2 = grouped == {"A": ["A", "A", "A"], "B": ["B", "B"], "C": ["C", "C"]}
        yield {
            "name": "itertools.chain / groupby",
            "status": ok1 and ok2,
            "detail": f"chain={chained}, groupby keys={list(grouped.keys())}" if ok1 and ok2 else f"chain={'成功' if ok1 else '失败'}, groupby={'成功' if ok2 else '失败'}",
        }
    except Exception as e:
        yield {
            "name": "itertools.chain / groupby",
            "status": False,
            "detail": str(e),
        }

    ws_dir = None
    try:
        ws_dir = os.path.join(WORKSPACE, "_shutil_test")
        os.makedirs(ws_dir, exist_ok=True)
        src = os.path.join(ws_dir, "test.txt")
        with open(src, "w") as f:
            f.write("hello shutil")
        dst = os.path.join(ws_dir, "copied.txt")
        shutil.copy2(src, dst)
        ok1 = os.path.exists(dst)
        shutil.rmtree(ws_dir)
        ok2 = not os.path.exists(ws_dir)
        yield {
            "name": "shutil copy / rmtree",
            "status": ok1 and ok2,
            "detail": f"copy={'成功' if ok1 else '失败'}, rmtree={'成功' if ok2 else '失败'}",
        }
    except Exception as e:
        yield {
            "name": "shutil copy / rmtree",
            "status": False,
            "detail": str(e),
        }
    finally:
        if ws_dir and os.path.exists(ws_dir):
            shutil.rmtree(ws_dir, ignore_errors=True)

    try:
        ws_dir2 = os.path.join(WORKSPACE, "_glob_test")
        os.makedirs(ws_dir2, exist_ok=True)
        for f in ["a.txt", "b.txt", "c.py", "d.py"]:
            pathlib.Path(os.path.join(ws_dir2, f)).touch()
        txt_files = glob.glob(os.path.join(ws_dir2, "*.txt"))
        py_files = glob.glob(os.path.join(ws_dir2, "*.py"))
        ok = len(txt_files) == 2 and len(py_files) == 2
        shutil.rmtree(ws_dir2, ignore_errors=True)
        yield {
            "name": "glob 文件模式匹配",
            "status": ok,
            "detail": f"*.txt={len(txt_files)}, *.py={len(py_files)}" if ok else f"txt={len(txt_files)}, py={len(py_files)}",
        }
    except Exception as e:
        yield {
            "name": "glob 文件模式匹配",
            "status": False,
            "detail": str(e),
        }
    finally:
        if ws_dir2 and os.path.exists(ws_dir2):
            shutil.rmtree(ws_dir2, ignore_errors=True)

    try:
        p = pathlib.Path(WORKSPACE) / "_pathlib_test.txt"
        p.write_text("pathlib content", encoding="utf-8")
        content = p.read_text(encoding="utf-8")
        ok1 = content == "pathlib content"
        ok2 = p.suffix == ".txt"
        ok3 = p.stem == "_pathlib_test"
        p.unlink(missing_ok=True)
        ok4 = not p.exists()
        yield {
            "name": "pathlib 路径操作",
            "status": ok1 and ok2 and ok3 and ok4,
            "detail": f"读写={'成功' if ok1 else '失败'}, suffix={p.suffix}, stem={p.stem}",
        }
    except Exception as e:
        yield {
            "name": "pathlib 路径操作",
            "status": False,
            "detail": str(e),
        }

    try:
        @dataclasses.dataclass
        class User:
            name: str
            age: int
        u = User(name="测试", age=25)
        ok1 = u.name == "测试" and u.age == 25
        d = dataclasses.asdict(u)
        ok2 = d == {"name": "测试", "age": 25}
        yield {
            "name": "dataclasses 数据类",
            "status": ok1 and ok2,
            "detail": f"User={u}, asdict={d}" if ok1 and ok2 else f"创建={'成功' if ok1 else '失败'}, 转换={'成功' if ok2 else '失败'}",
        }
    except Exception as e:
        yield {
            "name": "dataclasses 数据类",
            "status": False,
            "detail": str(e),
        }

    try:
        class Color(enum.Enum):
            RED = 1
            GREEN = 2
            BLUE = 3
        ok1 = Color.RED.value == 1 and Color.GREEN.name == "GREEN"
        names = [c.name for c in Color]
        ok2 = names == ["RED", "GREEN", "BLUE"]
        yield {
            "name": "enum 枚举",
            "status": ok1 and ok2,
            "detail": f"RED.value={Color.RED.value}, names={names}" if ok1 and ok2 else "枚举异常",
        }
    except Exception as e:
        yield {
            "name": "enum 枚举",
            "status": False,
            "detail": str(e),
        }

    try:
        call_count = 0
        @functools.lru_cache(maxsize=10)
        def fib(n):
            nonlocal call_count
            call_count += 1
            if n < 2:
                return n
            return fib(n - 1) + fib(n - 2)
        result = fib(10)
        cached_count = call_count
        ok1 = result == 55
        result_again = fib(10)
        ok2 = call_count == cached_count
        yield {
            "name": "functools.lru_cache",
            "status": ok1 and ok2,
            "detail": f"fib(10)={result}, 调用次数={call_count}" if ok1 and ok2 else f"结果={result}, 缓存={'成功' if ok2 else '失败'}",
        }
    except Exception as e:
        yield {
            "name": "functools.lru_cache",
            "status": False,
            "detail": str(e),
        }

    try:
        add_5 = functools.partial(lambda a, b: a + b, 5)
        result = add_5(3)
        ok = result == 8
        yield {
            "name": "functools.partial",
            "status": ok,
            "detail": f"add_5(3)={result}" if ok else f"结果异常: {result}",
        }
    except Exception as e:
        yield {
            "name": "functools.partial",
            "status": False,
            "detail": str(e),
        }

    try:
        logger = logging.getLogger("_py_test")
        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        logger.addHandler(handler)
        logger.removeHandler(handler)
        yield {
            "name": "logging 日志配置",
            "status": True,
            "detail": f"Logger={logger.name}, level={logger.level}, handlers={len(logger.handlers)}",
        }
    except Exception as e:
        yield {
            "name": "logging 日志配置",
            "status": False,
            "detail": str(e),
        }

    try:
        text = "Hello World! Test 123."
        ok1 = re.sub(r"\d+", "NUM", text) == "Hello World! Test NUM."
        ok2 = re.findall(r"\w+", text) == ["Hello", "World", "Test", "123"]
        ok3 = re.split(r"\s+", text) == ["Hello", "World!", "Test", "123."]
        yield {
            "name": "re.sub / findall / split",
            "status": ok1 and ok2 and ok3,
            "detail": f"sub={'成功' if ok1 else '失败'}, findall={'成功' if ok2 else '失败'}, split={'成功' if ok3 else '失败'}",
        }
    except Exception as e:
        yield {
            "name": "re.sub / findall / split",
            "status": False,
            "detail": str(e),
        }

    try:
        with tempfile.NamedTemporaryFile(mode="w+", suffix=".tmp", prefix="_py_", delete=True) as f:
            f.write("temporary file test")
            f.seek(0)
            content = f.read()
            ok = content == "temporary file test"
        yield {
            "name": "tempfile.NamedTemporaryFile",
            "status": ok,
            "detail": f"读写={'成功' if ok else '失败'}, name={f.name}",
        }
    except Exception as e:
        yield {
            "name": "tempfile.NamedTemporaryFile",
            "status": False,
            "detail": str(e),
        }
