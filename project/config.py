import os

TEST_CATEGORIES = {
    "basic": "基础环境信息",
    "stdlib": "标准库模块检测",
    "thirdparty": "第三方包检测",
    "runtime": "运行时能力检测",
    "compile_crypto": "编译/加密核心",
    "advanced": "高级运行时能力",
    "stress": "系统压力/底层测试",
    "special": "特殊/边缘功能测试",
    "pip_test": "依赖安装卸载测试",
    "realworld": "实际项目功能测试",
}

WORKSPACE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_workspace")

PIP_TEST_PACKAGE = "psutil"

THIRD_PARTY_PACKAGES = [
    "tqdm",
    "colorama",
    "cryptography",
    "numpy",
    "pandas",
    "PIL",
    "requests",
    "rich",
]

STDLIB_MODULES = [
    "os", "sys", "json", "re", "math", "datetime", "pathlib",
    "hashlib", "base64", "itertools", "collections", "typing",
    "random", "socket", "http", "xml", "csv", "sqlite3",
    "threading", "multiprocessing", "subprocess", "zipfile",
    "tarfile", "logging", "configparser", "enum", "functools",
    "decimal", "statistics", "uuid", "tempfile", "shutil",
    "inspect", "codecs", "io", "struct", "array", "ctypes",
    "platform", "argparse", "string", "textwrap", "bisect",
    "heapq", "operator", "contextlib", "abc", "dataclasses",
    "secrets", "zlib", "gzip", "bz2", "lzma", "email",
    "ssl", "asyncio", "select", "signal", "mmap",
    "gc", "ast", "tokenize", "traceback", "weakref",
    "copy", "pprint", "numbers", "stat", "filecmp",
    "getpass", "linecache", "socketserver", "ipaddress",
    "netrc",
    "webbrowser", "gettext", "locale", "calendar",
    "time", "doctest", "unittest", "difflib",
    "tomllib", "graphlib",
]

DEPRECATED_MODULES = [
    "imp",
    "formatter",
    "pipes",
    "distutils",
    "asynchat",
    "asyncore",
    "audioop",
    "cgi",
    "cgitb",
    "chunk",
    "crypt",
    "imghdr",
    "mailcap",
    "msilib",
    "nis",
    "nntplib",
    "ossaudiodev",
    "sndhdr",
    "spwd",
    "sunau",
    "smtpd",
    "telnetlib",
    "uu",
    "xdrlib",
]
