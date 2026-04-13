from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WIKI_DIR = ROOT / "wiki"


def load_pages() -> list[dict[str, str]]:
    pages: list[dict[str, str]] = []
    for path in sorted(WIKI_DIR.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        title_match = re.search(r"^#\s+(.+)$", text, re.M)
        title = title_match.group(1).strip() if title_match else path.stem
        pages.append({"title": title, "path": path.name, "text": text})
    return pages


def strip_frontmatter(text: str) -> str:
    if not text.startswith("---\n"):
        return text.strip()
    parts = text.split("---", 2)
    if len(parts) < 3:
        return text.strip()
    return parts[2].strip()


def build_context(pages: list[dict[str, str]]) -> str:
    blocks = []
    for page in pages:
        blocks.append(f"[PAGE] {page['title']} ({page['path']})\n{strip_frontmatter(page['text'])}")
    return "\n\n".join(blocks)


def openai_base_url() -> str:
    base_url = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
    return base_url.rstrip("/")


def openai_model() -> str:
    return os.environ.get("OPENAI_MODEL", "gpt-4.1-mini")


def chat_with_openai(question: str, context: str) -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY 未设置")

    payload = {
        "model": openai_model(),
        "temperature": 0.2,
        "messages": [
            {
                "role": "system",
                "content": (
                    "你是一个基于 Markdown 知识库回答问题的教学助手。"
                    "只能依据提供的知识库内容回答，不要编造。"
                    "回答时尽量给出简洁结论，并在末尾列出引用到的页面标题，格式为 [[页面标题]]。"
                ),
            },
            {
                "role": "user",
                "content": (
                    f"知识库内容如下：\n\n{context}\n\n"
                    f"用户问题：{question}\n\n"
                    "请基于知识库直接回答。如果知识库不足以支持结论，请明确说明不足。"
                ),
            },
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
    with urllib.request.urlopen(request, timeout=120) as response:
        result = json.loads(response.read().decode("utf-8"))
    return result["choices"][0]["message"]["content"].strip()


def tokenize(text: str) -> list[str]:
    tokens: list[str] = []
    for chunk in re.findall(r"[\u4e00-\u9fff]+|[A-Za-z0-9_]+", text.lower()):
        if re.fullmatch(r"[\u4e00-\u9fff]+", chunk):
            tokens.extend(chunk)
        else:
            tokens.append(chunk)
    return tokens


def local_answer(question: str, pages: list[dict[str, str]]) -> str:
    query_tokens = tokenize(question)
    query_counter = Counter(query_tokens)
    scored: list[tuple[int, dict[str, str]]] = []
    for page in pages:
        text = strip_frontmatter(page["text"])
        page_tokens = Counter(tokenize(text))
        score = sum(min(query_counter[token], page_tokens[token]) for token in query_counter)
        scored.append((score, page))

    scored.sort(key=lambda item: (item[0], len(item[1]["text"])), reverse=True)
    top_pages = [page for score, page in scored[:3] if score > 0]
    if not top_pages:
        top_pages = [pages[0]] if pages else []

    if not top_pages:
        return "知识库为空，无法回答。"

    lines = ["本地模式回答：当前未配置 OPENAI_API_KEY，因此使用页面匹配结果给出参考答案。", ""]
    lines.append(f"问题：{question}")
    lines.append("")
    lines.append("参考页面：")
    for page in top_pages:
        lines.append(f"- [[{page['title']}]]")
    lines.append("")
    lines.append("综合判断：")
    lines.append(
        "这个问题可以从上述页面的摘要、核心要点和公式部分拼接理解。"
        "如果你提供 OpenAI 兼容模型，本脚本会把整个 wiki 直接送进长上下文模型，由模型生成更完整的答案。"
    )
    lines.append("")
    for page in top_pages:
        excerpt = strip_frontmatter(page["text"])
        excerpt = re.sub(r"\n{3,}", "\n\n", excerpt)
        lines.append(f"### {page['title']}")
        lines.append("```text")
        lines.append(excerpt[:800])
        lines.append("```")
        lines.append("")
    return "\n".join(lines).strip()


def answer(question: str) -> str:
    pages = load_pages()
    context = build_context(pages)
    try:
        return chat_with_openai(question, context)
    except Exception as exc:
        fallback = local_answer(question, pages)
        return fallback + f"\n\n[提示] 外部模型调用失败：{exc}"


def interactive() -> int:
    print("进入问答模式，直接输入问题，回车后回答。输入 exit 退出。")
    while True:
        try:
            question = input("\n问题> ").strip()
        except EOFError:
            break
        if not question:
            continue
        if question.lower() in {"exit", "quit", "q"}:
            break
        print("\n" + answer(question) + "\n")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="基于 wiki 的长上下文问答")
    parser.add_argument("question", nargs="*", help="要回答的问题")
    parser.add_argument("-i", "--interactive", action="store_true", help="进入交互式问答")
    args = parser.parse_args()

    if args.interactive:
        return interactive()

    question = " ".join(args.question).strip()
    if not question:
        parser.error("请提供一个问题，或使用 --interactive")
    print(answer(question))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
