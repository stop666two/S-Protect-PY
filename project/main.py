"""Multi-Folder Chaos Detection System - Entry point.
5 directories, 17+ interconnected files with hash chain cross-validation."""
import sys, os, importlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Explicitly import all packages first to ensure subpackage resolution
for _mod in ["core", "crypto", "data", "utils", "tests"]:
    importlib.import_module(_mod)

from utils.verify import print_summary

if __name__ == "__main__":
    passed, failed = print_summary()
    sys.exit(0 if failed == 0 else 1)
