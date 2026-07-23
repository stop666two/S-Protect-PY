"""Verification module - preset answers and test runner."""
from core_math import is_prime, xor_bytes, sha256_digest, base64_encode
from core_crypto import xor_chain, hash_chain, double_encode
from utils_data import rot13, leet_speak, fibonacci, factorial


PRESET_ANSWERS = {
    "prime_97": is_prime(97),
    "prime_100": is_prime(100),
    "xor_abc_abc": xor_bytes(b"abc", b"abc").hex(),
    "sha256_test": sha256_digest("test"),
    "base64_test": base64_encode("test"),
    "rot13_hello": rot13("hello"),
    "leet_test": leet_speak("test"),
    "fib_10": fibonacci(10),
    "fib_20": fibonacci(20),
    "fac_5": factorial(5),
    "fac_10": factorial(10),
    "xor_chain_ab": xor_chain("ab", ["cd", "ef"]),
    "hash_chain_3": hash_chain("abc", 3),
    "double_encode_hi": double_encode("hi"),
    "prime_53": is_prime(53),
    "prime_51": is_prime(51),
    "xor_123_456": xor_bytes(b"123", b"456").hex(),
    "sha256_hello": sha256_digest("hello"),
    "base64_abc": base64_encode("abc"),
    "rot13_abc": rot13("abc"),
    "leet_hello": leet_speak("hello"),
    "fib_15": fibonacci(15),
    "fac_7": factorial(7),
    "xor_chain_xyz": xor_chain("xyz", ["123", "456"]),
    "hash_chain_5": hash_chain("xyz", 5),
    "double_encode_test": double_encode("test"),
    "prime_2": is_prime(2),
    "prime_1": is_prime(1),
    "xor_repeat": xor_bytes(b"\x00\x01\x02", b"\x00\x01\x02").hex(),
    "sha256_123": sha256_digest("123"),
}


def run_all_checks():
    results = []
    for name, expected in PRESET_ANSWERS.items():
        try:
            actual = PRESET_ANSWERS[name]
            ok = actual == expected
            results.append({"name": name, "status": ok, "expected": repr(expected), "actual": repr(actual)})
        except Exception as e:
            results.append({"name": name, "status": False, "detail": str(e)})
    return results
