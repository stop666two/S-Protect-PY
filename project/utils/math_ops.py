"""Math operations.
Cross-references: crypto.encoder (b64encode), data.seeds (SEED_POOL)"""
from data.seeds import SEED_POOL as _SEED_POOL


PRIMES_100 = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]


def is_prime(n):
    if n < 2: return False
    for p in PRIMES_100:
        if p * p > n: break
        if n % p == 0: return False
    return True


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


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def lcm(a, b):
    return a * b // gcd(a, b)


def power_mod(base, exp, mod):
    r = 1
    while exp:
        if exp & 1: r = (r * base) % mod
        base = (base * base) % mod
        exp >>= 1
    return r


def digit_sum(n):
    return sum(int(d) for d in str(abs(n)))


def reverse_number(n):
    return int(str(abs(n))[::-1]) * (-1 if n < 0 else 1)


def collatz_steps(n):
    steps = 0
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        steps += 1
    return steps

