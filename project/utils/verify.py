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
    _add("prime_53", _um.is_prime(53))
    _add("prime_99", not _um.is_prime(99))
    _add("fib_10", _um.fibonacci(10) == 55)
    _add("fib_20", _um.fibonacci(20) == 6765)
    _add("fib_15", _um.fibonacci(15) == 610)
    _add("fib_25", _um.fibonacci(25) == 75025)
    _add("fib_30", _um.fibonacci(30) == 832040)
    _add("fac_5", _um.factorial(5) == 120)
    _add("fac_7", _um.factorial(7) == 5040)
    _add("fac_10", _um.factorial(10) == 3628800)
    _add("fac_3", _um.factorial(3) == 6)
    _add("fac_8", _um.factorial(8) == 40320)
    _add("gcd_12_8", _um.gcd(12, 8) == 4)
    _add("gcd_17_5", _um.gcd(17, 5) == 1)
    _add("lcm_4_6", _um.lcm(4, 6) == 12)
    _add("pow_mod_2_10_1000", _um.power_mod(2, 10, 1000) == 24)
    _add("digit_sum_12345", _um.digit_sum(12345) == 15)
    _add("digit_sum_999", _um.digit_sum(999) == 27)
    _add("rev_num_1234", _um.reverse_number(1234) == 4321)
    _add("rev_num_neg", _um.reverse_number(-789) == -987)
    _add("collatz_6", _um.collatz_steps(6) == 8)
    _add("collatz_27", _um.collatz_steps(27) == 111)
    _add("b64_abc", _ce.b64encode("abc") == "YWJj")
    _add("b64_test", _ce.b64encode("test") == "dGVzdA==")
    _add("b64_hello", _ce.b64encode("hello") == "aGVsbG8=")
    _add("b64_decode", _ce.b64decode("aGVsbG8=") == "hello")
    _add("xor_abc_abc", _ce.xor_data(b"abc", b"abc").hex() == "000000")
    _add("xor_123_456", _ce.xor_data(b"123", b"456").hex() == "050705")
    _add("xor_repeat", _ce.xor_data(b"\x00\x01\x02", b"\x00\x01\x02").hex() == "000000")
    _add("xor_abc_xyz", _ce.xor_data(b"abc", b"xyz").hex() == "191b19")
    _add("rot13_hello", _us.rot13("hello") == "uryyb")
    _add("rot13_abc", _us.rot13("abc") == "nop")
    _add("rot13_uryyb", _us.rot13("uryyb") == "hello")
    _add("leet_test", _us.leet_speak("test") == "7357")
    _add("leet_hello", _us.leet_speak("hello") == "h3110")
    _add("leet_leet", _us.leet_speak("leet") == "1337")
    _add("reverse_abc", _us.reverse_str("abc") == "cba")
    _add("reverse_hello", _us.reverse_str("hello") == "olleh")
    _add("palindrome_racecar", _us.is_palindrome("racecar"))
    _add("palindrome_hello", not _us.is_palindrome("hello"))
    _add("vowels_hello", _us.count_vowels("hello") == 2)
    _add("vowels_aeiou", _us.count_vowels("aeiou") == 5)
    _add("caesar_abc", _us.caesar_shift("abc", 3) == "def")
    _add("caesar_xyz", _us.caesar_shift("xyz", 3) == "abc")
    _add("atbash_abc", _us.atbash("abc") == "zyx")
    _add("atbash_hello", _us.atbash("hello") == "svool")
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
