from __future__ import annotations

import html
import re
from pathlib import Path

from kb_blueprint import CHAPTERS, SITE_TITLE


ROOT = Path(__file__).resolve().parents[1]
WIKI_DIR = ROOT / "wiki"
EXPORT_DIR = ROOT / "export"


def md_to_html(markdown_text: str) -> str:
    escaped = html.escape(markdown_text)
    escaped = re.sub(r"\[\[([^\]]+)\]\]", r"<a href='\1.html'>\1</a>", escaped)
    escaped = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"<a href='\2'>\1</a>", escaped)

    lines: list[str] = []
    in_list = False
    for raw_line in escaped.splitlines():
        line = raw_line.rstrip()
        if line.startswith("# "):
            if in_list:
                lines.append("</ul>")
                in_list = False
            lines.append(f"<h1>{line[2:]}</h1>")
        elif line.startswith("## "):
            if in_list:
                lines.append("</ul>")
                in_list = False
            lines.append(f"<h2>{line[3:]}</h2>")
        elif line.startswith("- "):
            if not in_list:
                lines.append("<ul>")
                in_list = True
            lines.append(f"<li>{line[2:]}</li>")
        elif not line:
            if in_list:
                lines.append("</ul>")
                in_list = False
            lines.append("<p></p>")
        else:
            if in_list:
                lines.append("</ul>")
                in_list = False
            lines.append(f"<p>{line}</p>")
    if in_list:
        lines.append("</ul>")
    return "\n".join(lines)


def wrap_page(title: str, body_html: str) -> str:
    return f"""<!doctype html>
<html lang='zh-CN'>
<head>
  <meta charset='utf-8'>
  <meta name='viewport' content='width=device-width, initial-scale=1'>
  <title>{html.escape(title)}</title>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Microsoft YaHei', sans-serif; max-width: 980px; margin: 0 auto; padding: 32px 20px; line-height: 1.7; background: #f7f5ef; color: #1f2328; }}
    a {{ color: #0b5cad; }}
    h1, h2 {{ line-height: 1.2; }}
    li {{ margin: 0.25rem 0; }}
    .card {{ background: white; border: 1px solid #ddd7c8; border-radius: 16px; padding: 24px; box-shadow: 0 12px 30px rgba(0,0,0,0.04); }}
    nav {{ margin-bottom: 20px; }}
  </style>
</head>
<body>
  <nav><a href='index.html'>返回索引</a></nav>
  <div class='card'>
{body_html}
  </div>
</body>
</html>"""


def main() -> int:
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    index_md = (WIKI_DIR / "index.md").read_text(encoding="utf-8")
    (EXPORT_DIR / "index.html").write_text(wrap_page(SITE_TITLE, md_to_html(index_md)), encoding="utf-8")

    for chapter in CHAPTERS:
        md_path = WIKI_DIR / f"{chapter['slug']}.md"
        html_path = EXPORT_DIR / f"{chapter['slug']}.html"
        html_path.write_text(wrap_page(chapter["title"], md_to_html(md_path.read_text(encoding="utf-8"))), encoding="utf-8")

    print(f"Exported {len(CHAPTERS) + 1} HTML pages to {EXPORT_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
