#!/usr/bin/env python3
"""Repository-wide structural and syntax audit for curriculum notebooks.

The audit is intentionally static: it validates every notebook without importing or
executing optional scientific stacks. Runtime execution is a separate verification
layer because many advanced notebooks require network, GPU, or system dependencies.
"""

from __future__ import annotations

import argparse
import ast
import builtins
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
BLANKET_WARNING_RE = re.compile(r"warnings\.filterwarnings\(\s*['\"]ignore['\"]\s*\)")

REQUIRED_SECTIONS = {
    "lens": re.compile(r"^##\s+The Lens(?::|\s|$)", re.MULTILINE | re.IGNORECASE),
    "objectives": re.compile(
        r"^#{1,4}\s+(?:\d+(?:\.\d+)*[.)]?\s+)?Learning Objectives\b",
        re.MULTILINE | re.IGNORECASE,
    ),
    "prerequisites": re.compile(
        r"^#{1,4}\s+(?:\d+(?:\.\d+)*[.)]?\s+)?Prerequisites\b",
        re.MULTILINE | re.IGNORECASE,
    ),
    "toc": re.compile(
        r"^#{1,4}\s+(?:\d+(?:\.\d+)*[.)]?\s+)?Table of Contents\b",
        re.MULTILINE | re.IGNORECASE,
    ),
    "exercises": re.compile(
        r"^#{1,4}\s+(?:\d+(?:\.\d+)*[.)]?\s+)?(?:.*\bExercises?\b|Test Your Knowledge\b)",
        re.MULTILINE | re.IGNORECASE,
    ),
    "summary": re.compile(
        r"^#{1,4}\s+(?:\d+(?:\.\d+)*[.)]?\s+)?(?:Summary|Summary & Key Takeaways)\b",
        re.MULTILINE | re.IGNORECASE,
    ),
    "references": re.compile(
        r"^#{1,4}\s+(?:\d+(?:\.\d+)*[.)]?\s+)?(?:.*\bReferences\b.*|Further Reading\b)",
        re.MULTILINE | re.IGNORECASE,
    ),
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
    bootstrap_name_errors: list[str]
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
                self.bootstrap_name_errors,
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


# Cell magics whose body is plain Python. The IPython transformer turns the
# whole cell into run_cell_magic(name, args, "body"), so the body is a string
# argument that ast.parse never inspects. For Python-valued magics the body is
# real Python and belongs under the syntax gate.
_PYTHON_BODY_MAGICS = frozenset({"time", "timeit", "capture", "prun"})


def _split_cell_magic(source: str) -> tuple[str, str] | None:
    lines = source.splitlines()
    if not lines:
        return None
    first = lines[0].lstrip()
    if not first.startswith("%%"):
        return None
    name = first[2:].split(None, 1)[0].strip()
    body = "\n".join(lines[1:])
    return name, body


def _parseable_source(source: str) -> str:
    """Transform a cell for ast.parse, keeping Python-valued magic bodies.

    IPython's transformer wraps ``%%magic`` bodies in a string argument, which
    let syntax errors inside ``%%time`` blocks pass the strict gate. Python-
    bodied magics are parsed directly; non-Python magics (%%bash, %%html, ...)
    are replaced with a placeholder as before.
    """
    magic = _split_cell_magic(source)
    if magic is not None:
        name, body = magic
        if name in _PYTHON_BODY_MAGICS:
            return _transform_python(body)
    return _transform_python(source)


_BOOTSTRAP_BUILTINS = frozenset(dir(builtins)) | {"get_ipython", "__name__"}


def _bound_names(node: ast.AST) -> set[str]:
    """Return names bound by one top-level statement after it executes."""
    names: set[str] = set()
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
        names.add(node.name)
    elif isinstance(node, (ast.Import, ast.ImportFrom)):
        for alias in node.names:
            if alias.asname:
                names.add(alias.asname)
            elif isinstance(node, ast.Import):
                names.add(alias.name.split(".", 1)[0])
            else:
                names.add(alias.name)
    else:
        for child in ast.walk(node):
            if isinstance(child, ast.Name) and isinstance(
                child.ctx, (ast.Store, ast.Del)
            ):
                names.add(child.id)
    return names


class _ImmediateLoadVisitor(ast.NodeVisitor):
    """Collect names evaluated immediately by a top-level statement.

    Function/class bodies and lambdas execute later, so their interior names are
    excluded from the bootstrap ordering check. Decorators, defaults, bases and
    assignment expressions are still visited because they execute immediately.
    """

    def __init__(self) -> None:
        self.loads: set[str] = set()

    def visit_Name(self, node: ast.Name) -> None:
        if isinstance(node.ctx, ast.Load):
            self.loads.add(node.id)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        for decorator in node.decorator_list:
            self.visit(decorator)
        for default in (*node.args.defaults, *node.args.kw_defaults):
            if default is not None:
                self.visit(default)
        if node.returns is not None:
            self.visit(node.returns)

    visit_AsyncFunctionDef = visit_FunctionDef

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        for decorator in node.decorator_list:
            self.visit(decorator)
        for base in node.bases:
            self.visit(base)
        for keyword in node.keywords:
            self.visit(keyword.value)

    def visit_Lambda(self, node: ast.Lambda) -> None:
        for default in (*node.args.defaults, *node.args.kw_defaults):
            if default is not None:
                self.visit(default)


def _bootstrap_name_errors(source: str) -> list[str]:
    """Catch use-before-import/definition in the first executable code cell.

    Later notebook cells deliberately share state and are validated by the
    ordered execution lane. The first code cell, however, must bootstrap from a
    clean kernel and therefore cannot depend on aliases that it defines later.
    """
    tree = ast.parse(_parseable_source(source))
    known = set(_BOOTSTRAP_BUILTINS)
    errors: list[str] = []
    for statement in tree.body:
        visitor = _ImmediateLoadVisitor()
        visitor.visit(statement)
        for name in sorted(visitor.loads - known - _bound_names(statement)):
            errors.append(
                f"line {getattr(statement, 'lineno', '?')}: "
                f"{name!r} used before import/definition"
            )
        known.update(_bound_names(statement))
    return errors


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
    markdown = "\n\n".join(
        _source(c) for c in cells if c.get("cell_type") == "markdown"
    )
    code_cells = [
        (i, _source(c)) for i, c in enumerate(cells) if c.get("cell_type") == "code"
    ]

    missing_sections = [
        name
        for name, pattern in REQUIRED_SECTIONS.items()
        if not pattern.search(markdown)
    ]
    missing_exercise_tiers = [
        label
        for label in ("Conceptual", "Applied", "Challenge")
        if not re.search(rf"\b{label}\b", markdown, re.IGNORECASE)
    ]
    missing_badges = [
        badge
        for badge, needle in (
            ("Colab", "colab.research.google.com"),
            ("Binder", "mybinder.org"),
        )
        if needle not in markdown
    ]

    ids = [c.get("id") for c in cells]
    missing_ids = [i for i, cell_id in enumerate(ids) if not cell_id]
    counts = Counter(cell_id for cell_id in ids if cell_id)
    duplicate_ids = sorted(cell_id for cell_id, count in counts.items() if count > 1)

    syntax_errors: list[str] = []
    bootstrap_name_errors: list[str] = []
    placeholders: list[str] = []
    blanket_warnings: list[int] = []
    for index, source in code_cells:
        if PLACEHOLDER_RE.search(source):
            placeholders.append(
                f"cell {index}: {PLACEHOLDER_RE.search(source).group(0)}"
            )
        if BLANKET_WARNING_RE.search(source):
            blanket_warnings.append(index)
        try:
            ast.parse(_parseable_source(source), filename=f"{path}::cell-{index}")
        except SyntaxError as exc:
            syntax_errors.append(f"cell {index}: line {exc.lineno}: {exc.msg}")

    if code_cells:
        first_index, first_source = code_cells[0]
        try:
            bootstrap_name_errors = [
                f"cell {first_index}: {item}"
                for item in _bootstrap_name_errors(first_source)
            ]
        except SyntaxError:
            # The syntax gate above already reports this source.
            bootstrap_name_errors = []

    broken_images: list[str] = []
    for match in IMAGE_RE.finditer(markdown):
        candidate = _resolve_image(path, match.group(1), root)
        if candidate is not None and (
            not candidate.is_file() or candidate.stat().st_size == 0
        ):
            broken_images.append(match.group(1))

    broken_code_images: list[str] = []
    for _, source in code_cells:
        for match in CODE_IMAGE_RE.finditer(source):
            candidate = _resolve_image(path, match.group(1), root)
            if candidate is not None and (
                not candidate.is_file() or candidate.stat().st_size == 0
            ):
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
        bootstrap_name_errors=bootstrap_name_errors,
        placeholders=placeholders,
        blanket_warning_suppression=blanket_warnings,
        broken_images=sorted(set(broken_images)),
        broken_code_images=sorted(set(broken_code_images)),
        empty_cells=empty_cells,
    )


