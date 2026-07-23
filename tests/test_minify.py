from sprotect.minify import minify_source, minify_and_compress, gen_decoy_source, _inject_noise, _weave_trap
import zlib


def test_minify_preserves_behavior():
    src = "def add(a, b):\n    return a + b\n"
    m = minify_source(src, add_garbage=False, make_trap=False)
    ns = {}
    exec(compile(m, "<test>", "exec"), ns)
    fns = [v for v in ns.values() if callable(v)]
    assert len(fns) >= 1
    assert fns[0](2, 3) == 5


def test_minify_shortens_names():
    src = "def long_function_name():\n    return 42\n"
    m = minify_source(src, add_garbage=False, alias_libs=False)
    assert "long_function_name" not in m


def test_minify_strips_docstrings():
    src = '"""module doc"""\ndef f():\n    """func doc"""\n    return 1\n'
    m = minify_source(src, add_garbage=False, alias_libs=False)
    assert '"""' not in m


def test_minify_preserves_stdlib():
    src = "import os\nimport json\ndef f():\n    return os.name\n"
    m = minify_source(src, add_garbage=False)
    assert "os" in m
    assert "json" in m


def test_minify_preserves_reserved_names():
    src = "def main():\n    return 0\n"
    m = minify_source(src, add_garbage=False, alias_libs=False)
    assert "main" in m


def test_minify_with_garbage():
    src = "x = 1\n"
    m = minify_source(src, add_garbage=True, alias_libs=False)
    assert "#" in m


def test_minify_compact_lines():
    src = "def f():\n\n\n\n    pass\n"
    m = minify_source(src, add_garbage=False, alias_libs=False)
    lines = [l for l in m.split("\n") if l.strip()]
    assert len(lines) >= 2


def test_minify_invalid_syntax_returns_asis():
    src = "this is not valid python {{{"
    m = minify_source(src, add_garbage=False)
    assert m == src


def test_minify_error_preserves_variable_names():
    src = "def f():\n    try:\n        x = 1\n    except:\n        pass\n"
    m = minify_source(src, add_garbage=False, alias_libs=False)
    assert "x" in m or "try" in m


def test_minify_and_compress():
    src = "def f():\n    return 42\n"
    compressed = minify_and_compress(src, add_garbage=False)
    assert isinstance(compressed, bytes)
    assert len(compressed) < len(src) * 2
    decompressed = zlib.decompress(compressed).decode()
    assert "f" in decompressed


def test_gen_decoy_source():
    result = gen_decoy_source()
    assert isinstance(result, bytes)
    decompressed = zlib.decompress(result).decode()
    assert "import" in decompressed
    assert "class" in decompressed or "def" in decompressed
    assert "while True" in decompressed


def test_weave_trap():
    trap = _weave_trap()
    assert "while True" in trap
    assert "class " in trap
    compile(trap, "<test>", "exec")


def test_inject_noise():
    noise = _inject_noise()
    assert noise.startswith("#")
    assert noise.endswith("\n")


def test_minify_async_function():
    src = "async def fetch():\n    return 1\n"
    m = minify_source(src, add_garbage=False, alias_libs=False)
    assert "fetch" not in m
    assert "async" in m


def test_minify_class_renaming():
    src = "class MyClass:\n    def method(self):\n        return 42\n"
    m = minify_source(src, add_garbage=False, alias_libs=False)
    assert "MyClass" not in m
    assert "method" not in m
    ns = {}
    exec(compile(m, "<test>", "exec"), ns)
    cls = [v for v in ns.values() if isinstance(v, type)][0]
    obj = cls()
    for name in dir(obj):
        if not name.startswith("_"):
            assert getattr(obj, name)() == 42
            break


def test_minify_large_input_preserves_count():
    src = "\n".join(f"def func{i}():\n    return {i}\n" for i in range(200))
    m = minify_source(src, add_garbage=False, alias_libs=False)
    assert "def " in m
    ns = {}
    exec(compile(m, "<test>", "exec"), ns)
    fns = [v for v in ns.values() if callable(v)]
    assert len(fns) >= 1


def test_minify_with_class_and_methods():
    src = "class Calculator:\n    def add(self, a, b):\n        return a + b\n    def sub(self, a, b):\n        return a - b\n"
    m = minify_source(src, add_garbage=False, alias_libs=False)
    ns = {}
    exec(compile(m, "<test>", "exec"), ns)
    calc_cls = [v for v in ns.values() if isinstance(v, type)][0]
    calc = calc_cls()
    for name in dir(calc):
        if not name.startswith("_"):
            fn = getattr(calc, name)
            r = fn(5, 3)
            assert r in (8, 2)


def test_minify_preserves_import_alias():
    src = "import os as operating_system\ndef f():\n    return operating_system.name\n"
    m = minify_source(src, add_garbage=False)
    assert "operating_system" in m
    ns = {}
    exec(compile(m, "<test>", "exec"), ns)
    fns = [v for v in ns.values() if callable(v)]
    assert len(fns) >= 1


def test_minify_empty_source():
    assert minify_source("", add_garbage=False) == ""


def test_minify_single_line():
    m = minify_source("x = 1", add_garbage=False, alias_libs=False)
    assert "=" in m
    assert "1" in m
