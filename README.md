# 2pdf

[中文](./README_zh.md) | **English**

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)
[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-green?style=flat-square)](https://docs.openclaw.ai/skills/)

Convert `.docx`, `.pptx`, `.md` files to PDF — one command, same directory, same filename.

Powered by [LibreOffice](https://www.libreoffice.org/) headless for high-fidelity rendering. Markdown files use GitHub-flavored styling.

## Install

```bash
# Clone into your OpenClaw skills directory
git clone https://github.com/Eric-Zhou-0302/2pdf ~/.openclaw/skills/2pdf

# Install the only Python dependency (for .md conversion)
pip install markdown
```

**Prerequisite:** [LibreOffice](https://www.libreoffice.org/) must be installed.

```bash
brew install --cask libreoffice          # macOS
sudo apt install libreoffice-core        # Ubuntu/Debian
```

## Usage

```bash
python ~/.openclaw/skills/2pdf/scripts/convert.py <file>
```

| Input | Output | Engine |
|-------|--------|--------|
| `report.docx` | `report.pdf` | LibreOffice |
| `slides.pptx` | `slides.pdf` | LibreOffice |
| `notes.md` | `notes.pdf` | markdown → HTML → LibreOffice |

### Custom output path

```bash
python ~/.openclaw/skills/2pdf/scripts/convert.py input.docx /tmp/output.pdf
```

### Batch convert

```bash
for f in /path/to/*.docx /path/to/*.pptx /path/to/*.md; do
  python ~/.openclaw/skills/2pdf/scripts/convert.py "$f"
done
```

### Python API

```python
from scripts.convert import convert

convert("/path/to/file.md")                    # → /path/to/file.pdf
convert("/path/to/file.docx", "/tmp/out.pdf")  # custom output
```

## How it works

```
docx ──→ soffice --headless --convert-to pdf ──→ PDF
pptx ──→ soffice --headless --convert-to pdf ──→ PDF
md   ──→ markdown → HTML (+ CSS) → soffice    ──→ PDF
```

All three formats render through LibreOffice. For Markdown, content is first converted to HTML with embedded GitHub-style CSS (tables, code blocks, blockquotes, lists), then handed to LibreOffice for PDF rendering.

## Project structure

```
2pdf/
├── SKILL.md              # OpenClaw skill definition
├── README.md             # English
├── README_zh.md          # 中文
├── scripts/
│   └── convert.py        # Conversion script
└── assets/
    └── github.css        # GitHub-flavored CSS
```

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `LibreOffice not found` | `brew install --cask libreoffice` |
| Chinese chars garbled | System fonts required (STHeiti / PingFang) |
| Conversion timeout | `pkill soffice` and retry |
| Empty PDF output | `soffice --version` to verify installation |

## License

[MIT](LICENSE)
