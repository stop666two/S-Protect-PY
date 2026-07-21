import os, json, ast
os.chdir(r"D:\administrator\Documents\project\S-Protect-PY")
from sprotect.loader import gen_loader_source
from sprotect.minify import minify_source

module_map = {"main": "abc123", "utils": "def456"}
map_json = json.dumps(module_map, separators=(",", ":"))

loader_src = gen_loader_source()
escaped = json.dumps(map_json)
loader_src = loader_src.replace('_MAP = ""', f"_MAP = {escaped}")
loader_src = minify_source(loader_src, add_garbage=True)

try:
    ast.parse(loader_src)
    print("Valid syntax")
    print("Has def run:", "def run" in loader_src)
    # Check that _MAP wasn't renamed weirdly
    for line in loader_src.split("\n"):
        if "MAP" in line or "map" in line:
            print(f"  MAP: {line[:80]}")
except SyntaxError as e:
    print(f"Syntax error: {e}")
    print(loader_src[:500])
