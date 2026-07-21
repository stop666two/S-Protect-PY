import os
from datetime import datetime
from colorama import init, Fore, Back, Style

init(autoreset=True)


def _is_normal(r):
    expect_pass = r.get("expect", "pass") == "pass"
    return r["status"] == expect_pass


def _calc_stats(categories):
    total = sum(len(c["results"]) for c in categories)
    normal = sum(1 for c in categories for r in c["results"] if _is_normal(r))
    abnormal = total - normal
    return total, normal, abnormal


def _get_abnormal_items(categories):
    items = []
    for cat in categories:
        for r in cat["results"]:
            if not _is_normal(r):
                items.append((cat["name"], r))
    return items


def print_report(categories):
    total, normal, abnormal = _calc_stats(categories)
    verdict = "正常" if abnormal == 0 else "异常"

    print()
    print(Fore.CYAN + Style.BRIGHT + "=" * 60)
    print(Fore.CYAN + Style.BRIGHT + "         Python 环境测试报告")
    print(Fore.CYAN + Style.BRIGHT + "=" * 60)
    print()

    for cat in categories:
        print(Fore.YELLOW + Style.BRIGHT + f"【{cat['name']}】")
        print(Fore.YELLOW + "-" * 50)
        for r in cat["results"]:
            expect_pass = r.get("expect", "pass") == "pass"
            is_normal = _is_normal(r)

            if is_normal:
                if expect_pass:
                    icon = Fore.GREEN + "PASS"
                    status_text = Fore.GREEN + "通过"
                else:
                    icon = Fore.WHITE + "SKIP"
                    status_text = Fore.WHITE + "预期失败"
            else:
                if expect_pass:
                    icon = Fore.RED + "FAIL"
                    status_text = Fore.RED + "异常失败"
                else:
                    icon = Fore.YELLOW + "ALRT"
                    status_text = Fore.YELLOW + "异常通过"

            expect_label = "预期通过" if expect_pass else "预期失败"
            print(f"  {icon} {r['name']:<30} {status_text}")
            print(f"    {Fore.WHITE}信息: {r['detail']} ({expect_label})")
        print()

    print(Fore.CYAN + Style.BRIGHT + "=" * 60)
    norm_color = Fore.GREEN if abnormal == 0 else Fore.RED
    print(f"  {Fore.WHITE}总计: {total}  |  "
          f"{Fore.GREEN}正常: {normal}  |  "
          f"{norm_color}异常: {abnormal}")
    verdict_color = Fore.GREEN if abnormal == 0 else Fore.RED
    print(f"  {verdict_color}{Style.BRIGHT}判定: {verdict}")
    print(Fore.CYAN + Style.BRIGHT + "=" * 60)

    if abnormal > 0:
        print()
        print(Fore.RED + Style.BRIGHT + "异常项目明细:")
        print(Fore.RED + "-" * 50)
        for cat_name, r in _get_abnormal_items(categories):
            expect_pass = r.get("expect", "pass") == "pass"
            if expect_pass:
                label = "预期通过但失败"
                color = Fore.RED
            else:
                label = "预期失败但通过"
                color = Fore.YELLOW
            print(f"  {color}[{label}] {cat_name} > {r['name']} | {r['detail']}")
        print()

    print()


