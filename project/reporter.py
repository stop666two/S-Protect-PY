import os

def generate_report(results):
    base = os.path.dirname(os.path.abspath(__file__))

    total = len(results)
    passed = sum(1 for r in results if r["status"])
    failed = total - passed

    html = """<!DOCTYPE html><html><head><meta charset="utf-8"><title>Test Report</title>
<style>body{font-family:sans-serif;margin:20px}
.pass{color:green}.fail{color:red}
table{border-collapse:collapse;width:100%}
td,th{border:1px solid #ccc;padding:8px;text-align:left}
</style></head><body>
<h1>S-Protect Encrypted Test Report</h1>
<table><tr><th>Test</th><th>Status</th><th>Detail</th></tr>"""
    
    md = "# S-Protect Encrypted Test Report\n\n| Test | Status | Detail |\n|------|--------|--------|\n"
    
    for r in results:
        status = "PASS" if r["status"] else "FAIL"
        cls = "pass" if r["status"] else "fail"
        html += f'<tr class="{cls}"><td>{r["name"]}</td><td>{status}</td><td>{r["detail"]}</td></tr>\n'
        md += f'| {r["name"]} | {status} | {r["detail"]} |\n'
    
    html += f'</table><br><strong>Total: {total} | Passed: {passed} | Failed: {failed}</strong></body></html>'
    md += f'\n**Total: {total} | Passed: {passed} | Failed: {failed}**\n'

    with open(os.path.join(base, "report.html"), "w", encoding="utf-8") as f:
        f.write(html)
    with open(os.path.join(base, "report.md"), "w", encoding="utf-8") as f:
        f.write(md)
    
    print(f"\nReport: {os.path.join(base, 'report.html')}")
