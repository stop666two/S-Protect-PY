"""Data utilities - transformations and test data."""
from core_math import is_prime, xor_bytes, sha256_digest


TEST_VECTORS = {
    "prime_97": (97, True),
    "prime_100": (100, False),
    "xor_abc": ("abc", "abc"),
    "sha256_empty": ("", "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
    "base64_hello": ("Hello", "SGVsbG8="),
}


def rot13(text):
    result = []
    for c in text:
        if "a" <= c <= "z":
            result.append(chr((ord(c) - ord("a") + 13) % 26 + ord("a")))
        elif "A" <= c <= "Z":
            result.append(chr((ord(c) - ord("A") + 13) % 26 + ord("A")))
        else:
            result.append(c)
    return "".join(result)


def leet_speak(text):
    m = {"e": "3", "a": "4", "o": "0", "l": "1", "s": "5", "t": "7"}
    return "".join(m.get(c.lower(), c) for c in text)


def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def factorial(n):
    r = 1
    for i in range(2, n + 1):
        r *= i
    return r
