from __future__ import annotations

import json
import os
import re
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "raw"
WIKI_DIR = ROOT / "wiki"
DATA_DIR = ROOT / "data"


def openai_base_url() -> str:
    return os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")


def openai_model() -> str:
    return os.environ.get("OPENAI_MODEL", "gpt-4.1-mini")


def load_raw_documents() -> list[dict[str, str]]:
    if not RAW_DIR.exists():
        raise RuntimeError("raw 目录不存在，请先创建 raw 并放入 txt/md 文件")

    docs: list[dict[str, str]] = []
    for pattern in ("*.txt", "*.md"):
        for path in sorted(RAW_DIR.glob(pattern)):
            text = path.read_text(encoding="utf-8", errors="ignore").strip()
            if text:
                docs.append({"name": path.name, "text": text})

    if not docs:
        raise RuntimeError("raw 目录中没有可用文本文件，请放入 .txt 或 .md")
    return docs


def frontmatter(page: dict[str, object]) -> str:
    lines = ["---"]
    lines.append(f'title: "{page["title"]}"')
    lines.append(f'date: "{date.today().isoformat()}"')
    lines.append("tags:")
    for tag in page.get("tags", []):
        lines.append(f"  - {tag}")
    lines.append("related:")
    for related in page.get("related", []):
        lines.append(f"  - {related}")
    lines.append("---")
    return "\n".join(lines)


def slugify(title: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9\u4e00-\u9fff]+", "-", title).strip("-").lower()
    return slug or "untitled"


def build_prompt(raw_docs: list[dict[str, str]]) -> str:
    sections = []
    for doc in raw_docs:
        sections.append(f"[RAW:{doc['name']}]\n{doc['text']}")
    raw_content = "\n\n".join(sections)

    max_chars = int(os.environ.get("RAW_MAX_CHARS", "220000"))
    if len(raw_content) > max_chars:
        raw_content = raw_content[:max_chars]

    return (
        "你是知识库编译器。请读取原始资料并输出 JSON，不要输出任何解释。\n"
        "目标：生成至少10个页面，每个页面用于 Obsidian 双向链接。\n"
        "输出 JSON 格式必须是：\n"
        "{\n"
        '  "site_title": "...",\n'
        '  "pages": [\n'
        "    {\n"
        '      "title": "页面标题",\n'
        '      "summary": "一段概览",\n'
        '      "highlights": ["要点1", "要点2"],\n'
        '      "equations": ["公式或表达1"],\n'
        '      "questions": ["复习问题1"],\n'
        '      "tags": ["标签1"],\n'
        '      "related": ["其他页面标题A", "其他页面标题B"]\n'
        "    }\n"
        "  ]\n"
        "}\n"
        "要求：\n"
        "1) pages 数量 >= 10。\n"
        "2) related 必须引用 pages 中实际存在的标题。\n"
        "3) 内容主题聚焦电磁场与电磁波课程。\n"
        "4) 语言使用中文。\n\n"
        f"原始资料如下：\n\n{raw_content}"
    )


def call_llm(prompt: str) -> dict[str, object]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("未设置 OPENAI_API_KEY")

    payload = {
        "model": openai_model(),
        "temperature": 0.2,
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": "你是严谨的知识编译助手，只输出合法 JSON。"},
            {"role": "user", "content": prompt},
        ],
    }
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        f"{openai_base_url()}/chat/completions",
        data=data,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=240) as response:
            result = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"模型调用失败: HTTP {exc.code} {detail}") from exc

    content = result["choices"][0]["message"]["content"].strip()
    return json.loads(content)


def validate_payload(payload: dict[str, object]) -> list[dict[str, object]]:
    pages = payload.get("pages")
    if not isinstance(pages, list) or len(pages) < 10:
        raise RuntimeError("模型输出 pages 不足 10 篇，或格式不正确")

    titles = {str(page.get("title", "")).strip() for page in pages}
    if "" in titles:
        raise RuntimeError("存在空标题页面")

    for page in pages:
        related = page.get("related", [])
        if not isinstance(related, list):
            page["related"] = []
            continue
        page["related"] = [r for r in related if r in titles and r != page.get("title")]
    return pages


def write_wiki(payload: dict[str, object], pages: list[dict[str, object]]) -> None:
    site_title = str(payload.get("site_title", "长上下文知识库")).strip() or "长上下文知识库"
    WIKI_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    index_lines = [f"# {site_title}", "", "## 页面导航"]
    for page in pages:
        index_lines.append(f"- [[{page['title']}]]")
    index_lines.append("")
    index_lines.append("## 编译方式")
    index_lines.append("- 来源：raw 目录原始资料")
    index_lines.append("- 方法：长上下文模型自动编译")
    (WIKI_DIR / "index.md").write_text("\n".join(index_lines), encoding="utf-8")

    graph_nodes = [{"id": "index", "label": site_title, "type": "index"}]
    graph_edges = []

    for page in pages:
        title = str(page["title"])
        slug = slugify(title)
        tags = page.get("tags", []) if isinstance(page.get("tags"), list) else []
        highlights = page.get("highlights", []) if isinstance(page.get("highlights"), list) else []
        equations = page.get("equations", []) if isinstance(page.get("equations"), list) else []
        questions = page.get("questions", []) if isinstance(page.get("questions"), list) else []
        related = page.get("related", []) if isinstance(page.get("related"), list) else []

        fm = frontmatter({"title": title, "tags": tags, "related": related})
        body_lines = [f"# {title}", "", "## 概览", str(page.get("summary", "")), "", "## 核心要点"]
        for item in highlights:
            body_lines.append(f"- {item}")
        body_lines.extend(["", "## 常用表达"])
        for eq in equations:
            body_lines.append(f"- {eq}")
        body_lines.extend(["", "## 关联页面"])
        for rel in related:
            body_lines.append(f"- [[{rel}]]")
        body_lines.extend(["", "## 复习问题"])
        for q in questions:
            body_lines.append(f"- {q}")

        content = fm + "\n\n" + "\n".join(body_lines) + "\n"
        (WIKI_DIR / f"{slug}.md").write_text(content, encoding="utf-8")

        graph_nodes.append({"id": slug, "label": title, "type": "chapter"})
        graph_edges.append({"source": "index", "target": slug, "type": "contains"})
        for rel in related:
            graph_edges.append({"source": slug, "target": slugify(rel), "type": "related"})

    graph = {"site_title": site_title, "nodes": graph_nodes, "edges": graph_edges}
    (DATA_DIR / "graph.json").write_text(json.dumps(graph, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> int:
    raw_docs = load_raw_documents()
    prompt = build_prompt(raw_docs)
    payload = call_llm(prompt)
    pages = validate_payload(payload)
    write_wiki(payload, pages)
    print(f"LLM compile done. Generated {len(pages)} pages from raw/ into wiki/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
