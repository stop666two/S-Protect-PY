import sys, os
sys.stdout = open("_run_output.txt", "w", encoding="utf-8")
sys.stderr = sys.stdout
os.chdir(r"D:\administrator\Documents\project\S-Protect-PY\output")
exec(compile(open("main.py", "rb").read(), "main.py", "exec"))
