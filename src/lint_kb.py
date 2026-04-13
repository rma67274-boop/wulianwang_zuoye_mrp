from __future__ import annotations

import re
from pathlib import Path

from kb_blueprint import CHAPTERS


ROOT = Path(__file__).resolve().parents[1]
WIKI_DIR = ROOT / "wiki"


def page_titles() -> set[str]:
    titles = {"电磁场与电磁波长上下文知识库"}
    titles.update(chapter["title"] for chapter in CHAPTERS)
    return titles


def find_links(text: str) -> set[str]:
    links = set(re.findall(r"\[\[([^\]]+)\]\]", text))
    links.update(re.findall(r"\[[^\]]+\]\(([^)]+\.md)\)", text))
    return links


def main() -> int:
    issues: list[str] = []
    expected = page_titles()
    md_files = sorted(WIKI_DIR.glob("*.md"))
    if len(md_files) < 10:
        issues.append(f"wiki 页面数量不足：当前只有 {len(md_files)} 个 markdown 文件")

    existing_titles = {path.stem for path in md_files}
    for path in md_files:
        text = path.read_text(encoding="utf-8")
        for link in find_links(text):
            if link.endswith(".md"):
                target = Path(link).stem
                if target not in existing_titles:
                    issues.append(f"{path.name} 引用了不存在的页面文件 {link}")
            elif link not in expected:
                issues.append(f"{path.name} 引用了未知标题 [[{link}]]")

        if text.count("---") == 1:
            issues.append(f"{path.name} 的 frontmatter 可能不完整")

    if issues:
        print("Lint failed:")
        for issue in issues:
            print(f"- {issue}")
        return 1

    print(f"Lint passed for {len(md_files)} pages.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
