# 2pdf

[中文](./README_zh.md) | **English**

[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-green?style=flat-square)](https://docs.openclaw.ai/skills/)
[![Claude Code Compatible](https://img.shields.io/badge/Claude%20Code-Compatible-orange?style=flat-square)](https://docs.anthropic.com/en/docs/claude-code)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)

An AI agent skill that converts `.docx`, `.pptx`, `.md` files to PDF. Works with OpenClaw, Claude Code, Codex, and any agent that supports the `SKILL.md` standard.

Just tell your agent: *"Convert this file to PDF"* — it handles the rest.

## Install

### OpenClaw

```bash
git clone https://github.com/Eric-Zhou-0302/2pdf ~/.openclaw/skills/2pdf
```

### Claude Code

```bash
git clone https://github.com/Eric-Zhou-0302/2pdf ~/.claude/skills/2pdf
```

### Manual

Clone this repo into any `skills/` directory your agent reads from.

### Prerequisites

- **Python 3.10+**
- **LibreOffice** — `brew install --cask libreoffice` (macOS) / `sudo apt install libreoffice-core` (Linux)
- **markdown** — `pip install markdown` (for .md files only)

## How to use

Once installed, just talk to your agent naturally:

> *"Convert the lecture slides to PDF"*
> *"Turn my notes.md into a PDF"*
> *"Export all .docx files in this folder to PDF"*

The agent reads the skill, picks the right conversion path, and outputs PDFs beside the original files — same name, `.pdf` extension.

## What it does

| Format | Method | Output |
|--------|--------|--------|
| `.docx` | LibreOffice headless | Exact formatting preserved |
| `.pptx` | LibreOffice headless | One page per slide |
| `.md` | markdown → HTML → LibreOffice | GitHub-flavored styling |

All rendering goes through LibreOffice. Markdown files get converted to HTML with embedded GitHub-style CSS (tables, code blocks, blockquotes) before PDF rendering.

## How it works

The skill contains a single Python script (`scripts/convert.py`) that:

1. Detects file format from extension
2. For `.docx` / `.pptx`: calls `soffice --headless --convert-to pdf`
3. For `.md`: converts to HTML via the `markdown` library, embeds GitHub CSS, then passes to LibreOffice
4. Outputs the PDF to the same directory with the same filename

Your agent reads `SKILL.md` to know when and how to invoke this.

## Project structure

```
2pdf/
├── SKILL.md              # Skill definition (what the agent reads)
├── README.md             # English
├── README_zh.md          # 中文
├── scripts/
│   └── convert.py        # Conversion script
└── assets/
    └── github.css        # GitHub-flavored CSS for Markdown
```

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `LibreOffice not found` | `brew install --cask libreoffice` |
| Chinese chars garbled | System fonts required (STHeiti / PingFang) |
| Conversion timeout | `pkill soffice` and retry |

## License

[MIT](LICENSE)
