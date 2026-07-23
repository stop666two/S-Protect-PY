"""Multi-File Detection System - Entry point.
6 interconnected files: core_math, core_crypto, utils_data, core_verify, utils_report
Runs 30+ preset tests and reports pass/fail."""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils_report import print_report

if __name__ == "__main__":
    passed, failed = print_report()
    sys.exit(0 if failed == 0 else 1)