# Directories that are never source notebooks: build artifacts, executed
# output mirrors, dependency caches, and any dir starting with ".".
# The audit only inspects the curated source tree under repo root.
_SKIP_DIRS = frozenset({"build", "node_modules", "venv", ".venv"})


def iter_notebooks(root: Path) -> Iterable[Path]:
    for path in sorted(root.rglob("*.ipynb")):
        rel_parts = path.relative_to(root).parts
        if ".ipynb_checkpoints" in rel_parts:
            continue
        if any(part.startswith(".") for part in rel_parts[:-1]):
            continue
        if any(part in _SKIP_DIRS for part in rel_parts):
            continue
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
        "- Audit scope: structural requirements, three-tier exercises, cell identities, Python/IPython syntax, clean-kernel bootstrap name ordering, strong placeholder markers, blanket warning suppression, and local Markdown/code image integrity.",
        "- Runtime semantics are verified separately; a clean static audit is not evidence that optional network/GPU paths execute in every environment.",
        "",
    ]
    if failures:
        lines += ["## Blocking Findings", ""]
        for result in failures:
            lines.append(f"### `{result.path}`")
            for key, value in asdict(result).items():
                if (
                    key
                    not in {
                        "path",
                        "cells",
                        "code_cells",
                        "markdown_cells",
                        "empty_cells",
                    }
                    and value
                ):
                    lines.append(f"- **{key.replace('_', ' ').title()}:** {value}")
            lines.append("")
    else:
        lines += [
            "## Result",
            "",
            "All blocking notebook-quality invariants passed.",
            "",
        ]
    lines += [
        "## Per-Notebook Ledger",
        "",
        "| Notebook | Cells | Code | Empty cells | Status |",
        "|---|---:|---:|---:|---|",
    ]
    for result in results:
        status = "PASS" if not result.errors else "FAIL"
        lines.append(
            f"| `{result.path}` | {result.cells} | {result.code_cells} | {len(result.empty_cells)} | {status} |"
        )
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--root", type=Path, default=Path(__file__).resolve().parents[1]
    )
    parser.add_argument("--output-dir", type=Path, default=None)
    parser.add_argument(
        "--strict", action="store_true", help="exit non-zero on blocking findings"
    )
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
        "results": [
            asdict(result) | {"status": "PASS" if not result.errors else "FAIL"}
            for result in results
        ],
    }
    (output / "notebook_audit.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    (output / "NOTEBOOK_AUDIT.md").write_text(
        markdown_report(results), encoding="utf-8"
    )

    print(
        f"Audited {len(results)} notebooks; blocking findings in {summary['blocking_notebooks']}."
    )
    for result in results:
        if not result.errors:
            continue
        print(f"BLOCKING: {result.path}")
        for key, value in asdict(result).items():
            if key in {
                "path",
                "cells",
                "code_cells",
                "markdown_cells",
                "empty_cells",
            }:
                continue
            if value:
                print(f"  {key}: {value}")
    print(
        f"Reports: {output / 'NOTEBOOK_AUDIT.md'} and {output / 'notebook_audit.json'}"
    )
    return 1 if args.strict and summary["blocking_notebooks"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
