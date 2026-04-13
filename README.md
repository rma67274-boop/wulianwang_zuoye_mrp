# 电磁场与电磁波长上下文知识库

这是一个按 Karpathy 风格整理的长上下文知识库项目，资料来源是当前目录中的《电磁场与电磁波教学指导书》第 4 版 PDF。

项目目标：

- 以 Markdown 作为唯一知识存储格式。
- 不使用向量数据库，不做传统 RAG。
- 将教材主题整理成可在 Obsidian 中直接打开、双向链接清晰的 wiki 页面。
- 提供知识图谱数据、链接检查和 HTML 导出。

## 目录说明

- `src/`：生成、校验、导出脚本。
- `wiki/`：生成后的知识库页面。
- `data/`：图谱与清单数据。
- `export/`：HTML 导出结果。
- `reports/`：实验报告。

## 运行方式

1. 生成知识库：`python src/build_kb.py`
2. 检查链接：`python src/lint_kb.py`
3. 导出 HTML：`python src/export_html.py`
4. 问答：`python src/qa.py "高斯定律和静电场有什么关系"`
5. 交互式问答：`python src/qa.py --interactive`
6. 自动编译（LLM 读取 raw）：`python src/compile_raw_llm.py`

## 问答功能

问答脚本默认把 `wiki/` 目录中的全部页面拼成长上下文，然后尝试调用 OpenAI 兼容接口。

你可以通过下面这些环境变量接入模型：

- `OPENAI_API_KEY`：模型 API Key
- `OPENAI_BASE_URL`：OpenAI 兼容接口地址，默认 `https://api.openai.com/v1`
- `OPENAI_MODEL`：模型名，默认 `gpt-4.1-mini`

如果没有配置外部模型，脚本会自动退化成本地模式，根据页面关键词匹配给出参考答案和相关页面，至少可以用于演示和调试。

## LLM 自动编译 raw

这个流程用于满足“LLM 自动读取 raw 后编译”的要求。

1. 在项目根目录创建 `raw/`，放入教材文本（`.txt` 或 `.md`）。
2. 配置模型环境变量：
	- `OPENAI_API_KEY`
	- `OPENAI_BASE_URL`（可选，默认 `https://api.openai.com/v1`）
	- `OPENAI_MODEL`（可选）
3. 运行：`python src/compile_raw_llm.py`
4. 结果会自动写入 `wiki/` 与 `data/graph.json`。

## 说明

由于原始 PDF 是扫描版，自动抽取文本效果有限，所以本项目采用“教材结构 + 人工编译”的方式完成知识库。这样更符合课程要求里的 Karpathy 方案：重点是把知识整理成结构化 Markdown，并保持页面之间的链接和可维护性。
