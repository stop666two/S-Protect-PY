with open("sprotect/loader.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Find the f-string block (starts with f''' on some line, ends with ''')
in_fstring = False
for i, line in enumerate(lines):
    stripped = line.strip()
    if stripped.startswith("f'''") or stripped.startswith('f"""'):
        in_fstring = True
        print(f"F-string starts at line {i+1}")
    if in_fstring:
        # Check for single } that's not }}
        for j, ch in enumerate(line):
            if ch == '}':
                # Check if next char is also }
                if j+1 < len(line) and line[j+1] == '}':
                    pass  # Escaped }}
                else:
                    # This could be an issue - but only if inside the f-string
                    # Find the matching { before it
                    pass
    if in_fstring and stripped == "'''" or stripped == '"""':
        if in_fstring:
            print(f"F-string ends at line {i+1}")
            break
