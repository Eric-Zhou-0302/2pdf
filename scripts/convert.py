#!/usr/bin/env python3
"""
2pdf — Convert docx/pptx/md to PDF via LibreOffice headless.

Usage:
    python convert.py <input_file> [output_file]

If output_file is omitted, PDF is written beside the input file
with the same name and a .pdf extension.

Supported formats: .docx, .pptx, .md
"""

import argparse
import os
import shutil
import subprocess
import sys
import tempfile

# ── Markdown extensions ─────────────────────────────────────────────
import markdown

MD_EXTENSIONS = [
    "markdown.extensions.tables",
    "markdown.extensions.fenced_code",
    "markdown.extensions.codehilite",
    "markdown.extensions.toc",
    "markdown.extensions.footnotes",
    "markdown.extensions.attr_list",
    "markdown.extensions.def_list",
    "markdown.extensions.abbr",
    "markdown.extensions.admonition",
    "markdown.extensions.meta",
    "markdown.extensions.smarty",
    "markdown.extensions.md_in_html",
]

# ── GitHub-style CSS (embedded) ─────────────────────────────────────
GITHUB_CSS_DIR = os.path.join(os.path.dirname(__file__), "..", "assets")


def _load_github_css() -> str:
    css_path = os.path.join(GITHUB_CSS_DIR, "github.css")
    if os.path.exists(css_path):
        return open(css_path, encoding="utf-8").read()
    # Fallback: minimal inline styles
    return """
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
           font-size: 14px; line-height: 1.6; color: #24292e; max-width: 900px;
           margin: 0 auto; padding: 32px 64px; }
    h1, h2, h3, h4, h5, h6 { margin-top: 24px; margin-bottom: 16px; font-weight: 600; line-height: 1.25; }
    h1 { font-size: 2em; border-bottom: 1px solid #eaecef; padding-bottom: .3em; }
    h2 { font-size: 1.5em; border-bottom: 1px solid #eaecef; padding-bottom: .3em; }
    code { background: #f6f8fa; padding: .2em .4em; border-radius: 3px; font-size: 85%; }
    pre { background: #f6f8fa; padding: 16px; border-radius: 6px; overflow: auto; }
    pre code { background: transparent; padding: 0; }
    blockquote { border-left: .25em solid #dfe2e5; color: #6a737d; padding: 0 1em; margin: 0 0 16px; }
    table { border-collapse: collapse; width: 100%; margin-bottom: 16px; }
    th, td { border: 1px solid #dfe2e5; padding: 6px 13px; }
    tr:nth-child(2n) { background: #f6f8fa; }
    img { max-width: 100%; }
    hr { height: .25em; padding: 0; margin: 24px 0; background-color: #e1e4e8; border: 0; }
    a { color: #0366d6; text-decoration: none; }
    ul, ol { padding-left: 2em; }
    """


# ── LibreOffice discovery ───────────────────────────────────────────
def _find_soffice() -> str:
    """Locate the soffice binary."""
    # Check PATH first
    soffice = shutil.which("soffice")
    if soffice:
        return soffice
    # Common macOS location
    mac_path = "/Applications/LibreOffice.app/Contents/MacOS/soffice"
    if os.path.isfile(mac_path):
        return mac_path
    raise FileNotFoundError(
        "LibreOffice not found. Install it:\n"
        "  brew install --cask libreoffice"
    )


# ── Conversion functions ────────────────────────────────────────────
def _convert_office(input_path: str, output_dir: str, soffice: str) -> str:
    """Convert docx/pptx to PDF via LibreOffice headless."""
    cmd = [
        soffice,
        "--headless",
        "--convert-to", "pdf",
        "--outdir", output_dir,
        input_path,
    ]
    result = subprocess.run(
        cmd, capture_output=True, text=True, timeout=120
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"LibreOffice conversion failed:\n{result.stderr.strip()}"
        )
    # soffice outputs: "convert /path/to/file.docx -> /path/to/file.pdf using filter : writer_pdf_Export"
    base = os.path.splitext(os.path.basename(input_path))[0]
    expected = os.path.join(output_dir, base + ".pdf")
    if not os.path.isfile(expected):
        raise RuntimeError(
            f"Conversion succeeded but output not found at {expected}\n"
            f"soffice output: {result.stdout.strip()}"
        )
    return expected


