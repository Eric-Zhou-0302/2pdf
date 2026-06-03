# 2pdf

**中文** | [English](./README.md)

[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-green?style=flat-square)](https://docs.openclaw.ai/skills/)
[![Claude Code Compatible](https://img.shields.io/badge/Claude%20Code-Compatible-orange?style=flat-square)](https://docs.anthropic.com/en/docs/claude-code)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)

一个 AI Agent Skill，将 `.docx`、`.pptx`、`.md` 文件转换为 PDF。适用于 OpenClaw、Claude Code、Codex 及所有支持 `SKILL.md` 标准的智能体。

直接告诉你的 Agent：*"把这个文件转成 PDF"* —— 它会自动处理。

## 安装

### OpenClaw

```bash
git clone https://github.com/Eric-Zhou-0302/2pdf ~/.openclaw/skills/2pdf
```

### Claude Code

```bash
git clone https://github.com/Eric-Zhou-0302/2pdf ~/.claude/skills/2pdf
```

### 其他 Agent

将本仓库克隆到你的 Agent 读取的 `skills/` 目录下即可。

### 前置条件

- **Python 3.10+**
- **LibreOffice** — `brew install --cask libreoffice`（macOS）/ `sudo apt install libreoffice-core`（Linux）
- **markdown** — `pip install markdown`（仅 .md 文件需要）

## 使用方式

安装完成后，直接用自然语言告诉你的 Agent：

> *"把课件转成 PDF"*
> *"把 notes.md 转成 PDF"*
> *"把这个文件夹里所有 .docx 都导出成 PDF"*

Agent 会读取 Skill，选择正确的转换路径，输出 PDF 到原文件同目录 —— 同文件名，`.pdf` 后缀。

## 转换原理

| 格式 | 方式 | 效果 |
|------|------|------|
| `.docx` | LibreOffice headless | 完整保留格式 |
| `.pptx` | LibreOffice headless | 每页幻灯片对应一页 PDF |
| `.md` | markdown → HTML → LibreOffice | GitHub 风格样式 |

所有格式均通过 LibreOffice 渲染。Markdown 文件先转为 HTML 并嵌入 GitHub 风格 CSS（表格、代码块、引用块），再交给 LibreOffice 生成 PDF。

## 工作原理

Skill 包含一个 Python 脚本（`scripts/convert.py`）：

1. 根据扩展名判断格式
2. `.docx` / `.pptx`：调用 `soffice --headless --convert-to pdf`
3. `.md`：通过 `markdown` 库转为 HTML，嵌入 GitHub CSS，再交给 LibreOffice
4. 输出 PDF 到同目录、同文件名

Agent 通过读取 `SKILL.md` 来了解何时以及如何调用此脚本。

## 项目结构

```
2pdf/
├── SKILL.md              # Skill 定义（Agent 读取的文件）
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

## 许可证

[MIT](LICENSE)
