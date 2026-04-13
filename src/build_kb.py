from __future__ import annotations

import json
from datetime import date
from pathlib import Path

from kb_blueprint import CHAPTERS, SITE_TITLE, SOURCE_NOTE, SOURCE_PDF


ROOT = Path(__file__).resolve().parents[1]
WIKI_DIR = ROOT / "wiki"
DATA_DIR = ROOT / "data"
EXPORT_DIR = ROOT / "export"


def slug_to_title_map() -> dict[str, str]:
    return {chapter["slug"]: chapter["title"] for chapter in CHAPTERS}


def frontmatter(chapter: dict[str, object]) -> str:
    related_titles = [slug_to_title_map()[slug] for slug in chapter["related"]]
    lines = ["---"]
    lines.append(f'title: "{chapter["title"]}"')
    lines.append(f'chapter: "{chapter["chapter"]}"')
    lines.append(f'slug: "{chapter["slug"]}"')
    lines.append(f'source: "{SOURCE_PDF}"')
    lines.append(f'date: "{date.today().isoformat()}"')
    lines.append("tags:")
    for tag in chapter["tags"]:
        lines.append(f"  - {tag}")
    lines.append("related:")
    for title in related_titles:
        lines.append(f"  - {title}")
    lines.append("---")
    return "\n".join(lines)


def page_body(chapter: dict[str, object]) -> str:
    related_titles = [slug_to_title_map()[slug] for slug in chapter["related"]]
    lines = [f"# {chapter['title']}"]
    lines.append("")
    lines.append("## 概览")
    lines.append(chapter["summary"])
    lines.append("")
    lines.append("## 核心要点")
    for item in chapter["highlights"]:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("## 常用表达")
    for equation in chapter["equations"]:
        lines.append(f"- {equation}")
    lines.append("")
    lines.append("## 关联页面")
    for title in related_titles:
        lines.append(f"- [[{title}]]")
    lines.append("")
    lines.append("## 复习问题")
    for question in chapter["questions"]:
        lines.append(f"- {question}")
    lines.append("")
    lines.append("## 学习提示")
    lines.append("这部分内容适合结合典型例题一起看。先抓住物理意义，再把公式和边界条件串起来。")
    return "\n".join(lines)


def index_page() -> str:
    lines = [f"# {SITE_TITLE}", ""]
    lines.append("## 项目目标")
    lines.append("- 以 Markdown 作为唯一存储格式。")
    lines.append("- 通过长上下文模型直接阅读完整 wiki，而不是做向量检索。")
    lines.append("- 保持 Obsidian 可读、可视化、可维护。")
    lines.append("")
    lines.append("## 来源资料")
    lines.append(f"- {SOURCE_PDF}")
    lines.append(f"- {SOURCE_NOTE}")
    lines.append("")
    lines.append("## 页面导航")
    for chapter in CHAPTERS:
        lines.append(f"- [[{chapter['title']}]]")
    lines.append("")
    lines.append("## 使用方式")
    lines.append("1. 先看索引页，再按章节顺序浏览。")
    lines.append("2. 问答时把整个 wiki 作为上下文输入长上下文模型。")
    lines.append("3. 通过链接和图谱检查知识结构是否合理。")
    return "\n".join(lines)


def build_graph() -> dict[str, object]:
    nodes = [{"id": "index", "label": SITE_TITLE, "type": "index"}]
    edges = []
    for chapter in CHAPTERS:
        nodes.append({"id": chapter["slug"], "label": chapter["title"], "type": "chapter"})
        edges.append({"source": "index", "target": chapter["slug"], "type": "contains"})
        for related in chapter["related"]:
            edges.append({"source": chapter["slug"], "target": related, "type": "related"})
    return {"site_title": SITE_TITLE, "nodes": nodes, "edges": edges}


def write_pages() -> None:
    WIKI_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)

    (WIKI_DIR / "index.md").write_text(index_page(), encoding="utf-8")
    for chapter in CHAPTERS:
        path = WIKI_DIR / f"{chapter['slug']}.md"
        content = frontmatter(chapter) + "\n\n" + page_body(chapter) + "\n"
        path.write_text(content, encoding="utf-8")

    graph = build_graph()
    (DATA_DIR / "graph.json").write_text(json.dumps(graph, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    write_pages()
    print(f"Generated {len(CHAPTERS)} chapter pages in {WIKI_DIR}")
