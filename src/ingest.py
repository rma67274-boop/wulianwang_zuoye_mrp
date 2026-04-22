from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    import pdfplumber
except ImportError:
    pdfplumber = None

try:
    from PIL import Image
    import pytesseract
except ImportError:
    Image = pytesseract = None


ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "raw"


def ingest_pdf(pdf_path: str, output_name: str | None = None) -> str:
    """Extract text from PDF and save as Markdown."""
    if not pdfplumber:
        raise RuntimeError(
            "pdfplumber 未安装。运行：pip install pdfplumber"
        )

    pdf_file = Path(pdf_path)
    if not pdf_file.exists():
        raise FileNotFoundError(f"PDF 文件不存在: {pdf_path}")

    if not output_name:
        output_name = pdf_file.stem + ".md"

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    output_path = RAW_DIR / output_name

    text_content = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages, 1):
            text = page.extract_text()
            if text:
                text_content.append(f"# 第 {i} 页\n\n{text}")

    full_text = "\n\n".join(text_content)
    output_path.write_text(full_text, encoding="utf-8")
    print(f"[Ingest] PDF 已导入: {output_path}")
    return str(output_path)


def ingest_image_ocr(image_path: str, output_name: str | None = None) -> str:
    """Extract text from image using OCR."""
    if not Image or not pytesseract:
        raise RuntimeError(
            "pytesseract 和 Pillow 未安装。运行：pip install pytesseract pillow\n"
            "并确保系统已安装 tesseract-ocr（https://github.com/UB-Mannheim/tesseract/wiki）"
        )

    image_file = Path(image_path)
    if not image_file.exists():
        raise FileNotFoundError(f"图片文件不存在: {image_path}")

    if not output_name:
        output_name = image_file.stem + ".md"

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    output_path = RAW_DIR / output_name

    img = Image.open(image_path)
    text = pytesseract.image_to_string(img, lang="chi_sim+eng")
    output_path.write_text(text, encoding="utf-8")
    print(f"[Ingest] 图片 OCR 已导入: {output_path}")
    return str(output_path)


def ingest_markdown(markdown_path: str, output_name: str | None = None) -> str:
    """Copy Markdown file to raw directory."""
    md_file = Path(markdown_path)
    if not md_file.exists():
        raise FileNotFoundError(f"Markdown 文件不存在: {markdown_path}")

    if not output_name:
        output_name = md_file.name

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    output_path = RAW_DIR / output_name

    content = md_file.read_text(encoding="utf-8")
    output_path.write_text(content, encoding="utf-8")
    print(f"[Ingest] Markdown 已导入: {output_path}")
    return str(output_path)


def main() -> int:
    parser = argparse.ArgumentParser(description="将各种格式文档导入到 raw/ 目录")
    parser.add_argument("file", help="输入文件路径（PDF/图片/Markdown）")
    parser.add_argument("-o", "--output", help="输出文件名（默认为原文件名）")
    parser.add_argument("-t", "--type", choices=["pdf", "ocr", "md"], help="文件类型（自动检测如果不指定）")

    args = parser.parse_args()
    input_file = Path(args.file)

    if not input_file.exists():
        print(f"错误：文件不存在 {args.file}", file=sys.stderr)
        return 1

    file_type = args.type
    if not file_type:
        suffix = input_file.suffix.lower()
        if suffix == ".pdf":
            file_type = "pdf"
        elif suffix in {".png", ".jpg", ".jpeg", ".bmp", ".gif"}:
            file_type = "ocr"
        elif suffix == ".md":
            file_type = "md"
        else:
            print(f"错误：无法识别文件类型 {suffix}，请用 -t 指定", file=sys.stderr)
            return 1

    try:
        if file_type == "pdf":
            ingest_pdf(args.file, args.output)
        elif file_type == "ocr":
            ingest_image_ocr(args.file, args.output)
        elif file_type == "md":
            ingest_markdown(args.file, args.output)
        return 0
    except Exception as exc:
        print(f"错误：{exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
