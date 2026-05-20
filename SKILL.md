---
name: paper-hexo-deepread
description: Create deep-reading Hexo blog posts from academic paper URLs. Use when the user gives a paper URL, arXiv/OpenReview/project page/PDF link, DOI, or paper title and wants an agent to identify paper metadata, summarize methods, capture figures/tables, create a Hexo markdown post in G:\Document\myBlog, save images under source\img, validate the report, deploy with hexo, and check the live GitHub Pages site.
---

# Paper Hexo Deepread

## Overview

Turn a paper URL into a published Hexo deep-reading report in the user's blog repository.
Follow the local style of `G:\Document\myBlog\source\_posts\DVD.md`, write the report in Chinese unless the user asks otherwise, and keep every claim grounded in the paper.

## Workflow

1. **Collect source material**
   - Open the paper URL and prefer primary sources: arXiv/PDF, conference page, OpenReview, project page, code repository, and official supplementary material.
   - Extract title, method acronym, authors, affiliations, venue/source/year, abstract, figures, tables, datasets, compute, experiments, limitations, and links.
   - If paper metadata is incomplete in one source, cross-check with another primary source before guessing.

2. **Choose `papername`**
   - Use the method acronym when the paper has one, such as `DVD`.
   - Otherwise use a short ASCII abbreviation of the paper title, without spaces. Keep it stable for file names and image names.
   - Use `papername` only for filenames, image names, and `hexo new`. Do **not** use `papername` to rewrite the paper title.
   - In Markdown frontmatter, set `title` to the exact title shown in the PDF/arXiv metadata. For example, use `title: 'VGGT-Ω'`, not `title: 'VGGTOmega: VGGT-Ω'`.

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
   - Name images as `papername-0.png`, `papername-1.png`, `papername-2.png`, etc. Number images in the order they appear in the reading note, but do **not** assume `papername-0.png` must be the cover.
   - Choose the cover image from the actual paper visuals after building the figure/table inventory:
     - If the paper has a teaser figure, use the teaser as `cover`.
     - If it has no teaser, use the pipeline / architecture / method overview figure as `cover`.
     - Set `cover` to the selected image's real path, such as `/img/papername-3.png` when the selected teaser/pipeline image is `papername-3.png`. Do not rename or force an unrelated `papername-0.png` cover just for convention.
   - Each saved PNG must be a **complete and independent visual unit**:
     - Crop one figure or one table per image, unless the paper explicitly presents them as one inseparable composite.
     - Include the full visual content, axis labels, legends, subfigure labels, table headers, row/column labels, and caption when useful for interpretation.
     - Do not cut off any part of the figure/table.
     - Do not leave visible outer white borders or PDF page canvas around the visual. Trim to the visual content with only a small safety margin for anti-aliased edges.
     - Do not over-trim: every axis label, legend, arrow, subfigure label, table rule/header, and caption text that is needed for understanding must remain complete and readable.
     - Leave a small safe margin around the non-white content after trimming, especially around captions, legends, axis labels, table titles, and the first/last row of tables. A crop is too tight if text touches the image edge or would look clipped after blog scaling.
     - Check all four edges for accidental truncation. Common failures to reject and recrop: left edge cuts off a diagram box or y-axis label; top edge cuts off a legend or table title; right edge cuts off a caption line or final table column; bottom edge cuts off the last caption line, x-axis label, or table rule.
     - Do not include unrelated neighboring content, such as the abstract, body paragraphs, references, another figure, another table, page numbers, or partial text from the next column.
     - Do not under-trim either: if the crop includes the previous/next paragraph, section heading, page footer, or a stray line of body text above/below the figure, recrop. The final PNG should contain the figure/table plus its useful caption only, not surrounding prose.
     - When a figure and table are adjacent on the same page, crop and save them separately.
     - When a figure or table spans columns/pages, stitch or crop so the final PNG is still complete and standalone.
   - Build a contact sheet or preview of the extracted PNGs and visually inspect it before inserting them. Reject and recrop any image that has large white margins, PDF page canvas, bleed-through from surrounding text, truncated content, too-tight text at the image edge, clipped legends/captions/axis labels/table rules, or combines unrelated figure/table content.
   - After contact-sheet review, open any suspicious PNG at original size and compare it against the rendered PDF page. Contact sheets can hide small truncation errors, so use full-size review for dense architecture diagrams, ablation plots, wide tables, and figures with captions near the edge.
   - If a recrop fixes over-trimming but introduces surrounding prose, adjust the crop manually rather than accepting the new artifact. The correct crop is the narrowest complete visual unit with a small safety margin.
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

7. **Validate before publishing**
   - Run:
     ```powershell
     python G:\Document\myBlog\.codex\skills\paper-hexo-deepread\scripts\check_hexo_report.py G:\Document\myBlog\source\_posts\papername.md --image-dir G:\Document\myBlog\source\img
     ```
   - Fix every reported issue.
   - Manually audit: metadata accuracy, section completeness, image order, formula rendering, citations/links, and whether the report overstates any paper claim.
   - Manually audit every extracted PNG against the source PDF. Confirm each image/table is complete, standalone, readable, tightly cropped, free of visible outer white borders, and free of unrelated surrounding content. If a crop contains large blank margins, PDF page canvas, part of the abstract/body text, another visual, a truncated caption, a clipped legend/axis/table title, text pressed against the image edge, or a partial table/figure, recrop before publishing.
   - Perform a final edge audit on the saved PNGs after all recrops. Explicitly check top, bottom, left, and right boundaries for both over-trimming and under-trimming: no clipped content, no stray prose, no page footer/header, and no caption line cut off or flush against the edge.

8. **Deploy and check the live site**
   - Only deploy when the user requested publishing or the task explicitly includes blog update/upload.
   - From Git Bash in `G:\Document\myBlog`, run:
     ```bash
     hexo c && hexo g && hexo d
     hexo c && hexo g && hexo d
     ```
   - Wait for GitHub Pages to build, then open `https://zjj-low-key.github.io/` and confirm the new post appears and renders correctly.
   - If the post is not visible after the first check, wait a few minutes and check again before declaring failure.

9. **Clean intermediate files**
   - After successful deployment and live-site verification, remove intermediate files created during the reading workflow so the blog workspace stays clean.
   - Delete temporary downloads and working artifacts such as paper PDFs, arXiv source archives, extracted LaTeX sources, rendered PDF pages, crop scratch files, contact sheets, OCR/text dumps, browser screenshots, and temporary backup folders created only for figure review.
   - Do **not** delete final deliverables or build/deploy outputs that belong to the blog: keep `source\_posts\papername.md`, the final selected PNGs under `source\img`, `public\`, `.deploy_git\`, Hexo config/cache needed by the site, and any user-created files.
   - Before recursive deletion, verify the resolved absolute path is inside an intended temporary workspace such as `G:\Document\myBlog\.codex\work\papername-or-arxiv-id` or another explicitly created scratch directory for the current paper.
   - Mention in the final summary which temporary directory or files were cleaned. If cleanup is skipped because a file may be user-owned, say so briefly instead of guessing.

## Resources

- `references/report-format.md`: local article format, section requirements, and final review checklist.
- `scripts/summarize_hexo_taxonomy.py`: summarize existing tags/categories from Hexo posts.
- `scripts/check_hexo_report.py`: validate frontmatter, required sections, image references, local image files, cover image, and formula block balance.
