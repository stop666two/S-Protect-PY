"""Self-integrity check - validates every file's hash against registry.
Cross-references: data.registry (FILE_REGISTRY), core.validator (hash_file),
                 crypto.hasher (sha256_data), utils.verify (print_summary)"""
import os
from data.registry import FILE_REGISTRY as _REG
from core.validator import hash_file as _hash_file


def check_integrity():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    issues = []
    for rel, expected in _REG.items():
        fp = os.path.join(base, rel.replace("/", os.sep))
        if not os.path.isfile(fp):
            issues.append(f"MISSING:{rel}")
            continue
        actual = _hash_file(fp)
        if actual != expected:
            issues.append(f"MODIFIED:{rel}")
    if not issues:
        return {"status": True, "detail": "all files intact"}
    return {"status": False, "detail": "; ".join(issues)}
