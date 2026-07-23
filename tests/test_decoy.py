from sprotect.decoy import generate_decoy_source, generate_trap_source, _gen_fake_name, _gen_fake_body
import sys, os


def test_generate_decoy_source_is_valid_python():
    src = generate_decoy_source()
    assert isinstance(src, str)
    assert len(src) > 50
    compile(src, "<test>", "exec")


def test_generate_decoy_source_varied():
    sources = [generate_decoy_source() for _ in range(10)]
    assert len(set(sources)) > 1


def test_generate_decoy_source_has_imports():
    src = generate_decoy_source()
    assert "import" in src or "from " in src


def test_generate_decoy_source_has_functions():
    src = generate_decoy_source()
    assert "def " in src


def test_generate_trap_source_is_valid_python():
    src = generate_trap_source()
    assert isinstance(src, str)
    assert len(src) > 50
    compile(src, "<test>", "exec")


def test_generate_trap_source_has_infinite_loop():
    src = generate_trap_source()
    assert "while True" in src


def test_generate_trap_source_has_class():
    src = generate_trap_source()
    assert "class " in src


def test_generate_trap_source_varied():
    sources = [generate_trap_source() for _ in range(10)]
    assert len(set(sources)) > 1


def test_gen_fake_name():
    name = _gen_fake_name()
    assert isinstance(name, str)
    assert len(name) > 3


def test_gen_fake_body():
    body = _gen_fake_body()
    assert isinstance(body, str)
    assert len(body) > 10


def test_decoy_source_contains_python_keywords():
    src = generate_decoy_source()
    assert any(kw in src for kw in ["def ", "class ", "return ", "for ", "import "])


def test_trap_source_defines_class_and_main():
    src = generate_trap_source()
    code = compile(src, "<test>", "exec")
    ns = {}
    exec(code, ns)
    assert "main" in ns
