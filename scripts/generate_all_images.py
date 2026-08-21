#!/usr/bin/env python3
"""Safe subprocess orchestrator for curriculum image-generation scripts."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"


def discover() -> list[Path]:
    excluded = {Path(__file__).name, "generate_image_manifest.py", "generate_release_audit.py"}
    return [p for p in sorted(SCRIPTS.glob("generate_*.py")) if p.name not in excluded]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument("--continue-on-error", action="store_true")
    parser.add_argument("--report", type=Path, default=ROOT / "audit" / "image_generation_report.json")
    args = parser.parse_args()
    scripts = discover()
    if args.list:
        print("\n".join(str(p.relative_to(ROOT)) for p in scripts))
        return 0
    results = []
    for script in scripts:
        rel = str(script.relative_to(ROOT))
        if args.dry_run:
            results.append({"script": rel, "status": "DRY_RUN"})
            continue
        start = time.perf_counter()
        try:
            proc = subprocess.run([sys.executable, str(script)], cwd=ROOT, text=True, capture_output=True, timeout=args.timeout)
            status = "PASS" if proc.returncode == 0 else "FAIL"
            row = {"script": rel, "status": status, "returncode": proc.returncode, "seconds": round(time.perf_counter() - start, 3), "stderr_tail": proc.stderr[-1200:]}
        except subprocess.TimeoutExpired:
            row = {"script": rel, "status": "TIMEOUT", "seconds": args.timeout}
        results.append(row)
        print(f"{row['status']:8} {rel}")
        if row["status"] != "PASS" and not args.continue_on_error:
            break
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(results, indent=2), encoding="utf-8")
    return 1 if any(r["status"] not in {"PASS", "DRY_RUN"} for r in results) else 0


if __name__ == "__main__":
    raise SystemExit(main())
