from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

try:
    import markdown
except ImportError:
    markdown = None


ROOT = Path(__file__).resolve().parents[1]
WIKI_DIR = ROOT / "wiki"
EXPORT_DIR = ROOT / "export"


def export_markdown_to_html(wiki_file: Path, output_file: Path) -> None:
    """Convert Markdown to HTML."""
    if not markdown:
        raise RuntimeError("markdown 包未安装。运行：pip install markdown")

    content = wiki_file.read_text(encoding="utf-8")
    html_body = markdown.markdown(content, extensions=["tables", "fenced_code", "codehilite"])

    html_template = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{wiki_file.stem}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; margin: 40px auto; max-width: 900px; line-height: 1.6; color: #333; }}
        h1 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
        h2 {{ color: #34495e; margin-top: 30px; }}
        code {{ background: #f4f4f4; padding: 2px 6px; border-radius: 3px; font-family: "Monaco", "Courier New", monospace; }}
        pre {{ background: #f4f4f4; padding: 12px; border-radius: 5px; overflow-x: auto; }}
        table {{ border-collapse: collapse; width: 100%; }}
        table, th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
        th {{ background-color: #3498db; color: white; }}
        a {{ color: #3498db; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    {html_body}
</body>
</html>"""

    output_file.write_text(html_template, encoding="utf-8")
    print(f"[Export] HTML 已生成: {output_file}")


def export_markdown_to_pdf(wiki_file: Path, output_file: Path) -> None:
    """Convert Markdown to PDF using pandoc."""
    if not Path("pandoc").exists() and not Path("pandoc.exe").exists():
        raise RuntimeError(
            "pandoc 未安装。访问 https://pandoc.org/installing.html 安装，或使用 HTML 导出。"
        )

    try:
        subprocess.run(
            [
                "pandoc",
                str(wiki_file),
                "-o", str(output_file),
                "--pdf-engine=xelatex",
                "-V", "lang=zh",
                "-V", "documentclass=ctexart",
            ],
            check=True,
            capture_output=True,
        )
        print(f"[Export] PDF 已生成: {output_file}")
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(f"PDF 生成失败: {exc.stderr.decode('utf-8', errors='ignore')}")


def export_wiki(format: str = "html") -> int:
    """Export all wiki pages to specified format."""
    if not WIKI_DIR.exists():
        print("错误：wiki 目录不存在，请先运行编译", file=sys.stderr)
        return 1

    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    format = format.lower()

    if format not in {"html", "pdf"}:
        print(f"错误：不支持的格式 {format}，使用 html 或 pdf", file=sys.stderr)
        return 1

    suffix = ".html" if format == "html" else ".pdf"
    count = 0

    for md_file in sorted(WIKI_DIR.glob("*.md")):
        output_file = EXPORT_DIR / f"{md_file.stem}{suffix}"

        try:
            if format == "html":
                export_markdown_to_html(md_file, output_file)
            else:
                export_markdown_to_pdf(md_file, output_file)
            count += 1
        except Exception as exc:
            print(f"警告：{md_file.name} 导出失败：{exc}", file=sys.stderr)

    print(f"\n成功导出 {count} 个文件到 {EXPORT_DIR}/")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="将 wiki 文件导出为 HTML 或 PDF")
    parser.add_argument(
        "-f", "--format",
        choices=["html", "pdf"],
        default="html",
        help="导出格式（默认 html）"
    )
    args = parser.parse_args()

    return export_wiki(args.format)


if __name__ == "__main__":
    raise SystemExit(main())
