#!/usr/bin/env python3
"""Render each tracks/<NN-name>/README.md into a published web page under
docs/tracks/<NN-name>.html.

The curriculum markdown under tracks/ is the single source of truth; these HTML
pages are a regenerable rendering of it, so the two never drift. This script is
an OPTIONAL authoring convenience — deploying the site needs no build step, it
just serves the committed docs/. Re-run after editing any track README:

    python3 tools/build_track_pages.py

Handles the small Markdown subset the maps use: #/## headings, GFM tables,
unordered lists, blockquotes, paragraphs, and inline **bold**, `code`, [links].
No third-party dependencies.
"""
from __future__ import annotations
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TRACKS = ROOT / "tracks"
OUT = ROOT / "docs" / "tracks"

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — Plaintext</title>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@300;400;600;700&family=IBM+Plex+Sans:wght@300;400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="track.css">
</head>
<body>
<nav>
  <a class="logo" href="../index.html">plain<span>text</span></a>
  <a class="back" href="../index.html">← all tracks</a>
</nav>
<main>
{body}
</main>
<footer>
  <div class="logo-small">plain<span>text</span></div>
  <div>Open security education for everyone · CC BY 4.0</div>
</footer>
</body>
</html>
"""

INLINE = [
    (re.compile(r"\*\*(.+?)\*\*"), r"<strong>\1</strong>"),
    (re.compile(r"\*([^*\n]+?)\*"), r"<em>\1</em>"),
    (re.compile(r"`([^`]+?)`"), r"<code>\1</code>"),
    (re.compile(r"\[([^\]]+?)\]\((https?://[^)]+?)\)"), r'<a href="\2">\1</a>'),
]


def inline(text: str) -> str:
    text = html.escape(text, quote=False)
    for pattern, repl in INLINE:
        text = pattern.sub(repl, text)
    return text


def cells(row: str) -> list[str]:
    parts = [c.strip() for c in row.strip().strip("|").split("|")]
    return parts


def convert(md: str) -> tuple[str, str]:
    lines = md.splitlines()
    out: list[str] = []
    para: list[str] = []
    title = "Track"
    i = 0

    def flush_para() -> None:
        if para:
            out.append("<p>" + inline(" ".join(para)) + "</p>")
            para.clear()

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Tables: a header row followed by a |---| separator.
        if stripped.startswith("|") and i + 1 < len(lines) and re.match(
            r"^\s*\|[\s:|-]+\|\s*$", lines[i + 1]
        ):
            flush_para()
            header = cells(stripped)
            out.append("<table><thead><tr>"
                       + "".join(f"<th>{inline(c)}</th>" for c in header)
                       + "</tr></thead><tbody>")
            i += 2
            while i < len(lines) and lines[i].strip().startswith("|"):
                out.append("<tr>" + "".join(
                    f"<td>{inline(c)}</td>" for c in cells(lines[i].strip())
                ) + "</tr>")
                i += 1
            out.append("</tbody></table>")
            continue

        # Blockquote (one or more consecutive > lines).
        if stripped.startswith(">"):
            flush_para()
            buf: list[str] = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                buf.append(lines[i].strip().lstrip(">").strip())
                i += 1
            out.append("<blockquote>" + inline(" ".join(buf)) + "</blockquote>")
            continue

        # Unordered list.
        if stripped.startswith("- "):
            flush_para()
            out.append("<ul>")
            while i < len(lines) and lines[i].strip().startswith("- "):
                out.append("<li>" + inline(lines[i].strip()[2:]) + "</li>")
                i += 1
            out.append("</ul>")
            continue

        # Headings.
        if stripped.startswith("## "):
            flush_para()
            out.append("<h2>" + inline(stripped[3:]) + "</h2>")
            i += 1
            continue
        if stripped.startswith("# "):
            flush_para()
            title = stripped[2:].strip()
            out.append("<h1>" + inline(stripped[2:]) + "</h1>")
            i += 1
            continue

        # Blank line ends a paragraph.
        if not stripped:
            flush_para()
            i += 1
            continue

        para.append(stripped)
        i += 1

    flush_para()
    return title, "\n".join(out)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    built = []
    for track_dir in sorted(p for p in TRACKS.iterdir() if p.is_dir()):
        readme = track_dir / "README.md"
        if not readme.exists():
            continue
        title, body = convert(readme.read_text())
        page = PAGE.format(title=html.escape(title), body=body)
        dest = OUT / f"{track_dir.name}.html"
        dest.write_text(page)
        built.append(dest.relative_to(ROOT).as_posix())
    print(f"Built {len(built)} track page(s):")
    for b in built:
        print(f"  {b}")


if __name__ == "__main__":
    main()
