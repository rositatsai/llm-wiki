#!/usr/bin/env python3
"""LLM Wiki — Static site builder.

Reads wiki/ Markdown files, resolves [[wikilinks]], generates a static HTML site
with tag-based navigation, full-text search index, and cross-references.

Usage:  python build.py
Output: site/
"""

import json
import os
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

import yaml
import markdown as md

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent
WIKI_DIR = ROOT / "wiki"
TMPL_DIR = ROOT / "templates"
STATIC_DIR = ROOT / "static"
SITE_DIR = ROOT / "site"

TYPE_LABELS = {
    "concept": "概念",
    "entity": "實體",
    "summary": "摘要",
    "analysis": "分析",
}
TYPE_ORDER = ["analysis", "concept", "summary", "entity"]

# ---------------------------------------------------------------------------
# Phase A: Parse all wiki pages
# ---------------------------------------------------------------------------

def parse_page(path: Path) -> dict:
    """Parse a wiki .md file into {slug, meta, body}."""
    text = path.read_text(encoding="utf-8")
    slug = path.stem  # filename without .md

    # Split YAML frontmatter
    meta = {}
    body = text
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            meta = yaml.safe_load(parts[1]) or {}
            body = parts[2].strip()

    return {
        "slug": slug,
        "title": meta.get("title", slug),
        "type": meta.get("type", "page"),
        "created": str(meta.get("created", "")),
        "updated": str(meta.get("updated", "")),
        "tags": meta.get("tags", []) or [],
        "sources": meta.get("sources", []) or [],
        "body_md": body,
        "path": path,
    }


def load_all_pages() -> dict:
    """Walk wiki/ and return {slug: page_dict}."""
    pages = {}
    for md_file in WIKI_DIR.rglob("*.md"):
        page = parse_page(md_file)
        pages[page["slug"]] = page
    return pages

# ---------------------------------------------------------------------------
# Phase B: Build indices
# ---------------------------------------------------------------------------

def build_indices(pages):
    tag_index = {}       # tag -> [slug, ...]
    type_index = {}      # type -> [slug, ...]
    slug_to_title = {}   # slug -> title

    for slug, p in pages.items():
        slug_to_title[slug] = p["title"]
        type_index.setdefault(p["type"], []).append(slug)
        for tag in p["tags"]:
            tag_index.setdefault(tag, []).append(slug)

    return tag_index, type_index, slug_to_title

# ---------------------------------------------------------------------------
# Phase C: Resolve wikilinks & render Markdown
# ---------------------------------------------------------------------------

WIKILINK_RE = re.compile(r"\[\[([^\]|]+?)(?:\|([^\]]+?))?\]\]")


def resolve_wikilinks(body_md, slug_to_title, current_slug=None):
    """Replace [[slug|display]] with HTML links. Return (html_body, set_of_targets)."""
    targets = set()

    def replacer(m):
        target_slug = m.group(1).strip()
        display = m.group(2) or slug_to_title.get(target_slug, target_slug)
        display = display.strip()
        targets.add(target_slug)
        if target_slug in slug_to_title:
            return f'<a href="{target_slug}.html" class="wikilink">{display}</a>'
        else:
            return f'<span class="broken-link" title="Page not found: {target_slug}">{display}</span>'

    resolved = WIKILINK_RE.sub(replacer, body_md)
    return resolved, targets


def render_markdown(body_md):
    """Convert Markdown to HTML."""
    extensions = ["tables", "fenced_code", "toc", "nl2br"]
    return md.markdown(body_md, extensions=extensions)

# ---------------------------------------------------------------------------
# Phase D: Generate HTML
# ---------------------------------------------------------------------------

def load_template(name):
    return (TMPL_DIR / name).read_text(encoding="utf-8")


def fill(template, **kwargs):
    """Simple {{key}} replacement."""
    result = template
    for k, v in kwargs.items():
        result = result.replace("{{" + k + "}}", str(v))
    return result


def build_tag_cloud_html(tag_index, root=""):
    """Generate tag pill links for the sidebar."""
    sorted_tags = sorted(tag_index.items(), key=lambda x: -len(x[1]))
    pills = []
    for tag, slugs in sorted_tags:
        count = len(slugs)
        pills.append(
            f'<a href="{root}tag/{tag}.html" class="tag-pill" data-tag="{tag}">'
            f'{tag} <small>({count})</small></a>'
        )
    return "\n".join(pills)


def build_backlinks(pages, slug_to_title):
    """Compute backlinks for every page."""
    backlinks = {slug: set() for slug in pages}
    for slug, p in pages.items():
        _, targets = resolve_wikilinks(p["body_md"], slug_to_title, slug)
        for t in targets:
            if t in backlinks:
                backlinks[t].add(slug)
    return backlinks


