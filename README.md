# Paper Hexo Deepread

English | [中文](#中文说明)

`paper-hexo-deepread` is a Codex skill for turning an academic paper URL, DOI, PDF, arXiv page, OpenReview page, project page, or paper title into a structured Hexo deep-reading blog post.

The skill is opinionated: it expects an existing Hexo blog, extracts and checks paper figures/tables, writes a Chinese deep-reading note, validates the generated Markdown, and optionally deploys the Hexo site.

## What this skill does

- Collects paper metadata from primary sources such as arXiv, OpenReview, project pages, PDFs, and official repositories.
- Builds a figure/table inventory before writing the post.
- Saves final PNG assets into the Hexo image directory.
- Creates a Hexo-compatible Markdown post with front matter, metadata, required sections, and image references.
- Validates the generated post with `scripts/check_hexo_report.py`.
- Summarizes existing Hexo tags and categories with `scripts/summarize_hexo_taxonomy.py`.
- Guides optional `hexo clean`, `hexo generate`, and `hexo deploy` checks.

## What this skill does not do

This skill does **not** create a Hexo site from scratch and does **not** create a new Hexo theme, page layout, GitHub Pages repository, or deployment configuration for you.

You should already have a working Hexo blog before using it. If you do not, set one up first:

- [Hexo documentation](https://hexo.io/docs/)
- [Hexo writing guide](https://hexo.io/docs/writing)
- [Hexo commands](https://hexo.io/docs/commands)
- [Hexo one-command deployment](https://hexo.io/docs/one-command-deployment)
- [GitHub Pages getting started](https://pages.github.com/)

## Repository layout

```text
paper-hexo-deepread/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   └── report-format.md
└── scripts/
    ├── check_hexo_report.py
    └── summarize_hexo_taxonomy.py
```

## Installation

Clone or copy this folder into your Codex skill directory:

```powershell
git clone https://github.com/Zjj-Low-Key/paper-hexo-deepread.git "$env:USERPROFILE\.codex\skills\paper-hexo-deepread"
```

Restart Codex after installing or updating the skill so it can rediscover `SKILL.md`.

## Required local setup

Before using the skill, make sure your machine has:

- A working Hexo blog.
- Node.js and Hexo installed for that blog.
- Git configured for the blog repository.
- Python 3 for the validation scripts.
- Optional but recommended PDF/image tools such as `pdftoppm`, ImageMagick, or another crop/preview workflow for paper figures.

## Customize before use

The current skill was written for a local blog workflow and includes concrete paths such as:

- Blog root: `G:\Document\myBlog`
- Posts directory: `G:\Document\myBlog\source\_posts`
- Image directory: `G:\Document\myBlog\source\img`
- Reference article: `G:\Document\myBlog\source\_posts\DVD.md`
- Live site: `https://zjj-low-key.github.io/`

Other users will probably not have these files, especially the referenced Markdown example article. Treat them as examples of one author's blog convention, not universal defaults.

Before using the skill, edit these files for your own blog:

- `SKILL.md`: update the blog root, post path, image path, example article, deployment command, and live-site URL.
- `references/report-format.md`: update front matter, required sections, taxonomy rules, image path rules, and final review checklist to match your writing style.
- `scripts/check_hexo_report.py`: update `REQUIRED_SECTIONS` and `REQUIRED_METADATA` if your article template uses different headings.

If your blog uses a different writing structure, replace the `DVD.md` reference with one of your own mature paper-reading posts and adjust the section names accordingly.

## Typical usage

Ask Codex to use the skill with a paper source:

```text
Use $paper-hexo-deepread to write a Hexo deep-reading post for https://arxiv.org/abs/xxxx.xxxxx
```

For safer operation, specify whether you want only a draft or a deployed post:

```text
Use $paper-hexo-deepread to create a draft only. Do not deploy.
```

```text
Use $paper-hexo-deepread to create, validate, deploy, and check the live site.
```

## Validation scripts

Summarize tags and categories from an existing Hexo blog:

```powershell
python scripts/summarize_hexo_taxonomy.py G:\Document\myBlog\source\_posts
```

Validate a generated post:

```powershell
python scripts/check_hexo_report.py G:\Document\myBlog\source\_posts\papername.md --image-dir G:\Document\myBlog\source\img
```

Change the paths to match your own Hexo repository.

## Notes for maintainers

- Keep `SKILL.md` precise. Skills are operational instructions, not just documentation.
- Keep local assumptions visible in README whenever the skill references a private path, sample article, or deployment target.
- Prefer primary paper sources over secondary summaries.
- Keep validation strict enough to catch missing front matter, broken image references, absent sections, and obvious figure-crop issues.

## License

MIT License. See [LICENSE](LICENSE).

---

## 中文说明

[English](#paper-hexo-deepread) | 中文

`paper-hexo-deepread` 是一个 Codex skill，用来把论文 URL、DOI、PDF、arXiv 页面、OpenReview 页面、项目主页或论文标题，转换成结构化的 Hexo 论文精读博客文章。

这个 skill 带有明确的个人工作流假设：它默认你已经有一个可用的 Hexo 博客，会提取并检查论文图表，撰写中文精读笔记，校验生成的 Markdown，并在需要时引导执行 Hexo 部署。

## 这个 skill 会做什么

- 从 arXiv、OpenReview、项目主页、PDF、官方代码仓库等一手来源收集论文元数据。
- 在写作前建立主文图表清单。
- 将最终 PNG 图像保存到 Hexo 的图片目录。
- 生成兼容 Hexo 的 Markdown 文章，包括 front matter、论文元信息、固定章节和图片引用。
- 使用 `scripts/check_hexo_report.py` 校验生成的文章。
- 使用 `scripts/summarize_hexo_taxonomy.py` 汇总现有 Hexo 文章的标签和分类。
- 引导可选的 `hexo clean`、`hexo generate`、`hexo deploy` 检查。

## 这个 skill 不会做什么

这个 skill **不会** 从零创建 Hexo 站点，也**不会**为你新建 Hexo 主题、页面布局、GitHub Pages 仓库或部署配置。

使用它之前，你应该已经有一个能正常运行的 Hexo 博客。如果还没有，请先参考：

- [Hexo 官方文档](https://hexo.io/docs/)
- [Hexo 写作指南](https://hexo.io/docs/writing)
- [Hexo 命令说明](https://hexo.io/docs/commands)
- [Hexo 一键部署](https://hexo.io/docs/one-command-deployment)
- [GitHub Pages 入门](https://pages.github.com/)

## 仓库结构

```text
paper-hexo-deepread/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   └── report-format.md
└── scripts/
    ├── check_hexo_report.py
    └── summarize_hexo_taxonomy.py
```

## 安装方式

把这个仓库克隆或复制到你的 Codex skill 目录：

```powershell
git clone https://github.com/Zjj-Low-Key/paper-hexo-deepread.git "$env:USERPROFILE\.codex\skills\paper-hexo-deepread"
```

安装或更新后，重启 Codex，让它重新发现 `SKILL.md`。

## 本地前置条件

使用前请确认你的机器已经具备：

- 一个可以正常运行的 Hexo 博客。
- 该博客已经安装 Node.js 和 Hexo。
- 博客仓库已经配置好 Git。
- Python 3，用于运行校验脚本。
- 可选但推荐的 PDF/图像工具，例如 `pdftoppm`、ImageMagick，或其他用于论文图表裁剪和预览的工具链。

## 使用前请先自定义

当前 skill 来自一个本地博客工作流，里面包含一些具体路径，例如：

- 博客根目录：`G:\Document\myBlog`
- 文章目录：`G:\Document\myBlog\source\_posts`
- 图片目录：`G:\Document\myBlog\source\img`
- 参考文章：`G:\Document\myBlog\source\_posts\DVD.md`
- 在线站点：`https://zjj-low-key.github.io/`

其他用户通常不会拥有这些文件，尤其是 README 中提到的参考 Markdown 文章。请把它们理解为作者个人博客格式的示例，而不是通用默认值。

使用前建议修改以下文件：

- `SKILL.md`：改成你自己的博客根目录、文章目录、图片目录、参考文章、部署命令和线上站点地址。
- `references/report-format.md`：改成你自己的 front matter、章节结构、分类标签规则、图片路径规则和最终检查清单。
- `scripts/check_hexo_report.py`：如果你的文章模板使用不同章节标题，修改 `REQUIRED_SECTIONS` 和 `REQUIRED_METADATA`。

如果你的论文写作习惯和作者不同，请把 `DVD.md` 这个参考文章替换成你自己写得比较成熟的一篇论文精读文章，并同步调整章节标题和校验规则。

## 典型用法

给 Codex 一个论文来源，并显式调用这个 skill：

```text
Use $paper-hexo-deepread to write a Hexo deep-reading post for https://arxiv.org/abs/xxxx.xxxxx
```

为了更稳妥，建议说明你只需要草稿，还是需要部署：

```text
Use $paper-hexo-deepread to create a draft only. Do not deploy.
```

```text
Use $paper-hexo-deepread to create, validate, deploy, and check the live site.
```

## 校验脚本

从现有 Hexo 博客中汇总标签和分类：

```powershell
python scripts/summarize_hexo_taxonomy.py G:\Document\myBlog\source\_posts
```

校验生成的文章：

```powershell
python scripts/check_hexo_report.py G:\Document\myBlog\source\_posts\papername.md --image-dir G:\Document\myBlog\source\img
```

实际使用时，请把路径换成你自己的 Hexo 仓库路径。

## 维护建议

- 保持 `SKILL.md` 精确。Skill 是会被 agent 执行的操作指令，不只是说明文档。
- 只要 skill 引用了个人路径、示例文章或部署目标，就应在 README 中明确说明。
- 论文信息优先使用一手来源，不要只依赖二手总结。
- 校验脚本应保持足够严格，用来发现缺失 front matter、图片引用错误、章节缺失和明显的图表裁剪问题。

## 许可证

MIT License。详见 [LICENSE](LICENSE)。
