from sprotect.minify import minify_source

# Test 1: bootloader
boot = """import sys, os
import zlib as _Z
def _xof(l, s): pass
def _boot(k): pass
exec(compile(_boot(b"x"), "", "exec"))
run("main", ".")
"""
r1 = minify_source(boot, add_garbage=False)
print("=== Bootloader ===")
print(r1)
print()

# Test 2: loader source
src = """import sys, os
def run(entry, root=""):
    return 42
"""
r2 = minify_source(src, add_garbage=False)
print("=== Loader ===")
print(r2)
