#!/usr/bin/env python3
"""Notation-convention linter for curriculum code cells.

Enforces the variable-to-LaTeX alignment rules from
plan/CURRICULUM_HEALTH_SCORECARD.md section 3:

    scalar x -> x          vector x -> x_vec       matrix X -> X_mat
    tensor     -> x_tensor   expectation -> expected_value
    transition matrix P -> P_trans   discount beta -> beta

Flags identifiers in notebook code cells that use known-banned cryptic
abbreviation patterns (tmp1/tmp2/xx/df2/arr3 style). Exit code 1 if any
violation is found, so CI can gate on it once adopted.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

BANNED = re.compile(r"\b(tmp\d|temp\d|xx|yy|zz|df\d|arr\d|lst\d)\s*=")

# Canonical domain notations that look like banned patterns but are standard:
#   d1 / d2 - Black-Scholes/Merton model terms (Hull ch.13; Merton 1974)
WHITELIST = {"d1", "d2"}

def audit_notebook(path: Path):
    nb = json.loads(path.read_text(encoding="utf-8"))
    hits = []
    for i, c in enumerate(nb.get("cells", [])):
        if c.get("cell_type") != "code":
            continue
        s = c.get("source", "")
        s = "".join(s) if isinstance(s, list) else s
        for m in BANNED.finditer(s):
            hits.append((i, m.group(0)))
    return hits

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = ap.parse_args()
    violations = []
    count = 0
    for d in sorted(p for p in args.root.iterdir() if p.is_dir() and p.name[:2].isdigit()):
        for p in sorted(d.glob("*.ipynb")):
            for cell_idx, token in audit_notebook(p):
                violations.append(f"{p.relative_to(args.root)} :: cell {cell_idx} :: {token}")
                count += 1
    for v in violations:
        print(v)
    print(f"\n{count} banned-identifier assignment(s) found.")
    return 1 if count else 0

if __name__ == "__main__":
    raise SystemExit(main())
