"""Reporting module - format and display test results."""
from core_verify import run_all_checks


def print_report():
    results = run_all_checks()
    total = len(results)
    passed = sum(1 for r in results if r["status"])
    failed = total - passed

    print("=" * 60)
    print("         Multi-File Detection System v2.0")
    print("=" * 60)
    print()

    for r in results:
        status = "PASS" if r["status"] else "FAIL"
        detail = r.get("detail", f"exp={r.get('expected','?')} act={r.get('actual','?')}")
        print(f"  [{status}] {r['name']:<25s} {detail}")

    print()
    print("-" * 60)
    print(f"  Total: {total}  |  Pass: {passed}  |  Fail: {failed}")
    verdict = "NORMAL" if failed == 0 else "ABNORMAL"
    print(f"  Verdict: {verdict}")
    print("=" * 60)

    return passed, failed