def _convert_md(input_path: str, output_path: str, soffice: str) -> str:
    """Convert Markdown to PDF: md → HTML (with GitHub CSS) → PDF via LibreOffice."""
    # Read markdown content
    with open(input_path, encoding="utf-8") as f:
        md_text = f.read()

    # Convert to HTML body
    html_body = markdown.markdown(md_text, extensions=MD_EXTENSIONS)

    # Build full HTML document with embedded CSS
    css = _load_github_css()
    html_doc = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<style>
{css}
</style>
</head>
<body class="markdown-body">
{html_body}
</body>
</html>"""

    # Write temp HTML file
    output_dir = os.path.dirname(output_path) or "."
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".html", dir=output_dir,
        delete=False, encoding="utf-8"
    ) as tmp:
        tmp.write(html_doc)
        tmp_html = tmp.name

    try:
        # Convert HTML → PDF via LibreOffice
        cmd = [
            soffice,
            "--headless",
            "--convert-to", "pdf",
            "--outdir", output_dir,
            tmp_html,
        ]
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=120
        )
        if result.returncode != 0:
            raise RuntimeError(
                f"LibreOffice HTML→PDF conversion failed:\n{result.stderr.strip()}"
            )

        # Move to desired output path if needed
        tmp_base = os.path.splitext(os.path.basename(tmp_html))[0]
        tmp_pdf = os.path.join(output_dir, tmp_base + ".pdf")
        if os.path.isfile(tmp_pdf) and tmp_pdf != output_path:
            shutil.move(tmp_pdf, output_path)
        elif not os.path.isfile(output_path):
            raise RuntimeError(
                f"PDF output not found at {output_path}\n"
                f"soffice output: {result.stdout.strip()}"
            )
    finally:
        # Clean up temp HTML
        if os.path.exists(tmp_html):
            os.remove(tmp_html)

    return output_path


# ── Main ─────────────────────────────────────────────────────────────
def convert(input_path: str, output_path: str | None = None) -> str:
    """
    Convert a file to PDF.

    Args:
        input_path:  Path to .docx / .pptx / .md file
        output_path: Optional output PDF path. Defaults to same dir, same name.

    Returns:
        Absolute path to the generated PDF.
    """
    input_path = os.path.abspath(input_path)
    if not os.path.isfile(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")

    ext = os.path.splitext(input_path)[1].lower()
    if ext not in (".docx", ".pptx", ".md"):
        raise ValueError(
            f"Unsupported format: {ext}. Supported: .docx, .pptx, .md"
        )

    # Default output: same directory, same name, .pdf extension
    if output_path is None:
        output_path = os.path.splitext(input_path)[0] + ".pdf"
    output_path = os.path.abspath(output_path)
    output_dir = os.path.dirname(output_path)

    soffice = _find_soffice()

    if ext in (".docx", ".pptx"):
        result = _convert_office(input_path, output_dir, soffice)
    elif ext == ".md":
        result = _convert_md(input_path, output_path, soffice)
    else:
        raise ValueError(f"No handler for {ext}")

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Convert docx/pptx/md to PDF via LibreOffice"
    )
    parser.add_argument("input", help="Input file (.docx, .pptx, .md)")
    parser.add_argument(
        "output", nargs="?", default=None,
        help="Output PDF path (default: same dir, same name)"
    )
    args = parser.parse_args()

    try:
        result = convert(args.input, args.output)
        print(f"✅ {os.path.basename(result)}")
        print(f"   {result}")
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
