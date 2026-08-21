#!/usr/bin/env python3
"""Static documentation integrity audit independent of a MkDocs installation."""
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
NAV_RE = re.compile(r"^\s*-\s+(?:[^:]+:\s*)?([^#\s][^\s]*\.(?:md|html))\s*$", re.MULTILINE)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    findings: list[str] = []

    config = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
    for ref in NAV_RE.findall(config):
        if not (DOCS / ref).is_file():
            findings.append(f"mkdocs nav target missing: {ref}")
    if "polyfill.io" in config:
        findings.append("mkdocs.yml contains forbidden polyfill.io reference")

    for path in DOCS.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        if "Content coming soon" in text:
            findings.append(f"placeholder documentation remains: {path.relative_to(ROOT)}")
        # Generated notebook pages intentionally contain source-faithful prose and
        # many external links; only validate documentation-local page links there.
        for target in LINK_RE.findall(text):
            target = target.strip().split("#", 1)[0].split("?", 1)[0].strip("<>")
            if not target or re.match(r"^(?:https?:|mailto:|data:)", target, re.I):
                continue
            if not target.endswith((".md", ".html")):
                continue
            resolved = (path.parent / target).resolve()
            if not resolved.is_file():
                findings.append(f"broken docs link: {path.relative_to(ROOT)} -> {target}")

    interactive = (DOCS / "resources" / "interactive" / "index.html").read_text(encoding="utf-8")
    for token in ("three.min.js", "cobe", "mermaid", "matter-js", "market-reset"):
        if token not in interactive:
            findings.append(f"interactive lab missing required component: {token}")

    report = ROOT / "audit" / "DOCS_AUDIT.md"
    report.parent.mkdir(exist_ok=True)
    lines = ["# Documentation Integrity Audit", "", f"Blocking findings: **{len(findings)}**", ""]
    lines += ([f"- {item}" for item in findings] if findings else ["All static documentation integrity checks passed."])
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Documentation findings: {len(findings)}")
    if findings:
        print("\n".join(findings[:50]))
    return 1 if args.strict and findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
