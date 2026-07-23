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
