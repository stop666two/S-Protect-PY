"""Verification runner - runs all tests and reports."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import core.validator as _cv
import core.crosscheck as _cc
import crypto.hasher as _ch
import crypto.encoder as _ce
import data.registry as _dr
import data.seeds as _ds
import utils.math_ops as _um
import utils.str_ops as _us


def _run():
    results = []
    def _add(name, status, detail=""):
        results.append({"name": name, "status": status, "detail": detail})

    for r in _cv.validate_chain():
        _add(r["name"], r["status"], r.get("detail", ""))
    for r in _cc.cross_verify():
        _add(r["name"], r["status"])
    _add("prime_97", _um.is_prime(97))
    _add("prime_51", not _um.is_prime(51))
    _add("prime_2", _um.is_prime(2))
    _add("prime_1", not _um.is_prime(1))
    _add("fib_10", _um.fibonacci(10) == 55)
    _add("fib_20", _um.fibonacci(20) == 6765)
    _add("fib_15", _um.fibonacci(15) == 610)
    _add("fac_5", _um.factorial(5) == 120)
    _add("fac_7", _um.factorial(7) == 5040)
    _add("fac_10", _um.factorial(10) == 3628800)
    _add("b64_abc", _ce.b64encode("abc") == "YWJj")
    _add("b64_test", _ce.b64encode("test") == "dGVzdA==")
    _add("xor_abc_abc", _ce.xor_data(b"abc", b"abc").hex() == "000000")
    _add("xor_123_456", _ce.xor_data(b"123", b"456").hex() == "050705")
    _add("xor_repeat", _ce.xor_data(b"\x00\x01\x02", b"\x00\x01\x02").hex() == "000000")
    _add("rot13_hello", _us.rot13("hello") == "uryyb")
    _add("rot13_abc", _us.rot13("abc") == "nop")
    _add("leet_test", _us.leet_speak("test") == "7357")
    _add("leet_hello", _us.leet_speak("hello") == "h3110")
    _add("registry_count", len(_dr.FILE_REGISTRY) >= 1, f"files={len(_dr.FILE_REGISTRY)}")
    _add("registry_has_main", "main.py" in _dr.FILE_REGISTRY or any("main" in k for k in _dr.FILE_REGISTRY))
    return results


def run_all():
    return _run()


def print_summary():
    results = _run()
    total = len(results)
    passed = sum(1 for r in results if r["status"])
    failed = total - passed
    print("=" * 60)
    print("         Multi-Folder Chaos Detection System")
    print("=" * 60)
    print()
    for r in results:
        s = "PASS" if r["status"] else "FAIL"
        d = r.get("detail", r.get("expected", ""))
        print(f"  [{s}] {r['name']:<35s} {d}")
    print()
    print("-" * 60)
    print(f"  Total: {total}  |  Pass: {passed}  |  Fail: {failed}")
    verdict = "NORMAL" if failed == 0 else "ABNORMAL"
    print(f"  Verdict: {verdict}")
    print("=" * 60)
    return passed, failed
