# raw 目录说明

把原始资料放在这里（建议 `.txt` 或 `.md`）。

示例：
- textbook_notes.txt
- chapter_1.md

然后运行：
python src/compile_raw_llm.py

脚本会调用长上下文模型，自动生成 wiki 页面到 `wiki/`。
