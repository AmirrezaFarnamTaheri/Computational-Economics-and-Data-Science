#!/usr/bin/env python3
"""Generate baseline-vs-final metrics and a source-to-final file manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from audit_curriculum_ast import REQUIRED_SECTIONS, audit_notebook

EXCLUDED_PARTS = {".pytest_cache", "__pycache__", ".ipynb_checkpoints", "site"}
EXCLUDED_FILES = {"audit/CHANGE_MANIFEST.md", "audit/CHANGE_MANIFEST.json"}


def notebooks(root: Path) -> list[Path]:
    return [
        p
        for p in sorted(root.rglob("*.ipynb"))
        if not any(part in EXCLUDED_PARTS for part in p.parts)
    ]


def metrics(root: Path) -> dict[str, int]:
    paths = notebooks(root)
    results = [audit_notebook(p, root) for p in paths]
    out: dict[str, int] = {"Notebook count": len(paths)}
    for section in REQUIRED_SECTIONS:
        out[section] = sum(section not in r.missing_sections for r in results)
    for tier in ("Conceptual", "Applied", "Challenge"):
        out[f"Exercise tier: {tier}"] = sum(
            tier not in r.missing_exercise_tiers for r in results
        )
    for badge in ("Colab", "Binder"):
        out[f"{badge} badges"] = sum(badge not in r.missing_badges for r in results)
    out["Notebooks with duplicate cell IDs"] = sum(
        bool(r.duplicate_cell_ids) for r in results
    )
    out["Notebooks with missing cell IDs"] = sum(
        bool(r.missing_cell_ids) for r in results
    )
    out["Notebooks with strong placeholders"] = sum(
        bool(r.placeholders) for r in results
    )
    out["Notebooks with blanket warning suppression"] = sum(
        bool(r.blanket_warning_suppression) for r in results
    )
    out["Notebooks with Python/IPython syntax errors"] = sum(
        bool(r.syntax_errors) for r in results
    )
    out["Broken local Markdown image references"] = sum(
        len(r.broken_images) for r in results
    )
    out["Broken code Image(filename=...) references"] = sum(
        len(r.broken_code_images) for r in results
    )
    image_files = (
        [p for p in (root / "images").rglob("*") if p.is_file()]
        if (root / "images").exists()
        else []
    )
    out["Zero-byte image assets"] = sum(p.stat().st_size == 0 for p in image_files)
    out["Blocking notebooks under strict audit"] = sum(r.errors > 0 for r in results)
    return out


def file_hashes(root: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(root).as_posix()
        if rel in EXCLUDED_FILES or any(
            part in EXCLUDED_PARTS for part in path.relative_to(root).parts
        ):
            continue
        if path.suffix == ".pyc":
            continue
        result[rel] = hashlib.sha256(path.read_bytes()).hexdigest()
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline-root", type=Path, required=True)
    parser.add_argument(
        "--final-root", type=Path, default=Path(__file__).resolve().parents[1]
    )
    args = parser.parse_args()
    baseline = args.baseline_root.resolve()
    final = args.final_root.resolve()
    audit = final / "audit"
    audit.mkdir(exist_ok=True)

    before = metrics(baseline)
    after = metrics(final)
    labels = [
        "Notebook count",
        "lens",
        "objectives",
        "prerequisites",
        "toc",
        "exercises",
        "summary",
        "references",
        "Exercise tier: Conceptual",
        "Exercise tier: Applied",
        "Exercise tier: Challenge",
        "Colab badges",
        "Binder badges",
        "Notebooks with duplicate cell IDs",
        "Notebooks with missing cell IDs",
        "Notebooks with strong placeholders",
        "Notebooks with blanket warning suppression",
        "Notebooks with Python/IPython syntax errors",
        "Broken local Markdown image references",
        "Broken code Image(filename=...) references",
        "Zero-byte image assets",
        "Blocking notebooks under strict audit",
    ]
    friendly = {
        "lens": "Standard `## The Lens` heading",
        "objectives": "Learning Objectives",
        "prerequisites": "Prerequisites",
        "toc": "Table of Contents",
        "exercises": "Exercises",
        "summary": "Summary/Key Takeaways",
        "references": "References/Further Reading",
    }
    lines = [
        "# Baseline vs Final Curriculum Quality",
        "",
        "The baseline is the user-provided ZIP as received. The final column is the improved tree at release-audit time.",
        "",
        "| Metric | Baseline | Final |",
        "|---|---:|---:|",
    ]
    for label in labels:
        lines.append(
            f"| {friendly.get(label, label)} | {before[label]} | {after[label]} |"
        )
    lines += [
        "",
        "Strict structural compliance is intentionally stronger in the final audit than the historical planning documents: every notebook must expose all three exercise tiers, stable cell IDs, valid local asset references, and parseable Python/IPython code.",
        "",
    ]
    (audit / "BASELINE_VS_FINAL.md").write_text("\n".join(lines), encoding="utf-8")
    (audit / "BASELINE_VS_FINAL.json").write_text(
        json.dumps({"baseline": before, "final": after}, indent=2), encoding="utf-8"
    )

    base_files = file_hashes(baseline)
    final_files = file_hashes(final)
    base_set, final_set = set(base_files), set(final_files)
    added = sorted(final_set - base_set)
    removed = sorted(base_set - final_set)
    changed = sorted(p for p in base_set & final_set if base_files[p] != final_files[p])
    unchanged = sorted(
        p for p in base_set & final_set if base_files[p] == final_files[p]
    )
    manifest = {
        "baseline_root": str(baseline),
        "final_root": str(final),
        "baseline_files": len(base_files),
        "final_files": len(final_files),
        "added_count": len(added),
        "removed_count": len(removed),
        "changed_count": len(changed),
        "unchanged_count": len(unchanged),
        "added": added,
        "removed": removed,
        "changed": changed,
    }
    (audit / "CHANGE_MANIFEST.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )
    md = [
        "# Source-to-Final Change Manifest",
        "",
        f"- Baseline files: **{len(base_files)}**",
        f"- Final files: **{len(final_files)}**",
        f"- Added: **{len(added)}**",
        f"- Removed: **{len(removed)}**",
        f"- Changed in place: **{len(changed)}**",
        f"- Unchanged: **{len(unchanged)}**",
        "",
        "## Added files",
        "",
    ]
    md += [f"- `{p}`" for p in added] or ["- None"]
    md += ["", "## Removed files", ""] + ([f"- `{p}`" for p in removed] or ["- None"])
    md += ["", "## Changed files", ""] + ([f"- `{p}`" for p in changed] or ["- None"])
    md.append("")
    (audit / "CHANGE_MANIFEST.md").write_text("\n".join(md), encoding="utf-8")
    print(
        f"Baseline notebooks: {before['Notebook count']}; final notebooks: {after['Notebook count']}"
    )
    print(f"Files: +{len(added)} -{len(removed)} ~{len(changed)} ={len(unchanged)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