def generate_html(categories, path):
    total, normal, abnormal = _calc_stats(categories)
    verdict = "正常" if abnormal == 0 else "异常"

    rows = ""
    for cat in categories:
        rows += f"<tr><td colspan='4' style='background:#f0f0f0;font-weight:bold'>{cat['name']}</td></tr>\n"
        for r in cat["results"]:
            is_normal = _is_normal(r)
            expect_pass = r.get("expect", "pass") == "pass"

            if is_normal and expect_pass:
                status_color = "#4caf50"
                status_text = "通过"
            elif is_normal and not expect_pass:
                status_color = "#9e9e9e"
                status_text = "预期失败"
            elif not is_normal and expect_pass:
                status_color = "#f44336"
                status_text = "异常失败"
            else:
                status_color = "#ff9800"
                status_text = "异常通过"

            expect_label = "预期通过" if expect_pass else "预期失败"
            rows += f"<tr><td>{r['name']}</td><td style='color:{status_color}'>{status_text}</td><td>{r['detail']}</td><td>{expect_label}</td></tr>\n"

    overall_color = "#4caf50" if abnormal == 0 else "#f44336"
    overview_text = f"正常: {normal} | 异常: {abnormal}"

    abnormal_rows = ""
    if abnormal > 0:
        abnormal_rows = '<tr><th colspan="4" style="background:#ffebee;color:#c62828">异常项目明细</th></tr>\n'
        for cat_name, r in _get_abnormal_items(categories):
            expect_pass = r.get("expect", "pass") == "pass"
            label = "预期通过但失败" if expect_pass else "预期失败但通过"
            abnormal_rows += f"<tr style='background:#fff3e0'><td colspan='4'>{cat_name} &gt; {r['name']}: {label} | {r['detail']}</td></tr>\n"

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>Python 环境测试报告</title>
<style>
body {{ font-family: -apple-system, 'Segoe UI', sans-serif; max-width: 900px; margin: 40px auto; padding: 0 20px; }}
h1 {{ text-align: center; color: #333; }}
table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
th, td {{ padding: 10px 12px; text-align: left; border-bottom: 1px solid #ddd; }}
th {{ background: #333; color: #fff; }}
.summary {{ text-align: center; font-size: 1.2em; padding: 20px; background: {overall_color}; color: #fff; border-radius: 8px; }}
.timestamp {{ text-align: center; color: #999; font-size: 0.9em; }}
.verdict {{ font-size: 1.4em; font-weight: bold; }}
</style>
</head>
<body>
<h1>Python 环境测试报告</h1>
<p class="timestamp">生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
<table>
<thead><tr><th>测试项</th><th>状态</th><th>详细信息</th><th>预期</th></tr></thead>
<tbody>
{rows}
</tbody>
</table>
<table>
{abnormal_rows}
</table>
<div class="summary">
<p>{overview_text}</p>
<p class="verdict">判定: {verdict}</p>
</div>
</body>
</html>"""

    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    return path


def generate_markdown(categories, path):
    total, normal, abnormal = _calc_stats(categories)
    verdict = "正常" if abnormal == 0 else "异常"

    lines = []
    lines.append("# Python 环境测试报告")
    lines.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")
    lines.append(f"**判定: {verdict}** | 总计: {total} | 正常: {normal} | 异常: {abnormal}")
    lines.append("")

    for cat in categories:
        lines.append(f"## {cat['name']}")
        lines.append("| 测试项 | 状态 | 详细信息 | 预期 |")
        lines.append("| ------ | ---- | -------- | ---- |")
        for r in cat["results"]:
            is_normal = _is_normal(r)
            expect_pass = r.get("expect", "pass") == "pass"

            if is_normal and expect_pass:
                status_text = "通过"
            elif is_normal and not expect_pass:
                status_text = "预期失败"
            elif not is_normal and expect_pass:
                status_text = "异常失败"
            else:
                status_text = "异常通过"

            expect_label = "预期通过" if expect_pass else "预期失败"
            lines.append(f"| {r['name']} | {status_text} | {r['detail']} | {expect_label} |")
        lines.append("")

    if abnormal > 0:
        lines.append("---")
        lines.append("## 异常项目明细")
        for cat_name, r in _get_abnormal_items(categories):
            expect_pass = r.get("expect", "pass") == "pass"
            label = "预期通过但失败" if expect_pass else "预期失败但通过"
            lines.append(f"- **[{label}]** {cat_name} > {r['name']}: {r['detail']}")
        lines.append("")

    content = "\n".join(lines)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path
