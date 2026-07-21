import re
with open("sprotect/loader.py", "rb") as f:
    data = f.read()

# Find line 231 area
lines = data.decode("utf-8").split("\n")
print("Line 231:", repr(lines[230])[:200])
print("Line 230:", repr(lines[229])[:200])
print("Line 232:", repr(lines[231])[:200])
