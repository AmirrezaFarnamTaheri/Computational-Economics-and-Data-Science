#!/usr/bin/env python3
"""Generate searchable MkDocs pages from every course notebook without executing it."""

from __future__ import annotations

import argparse
import functools
import json
import os
import re
import subprocess
import unicodedata
from pathlib import Path

try:
    from scripts.image_provenance import provenance_for
except ImportError:
    from image_provenance import provenance_for

ROOT = Path(__file__).resolve().parents[1]
DOCS_ROOT = ROOT / "docs" / "notebooks"
REPO = (
    "https://github.com/AmirrezaFarnamTaheri/Computational-Economics-and-Data-Science"
)
RAW_BASE = "https://raw.githubusercontent.com/AmirrezaFarnamTaheri/Computational-Economics-and-Data-Science"
# Stable fallback for source archives that do not contain .git metadata.
# In a Git checkout, each link is pinned to the last commit that changed the
# linked path, so generated documentation never depends on mutable `main`.
PERMALINK_FALLBACK = os.environ.get(
    "DOCS_SOURCE_REF", "287dc86d99e95e5cb443b191e584d900f699157c"
)
RAW = f"{RAW_BASE}/{PERMALINK_FALLBACK}"
IMAGE_RE = re.compile(r"(!\[[^\]]*\]\()([^)]+)(\))")
HTML_IMAGE_RE = re.compile(
    r"""(<img\b[^>]*\bsrc=["'])([^"']+)(["'][^>]*>)""",
    re.IGNORECASE,
)
LINK_RE = re.compile(r"(\[[^\]]+\]\()([^)]+\.ipynb(?:#[^)]*)?)(\))")
# Any other relative link to a file in the repository: README, LICENSE, data
# files, PDFs. Copied unchanged these resolve to a nonexistent path under
# docs/notebooks/<track>/, so they must be rewritten too. The lookbehind
# accepts both plain links ``[t](dest)`` and links whose text is an image,
# the badge pattern ``[![t](img)](dest)`` where the ``]`` follows a ``)``.
BADGE_FILE_RE = re.compile(
    r"(?<=[)\]])\]\((?!https?://|mailto:|data:|attachment:|#)([^)]+)\)"
)
PLAIN_FILE_RE = re.compile(
    r"(?<!!)\[[^\]]+\]\((?!https?://|mailto:|data:|attachment:|#)([^)]+)\)"
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


@functools.lru_cache(maxsize=None)
def path_revision(path_text: str) -> str:
    """Return the immutable commit that most recently changed a repository path."""
    path = Path(path_text).resolve()
    try:
        rel = path.relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return PERMALINK_FALLBACK
    try:
        completed = subprocess.run(
            ["git", "log", "-1", "--format=%H", "--", rel],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return PERMALINK_FALLBACK
    return completed.stdout.strip() or PERMALINK_FALLBACK


def raw_url(path: Path) -> str:
    """Build an immutable raw-content URL for a repository file."""
    resolved = path.resolve()
    rel = resolved.relative_to(ROOT.resolve()).as_posix()
    return f"{RAW_BASE}/{path_revision(str(resolved))}/{rel}"


def blob_url(path: Path) -> str:
    """Build an immutable GitHub browser URL for a repository file."""
    resolved = path.resolve()
    rel = resolved.relative_to(ROOT.resolve()).as_posix()
    return f"{REPO}/blob/{path_revision(str(resolved))}/{rel}"


def notebook_docs_target(
    notebook: Path, target: Path, anchor: str | None = None
) -> str:
    """Return a local MkDocs source link for a notebook-to-notebook reference."""
    current_doc = DOCS_ROOT / notebook.relative_to(ROOT).with_suffix(".md")
    target_doc = DOCS_ROOT / target.relative_to(ROOT).with_suffix(".md")
    relative = os.path.relpath(target_doc, start=current_doc.parent).replace(
        os.sep, "/"
    )
    if anchor:
        relative += f"#{_mkdocs_slug(anchor)}"
    return relative


def source(cell: dict) -> str:
    value = cell.get("source", "")
    return "".join(value) if isinstance(value, list) else str(value)


def rewrite_links(
    text: str, notebook: Path, *, enforce_provenance: bool = False
) -> str:
    def repository_file_url(target: str) -> str | None:
        file_part, _sep, _frag = target.strip().partition("#")
        if not file_part:
            return None
        resolved = (notebook.parent / file_part).resolve()
        try:
            rel = resolved.relative_to(ROOT.resolve()).as_posix()
        except ValueError:
            return None
        # Only rewrite links that point at a committed/local repository file;
        # nonexistent paths must remain visible so the docs audit can flag them.
        if not (ROOT.resolve() / rel).is_file():
            return None
        return raw_url(ROOT / rel)

    def provenance_block(resolved: Path) -> str:
        rel = resolved.relative_to(ROOT.resolve()).as_posix()
        return (
            '<div class="figure-provenance-blocked" role="note">'
            "<strong>Figure omitted from the published reading site.</strong> "
            f"Provenance for <code>{rel}</code> is not yet verified. "
            "The local source notebook retains the asset for provenance review."
            "</div>"
        )

    def image(match: re.Match[str]) -> str:
        target = match.group(2).strip()
        if re.match(r"^(?:https?:|data:|attachment:)", target, re.I):
            return match.group(0)
        resolved = (notebook.parent / target.split("#", 1)[0]).resolve()
        try:
            rel = resolved.relative_to(ROOT.resolve()).as_posix()
        except ValueError:
            return match.group(0)
        if enforce_provenance and not provenance_for(resolved).publishable:
            return provenance_block(resolved)
        return f"{match.group(1)}{raw_url(ROOT / rel)}{match.group(3)}"

    def html_image(match: re.Match[str]) -> str:
        target = match.group(2).strip()
        if re.match(r"^(?:https?:|data:|attachment:)", target, re.I):
            return match.group(0)
        resolved = (notebook.parent / target.split("#", 1)[0]).resolve()
        try:
            rel = resolved.relative_to(ROOT.resolve()).as_posix()
        except ValueError:
            return match.group(0)
        if enforce_provenance and not provenance_for(resolved).publishable:
            return provenance_block(resolved)
        return f"{match.group(1)}{raw_url(ROOT / rel)}{match.group(3)}"

    def notebook_link(match: re.Match[str]) -> str:
        target = match.group(2)
        file_part, *anchor = target.split("#", 1)
        resolved = (notebook.parent / file_part).resolve()
        try:
            rel = resolved.relative_to(ROOT.resolve()).as_posix()
        except ValueError:
            return match.group(0)
        target_path = ROOT / rel
        if not target_path.is_file():
            return match.group(0)
        target = notebook_docs_target(
            notebook,
            target_path,
            anchor[0] if anchor else None,
        )
        return f"{match.group(1)}{target}{match.group(3)}"

    def badge_file_link(match: re.Match[str]) -> str:
        target = match.group(1).strip()
        url = repository_file_url(target)
        return match.group(0) if url is None else f"]({url})"

    def plain_file_link(match: re.Match[str]) -> str:
        target = match.group(1).strip()
        url = repository_file_url(target)
        if url is None:
            return match.group(0)
        prefix = match.group(0).rsplit("](", 1)[0]
        return f"{prefix}]({url})"

    text = IMAGE_RE.sub(image, text)
    text = HTML_IMAGE_RE.sub(html_image, text)
    text = LINK_RE.sub(notebook_link, text)
    text = BADGE_FILE_RE.sub(badge_file_link, text)
    return PLAIN_FILE_RE.sub(plain_file_link, text)


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


ANSI_ESCAPE_RE = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")


def output_text(value: object) -> str:
    """Normalize the list-or-string text representation used by nbformat."""
    if isinstance(value, list):
        return "".join(str(part) for part in value)
    return str(value)


def render_saved_output(output: dict, cell_id: str, index: int) -> list[str]:
    """Render one saved Jupyter output into portable Markdown/HTML.

    Rich outputs choose one highest-fidelity representation to avoid publishing
    the same result twice. PNG/SVG plots are embedded so the reading edition
    carries the actual saved evidence instead of silently dropping it.
    """
    output_type = output.get("output_type")
    label = f"Saved output from cell {cell_id or 'unknown'}, result {index + 1}"

    if output_type == "stream":
        value = ANSI_ESCAPE_RE.sub("", output_text(output.get("text", ""))).rstrip()
        return [] if not value else ["~~~text", value, "~~~", ""]

    if output_type == "error":
        traceback = output.get("traceback") or []
        value = "\n".join(
            ANSI_ESCAPE_RE.sub("", str(line)) for line in traceback
        ).rstrip()
        if not value:
            value = (
                f"{output.get('ename', 'Error')}: {output.get('evalue', '')}".rstrip()
            )
        return [
            f"> **Saved execution error — {label}.**",
            "",
            "~~~text",
            value,
            "~~~",
            "",
        ]

    if output_type not in {"display_data", "execute_result"}:
        return []

    data = output.get("data") or {}
    if "text/markdown" in data:
        value = output_text(data["text/markdown"]).rstrip()
        return [] if not value else [f"> **{label}.**", "", value, ""]

    if "image/svg+xml" in data:
        svg = output_text(data["image/svg+xml"]).strip()
        return (
            [] if not svg else [f'<figure aria-label="{label}">', svg, "</figure>", ""]
        )

    if "image/png" in data:
        payload = output_text(data["image/png"]).replace("\n", "").strip()
        if not payload:
            return []
        return [
            f'<img src="data:image/png;base64,{payload}" alt="{label}" '
            'loading="lazy" decoding="async">',
            "",
        ]

    if "image/jpeg" in data:
        payload = output_text(data["image/jpeg"]).replace("\n", "").strip()
        if not payload:
            return []
        return [
            f'<img src="data:image/jpeg;base64,{payload}" alt="{label}" '
            'loading="lazy" decoding="async">',
            "",
        ]

    if "text/plain" in data:
        value = ANSI_ESCAPE_RE.sub("", output_text(data["text/plain"])).rstrip()
        return [] if not value else ["~~~text", value, "~~~", ""]

    return []


def render_cell_outputs(cell: dict) -> list[str]:
    """Render all saved outputs attached to one code cell."""
    rendered: list[str] = []
    cell_id = str(cell.get("id", ""))
    for index, output in enumerate(cell.get("outputs") or []):
        rendered.extend(render_saved_output(output, cell_id, index))
    return rendered


def convert(notebook: Path) -> str:
    nb = json.loads(notebook.read_text(encoding="utf-8"))
    rel = notebook.relative_to(ROOT).as_posix()
    lines = [
        "<!-- AUTO-GENERATED by scripts/notebooks_to_docs.py; edit the notebook source instead. -->",
        "",
        f"> **Source notebook:** [`{rel}`]({blob_url(notebook)})",
        "",
        "> Saved notebook outputs are included when a portable representation is available, so plots, tables, diagnostics, and printed results remain visible in the reading edition.",
        "",
    ]
    for cell in nb.get("cells", []):
        text = source(cell).rstrip()
        if not text:
            continue
        if cell.get("cell_type") == "markdown":
            lines += [
                rewrite_links(
                    convert_headings_and_anchors(text),
                    notebook,
                    enforce_provenance=True,
                ),
                "",
            ]
        elif cell.get("cell_type") == "code":
            lines += ["```python", text, "```", ""]
            lines += render_cell_outputs(cell)
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
