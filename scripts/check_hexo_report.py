#!/usr/bin/env python3
"""Validate a Hexo paper reading report before deployment."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIRED_FRONTMATTER = ["title", "date", "tags", "categories", "cover", "copyright"]
REQUIRED_SECTIONS = ["研究动机", "核心方法", "数据集", "算力", "实验结果", "优势与不足", "记忆点"]
REQUIRED_METADATA = ["作者", "单位", "会议", "链接"]
IMAGE_RE = re.compile(r"!\[([^\]]+)\]\(/img/([^)'\"]+\.png)\s+'([^']+)'\)")


def has_large_outer_white_border(path: Path) -> str | None:
    """Return a warning string when an image appears to retain PDF page whitespace."""
    try:
        from PIL import Image
    except Exception:
        return None

    try:
        image = Image.open(path).convert("RGB")
    except Exception as exc:
        return f"could not inspect image whitespace for {path.name}: {exc}"

    width, height = image.size
    pixels = image.load()
    threshold = 248
    left, top, right, bottom = width, height, -1, -1

    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            if r < threshold or g < threshold or b < threshold:
                if x < left:
                    left = x
                if y < top:
                    top = y
                if x > right:
                    right = x
                if y > bottom:
                    bottom = y

    if right < 0:
        return f"{path.name} appears blank or all-white"

    margins = {
        "left": left,
        "top": top,
        "right": width - right - 1,
        "bottom": height - bottom - 1,
    }
    large = [
        f"{side}={value}px"
        for side, value in margins.items()
        if value > 40 and value / (width if side in {"left", "right"} else height) > 0.08
    ]
    if large:
        return f"{path.name} may have a large outer white border ({', '.join(large)}); recrop tightly while preserving all content"
    return None


def split_frontmatter(text: str) -> tuple[dict[str, str], str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text
    end = None
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end = i
            break
    if end is None:
        return {}, text

    data: dict[str, str] = {}
    for raw in lines[1:end]:
        match = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", raw)
        if match:
            data[match.group(1)] = match.group(2).strip()
    return data, "\n".join(lines[end + 1 :])


def section_body(body: str, section: str) -> str:
    pattern = re.compile(rf"^##\s+{re.escape(section)}\s*$", re.MULTILINE)
    match = pattern.search(body)
    if not match:
        return ""
    next_match = re.search(r"^##\s+", body[match.end() :], re.MULTILINE)
    if not next_match:
        return body[match.end() :].strip()
    return body[match.end() : match.end() + next_match.start()].strip()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("post", type=Path, help="Path to generated Hexo markdown post")
    parser.add_argument("--image-dir", type=Path, required=True, help="Path to Hexo source/img directory")
    args = parser.parse_args()

    errors: list[str] = []
    warnings: list[str] = []

    if not args.post.exists():
        parser.error(f"post does not exist: {args.post}")
    if not args.image_dir.exists():
        parser.error(f"image directory does not exist: {args.image_dir}")

    text = args.post.read_text(encoding="utf-8", errors="replace")
    frontmatter, body = split_frontmatter(text)
    papername = args.post.stem

    if not frontmatter:
        errors.append("missing YAML frontmatter delimited by ---")
    for key in REQUIRED_FRONTMATTER:
        if key not in frontmatter or not frontmatter[key]:
            errors.append(f"missing frontmatter field: {key}")

    cover = frontmatter.get("cover", "").strip("'\"")
    cover_filename = Path(cover).name
    if cover and not cover.startswith("/img/"):
        errors.append(f"cover should point under /img/, got {cover}")
    if cover and not cover.lower().endswith(".png"):
        errors.append(f"cover should point to a PNG image, got {cover}")
    if cover and not (args.image_dir / cover_filename).exists():
        errors.append(f"cover image file is missing: {args.image_dir / cover_filename}")

    for label in REQUIRED_METADATA:
        if f"**{label}：" not in body:
            errors.append(f"missing metadata line: **{label}：**")

    for section in REQUIRED_SECTIONS:
        content = section_body(body, section)
        if not content:
            errors.append(f"missing or empty section: ## {section}")

    images = list(IMAGE_RE.finditer(body))
    if not images:
        warnings.append("no Hexo image references found")
    seen_files: set[str] = set()
    for match in images:
        alt, filename, title = match.groups()
        stem = Path(filename).stem
        seen_files.add(filename)
        if alt != stem or title != stem:
            errors.append(f"image alt/title should match filename stem for {filename}")
        if not filename.startswith(f"{papername}-"):
            warnings.append(f"image filename does not start with {papername}-: {filename}")
        image_path = args.image_dir / filename
        if not image_path.exists():
            errors.append(f"referenced image file is missing: {image_path}")
        else:
            border_warning = has_large_outer_white_border(image_path)
            if border_warning:
                warnings.append(border_warning)

    if cover and cover_filename not in seen_files:
        warnings.append(f"cover image {cover_filename} is not inserted in the report body")

    if text.count("$$") % 2 != 0:
        errors.append("unbalanced $$ math delimiters")

    if "\ufffd" in text or "锛" in text or "鈥" in text:
        warnings.append("possible encoding artifact detected")

    for message in warnings:
        print(f"WARNING: {message}")
    for message in errors:
        print(f"ERROR: {message}", file=sys.stderr)

    if errors:
        return 1
    print("OK: Hexo paper report passed structural validation.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
