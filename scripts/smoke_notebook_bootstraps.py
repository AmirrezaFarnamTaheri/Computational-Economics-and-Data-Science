#!/usr/bin/env python3
"""Execute every notebook bootstrap cell in a clean subprocess.

A notebook can be syntactically valid and still fail before its first lesson
cell because a seeded generator, optional import, or helper is used before it
exists.  This smoke lane executes the first code cell of every canonical
notebook from a clean interpreter while stripping IPython-only magics that do
not affect Python bootstrap semantics.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {"build", "site", ".venv", "venv", "node_modules"}


def iter_notebooks() -> list[Path]:
    notebooks: list[Path] = []
    for path in ROOT.rglob("*.ipynb"):
        rel = path.relative_to(ROOT)
        if ".ipynb_checkpoints" in rel.parts:
            continue
        if any(part.startswith(".") for part in rel.parts[:-1]):
            continue
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        if rel.parts[:2] == ("docs", "notebooks"):
            continue
        notebooks.append(path)
    return sorted(notebooks)


def source(cell: dict) -> str:
    value = cell.get("source", "")
    return "".join(value) if isinstance(value, list) else str(value)


def bootstrap_source(path: Path) -> str:
    nb = json.loads(path.read_text(encoding="utf-8"))
    for cell in nb.get("cells", []):
        if cell.get("cell_type") != "code":
            continue
        raw = source(cell)
        lines = raw.splitlines()
        if lines and lines[0].lstrip().startswith("%%"):
            # Bootstrap cell magics are presentation/profiling wrappers.  Their
            # body remains Python for the common %%time/%%capture family.
            lines = lines[1:]
        cleaned: list[str] = []
        for line in lines:
            stripped = line.lstrip()
            if stripped.startswith(("%", "!")) or stripped.endswith("?"):
                cleaned.append("pass  # IPython-only bootstrap syntax")
            else:
                cleaned.append(line)
        return "\n".join(cleaned) + "\n"
    return ""


def smoke(path: Path, timeout: int) -> tuple[bool, str]:
    code = bootstrap_source(path)
    if not code.strip():
        return True, "no code cell"

    harness = (
        "import os\n"
        "import sys\n"
        "sys.path.insert(0, os.getcwd())\n"
        "os.environ.setdefault('MPLBACKEND', 'Agg')\n"
        "os.environ.setdefault('COURSE_RUN_MODE', 'quick')\n" + code
    )
    env = os.environ.copy()
    env.setdefault("MPLBACKEND", "Agg")
    env.setdefault("COURSE_RUN_MODE", "quick")
    env.setdefault("PYTHONHASHSEED", "0")

    with tempfile.NamedTemporaryFile(
        "w", suffix=".py", encoding="utf-8", delete=False
    ) as handle:
        handle.write(harness)
        temp_path = Path(handle.name)

    try:
        result = subprocess.run(
            [sys.executable, str(temp_path)],
            cwd=path.parent,
            env=env,
            text=True,
            capture_output=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return False, f"timed out after {timeout}s"
    finally:
        temp_path.unlink(missing_ok=True)

    if result.returncode == 0:
        return True, "ok"
    detail = (result.stderr or result.stdout).strip()
    return False, detail[-3000:]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timeout", type=int, default=45)
    parser.add_argument(
        "--report", type=Path, default=ROOT / "build" / "bootstrap-smoke.json"
    )
    args = parser.parse_args()

    results: list[dict] = []
    failed = 0
    for path in iter_notebooks():
        ok, detail = smoke(path, args.timeout)
        rel = path.relative_to(ROOT).as_posix()
        results.append(
            {"notebook": rel, "status": "pass" if ok else "fail", "detail": detail}
        )
        print(f"{'PASS' if ok else 'FAIL'} {rel}")
        if not ok:
            failed += 1
            print(detail)

    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(
        json.dumps(
            {
                "notebooks": len(results),
                "passed": len(results) - failed,
                "failed": failed,
                "results": results,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"Bootstrap smoke: {len(results) - failed}/{len(results)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
