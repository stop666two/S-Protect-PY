#!/usr/bin/env python3
import sys
import os
from tester import run_all_tests
from reporter import print_report, generate_html, generate_markdown


def main():
    print("=" * 60)
    print("       Python 环境测试工具")
    print("  github.com/stop666two/py-running-text")
    print("=" * 60)
    print()

    categories = run_all_tests()

    print_report(categories)

    base_dir = os.path.dirname(os.path.abspath(__file__))

    html_path = os.path.join(base_dir, "report.html")
    generate_html(categories, html_path)
    print(f"HTML 报告已保存: {html_path}")

    md_path = os.path.join(base_dir, "report.md")
    generate_markdown(categories, md_path)
    print(f"Markdown 报告已保存: {md_path}")
    print()


if __name__ == "__main__":
    main()