def render_page(page, pages, slug_to_title, backlinks, tag_index, base_tmpl, page_tmpl, build_time):
    slug = page["slug"]
    ptype = page["type"]

    # Resolve wikilinks and render body
    resolved_md, _ = resolve_wikilinks(page["body_md"], slug_to_title, slug)
    body_html = render_markdown(resolved_md)

    # Tags
    tags_html = " ".join(
        f'<a href="tag/{t}.html" class="tag-pill">{t}</a>' for t in page["tags"]
    )

    # Backlinks
    bl = backlinks.get(slug, set())
    if bl:
        bl_items = "".join(
            f'<li><a href="{s}.html" class="wikilink">{slug_to_title.get(s, s)}</a></li>'
            for s in sorted(bl)
        )
        backlinks_section = (
            f'<div class="backlinks"><h2>🔗 反向連結</h2><ul>{bl_items}</ul></div>'
        )
    else:
        backlinks_section = ""

    # Sources
    if page["sources"]:
        src_items = "".join(f"<li>{s}</li>" for s in page["sources"])
        sources_section = (
            f'<div class="sources-section"><h2>📎 來源</h2><ul>{src_items}</ul></div>'
        )
    else:
        sources_section = ""

    inner = fill(
        page_tmpl,
        title=page["title"],
        type=ptype,
        type_label=TYPE_LABELS.get(ptype, ptype),
        created=page["created"],
        updated=page["updated"],
        tags_html=tags_html,
        body=body_html,
        backlinks_section=backlinks_section,
        sources_section=sources_section,
    )

    return fill(
        base_tmpl,
        title=page["title"],
        root="",
        tag_cloud=build_tag_cloud_html(tag_index),
        content=inner,
        build_time=build_time,
    )


def render_index(pages, tag_index, type_index, slug_to_title, base_tmpl, index_tmpl, build_time):
    total_raw = 24
    total_wiki = len(pages)

    sections_html = ""
    for t in TYPE_ORDER:
        slugs = type_index.get(t, [])
        if not slugs:
            continue
        label = TYPE_LABELS.get(t, t)
        cards = ""
        for s in sorted(slugs, key=lambda x: pages[x]["title"]):
            p = pages[s]
            tag_pills = "".join(
                f'<span class="tag-pill">{tg}</span>' for tg in p["tags"]
            )
            tags_csv = ",".join(p["tags"])
            cards += (
                f'<div class="page-card" data-tags="{tags_csv}">'
                f'<span class="type-badge type-{t}">{label}</span> '
                f'<a href="{s}.html">{p["title"]}</a>'
                f'<div class="pc-tags">{tag_pills}</div>'
                f'</div>\n'
            )
        sections_html += (
            f'<div class="index-section" id="type-{t}">'
            f'<h2>{label}（{len(slugs)}）</h2>{cards}</div>\n'
        )

    inner = fill(
        index_tmpl,
        stats_line=f"{total_raw} 筆原始來源 · {total_wiki} 頁 Wiki · 4 大知識主軸",
        sections=sections_html,
    )

    return fill(
        base_tmpl,
        title="首頁",
        root="",
        tag_cloud=build_tag_cloud_html(tag_index),
        content=inner,
        build_time=build_time,
    )


def render_tag_page(tag, slugs, pages, tag_index, slug_to_title, base_tmpl, tag_tmpl, build_time):
    cards = ""
    for s in sorted(slugs, key=lambda x: pages[x]["title"]):
        p = pages[s]
        t = p["type"]
        label = TYPE_LABELS.get(t, t)
        tag_pills = "".join(
            f'<span class="tag-pill">{tg}</span>' for tg in p["tags"]
        )
        cards += (
            f'<div class="page-card">'
            f'<span class="type-badge type-{t}">{label}</span> '
            f'<a href="../{s}.html">{p["title"]}</a>'
            f'<div class="pc-tags">{tag_pills}</div>'
            f'</div>\n'
        )

    inner = fill(tag_tmpl, tag=tag, count=str(len(slugs)), pages_html=cards)

    return fill(
        base_tmpl,
        title=f"標籤：{tag}",
        root="../",
        tag_cloud=build_tag_cloud_html(tag_index, root="../"),
        content=inner,
        build_time=build_time,
    )


