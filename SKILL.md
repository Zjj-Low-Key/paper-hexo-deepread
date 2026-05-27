---
name: paper-hexo-deepread
description: Create deep-reading Hexo blog posts from academic paper URLs. Use when the user gives a paper URL, arXiv/OpenReview/project page/PDF link, DOI, or paper title and wants an agent to identify paper metadata, summarize methods, capture figures/tables, create a Hexo markdown post in G:\Document\myBlog, save images under source\img, validate the report, deploy with hexo, and check the live GitHub Pages site.
---

# Paper Hexo Deepread

## Overview

Turn a paper URL into a published Hexo deep-reading report in the user's blog repository.
Follow the local style of `G:\Document\myBlog\source\_posts\DVD.md`, write the report in Chinese unless the user asks otherwise, and keep every claim grounded in the paper.

## Reading Role

Act as a senior academic reader, critical reviewer, and structured knowledge organizer. The goal is not to rewrite the abstract in friendlier words. The goal is to help the blog reader understand the paper's problem logic, method design, empirical support, reusable ideas, boundary conditions, and memorable takeaways.

Read like a reviewer first and a blogger second:
- identify the real research question, motivation, task definition, inputs, outputs, assumptions, and constraints;
- separate the paper's explicit evidence from your own interpretation;
- explain why the method may work, not only what modules it contains;
- judge which claims are directly supported by experiments and which remain plausible but insufficiently verified;
- surface limitations, risks, failure cases, and transferability without overstating criticism beyond the paper.

## Reading Principles

- Build a global map before writing details. Use the title, abstract, introduction, method overview, experiments, and conclusion to form the paper-level story before diving into formulas, modules, and result tables.
- Do not spend equal effort on every paragraph. Prioritize research motivation, core contribution, method structure, key equations, experimental design, main results, limitations, and reusable insights. Compress routine background and repetitive descriptions.
- Stay close to the original paper when explaining methods. Preserve important terms, module names, variables, losses, and equations, then explain them in Chinese so the reader can connect the note back to the paper.
- Do not passively paraphrase. For each important section, ask: What problem is this solving? What is new compared with baselines or common practice? What assumption does it rely on? What evidence supports it? What remains unanswered?
- Treat uncertain metadata or external facts cautiously. If author background, venue ranking, CCF/SCI category, acceptance status, code status, or arXiv-to-conference status cannot be verified from reliable sources, mark it as unverified or uncertain instead of guessing.
- Prefer precise, reusable conclusions over long summaries. Capture method intuition, technical details worth reusing, experimental lessons, applicable scenarios, and research opportunities.
- When the user asks a narrow follow-up about one formula, figure, experiment, or comparison, answer that local question directly first. Do not repeat the full reading-note framework unless the user explicitly requests a complete summary.

## Workflow

1. **Collect source material**
   - Open the paper URL and prefer primary sources: arXiv/PDF, conference page, OpenReview, project page, code repository, and official supplementary material.
   - Extract title, method acronym, authors, affiliations, venue/source/year, abstract, figures, tables, datasets, compute, experiments, limitations, and links.
   - If paper metadata is incomplete in one source, cross-check with another primary source before guessing.
   - Classify the paper type when useful, such as survey, method, system, benchmark, dataset, theory, or application paper, and state the evidence for that classification in the report when it affects interpretation.
   - For arXiv-first papers, search for later official venue or acceptance information when practical. If no reliable confirmation is found, keep the publication or acceptance status explicit as unverified.

2. **Choose `papername`**
   - Use the method acronym when the paper has one, such as `DVD`.
   - Otherwise use a short ASCII abbreviation of the paper title, without spaces. Keep it stable for file names and image names.
   - Use the same exact `papername` for `hexo new`, markdown image filenames, alt text, and cover path.

3. **Inspect local blog conventions**
   - Read `G:\Document\myBlog\source\_posts\DVD.md` for the current article shape.
   - Run `scripts/summarize_hexo_taxonomy.py` against `G:\Document\myBlog\source\_posts` to choose tags and categories from existing posts:
     ```powershell
     python G:\Document\myBlog\.codex\skills\paper-hexo-deepread\scripts\summarize_hexo_taxonomy.py G:\Document\myBlog\source\_posts
     ```
   - Prefer existing categories/tags. Add a new one only when no existing taxonomy fits.

4. **Create the Hexo post**
   - From `G:\Document\myBlog`, use Git Bash to run:
     ```bash
     hexo new "papername"
     ```
   - If only PowerShell is available, call Git Bash explicitly, for example:
     ```powershell
     bash -lc "cd /g/Document/myBlog && hexo new 'papername'"
     ```
   - Edit the generated file under `G:\Document\myBlog\source\_posts\papername.md`.

