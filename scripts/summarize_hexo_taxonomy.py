#!/usr/bin/env python3
"""Summarize tags and categories used by Hexo markdown posts."""

from __future__ import annotations

import argparse
import collections
import json
import re
from pathlib import Path


def parse_scalar_list(value: str) -> list[str]:
    value = value.strip()
    if not value:
        return []
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [item.strip().strip("'\"") for item in inner.split(",") if item.strip()]
    return [value.strip().strip("'\"")]


def parse_frontmatter(text: str) -> dict[str, list[str] | str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}

    end = None
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end = i
            break
    if end is None:
        return {}

    data: dict[str, list[str] | str] = {}
    current_key: str | None = None
    list_items: list[str] = []

    for raw in lines[1:end]:
        line = raw.rstrip()
        if not line.strip():
            continue
        item_match = re.match(r"^\s*-\s*(.+?)\s*$", line)
        if item_match and current_key:
            list_items.append(item_match.group(1).strip().strip("'\""))
            data[current_key] = list_items[:]
            continue

        key_match = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if not key_match:
            current_key = None
            continue

        key, value = key_match.group(1), key_match.group(2)
        current_key = key
        if value.strip():
            parsed = parse_scalar_list(value)
            data[key] = parsed if key in {"tags", "categories"} else value.strip().strip("'\"")
            list_items = []
        else:
            list_items = []
            data[key] = list_items

    return data


def values_for(data: dict[str, list[str] | str], key: str) -> list[str]:
    value = data.get(key)
    if value is None:
        return []
    if isinstance(value, list):
        return [v for v in value if v]
    return [value] if value else []


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("posts_dir", type=Path, help="Path to Hexo source/_posts directory")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of Markdown")
    args = parser.parse_args()

    if not args.posts_dir.exists():
        parser.error(f"posts directory does not exist: {args.posts_dir}")

    tag_counts: collections.Counter[str] = collections.Counter()
    category_counts: collections.Counter[str] = collections.Counter()
    post_count = 0

    for path in sorted(args.posts_dir.glob("*.md")):
        text = path.read_text(encoding="utf-8", errors="replace")
        frontmatter = parse_frontmatter(text)
        if not frontmatter:
            continue
        post_count += 1
        tag_counts.update(values_for(frontmatter, "tags"))
        category_counts.update(values_for(frontmatter, "categories"))

    result = {
        "posts_scanned": post_count,
        "categories": category_counts.most_common(),
        "tags": tag_counts.most_common(),
    }

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    print(f"# Hexo taxonomy summary\n\nPosts scanned: {post_count}\n")
    print("## Categories")
    for name, count in category_counts.most_common():
        print(f"- {name}: {count}")
    print("\n## Tags")
    for name, count in tag_counts.most_common():
        print(f"- {name}: {count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
