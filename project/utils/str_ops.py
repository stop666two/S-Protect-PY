"""String operations.
Cross-references: core.validator (hash_file), crypto.encoder (b64decode)"""
import re


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


def reverse_str(s):
    return s[::-1]


def is_palindrome(s):
    c = "".join(c.lower() for c in s if c.isalnum())
    return c == c[::-1]


def count_vowels(s):
    return sum(1 for c in s.lower() if c in "aeiou")


def caesar_shift(s, n=3):
    r = []
    for c in s:
        if "a" <= c <= "z":
            r.append(chr((ord(c) - ord("a") + n) % 26 + ord("a")))
        elif "A" <= c <= "Z":
            r.append(chr((ord(c) - ord("A") + n) % 26 + ord("A")))
        else:
            r.append(c)
    return "".join(r)


def atbash(s):
    r = []
    for c in s:
        if "a" <= c <= "z":
            r.append(chr(ord("z") - (ord(c) - ord("a"))))
        elif "A" <= c <= "Z":
            r.append(chr(ord("Z") - (ord(c) - ord("A"))))
        else:
            r.append(c)
    return "".join(r)

