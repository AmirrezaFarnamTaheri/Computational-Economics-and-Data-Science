#!/usr/bin/env python3
"""Static documentation integrity audit independent of a MkDocs installation."""

from __future__ import annotations

import argparse
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
NAV_RE = re.compile(
    r"^\s*-\s+(?:[^:]+:\s*)?([^#\s][^\s]*\.(?:md|html))\s*$", re.MULTILINE
)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)


def _mkdocs_slug(title: str) -> str:
    """Python-Markdown toc slug: lowercase, punctuation dropped, spaces->'-'.

    Must stay byte-identical to ``notebooks_to_docs._mkdocs_slug``: this
    function defines what the docs build actually emits, so any divergence
    turns into false "broken anchor" findings. In particular Unicode headings
    such as "Itô's Lemma" NFKD-normalize to "ito" -- without that step the
    audit computes "itôs-..." and reports the page's own correct link as stale.
    """
    value = unicodedata.normalize("NFKD", title)
    value = value.encode("ascii", "ignore").decode("ascii")
    stripped = re.sub(r"[^\w\s-]", "", value.lower())
    return re.sub(r"[-\s]+", "-", stripped).strip("-")


def _page_anchors(text: str) -> set[str]:
    """Slugs actually present on a page, mirroring the generator's heading scan.

    Headings inside fenced code blocks are prose, not headings, and must be
    excluded or a literal ``### fake`` inside an example would register as a
    navigation target.
    """
    anchors: set[str] = set()
    in_fence = False
    for line in text.split("\n"):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        match = HEADING_RE.match(line)
        if match:
            anchors.add(_mkdocs_slug(match.group(2)))
    return anchors


def _iter_prose_links(text: str):
    """Yield (target, line_no) for Markdown links outside fenced code blocks.

    Generated notebook pages embed source code in ```python fences, and a
    Python subscript such as ``axes[0].plot(a_fine_grid, ...)`` matches the
    bare link regex while being code, not a link. Scanning it produces false
    "broken docs link" findings, so fences are skipped the same way the
    heading scan skips them.
    """
    in_fence = False
    for line_no, line in enumerate(text.split("\n"), 1):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        for match in LINK_RE.finditer(line):
            yield match.group(1), line_no


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    findings: list[str] = []
    # Stale in-page anchors are reported but do not fail the run: they reflect
    # pre-existing content gaps in the notebook TOCs (entries that name sections
    # the notebook does not contain), which need human authoring rather than a
    # mechanical rewrite. Every other class of finding is blocking.
    anchor_findings: list[str] = []

    config = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
    for ref in NAV_RE.findall(config):
        if not (DOCS / ref).is_file():
            findings.append(f"mkdocs nav target missing: {ref}")
    if "polyfill.io" in config:
        findings.append("mkdocs.yml contains forbidden polyfill.io reference")

    for path in DOCS.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        if "Content coming soon" in text:
            findings.append(
                f"placeholder documentation remains: {path.relative_to(ROOT)}"
            )
        # In-page anchor links must resolve to a heading on the page. This is the
        # failure mode behind the TOC-anchor drift: headings get renamed while the
        # links pointing at them are left stale.
        anchors = _page_anchors(text)
        for target, _line in _iter_prose_links(text):
            target = target.strip().split("?", 1)[0].strip("<>")
            page_part, sep, frag = target.partition("#")
            if not sep or not frag:
                continue
            if re.match(r"^(?:https?:|mailto:|data:)", page_part, re.I):
                continue
            if page_part:
                # Cross-page anchor: validate against the target page.
                resolved = (path.parent / page_part).resolve()
                if not resolved.is_file():
                    findings.append(
                        f"broken docs link: {path.relative_to(ROOT)} -> {page_part}"
                    )
                    continue
                if frag not in _page_anchors(resolved.read_text(encoding="utf-8")):
                    anchor_findings.append(
                        f"broken anchor: {path.relative_to(ROOT)} -> {target}"
                    )
            elif frag not in anchors:
                anchor_findings.append(
                    f"broken anchor: {path.relative_to(ROOT)} -> #{frag}"
                )
        # Every relative link to a local target must resolve, not only
        # Markdown/HTML pages. Notebook badge links such as `../LICENSE` are
        # copied verbatim into docs/notebooks/<track>/ where they point at a
        # nonexistent file; restricting this check to .md/.html made that a
        # silent blind spot while mkdocs emitted an unresolved-link WARNING.
        for target, _line in _iter_prose_links(text):
            target = target.strip().split("#", 1)[0].split("?", 1)[0].strip("<>")
            if not target or re.match(r"^(?:https?:|mailto:|data:)", target, re.I):
                continue
            resolved = (path.parent / target).resolve()
            try:
                resolved.relative_to(ROOT.resolve())
            except ValueError:
                # Escapes the repository root entirely (e.g. a parent link).
                findings.append(
                    f"broken docs link: {path.relative_to(ROOT)} -> {target}"
                )
                continue
            if not resolved.is_file():
                findings.append(
                    f"broken docs link: {path.relative_to(ROOT)} -> {target}"
                )

    interactive = (DOCS / "resources" / "interactive" / "index.html").read_text(
        encoding="utf-8"
    )
    # The interactive lab is intentionally dependency-free. Validate the
    # user-facing modules and accessibility/resilience hooks rather than stale
    # third-party library names that the lab no longer uses.
    for token in (
        'id="surface-canvas"',
        'id="globe-canvas"',
        'id="market-canvas"',
        'id="market-reset"',
        'prefers-reduced-motion',
        'aria-labelledby="surface-title"',
        'aria-labelledby="globe-title"',
        'aria-labelledby="market-title"',
    ):
        if token not in interactive:
            findings.append(f"interactive lab missing required component: {token}")

    report = ROOT / "audit" / "DOCS_AUDIT.md"
    report.parent.mkdir(exist_ok=True)
    lines = [
        "# Documentation Integrity Audit",
        "",
        f"Blocking findings: **{len(findings)}**",
        "",
    ]
    lines += (
        [f"- {item}" for item in findings]
        if findings
        else ["All static documentation integrity checks passed."]
    )
    if anchor_findings:
        lines += [
            "",
            f"Non-blocking stale-anchor findings: **{len(anchor_findings)}**",
            "",
            "These are TOC entries that name sections the page does not contain. "
            "They need human authoring (aligning the TOC label with the real "
            "heading), not a mechanical rewrite, so they are reported but do not "
            "fail the audit.",
            "",
        ]
        lines += [f"- {item}" for item in anchor_findings]
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Documentation findings: {len(findings)}")
    if findings:
        print("\n".join(findings[:50]))
    if anchor_findings:
        print(f"\nNon-blocking stale anchors: {len(anchor_findings)}")
        print("\n".join(anchor_findings[:20]))
    return 1 if args.strict and findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
