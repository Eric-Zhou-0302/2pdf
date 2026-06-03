---
name: 2pdf
description: "Convert docx, pptx, md files to PDF. Triggers on 'convert to pdf', 'export pdf', '2pdf', '转pdf', '导出pdf'."
---

# 2pdf — Document to PDF Converter

Convert `.docx`, `.pptx`, `.md` files to PDF using LibreOffice headless + Python.

## Quick Use

```bash
# Single file
python scripts/convert.py input.docx

# Custom output path
python scripts/convert.py input.md output/report.pdf

# Batch: all supported files in a directory
for f in /path/to/*.docx /path_to/*.pptx /path/to/*.md; do
  python scripts/convert.py "$f"
done
```

## Supported Formats

| Input | Engine | Notes |
|-------|--------|-------|
| `.docx` | LibreOffice headless | Full formatting preserved |
| `.pptx` | LibreOffice headless | Slides → one PDF page per slide |
| `.md` | markdown → HTML → LibreOffice | GitHub-flavored styling |

## Requirements

- **LibreOffice** must be installed (`soffice` in PATH or at `/Applications/LibreOffice.app`)
- Python packages: `markdown` (for .md conversion)
- Install: `pip install markdown`

## Default Behavior

- **Output location:** Same directory as input, same filename with `.pdf` extension
- **Overwrite:** Silently overwrites existing PDF at the target path
- **Timeout:** 120 seconds per conversion

## Programmatic Use

```python
from scripts.convert import convert
result = convert("/path/to/file.md")           # → "/path/to/file.pdf"
result = convert("/path/to/file.docx", "/tmp/out.pdf")  # custom output
```

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `LibreOffice not found` | `brew install --cask libreoffice` |
| Chinese chars garbled in .md PDF | Ensure system fonts available (STHeiti, PingFang) |
| Conversion timeout | Check for stuck soffice processes: `pkill soffice` |
