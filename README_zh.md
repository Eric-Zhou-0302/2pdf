# 2pdf

**中文** | [English](./README.md)

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)
[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-green?style=flat-square)](https://docs.openclaw.ai/skills/)

一条命令，将 `.docx`、`.pptx`、`.md` 文件转换为 PDF —— 输出到同目录、同文件名。

基于 [LibreOffice](https://www.libreoffice.org/) headless 引擎，高保真渲染。Markdown 文件使用 GitHub 风格样式。

## 安装

```bash
# 克隆到 OpenClaw skills 目录
git clone https://github.com/Eric-Zhou-0302/2pdf ~/.openclaw/skills/2pdf

# 安装唯一的 Python 依赖（用于 .md 转换）
pip install markdown
```

**前置条件：** 需已安装 [LibreOffice](https://www.libreoffice.org/)。

```bash
brew install --cask libreoffice          # macOS
sudo apt install libreoffice-core        # Ubuntu/Debian
```

## 使用

```bash
python ~/.openclaw/skills/2pdf/scripts/convert.py <文件>
```

| 输入 | 输出 | 引擎 |
|------|------|------|
| `report.docx` | `report.pdf` | LibreOffice |
| `slides.pptx` | `slides.pdf` | LibreOffice |
| `notes.md` | `notes.pdf` | markdown → HTML → LibreOffice |

### 指定输出路径

```bash
python ~/.openclaw/skills/2pdf/scripts/convert.py input.docx /tmp/output.pdf
```

### 批量转换

```bash
for f in /path/to/*.docx /path/to/*.pptx /path/to/*.md; do
  python ~/.openclaw/skills/2pdf/scripts/convert.py "$f"
done
```

### Python 调用

```python
from scripts.convert import convert

convert("/path/to/file.md")                    # → /path/to/file.pdf
convert("/path/to/file.docx", "/tmp/out.pdf")  # 指定输出
```

## 工作原理

```
docx ──→ soffice --headless --convert-to pdf ──→ PDF
pptx ──→ soffice --headless --convert-to pdf ──→ PDF
md   ──→ markdown → HTML（+ CSS）→ soffice    ──→ PDF
```

三种格式均通过 LibreOffice 渲染。Markdown 文件先转换为 HTML 并嵌入 GitHub 风格 CSS（表格、代码块、引用块、列表），再交给 LibreOffice 生成 PDF。

## 项目结构

```
2pdf/
├── SKILL.md              # OpenClaw Skill 定义
├── README.md             # English
├── README_zh.md          # 中文
├── scripts/
│   └── convert.py        # 转换脚本
└── assets/
    └── github.css        # GitHub 风格 CSS
```

## 常见问题

| 问题 | 解决 |
|------|------|
| `LibreOffice not found` | `brew install --cask libreoffice` |
| 中文字符乱码 | 需要系统字体（STHeiti / PingFang） |
| 转换超时 | `pkill soffice` 后重试 |
| 输出 PDF 为空 | `soffice --version` 检查安装 |

## 许可证

[MIT](LICENSE)
