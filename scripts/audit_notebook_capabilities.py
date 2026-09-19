#!/usr/bin/env python3
"""Validate notebook capability ownership and coverage."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "ci" / "notebook_capabilities.json"
DETERMINISTIC = ROOT / "ci" / "deterministic_notebooks.txt"


def notebooks() -> set[str]:
    result: set[str] = set()
    for path in ROOT.rglob("*.ipynb"):
        rel = path.relative_to(ROOT)
        if ".ipynb_checkpoints" in rel.parts:
            continue
        if rel.parts[:2] == ("docs", "notebooks"):
            continue
        if any(part in {"build", "site", ".venv", "venv"} for part in rel.parts):
            continue
        result.add(rel.as_posix())
    return result


def deterministic() -> set[str]:
    return {
        line.strip()
        for line in DETERMINISTIC.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    }


def main() -> int:
    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    records = payload.get("notebooks", {})
    actual = notebooks()
    listed = set(records)
    errors: list[str] = []

    if actual != listed:
        for path in sorted(actual - listed):
            errors.append(f"notebook missing from capability manifest: {path}")
        for path in sorted(listed - actual):
            errors.append(f"capability manifest points to missing notebook: {path}")

    required = {
        "bootstrap_environment",
        "bootstrap_owner_job",
        "bootstrap_requirement",
        "full_run_environment",
        "full_run_owner",
        "full_run_status",
        "last_full_run_evidence",
        "skip_reason",
    }
    det = deterministic()
    if not det <= actual:
        for path in sorted(det - actual):
            errors.append(f"deterministic list points to missing notebook: {path}")

    for path in sorted(actual & listed):
        record = records[path]
        missing = required - set(record)
        if missing:
            errors.append(f"{path}: missing manifest fields {sorted(missing)}")
            continue
        if record["bootstrap_owner_job"] != "notebook-bootstrap-smoke":
            errors.append(f"{path}: bootstrap owner must be notebook-bootstrap-smoke")
        if path in det:
            if record["skip_reason"] is not None:
                errors.append(f"{path}: deterministic notebook cannot have skip_reason")
            if record["full_run_owner"] != "deterministic-execution":
                errors.append(f"{path}: deterministic notebook full-run owner drifted")
        elif not str(record["skip_reason"] or "").strip():
            errors.append(
                f"{path}: non-deterministic notebook requires a concrete skip_reason"
            )

    print(
        f"Capability manifest: {len(actual)} notebooks; "
        f"{len(det)} deterministic full-run; {len(actual - det)} capability-dependent."
    )
    if errors:
        print("\n".join(f"ERROR: {item}" for item in errors))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
