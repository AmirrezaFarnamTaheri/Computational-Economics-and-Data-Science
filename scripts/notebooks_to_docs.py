#!/usr/bin/env python3
"""Generate searchable MkDocs pages from every course notebook without executing it."""

from __future__ import annotations

import argparse
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS_ROOT = ROOT / "docs" / "notebooks"
REPO = (
    "https://github.com/AmirrezaFarnamTaheri/Computational-Economics-and-Data-Science"
)
RAW = "https://raw.githubusercontent.com/AmirrezaFarnamTaheri/Computational-Economics-and-Data-Science/main"
IMAGE_RE = re.compile(r"(!\[[^\]]*\]\()([^)]+)(\))")
LINK_RE = re.compile(r"(\[[^\]]+\]\()([^)]+\.ipynb(?:#[^)]*)?)(\))")
# Any other relative link to a file in the repository: README, LICENSE, data
# files, PDFs. Copied unchanged these resolve to a nonexistent path under
# docs/notebooks/<track>/, so they must be rewritten too. The lookbehind
# accepts both plain links ``[t](dest)`` and links whose text is an image,
# the badge pattern ``[![t](img)](dest)`` where the ``]`` follows a ``)``.
FILE_RE = re.compile(
    r"(?<=[)\]])\]\((?!https?://|mailto:|data:|attachment:|#)([^)]+)\)"
)

TRACKS = [
    "01-Foundations",
    "02-Numerical-Methods",
    "03-Economic-Modeling",
    "04-Macro-Models",
    "05-Micro-Models",
    "06-Econometrics",
    "07-Machine-Learning",
    "08-Time-Series",
    "09-Finance",
    "10-Specialized-Models",
    "Appendix",
    "high_performance_python",
]


def source(cell: dict) -> str:
    value = cell.get("source", "")
    return "".join(value) if isinstance(value, list) else str(value)


def rewrite_links(text: str, notebook: Path) -> str:
    def image(match: re.Match[str]) -> str:
        target = match.group(2).strip()
        if re.match(r"^(?:https?:|data:|attachment:)", target, re.I):
            return match.group(0)
        resolved = (notebook.parent / target.split("#", 1)[0]).resolve()
        try:
            rel = resolved.relative_to(ROOT.resolve()).as_posix()
        except ValueError:
            return match.group(0)
        return f"{match.group(1)}{RAW}/{rel}{match.group(3)}"

    def notebook_link(match: re.Match[str]) -> str:
        target = match.group(2)
        file_part, *anchor = target.split("#", 1)
        resolved = (notebook.parent / file_part).resolve()
        try:
            rel = resolved.relative_to(ROOT.resolve()).as_posix()
        except ValueError:
            return match.group(0)
        suffix = f"#{anchor[0]}" if anchor else ""
        return f"{match.group(1)}{REPO}/blob/main/{rel}{suffix}{match.group(3)}"

    def file_link(match: re.Match[str]) -> str:
        target = match.group(1).strip()
        file_part, _sep, _frag = target.partition("#")
        if not file_part:
            return match.group(0)
        resolved = (notebook.parent / file_part).resolve()
        try:
            rel = resolved.relative_to(ROOT.resolve()).as_posix()
        except ValueError:
            return match.group(0)
        # Only rewrite links that point at a committed file; a link to a
        # nonexistent path is a notebook-side defect and should survive
        # verbatim so the docs audit can report it.
        if not (ROOT.resolve() / rel).is_file():
            return match.group(0)
        return f"]({RAW}/{rel})"

    text = LINK_RE.sub(notebook_link, IMAGE_RE.sub(image, text))
    return FILE_RE.sub(file_link, text)


def _mkdocs_slug(title: str) -> str:
    """Slugify like Python-Markdown's toc extension used by the docs theme."""
    value = unicodedata.normalize("NFKD", title)
    value = value.encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^\w\s-]", "", value.lower())
    return re.sub(r"[-\s]+", "-", value).strip("-")


def convert_headings_and_anchors(text: str) -> str:
    """Rewrite notebook TOC anchors to the slugs the docs build generates.

    Jupyter exports headings with GitHub-style anchors (spaces become
    hyphens, dots and apostrophes are kept, e.g. ``#3.1-Probability-Spaces``).
    The Material theme slugifies headings the Python-Markdown way instead:
    punctuation is dropped outright (``3.1`` becomes ``31``).  A table of
    contents copied from the notebook therefore lands on missing anchors.
    Slugs are computed from the page's own headings when available, falling
    back to the same algorithm for cross-references.
    """
    headings: set[str] = set()
    in_code_fence = False
    out_lines: list[str] = []
    for line in text.split("\n"):
        if line.lstrip().startswith("```"):
            in_code_fence = not in_code_fence
            out_lines.append(line)
            continue
        heading = None if in_code_fence else re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
        if heading:
            headings.add(heading.group(2))
        out_lines.append(line)
    body = "\n".join(out_lines)

    def anchor(match: re.Match[str]) -> str:
        name = match.group(2)[1:]
        slug = _mkdocs_slug(name if name not in headings else name)
        return f"{match.group(1)}#{slug}{match.group(3)}"

    return re.sub(r"(\[[^\]]*\]\()(#[^)\s]+)(\))", anchor, body)


def convert(notebook: Path) -> str:
    nb = json.loads(notebook.read_text(encoding="utf-8"))
    rel = notebook.relative_to(ROOT).as_posix()
    lines = [
        "<!-- AUTO-GENERATED by scripts/notebooks_to_docs.py; edit the notebook source instead. -->",
        "",
        f"> **Source notebook:** [`{rel}`]({REPO}/blob/main/{rel})",
        "",
        "> Notebook outputs are intentionally omitted from the documentation build; code and narrative remain source-faithful.",
        "",
    ]
    for cell in nb.get("cells", []):
        text = source(cell).rstrip()
        if not text:
            continue
        if cell.get("cell_type") == "markdown":
            lines += [rewrite_links(convert_headings_and_anchors(text), notebook), ""]
        elif cell.get("cell_type") == "code":
            lines += ["```python", text, "```", ""]
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--clean", action="store_true")
    args = parser.parse_args()
    if args.clean and DOCS_ROOT.exists():
        import shutil

        shutil.rmtree(DOCS_ROOT)
    written = 0
    for track in TRACKS:
        for notebook in sorted((ROOT / track).glob("*.ipynb")):
            target = DOCS_ROOT / track / f"{notebook.stem}.md"
            target.parent.mkdir(parents=True, exist_ok=True)
            # Explicit LF: this output is diffed byte-for-byte against the
            # committed pages by the CI staleness guard, and on Windows
            # write_text would otherwise emit CRLF via os.linesep.
            target.write_text(convert(notebook), encoding="utf-8", newline="\n")
            written += 1
    print(
        f"Generated {written} notebook documentation pages in {DOCS_ROOT.relative_to(ROOT)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