def render_type_page(type_key, slugs, pages, tag_index, slug_to_title, base_tmpl, tag_tmpl, build_time):
    label = TYPE_LABELS.get(type_key, type_key)
    cards = ""
    for s in sorted(slugs, key=lambda x: pages[x]["title"]):
        p = pages[s]
        tag_pills = "".join(
            f'<span class="tag-pill">{tg}</span>' for tg in p["tags"]
        )
        cards += (
            f'<div class="page-card">'
            f'<span class="type-badge type-{type_key}">{label}</span> '
            f'<a href="../{s}.html">{p["title"]}</a>'
            f'<div class="pc-tags">{tag_pills}</div>'
            f'</div>\n'
        )

    inner = fill(tag_tmpl, tag=f"{label}類頁面", count=str(len(slugs)), pages_html=cards)

    return fill(
        base_tmpl,
        title=f"分類：{label}",
        root="../",
        tag_cloud=build_tag_cloud_html(tag_index, root="../"),
        content=inner,
        build_time=build_time,
    )


def build_search_index(pages):
    """Generate JSON search index."""
    index = []
    for slug, p in pages.items():
        # Strip markdown formatting for plain text
        body_text = p["body_md"][:2000]
        body_text = re.sub(r"\[([^\]]*)\]\([^\)]*\)", r"\1", body_text)  # links
        body_text = re.sub(r"\[\[([^\]|]*?)(?:\|([^\]]*?))?\]\]", lambda m: m.group(2) or m.group(1), body_text)
        body_text = re.sub(r"[#*_`>|]", "", body_text)
        body_text = re.sub(r"\s+", " ", body_text).strip()
        index.append({
            "slug": slug,
            "title": p["title"],
            "type": p["type"],
            "tags": p["tags"],
            "body": body_text,
        })
    return index

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    build_time = datetime.now().strftime("%Y-%m-%d %H:%M")
    print(f"[build] LLM Wiki static site builder — {build_time}")

    # Load pages
    pages = load_all_pages()
    print(f"[build] Loaded {len(pages)} wiki pages")

    # Build indices
    tag_index, type_index, slug_to_title = build_indices(pages)
    print(f"[build] {len(tag_index)} tags, {len(type_index)} types")

    # Backlinks
    backlinks = build_backlinks(pages, slug_to_title)

    # Load templates
    base_tmpl = load_template("base.html")
    page_tmpl = load_template("page.html")
    index_tmpl = load_template("index_page.html")
    tag_tmpl = load_template("tag_page.html")

    # Prepare output
    if SITE_DIR.exists():
        shutil.rmtree(SITE_DIR)
    SITE_DIR.mkdir(parents=True)
    (SITE_DIR / "tag").mkdir()
    (SITE_DIR / "type").mkdir()

    # Copy static assets
    for f in STATIC_DIR.iterdir():
        shutil.copy2(f, SITE_DIR / f.name)
    print("[build] Copied static assets")

    # Render wiki pages
    for slug, page in pages.items():
        html = render_page(page, pages, slug_to_title, backlinks, tag_index, base_tmpl, page_tmpl, build_time)
        (SITE_DIR / f"{slug}.html").write_text(html, encoding="utf-8")
    print(f"[build] Rendered {len(pages)} pages")

    # Render index
    html = render_index(pages, tag_index, type_index, slug_to_title, base_tmpl, index_tmpl, build_time)
    (SITE_DIR / "index.html").write_text(html, encoding="utf-8")

    # Render tag pages
    for tag, slugs in tag_index.items():
        html = render_tag_page(tag, slugs, pages, tag_index, slug_to_title, base_tmpl, tag_tmpl, build_time)
        (SITE_DIR / "tag" / f"{tag}.html").write_text(html, encoding="utf-8")
    print(f"[build] Rendered {len(tag_index)} tag pages")

    # Render type pages
    for type_key, slugs in type_index.items():
        html = render_type_page(type_key, slugs, pages, tag_index, slug_to_title, base_tmpl, tag_tmpl, build_time)
        (SITE_DIR / "type" / f"{type_key}.html").write_text(html, encoding="utf-8")
    print(f"[build] Rendered {len(type_index)} type pages")

    # Search index
    search_data = build_search_index(pages)
    (SITE_DIR / "search-index.json").write_text(
        json.dumps(search_data, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print("[build] Generated search-index.json")

    # Tags JSON
    tags_json = {tag: len(slugs) for tag, slugs in tag_index.items()}
    (SITE_DIR / "tags.json").write_text(
        json.dumps(tags_json, ensure_ascii=False), encoding="utf-8"
    )

    print(f"[build] Done! Site output → {SITE_DIR}")
    print(f"[build] Preview: python -m http.server 8080 --directory \"{SITE_DIR}\"")


if __name__ == "__main__":
    main()
