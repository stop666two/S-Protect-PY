import inspect
import ast
import gc
import weakref
import heapq
import bisect
import array
import unicodedata
import types


def run_special_checks():
    try:
        src = inspect.getsource(run_special_checks)
        ok = "def run_special_checks" in src
        yield {
            "name": "inspect.getsource 源码获取",
            "status": ok,
            "detail": f"获取到 {len(src)} chars, 含函数定义={'成功' if ok else '失败'}",
            "expect": "pass",
        }
    except Exception as e:
        yield {
            "name": "inspect.getsource 源码获取",
            "status": False,
            "detail": str(e),
            "expect": "pass",
        }

    try:
        sig = inspect.signature(run_special_checks)
        ok = sig is not None
        yield {
            "name": "inspect.signature 签名获取",
            "status": ok,
            "detail": f"签名={sig}" if ok else "获取失败",
            "expect": "pass",
        }
    except Exception as e:
        yield {
            "name": "inspect.signature 签名获取",
            "status": False,
            "detail": str(e),
            "expect": "pass",
        }

    try:
        def gen():
            for i in range(3):
                yield i
        g = gen()
        v1 = next(g)
        v2 = g.send(None)
        val = next(g)
        ok = val == 2
        yield {
            "name": "生成器 send/throw/close",
            "status": ok,
            "detail": f"next->{v1}, send->{v2}, final->{val}" if ok else "生成器异常",
            "expect": "pass",
        }
    except Exception as e:
        yield {
            "name": "生成器 send/throw/close",
            "status": False,
            "detail": str(e),
            "expect": "pass",
        }

    try:
        data = {"name": "测试", "scores": [1, 2, 3], "valid": True}
        rep = repr(data)
        restored = eval(rep)
        ok = restored == data
        yield {
            "name": "repr() + eval() 往返",
            "status": ok,
            "detail": f"repr={rep[:50]}..., 还原={'成功' if ok else '失败'}",
            "expect": "pass",
        }
    except Exception as e:
        yield {
            "name": "repr() + eval() 往返",
            "status": False,
            "detail": str(e),
            "expect": "pass",
        }

    try:
        text = "{'a': 1, 'b': [2, 3]}"
        result = ast.literal_eval(text)
        ok = result == {"a": 1, "b": [2, 3]}
        yield {
            "name": "ast.literal_eval 安全求值",
            "status": ok,
            "detail": f"解析={'成功' if ok else '失败'}, type={type(result).__name__}",
            "expect": "pass",
        }
    except Exception as e:
        yield {
            "name": "ast.literal_eval 安全求值",
            "status": False,
            "detail": str(e),
            "expect": "pass",
        }

    try:
        MyClass = type("MyClass", (), {"x": 42, "greet": lambda self: "hello"})
        obj = MyClass()
        ok1 = obj.x == 42
        ok2 = obj.greet() == "hello"
        yield {
            "name": "type() 动态创建类",
            "status": ok1 and ok2,
            "detail": f"MyClass.x={obj.x}, greet={obj.greet()}" if ok1 and ok2 else "动态类异常",
            "expect": "pass",
        }
    except Exception as e:
        yield {
            "name": "type() 动态创建类",
            "status": False,
            "detail": str(e),
            "expect": "pass",
        }

    try:
        class Demo:
            def __init__(self):
                self._val = 0
            @property
            def val(self):
                return self._val
            @val.setter
            def val(self, v):
                self._val = v
            @staticmethod
            def static_method():
                return "static"
            @classmethod
            def class_method(cls):
                return "class"
        d = Demo()
        d.val = 42
        ok1 = d.val == 42
        ok2 = Demo.static_method() == "static"
        ok3 = Demo.class_method() == "class"
        yield {
            "name": "@property / @staticmethod / @classmethod",
            "status": ok1 and ok2 and ok3,
            "detail": f"property={d.val}, static={Demo.static_method()}, class={Demo.class_method()}",
            "expect": "pass",
        }
    except Exception as e:
        yield {
            "name": "@property / @staticmethod / @classmethod",
            "status": False,
            "detail": str(e),
            "expect": "pass",
        }

    try:
        class _RefTarget:
            pass
        gc.collect()
        obj = _RefTarget()
        ref = weakref.ref(obj)
        ok1 = ref() is obj
        del obj
        gc.collect()
        ok2 = ref() is None
        yield {
            "name": "weakref 弱引用",
            "status": ok1 and ok2,
            "detail": f"引用存活={'成功' if ok1 else '失败'}, 回收={'成功' if ok2 else '失败'}",
            "expect": "pass",
        }
    except Exception as e:
        yield {
            "name": "weakref 弱引用",
            "status": False,
            "detail": str(e),
            "expect": "pass",
        }

    try:
        gc.collect()
        old_count = len(gc.get_objects())
        _temp = [1, 2, 3]
        new_count = len(gc.get_objects())
        ok = new_count > old_count
        del _temp
        gc.collect()
        yield {
            "name": "gc.get_objects / gc.collect",
            "status": ok,
            "detail": f"对象数从 {old_count} 增至 {new_count}, 差值={new_count - old_count}" if ok else "GC 异常",
            "expect": "pass",
        }
    except Exception as e:
        yield {
            "name": "gc.get_objects / gc.collect",
            "status": False,
            "detail": str(e),
            "expect": "pass",
        }

    try:
        h = []
        heapq.heappush(h, 3)
        heapq.heappush(h, 1)
        heapq.heappush(h, 2)
        popped = [heapq.heappop(h) for _ in range(3)]
        ok1 = popped == [1, 2, 3]
        arr = [10, 20, 30, 40]
        idx = bisect.bisect_left(arr, 25)
        bisect.insort(arr, 25)
        ok2 = idx == 2 and arr == [10, 20, 25, 30, 40]
        yield {
            "name": "heapq / bisect",
            "status": ok1 and ok2,
            "detail": f"heappop={popped}, bisect idx={idx}, insort={arr[2]==25}" if ok1 and ok2 else "数据结构异常",
            "expect": "pass",
        }
    except Exception as e:
        yield {
            "name": "heapq / bisect",
            "status": False,
            "detail": str(e),
            "expect": "pass",
        }

    try:
        a = array.array("i", [1, 2, 3, 4, 5])
        ok1 = len(a) == 5 and a[2] == 3
        a.append(6)
        ok2 = len(a) == 6
        yield {
            "name": "array.array 紧凑数组",
            "status": ok1 and ok2,
            "detail": f"typecode={a.typecode}, len={len(a)}, a[2]={a[2]}",
            "expect": "pass",
        }
    except Exception as e:
        yield {
            "name": "array.array 紧凑数组",
            "status": False,
            "detail": str(e),
            "expect": "pass",
        }

    try:
        name = unicodedata.lookup("LATIN CAPITAL LETTER A")
        ok1 = name == "A"
        val = unicodedata.name("A", "UNKNOWN")
        ok2 = val == "LATIN CAPITAL LETTER A"
        cnt = unicodedata.east_asian_width("A")
        ok3 = isinstance(cnt, str)
        yield {
            "name": "unicodedata 字符属性",
            "status": ok1 and ok2 and ok3,
            "detail": f"lookup(A)={name}, name('A')={val}, width={cnt}" if ok1 and ok2 and ok3 else "Unicode 异常",
            "expect": "pass",
        }
    except Exception as e:
        yield {
            "name": "unicodedata 字符属性",
            "status": False,
            "detail": str(e),
            "expect": "pass",
        }

    try:
        import sys
        size = sys.getsizeof({"a": 1, "b": 2, "c": 3})
        ok = size > 0
        yield {
            "name": "sys.getsizeof 对象大小",
            "status": ok,
            "detail": f"dict(3 items)={size} bytes" if ok else "获取失败",
            "expect": "pass",
        }
    except Exception as e:
        yield {
            "name": "sys.getsizeof 对象大小",
            "status": False,
            "detail": str(e),
            "expect": "pass",
        }
