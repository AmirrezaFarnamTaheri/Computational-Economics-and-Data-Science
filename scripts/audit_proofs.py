#!/usr/bin/env python3
"""Structural proof/derivation coverage scanner for theory-heavy notebooks.

This tool does *not* pretend to prove mathematical correctness automatically. It
identifies where the curriculum has explicit assumptions, theorem statements,
derivations/proofs, and economic interpretation so human review can focus on weak
chains instead of relying on keyword counts alone.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

THEORY_TERMS = re.compile(
    r"theorem|lemma|proposition|proof|deriv|first[- ]order condition|kkt|bellman|equilibrium|asymptotic",
    re.I,
)
ASSUMPTION = re.compile(r"assumption|suppose|under the conditions|regularity", re.I)
STATEMENT = re.compile(r"theorem|lemma|proposition|result|condition", re.I)
WORKING = re.compile(r"proof|deriv|therefore|hence|implies|\$\$|\\begin\{align", re.I)
INTERPRETATION = re.compile(
    r"economic intuition|economic interpretation|policy implication|economically|interpretation",
    re.I,
)


def source(cell: dict) -> str:
    src = cell.get("source", "")
    return "".join(src) if isinstance(src, list) else str(src)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--root", type=Path, default=Path(__file__).resolve().parents[1]
    )
    parser.add_argument("--output-dir", type=Path, default=None)
    args = parser.parse_args()
    root = args.root.resolve()
    output = (args.output_dir or root / "audit").resolve()
    output.mkdir(parents=True, exist_ok=True)

    rows = []
    for path in sorted(root.rglob("*.ipynb")):
        if ".ipynb_checkpoints" in path.parts:
            continue
        nb = json.loads(path.read_text(encoding="utf-8"))
        markdown = "\n\n".join(
            source(c) for c in nb.get("cells", []) if c.get("cell_type") == "markdown"
        )
        theory_hits = len(THEORY_TERMS.findall(markdown))
        equation_count = markdown.count("$$") // 2 + markdown.count("\\begin{align")
        if theory_hits < 3 and equation_count < 4:
            continue
        dimensions = {
            "assumptions": bool(ASSUMPTION.search(markdown)),
            "formal_statement": bool(STATEMENT.search(markdown)),
            "working_or_derivation": bool(WORKING.search(markdown)),
            "economic_interpretation": bool(INTERPRETATION.search(markdown)),
        }
        score = sum(dimensions.values())
        rows.append(
            {
                "path": str(path.relative_to(root)),
                "theory_term_hits": theory_hits,
                "display_equations": equation_count,
                "dimensions": dimensions,
                "structural_score": score,
            }
        )

    rows.sort(
        key=lambda row: (row["structural_score"], -row["theory_term_hits"], row["path"])
    )
    (output / "proof_structure_audit.json").write_text(
        json.dumps({"candidates": rows}, indent=2), encoding="utf-8"
    )
    lines = [
        "# Proof & Derivation Structure Audit",
        "",
        "> This is a structural triage tool, not an automated mathematical correctness proof.",
        "",
        f"Theory-heavy notebooks triaged: **{len(rows)}**",
        "",
        "| Notebook | Assumptions | Statement | Working | Economic interpretation | Score |",
        "|---|:---:|:---:|:---:|:---:|---:|",
    ]

    def mark(value: bool) -> str:
        return "✓" if value else "—"

    for row in rows:
        d = row["dimensions"]
        lines.append(
            f"| `{row['path']}` | {mark(d['assumptions'])} | {mark(d['formal_statement'])} | "
            f"{mark(d['working_or_derivation'])} | {mark(d['economic_interpretation'])} | {row['structural_score']}/4 |"
        )
    lines += [
        "",
        "## Review Priority",
        "",
        "Notebooks scoring 0–2 should receive the first human proof-depth pass; 3–4 indicates the expected structural ingredients are present, not that the mathematics has been mechanically verified.",
        "",
    ]
    (output / "PROOF_STRUCTURE_AUDIT.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"Triaged {len(rows)} theory-heavy notebooks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
