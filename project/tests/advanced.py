import asyncio
import concurrent.futures
import subprocess
import sys
import importlib.metadata
import importlib.resources
import mmap
import timeit
import os
import tempfile


def run_advanced_checks():
    try:
        async def sample():
            await asyncio.sleep(0.01)
            return "async_ok"
        val = asyncio.run(sample())
        ok = val == "async_ok"
        yield {
            "name": "asyncio 事件循环",
            "status": ok,
            "detail": f"协程返回={val}" if ok else f"返回值异常: {val}",
            "expect": "pass",
        }
    except Exception as e:
        yield {
            "name": "asyncio 事件循环",
            "status": False,
            "detail": str(e),
            "expect": "pass",
        }

    try:
        def task(n):
            return n * n
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
            fut = ex.submit(task, 7)
            val = fut.result()
        ok = val == 49
        yield {
            "name": "concurrent.futures 线程池",
            "status": ok,
            "detail": f"7*7={val}" if ok else f"结果异常: {val}",
            "expect": "pass",
        }
    except Exception as e:
        yield {
            "name": "concurrent.futures 线程池",
            "status": False,
            "detail": str(e),
            "expect": "pass",
        }

    try:
        proc = subprocess.run(
            [sys.executable, "-c", "print('hello from sub')"],
            capture_output=True, text=True, timeout=10
        )
        out = proc.stdout.strip()
        ok = out == "hello from sub" and proc.returncode == 0
        yield {
            "name": "subprocess 子进程执行",
            "status": ok,
            "detail": f"输出='{out}', 返回码={proc.returncode}" if ok else f"输出='{out}', 返回码={proc.returncode}",
            "expect": "pass",
        }
    except Exception as e:
        yield {
            "name": "subprocess 子进程执行",
            "status": False,
            "detail": str(e),
            "expect": "pass",
        }

    try:
        proc = subprocess.run(
            [sys.executable, "-c", "import sys; data=sys.stdin.read(); print(len(data))"],
            input="hello pipe world", text=True, capture_output=True, timeout=10
        )
        ok = proc.stdout.strip() == "16" and proc.returncode == 0
        yield {
            "name": "subprocess 管道通信",
            "status": ok,
            "detail": f"输入16 bytes, 输出='{proc.stdout.strip()}'" if ok else f"输出='{proc.stdout.strip()}', err='{proc.stderr.strip()}'",
            "expect": "pass",
        }
    except Exception as e:
        yield {
            "name": "subprocess 管道通信",
            "status": False,
            "detail": str(e),
            "expect": "pass",
        }

    try:
        ver = importlib.metadata.version("tqdm")
        ok = isinstance(ver, str) and len(ver) > 0
        yield {
            "name": "importlib.metadata 读取包版本",
            "status": ok,
            "detail": f"tqdm version={ver}" if ok else f"版本读取异常: {ver}",
            "expect": "pass",
        }
    except Exception as e:
        yield {
            "name": "importlib.metadata 读取包版本",
            "status": False,
            "detail": str(e),
            "expect": "pass",
        }

    try:
        import importlib.resources as res
        from importlib.resources import files
        pkg = "tests"
        traversable = files(pkg)
        contents = [c for c in traversable.iterdir()]
        ok = len(contents) > 0
        yield {
            "name": "importlib.resources 包内资源",
            "status": ok,
            "detail": f"tests 包内有 {len(contents)} 个条目" if ok else "未找到资源文件",
            "expect": "pass",
        }
    except Exception as e:
        yield {
            "name": "importlib.resources 包内资源",
            "status": False,
            "detail": str(e),
            "expect": "pass",
        }

    tmp_mmap = None
    try:
        tmp_mmap = os.path.join(tempfile.gettempdir(), "_py_mmap_test.bin")
        data = b"mmap memory mapped file test"
        with open(tmp_mmap, "wb") as f:
            f.write(data)
        with open(tmp_mmap, "r+b") as f:
            with mmap.mmap(f.fileno(), 0) as m:
                read_back = m[:]
                m[0:4] = b"MMAP"
        with open(tmp_mmap, "rb") as f:
            verify = f.read()
        ok = read_back == data and verify.startswith(b"MMAP")
        yield {
            "name": "mmap 内存映射文件",
            "status": ok,
            "detail": f"读取={len(read_back)} bytes, 写入验证={'通过' if ok else '失败'}",
            "expect": "pass",
        }
    except Exception as e:
        yield {
            "name": "mmap 内存映射文件",
            "status": False,
            "detail": str(e),
            "expect": "pass",
        }
    finally:
        if tmp_mmap and os.path.exists(tmp_mmap):
            os.remove(tmp_mmap)

    try:
        elapsed = timeit.timeit("'-'.join(str(i) for i in range(100))", number=1000)
        ok = elapsed > 0
        yield {
            "name": "timeit 代码执行计时",
            "status": ok,
            "detail": f"1000 次迭代耗时 {elapsed*1000:.2f} ms" if ok else "计时异常",
            "expect": "pass",
        }
    except Exception as e:
        yield {
            "name": "timeit 代码执行计时",
            "status": False,
            "detail": str(e),
            "expect": "pass",
        }

    try:
        import tests.basic
        orig_count = len(dir(tests.basic))
        importlib.reload(tests.basic)
        new_count = len(dir(tests.basic))
        ok = new_count == orig_count
        yield {
            "name": "importlib.reload() 热重载",
            "status": ok,
            "detail": f"重载 tests.basic 模块 ({orig_count} -> {new_count} symbols)" if ok else f"符号数变化: {orig_count} -> {new_count}",
            "expect": "pass",
        }
    except Exception as e:
        yield {
            "name": "importlib.reload() 热重载",
            "status": False,
            "detail": str(e),
            "expect": "pass",
        }

    try:
        mod = __import__("json", fromlist=["dumps"])
        ok = hasattr(mod, "dumps") and hasattr(mod, "loads")
        yield {
            "name": "__import__() 内置导入",
            "status": ok,
            "detail": f"json 模块含 dumps={hasattr(mod, 'dumps')}, loads={hasattr(mod, 'loads')}",
            "expect": "pass",
        }
    except Exception as e:
        yield {
            "name": "__import__() 内置导入",
            "status": False,
            "detail": str(e),
            "expect": "pass",
        }

    try:
        rnd = os.urandom(16)
        pid = os.getpid()
        ok = len(rnd) == 16 and pid > 0
        yield {
            "name": "os.urandom / os.getpid",
            "status": ok,
            "detail": f"urandom={len(rnd)} bytes, PID={pid}" if ok else "获取失败",
            "expect": "pass",
        }
    except Exception as e:
        yield {
            "name": "os.urandom / os.getpid",
            "status": False,
            "detail": str(e),
            "expect": "pass",
        }

    try:
        prev = sys.gettrace()
        ok = prev is None or callable(prev)
        yield {
            "name": "sys.gettrace() 调试器检测",
            "status": ok,
            "detail": f"trace={'未设置' if prev is None else '已设置'}",
            "expect": "pass",
        }
    except Exception as e:
        yield {
            "name": "sys.gettrace() 调试器检测",
            "status": False,
            "detail": str(e),
            "expect": "pass",
        }

    try:
        import signal
        handler = signal.signal(signal.SIGINT, signal.SIG_DFL)
        signal.signal(signal.SIGINT, handler)
        yield {
            "name": "signal 信号处理",
            "status": True,
            "detail": f"SIGINT handler restore={'成功' if handler else '完成'}",
            "expect": "pass",
        }
    except Exception as e:
        yield {
            "name": "signal 信号处理",
            "status": False,
            "detail": str(e),
            "expect": "pass",
        }

    try:
        import typing
        hints = typing.get_type_hints(lambda x: int) or {}
        ok = isinstance(hints, dict)
        yield {
            "name": "typing.get_type_hints",
            "status": ok,
            "detail": f"类型提示解析={'成功' if ok else '失败'}",
            "expect": "pass",
        }
    except Exception as e:
        yield {
            "name": "typing.get_type_hints",
            "status": False,
            "detail": str(e),
            "expect": "pass",
        }
