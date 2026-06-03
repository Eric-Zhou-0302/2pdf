# 2pdf

**中文** | [English](./README.md)

轻量级文档转 PDF 工具，基于 LibreOffice headless 引擎。一条命令即可将 `.docx`、`.pptx`、`.md` 文件转换为 PDF。

## 功能

- **docx → PDF** — 完整保留格式（表格、图片、样式）
- **pptx → PDF** — 每页幻灯片对应 PDF 一页，布局不变
- **md → PDF** — GitHub 风格样式，支持代码高亮、表格、引用块
- **零配置** — 默认输出到同目录、同文件名、`.pdf` 后缀
- **支持批量** — 可脚本化批量转换

## 依赖

| 依赖 | 用途 | 安装方式 |
|------|------|----------|
| Python 3.10+ | 运行环境 | — |
| LibreOffice | 渲染引擎 | `brew install --cask libreoffice` |
| markdown | Markdown 解析 | `pip install markdown` |

## 快速开始

```bash
# 单文件转换
python scripts/convert.py report.docx

# 指定输出路径
python scripts/convert.py slides.pptx output/slides.pdf

# 批量转换目录下所有文件
for f in /path/to/*.docx /path/to/*.pptx /path/to/*.md; do
  python scripts/convert.py "$f"
done
```

## 工作原理

```
docx ──→ LibreOffice headless ──→ PDF
pptx ──→ LibreOffice headless ──→ PDF
md   ──→ markdown → HTML（+ GitHub CSS）→ LibreOffice ──→ PDF
```

三种格式均通过 LibreOffice 渲染引擎，确保高保真输出。Markdown 文件先转换为带 GitHub 风格样式（表格、代码块、引用块等）的 HTML，再渲染为 PDF。

## 编程调用

```python
from scripts.convert import convert

# 默认：同目录、同文件名、.pdf 后缀
result = convert("/path/to/file.md")
# → "/path/to/file.pdf"

# 指定输出路径
result = convert("/path/to/file.docx", "/tmp/output.pdf")
```

## 项目结构

```
2pdf/
├── SKILL.md              # OpenClaw Skill 定义
├── README.md             # 英文文档
├── README_zh.md          # 中文文档
├── scripts/
│   └── convert.py        # 核心转换脚本
└── assets/
    └── github.css        # Markdown 渲染的 GitHub 风格 CSS
```

## 常见问题

| 问题 | 解决方案 |
|------|----------|
| `LibreOffice not found` | 安装 LibreOffice：`brew install --cask libreoffice` |
| 中文字符乱码 | 确保系统字体可用（STHeiti、PingFang） |
| 转换超时 | 终止卡死的进程：`pkill soffice` |
| 输出 PDF 为空 | 检查 LibreOffice 版本：`soffice --version` |

## 许可证

MIT
