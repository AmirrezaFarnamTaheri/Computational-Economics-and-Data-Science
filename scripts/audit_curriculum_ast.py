#!/usr/bin/env python3
"""Repository-wide structural and syntax audit for curriculum notebooks.

The audit is intentionally static: it validates every notebook without importing or
executing optional scientific stacks. Runtime execution is a separate verification
layer because many advanced notebooks require network, GPU, or system dependencies.
"""
from __future__ import annotations

import argparse
import ast
import json
import re
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

try:
    from IPython.core.inputtransformer2 import TransformerManager
except ImportError:  # pragma: no cover - fallback is exercised in minimal CI images
    TransformerManager = None

IMAGE_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
CODE_IMAGE_RE = re.compile(r"Image\(\s*filename\s*=\s*[rRuUfF]*[\"']([^\"']+)[\"']")
PLACEHOLDER_RE = re.compile(
    r"\b(?:TODO|FIXME)\b|implementation would go here|raise\s+NotImplementedError",
    re.IGNORECASE,
)
BLANKET_WARNING_RE = re.compile(
    r"warnings\.filterwarnings\(\s*['\"]ignore['\"]\s*\)"
)

REQUIRED_SECTIONS = {
    "lens": re.compile(r"^##\s+The Lens(?::|\s|$)", re.MULTILINE | re.IGNORECASE),
    "objectives": re.compile(r"^#{1,4}\s+(?:\d+(?:\.\d+)*[.)]?\s+)?Learning Objectives\b", re.MULTILINE | re.IGNORECASE),
    "prerequisites": re.compile(r"^#{1,4}\s+(?:\d+(?:\.\d+)*[.)]?\s+)?Prerequisites\b", re.MULTILINE | re.IGNORECASE),
    "toc": re.compile(r"^#{1,4}\s+(?:\d+(?:\.\d+)*[.)]?\s+)?Table of Contents\b", re.MULTILINE | re.IGNORECASE),
    "exercises": re.compile(r"^#{1,4}\s+(?:\d+(?:\.\d+)*[.)]?\s+)?(?:.*\bExercises?\b|Test Your Knowledge\b)", re.MULTILINE | re.IGNORECASE),
    "summary": re.compile(r"^#{1,4}\s+(?:\d+(?:\.\d+)*[.)]?\s+)?(?:Summary|Summary & Key Takeaways)\b", re.MULTILINE | re.IGNORECASE),
    "references": re.compile(r"^#{1,4}\s+(?:\d+(?:\.\d+)*[.)]?\s+)?(?:.*\bReferences\b.*|Further Reading\b)", re.MULTILINE | re.IGNORECASE),
}


@dataclass
class NotebookResult:
    path: str
    cells: int
    code_cells: int
    markdown_cells: int
    missing_sections: list[str]
    missing_exercise_tiers: list[str]
    missing_badges: list[str]
    missing_cell_ids: list[int]
    duplicate_cell_ids: list[str]
    syntax_errors: list[str]
    placeholders: list[str]
    blanket_warning_suppression: list[int]
    broken_images: list[str]
    broken_code_images: list[str]
    empty_cells: list[int]

    @property
    def errors(self) -> int:
        return sum(
            bool(value)
            for value in (
                self.missing_sections,
                self.missing_exercise_tiers,
                self.missing_badges,
                self.missing_cell_ids,
                self.duplicate_cell_ids,
                self.syntax_errors,
                self.placeholders,
                self.blanket_warning_suppression,
                self.broken_images,
                self.broken_code_images,
            )
        )


def _source(cell: dict) -> str:
    src = cell.get("source", "")
    return "".join(src) if isinstance(src, list) else str(src)


def _transform_python(source: str) -> str:
    if TransformerManager is not None:
        try:
            return TransformerManager().transform_cell(source)
        except Exception:
            pass
    # Minimal fallback: remove IPython-only lines while preserving ordinary Python.
    lines = source.splitlines()
    if lines and lines[0].lstrip().startswith("%%"):
        return "pass\n"
    out: list[str] = []
    for line in lines:
        stripped = line.lstrip()
        if stripped.startswith(("%", "!")) or stripped.endswith("?"):
            indent = line[: len(line) - len(stripped)]
            out.append(f"{indent}pass  # IPython-only syntax")
        else:
            out.append(line)
    return "\n".join(out) + "\n"


def _resolve_image(notebook: Path, target: str, root: Path) -> Path | None:
    target = target.strip().split("#", 1)[0].split("?", 1)[0]
    if not target or re.match(r"^(?:https?:|data:|attachment:)", target, re.I):
        return None
    target = target.strip("<>\"'")
    candidate = (notebook.parent / target).resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError:
        return candidate
    return candidate


