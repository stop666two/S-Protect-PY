from sprotect.loader import gen_loader_source
from sprotect.minify import minify_source

src = gen_loader_source()
print("Original has 'run':", "def run" in src)
try:
    result = minify_source(src, add_garbage=False)
    print("Minified has 'run':", "def run" in result)
    print("Length:", len(result))
    # Try compiling
    compile(result, "<test>", "exec")
    print("Compiles OK")
except Exception as e:
    print("FAIL:", e)
    print(result[:500])
