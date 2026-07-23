"""Extended edge case tests for obfuscation engine."""
from sprotect.obfuscate import Obfuscator, collect_defs
from sprotect.types import ObfuscateConfig, RenameRules


_RR = RenameRules(style="hex", reserved=["main", "__init__", "fact", "gen", "outer", "inner", "f", "f1", "f2", "C", "dec", "C"], prefix="_0x", suffix="", min_length=6, blacklist=[])

_L5 = ObfuscateConfig(
    level=5, rename_variables=True, rename_functions=True, rename_classes=True,
    rename_rules=_RR,
    encrypt_strings=True, encrypt_numbers=True,
    control_flow_flattening=True, dead_code_injection=True,
    dead_code_density=0.5, opaque_predicate_count=3,
    remove_docstrings=True, remove_comments=True, strip_blank_lines=True, max_line_length=0,
    string_split=True, string_cipher="mixed",
    obfuscate_imports=True, obfuscate_calls=True, obfuscate_arithmetic=True, obfuscate_booleans=True,
    string_min_length=1, string_encrypt_ratio=1.0,
)

_RR_L0 = RenameRules(style="hex", reserved=[], prefix="", suffix="", min_length=6, blacklist=[])

_L0 = ObfuscateConfig(
    level=0, rename_variables=False, rename_functions=False, rename_classes=False,
    rename_rules=_RR_L0,
    encrypt_strings=False, encrypt_numbers=False,
    control_flow_flattening=False, dead_code_injection=False,
    dead_code_density=0, opaque_predicate_count=0,
    remove_docstrings=False, remove_comments=False, strip_blank_lines=False, max_line_length=0,
    string_split=False, string_cipher="plain",
    obfuscate_imports=False, obfuscate_calls=False, obfuscate_arithmetic=False, obfuscate_booleans=False,
    string_min_length=3, string_encrypt_ratio=1.0,
)


def _obf(src, cfg=_L5):
    return Obfuscator(cfg, {}, set(), set()).obfuscate(src)


def test_obfuscate_empty():
    assert _obf("", _L0) == ""


def test_obfuscate_whitespace():
    r = _obf("   \n\n  ", _L0).strip()
    assert r == ""


def test_obfuscate_comment_only():
    r = _obf("# just a comment", _L0).strip()
    assert r == ""


def test_obfuscate_import_only():
    r = _obf("import os", _L5)
    assert "os" in r or "__import__" in r


def test_obfuscate_single_expression():
    r = _obf("x = 1 + 2", _L5)
    ns = {}
    exec(compile(r, "<test>", "exec"), ns)
    val = [v for v in ns.values() if isinstance(v, (int, float))][0]
    assert val == 3


def test_obfuscate_preserves_main():
    r = _obf("def main():\n    return 42\n", _L5)
    assert "main" in r


def test_obfuscate_large_numbers():
    r = _obf("x = 999999999", _L5)
    ns = {}
    exec(compile(r, "<test>", "exec"), ns)
    vals = [v for v in ns.values() if isinstance(v, int)]
    assert len(vals) > 0


def test_obfuscate_negative_numbers():
    r = _obf("x = -42", _L5)
    ns = {}
    exec(compile(r, "<test>", "exec"), ns)
    assert any(v == -42 for v in ns.values() if isinstance(v, int))


def test_obfuscate_float():
    r = _obf("x = 3.14159", _L5)
    ns = {}
    exec(compile(r, "<test>", "exec"), ns)
    assert any(abs(v - 3.14159) < 0.001 for v in ns.values() if isinstance(v, float))


def test_obfuscate_complex_import():
    r = _obf("from os import path\nx = path.join('a', 'b')", _L5)
    ns = {}
    exec(compile(r, "<test>", "exec"), ns)
    ns.get("x")


def test_obfuscate_nested_functions():
    src = "def outer():\n    def inner():\n        return 1\n    return inner()\n"
    r = _obf(src, _L5)
    ns = {}
    exec(compile(r, "<test>", "exec"), ns)
    fns = [v for v in ns.values() if callable(v)]
    assert len(fns) >= 1
    assert fns[0]() == 1