def audit_notebook(path: Path, root: Path) -> NotebookResult:
    with path.open("r", encoding="utf-8") as handle:
        nb = json.load(handle)

    cells = nb.get("cells", [])
    markdown = "\n\n".join(_source(c) for c in cells if c.get("cell_type") == "markdown")
    code_cells = [(i, _source(c)) for i, c in enumerate(cells) if c.get("cell_type") == "code"]

    missing_sections = [name for name, pattern in REQUIRED_SECTIONS.items() if not pattern.search(markdown)]
    missing_exercise_tiers = [
        label for label in ("Conceptual", "Applied", "Challenge")
        if not re.search(rf"\b{label}\b", markdown, re.IGNORECASE)
    ]
    missing_badges = [
        badge
        for badge, needle in (("Colab", "colab.research.google.com"), ("Binder", "mybinder.org"))
        if needle not in markdown
    ]

    ids = [c.get("id") for c in cells]
    missing_ids = [i for i, cell_id in enumerate(ids) if not cell_id]
    counts = Counter(cell_id for cell_id in ids if cell_id)
    duplicate_ids = sorted(cell_id for cell_id, count in counts.items() if count > 1)

    syntax_errors: list[str] = []
    placeholders: list[str] = []
    blanket_warnings: list[int] = []
    for index, source in code_cells:
        if PLACEHOLDER_RE.search(source):
            placeholders.append(f"cell {index}: {PLACEHOLDER_RE.search(source).group(0)}")
        if BLANKET_WARNING_RE.search(source):
            blanket_warnings.append(index)
        try:
            ast.parse(_transform_python(source), filename=f"{path}::cell-{index}")
        except SyntaxError as exc:
            syntax_errors.append(f"cell {index}: line {exc.lineno}: {exc.msg}")

    broken_images: list[str] = []
    for match in IMAGE_RE.finditer(markdown):
        candidate = _resolve_image(path, match.group(1), root)
        if candidate is not None and (not candidate.is_file() or candidate.stat().st_size == 0):
            broken_images.append(match.group(1))

    broken_code_images: list[str] = []
    for _, source in code_cells:
        for match in CODE_IMAGE_RE.finditer(source):
            candidate = _resolve_image(path, match.group(1), root)
            if candidate is not None and (not candidate.is_file() or candidate.stat().st_size == 0):
                broken_code_images.append(match.group(1))

    empty_cells = [i for i, cell in enumerate(cells) if not _source(cell).strip()]
    return NotebookResult(
        path=str(path.relative_to(root)),
        cells=len(cells),
        code_cells=len(code_cells),
        markdown_cells=sum(c.get("cell_type") == "markdown" for c in cells),
        missing_sections=missing_sections,
        missing_exercise_tiers=missing_exercise_tiers,
        missing_badges=missing_badges,
        missing_cell_ids=missing_ids,
        duplicate_cell_ids=duplicate_ids,
        syntax_errors=syntax_errors,
        placeholders=placeholders,
        blanket_warning_suppression=blanket_warnings,
        broken_images=sorted(set(broken_images)),
        broken_code_images=sorted(set(broken_code_images)),
        empty_cells=empty_cells,
    )


def iter_notebooks(root: Path) -> Iterable[Path]:
    for path in sorted(root.rglob("*.ipynb")):
        if ".ipynb_checkpoints" not in path.parts and not any(part.startswith(".") for part in path.relative_to(root).parts[:-1]):
            yield path


def markdown_report(results: list[NotebookResult]) -> str:
    failures = [result for result in results if result.errors]
    total_cells = sum(result.cells for result in results)
    total_code = sum(result.code_cells for result in results)
    lines = [
        "# Curriculum Notebook Audit",
        "",
        f"- Notebooks audited: **{len(results)}**",
        f"- Cells inspected: **{total_cells}** ({total_code} code)",
        f"- Notebooks with blocking findings: **{len(failures)}**",
        "- Audit scope: structural requirements, three-tier exercises, cell identities, Python/IPython syntax, strong placeholder markers, blanket warning suppression, and local Markdown/code image integrity.",
        "- Runtime semantics are verified separately; a clean static audit is not evidence that optional network/GPU paths execute in every environment.",
        "",
    ]
    if failures:
        lines += ["## Blocking Findings", ""]
        for result in failures:
            lines.append(f"### `{result.path}`")
            for key, value in asdict(result).items():
                if key not in {"path", "cells", "code_cells", "markdown_cells", "empty_cells"} and value:
                    lines.append(f"- **{key.replace('_', ' ').title()}:** {value}")
            lines.append("")
    else:
        lines += ["## Result", "", "All blocking notebook-quality invariants passed.", ""]
    lines += ["## Per-Notebook Ledger", "", "| Notebook | Cells | Code | Empty cells | Status |", "|---|---:|---:|---:|---|"]
    for result in results:
        status = "PASS" if not result.errors else "FAIL"
        lines.append(f"| `{result.path}` | {result.cells} | {result.code_cells} | {len(result.empty_cells)} | {status} |")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output-dir", type=Path, default=None)
    parser.add_argument("--strict", action="store_true", help="exit non-zero on blocking findings")
    args = parser.parse_args()
    root = args.root.resolve()
    output = (args.output_dir or root / "audit").resolve()
    output.mkdir(parents=True, exist_ok=True)

    results = [audit_notebook(path, root) for path in iter_notebooks(root)]
    summary = {
        "notebooks": len(results),
        "cells": sum(result.cells for result in results),
        "code_cells": sum(result.code_cells for result in results),
        "blocking_notebooks": sum(bool(result.errors) for result in results),
        "results": [asdict(result) | {"status": "PASS" if not result.errors else "FAIL"} for result in results],
    }
    (output / "notebook_audit.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    (output / "NOTEBOOK_AUDIT.md").write_text(markdown_report(results), encoding="utf-8")

    print(f"Audited {len(results)} notebooks; blocking findings in {summary['blocking_notebooks']}.")
    print(f"Reports: {output / 'NOTEBOOK_AUDIT.md'} and {output / 'notebook_audit.json'}")
    return 1 if args.strict and summary["blocking_notebooks"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