5. **Extract and prepare paper figures/tables**
   - After obtaining the PDF, extract an inventory of **all figures and all tables in the main paper body** before writing the report. Use the PDF text/captions plus rendered page previews to build a checklist like `Figure 1`, `Figure 2`, `Table 1`, `Table 2`, with page number, caption summary, and the report section where it belongs. Include supplementary figures/tables only when they are needed for the reading note.
   - Render PDF pages at high enough resolution for readable crops, usually `pdftoppm -png -r 180` or higher. Prefer structured PDF extraction tools when they preserve the figure/table cleanly, but always verify the extracted image against the rendered page.
   - Save every report image under `G:\Document\myBlog\source\img`.
   - Name images as `papername-0.png`, `papername-1.png`, `papername-2.png`, etc. Choose the cover image by the principle of best representing the paper's distinctive contribution: use the paper's teaser image when it has one; otherwise use the main pipeline/architecture image. Save or rename the chosen cover image as `papername-0.png`, and set the frontmatter cover to `/img/papername-0.png`. The cover image must contain only the visual itself: do not include the figure caption, nearby body text, page numbers, or other surrounding PDF prose in `papername-0.png`. Number the remaining images in the order they appear in the reading note as much as practical.
   - Each saved PNG must be a **complete and independent visual unit**:
     - Crop one figure or one table per image, unless the paper explicitly presents them as one inseparable composite.
     - Include the full visual content, axis labels, legends, subfigure labels, table headers, row/column labels, and caption when useful for interpretation.
     - Do not cut off any part of the figure/table.
     - Do not include unrelated neighboring content, such as the abstract, body paragraphs, references, another figure, another table, page numbers, or partial text from the next column.
     - When a figure and table are adjacent on the same page, crop and save them separately.
     - When a figure or table spans columns/pages, stitch or crop so the final PNG is still complete and standalone.
   - Build a contact sheet or preview of the extracted PNGs and visually inspect it before inserting them. Reject and recrop any image that has bleed-through from surrounding text or combines unrelated figure/table content.
   - Insert images with the exact Hexo-compatible syntax:
     ```markdown
     ![papername-1](/img/papername-1.png 'papername-1')
     ```
   - Place each extracted figure/table near the paragraph that explains it:
     - motivation or teaser figures go in `鐮旂┒鍔ㄦ満`;
     - pipeline, architecture, representation, and loss diagrams go in `鏍稿績鏂规硶`;
     - dataset statistics or benchmark setup tables go in `鏁版嵁闆?`;
     - model size, training setup, GPU, batch size, or speed tables go in `绠楀姏` when relevant;
     - quantitative tables, qualitative comparisons, ablations, and user studies go in `瀹為獙缁撴灉`;
     - failure cases, limitations, editing examples, or diagnostic visuals can go in `浼樺娍涓庝笉瓒?` when they support the critique.
   - Do not skip paper-body figures or tables silently. If a figure/table is intentionally omitted because it is redundant or irrelevant to a concise reading note, mention that decision in the working notes or final summary.

6. **Write the report**
   - Follow `references/report-format.md` for the frontmatter, metadata block, section order, image syntax, and review checklist.
   - Required sections: `研究动机`, `核心方法`, `数据集`, `算力`, `实验结果`, `优势与不足`, `记忆点`.
   - Keep the explanation deeper than an abstract summary: explain what problem the method solves, why each component exists, how the experiments support the claims, and where the method may fail.
   - Use the figure/table inventory from step 5 as the insertion plan. The report should follow the paper's logic, not dump all images in one section.
   - In the motivation section, make clear what the paper is trying to solve, why the problem matters, what gap or bottleneck existed before, and how this task sits in the broader research landscape.
   - In the method section, explain the overall method idea, key modules, how modules connect, the input/output of important components, and the reason each design choice may help. For key equations, write the equation in LaTeX, define the main symbols, explain the mechanism it represents, and describe its role in the whole method.
   - In the experiment section, connect datasets, evaluation metrics, baselines, ablations, and main conclusions. Do not list numbers without interpretation. Explain what the results prove, what they only suggest, and why performance changes may happen.
   - For figures and tables, translate visual information into text. When first citing an important figure/table, briefly state what object it shows, what relationship or mechanism it reveals, and why it matters for understanding the paper. Prefer explaining information value over merely naming figure numbers.
   - In the limitations and takeaways sections, distinguish proven claims from unproven or weakly supported claims. Mention possible data bias, evaluation bias, generalization risk, resource dependence, narrow assumptions, missing comparisons, or scenarios where the method may not apply when the paper gives evidence or the concern follows directly from the setup.
   - End with a compact conclusion that covers the problem, why it matters, the key method, what the results show, the paper's value, its boundary, and what can be borrowed for future work.

7. **Validate before publishing**
   - Run:
     ```powershell
     python G:\Document\myBlog\.codex\skills\paper-hexo-deepread\scripts\check_hexo_report.py G:\Document\myBlog\source\_posts\papername.md --image-dir G:\Document\myBlog\source\img
     ```
   - Fix every reported issue.
   - Manually audit: metadata accuracy, section completeness, image order, formula rendering, citations/links, and whether the report overstates any paper claim.
   - Confirm that all formulas use valid LaTeX delimiters for this blog: inline formulas use single dollar signs and display formulas use double dollar signs.
   - Check that unverified external facts are labeled as unverified or uncertain, and that no claim relies on experience-based guessing.
   - Check that the report includes critical analysis, not only positive description: at minimum, it should discuss empirical support, applicable boundaries, and one or more limitations or open questions when the paper provides enough basis.
   - Manually audit every extracted PNG against the source PDF. Confirm each image/table is complete, standalone, readable, and free of unrelated surrounding content. If a crop contains part of the abstract/body text, another visual, a truncated caption, or a partial table/figure, recrop before publishing.
   - Audit the cover image separately. `papername-0.png` must be a clean visual-only cover crop, without the figure caption, surrounding prose, page footer/header, or other layout artifacts from the PDF page.

8. **Deploy and check the live site**
   - Only deploy when the user requested publishing or the task explicitly includes blog update/upload.
   - From Git Bash in `G:\Document\myBlog`, run:
     ```bash
     hexo c && hexo g && hexo d
     hexo c && hexo g && hexo d
     ```
   - Wait for GitHub Pages to build, then open `https://zjj-low-key.github.io/` and confirm the new post appears and renders correctly.
   - If the post is not visible after the first check, wait a few minutes and check again before declaring failure.

## Resources

- `references/report-format.md`: local article format, section requirements, and final review checklist.
- `scripts/summarize_hexo_taxonomy.py`: summarize existing tags/categories from Hexo posts.
- `scripts/check_hexo_report.py`: validate frontmatter, required sections, image references, local image files, cover image, and formula block balance.