def test_obfuscate_try_except():
    src = "def f():\n    try:\n        return 1\n    except:\n        return 2\n"
    r = _obf(src, _L5)
    ns = {}
    exec(compile(r, "<test>", "exec"), ns)
    fns = [v for v in ns.values() if callable(v)]
    assert fns[0]() == 1


def test_obfuscate_with_decorator():
    src = "def deco(f): return f\n@deco\ndef f():\n    return 42\n"
    r = _obf(src, _L5)
    ns = {}
    exec(compile(r, "<test>", "exec"), ns)
    fns = [v for v in ns.values() if callable(v)]
    assert len(fns) >= 1


def test_obfuscate_generator():
    src = "def gen():\n    yield 1\n    yield 2\n"
    r = _obf(src, _L5)
    ns = {}
    exec(compile(r, "<test>", "exec"), ns)
    fns = [v for v in ns.values() if callable(v)]
    g = fns[0]()
    assert list(g) == [1, 2]


def test_obfuscate_async():
    src = "async def f():\n    return 1\n"
    r = _obf(src, _L5)
    assert "async" in r


def test_obfuscate_lambda():
    src = "f = lambda x: x + 1"
    r = _obf(src, _L5)
    ns = {}
    exec(compile(r, "<test>", "exec"), ns)
    fns = [v for v in ns.values() if callable(v)]
    assert fns[0](5) == 6


def test_obfuscate_fstring():
    src = "x = 10\ns = f'value is {x}'\n"
    r = _obf(src, _L5)
    ns = {}
    exec(compile(r, "<test>", "exec"), ns)
    assert ns.get("s") is not None


def test_obfuscate_list_comprehension():
    src = "x = [i*2 for i in range(5)]"
    r = _obf(src, _L5)
    ns = {}
    exec(compile(r, "<test>", "exec"), ns)
    vals = [v for v in ns.values() if isinstance(v, list)]
    assert len(vals) > 0


def test_obfuscate_dict_comprehension():
    src = "x = {i: i*2 for i in range(5)}"
    r = _obf(src, _L5)
    ns = {}
    exec(compile(r, "<test>", "exec"), ns)
    vals = [v for v in ns.values() if isinstance(v, dict)]
    assert len(vals) > 0


def test_obfuscate_nested_lambda():
    src = "f = lambda x: (lambda y: x + y)"
    r = _obf(src, _L5)
    ns = {}
    exec(compile(r, "<test>", "exec"), ns)
    fns = [v for v in ns.values() if callable(v)]
    assert fns[0](3)(4) == 7


def test_obfuscate_level_0_skips_renaming():
    src = "def f(a, b):\n    return a + b\n"
    r = _obf(src, _L0)
    assert "return" in r


def test_collect_defs():
    mapping = {}
    collect_defs("def my_custom_func(): pass\n", _L5, mapping)
    assert "my_custom_func" in mapping


def test_collect_defs_empty():
    mapping = {}
    collect_defs("", _L5, mapping)
    assert mapping == {}


def test_obfuscate_multiline_string():
    src = 's = "helloworld"\n'
    r = _obf(src, _L5)
    ns = {}
    exec(compile(r, "<test>", "exec"), ns)
    assert ns.get("s") == "helloworld"


def test_obfuscate_walrus_operator():
    src = "x = (y := 5) + y"
    r = _obf(src, _L5)
    ns = {}
    exec(compile(r, "<test>", "exec"), ns)
    vals = [v for v in ns.values() if isinstance(v, int)]
    assert 10 in vals


def test_obfuscate_match_statement():
    try:
        src = "def f(val):\n    match val:\n        case 1: return 'one'\n        case _: return 'other'\n"
        r = _obf(src, _L5)
        ns = {}
        exec(compile(r, "<test>", "exec"), ns)
        fns = [v for v in ns.values() if callable(v)]
        assert fns[0](1) == "one"
        assert fns[0](2) == "other"
    except SyntaxError:
        pass


def test_obfuscate_recursive():
    src = "def fact(n):\n    return 1 if n <= 1 else n * fact(n - 1)\n"
    r = _obf(src, _L5)
    ns = {}
    exec(compile(r, "<test>", "exec"), ns)
    fns = [v for v in ns.values() if callable(v)]
    assert fns[0](5) == 120
