# 2pdf

[中文](./README_zh.md) | **English**

A lightweight document-to-PDF converter powered by LibreOffice headless. Converts `.docx`, `.pptx`, and `.md` files to PDF with a single command.

## Features

- **docx → PDF** — Full formatting preserved (tables, images, styles)
- **pptx → PDF** — One PDF page per slide, layout intact
- **md → PDF** — GitHub-flavored styling with code highlighting and tables
- **Zero config** — Same directory, same filename, `.pdf` extension
- **Batch friendly** — Easily scriptable for bulk conversion

## Requirements

| Dependency | Purpose | Install |
|------------|---------|---------|
| Python 3.10+ | Runtime | — |
| LibreOffice | Rendering engine | `brew install --cask libreoffice` |
| markdown | Markdown parsing | `pip install markdown` |

## Quick Start

```bash
# Single file
python scripts/convert.py report.docx

# Custom output path
python scripts/convert.py slides.pptx output/slides.pdf

# Batch convert a directory
for f in /path/to/*.docx /path/to/*.pptx /path/to/*.md; do
  python scripts/convert.py "$f"
done
```

## How It Works

```
docx ──→ LibreOffice headless ──→ PDF
pptx ──→ LibreOffice headless ──→ PDF
md   ──→ markdown → HTML (+ GitHub CSS) → LibreOffice ──→ PDF
```

All three formats go through LibreOffice's rendering engine, ensuring high-fidelity output. For Markdown files, the content is first converted to HTML with GitHub-flavored styling (tables, code blocks, blockquotes, etc.), then rendered to PDF.

## Programmatic Use

```python
from scripts.convert import convert

# Default: same directory, same name, .pdf extension
result = convert("/path/to/file.md")
# → "/path/to/file.pdf"

# Custom output path
result = convert("/path/to/file.docx", "/tmp/output.pdf")
```

## Project Structure

```
2pdf/
├── SKILL.md              # OpenClaw skill definition
├── README.md             # English documentation
├── README_zh.md          # 中文文档
├── scripts/
│   └── convert.py        # Core conversion script
└── assets/
    └── github.css        # GitHub-flavored CSS for Markdown rendering
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `LibreOffice not found` | Install LibreOffice: `brew install --cask libreoffice` |
| Chinese characters garbled | Ensure system fonts are available (STHeiti, PingFang) |
| Conversion timeout | Kill stuck processes: `pkill soffice` |
| Output PDF is empty | Check LibreOffice version: `soffice --version` |

## License

MIT
