#!/usr/bin/env python3
"""Compare notebook top-level imports with declared course dependencies."""
from __future__ import annotations

import ast
import json
import re
import sys
from collections import Counter
from pathlib import Path

try:
    from IPython.core.inputtransformer2 import TransformerManager
except ImportError:
    TransformerManager = None

ROOT = Path(__file__).resolve().parents[1]
IMPORT_TO_DIST = {
    "IPython": "ipython", "sklearn": "scikit-learn", "pandas_datareader": "pandas-datareader",
    "bs4": "beautifulsoup4", "sentence_transformers": "sentence-transformers", "vega_datasets": "vega-datasets",
    "pypfopt": "PyPortfolioOpt", "libpysal": "pysal", "pytensor": "pymc", "mpl_toolkits": "matplotlib",
}
OPTIONAL = {"cupy", "playwright", "pylogit"}


def declared() -> set[str]:
    names = set()
    for filename in ("requirements.txt", "requirements-optional.txt"):
        for line in (ROOT / filename).read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            name = re.split(r"[<=>\[; ]", line, maxsplit=1)[0].strip().lower().replace("_", "-")
            if name:
                names.add(name)
    return names


def main() -> int:
    tm = TransformerManager() if TransformerManager else None
    local = {p.stem for p in ROOT.rglob("*.py")}
    imports: Counter[str] = Counter()
    for p in ROOT.rglob("*.ipynb"):
        if ".ipynb_checkpoints" in p.parts:
            continue
        nb = json.loads(p.read_text(encoding="utf-8"))
        for c in nb.get("cells", []):
            if c.get("cell_type") != "code":
                continue
            src = "".join(c.get("source", []))
            try:
                src = tm.transform_cell(src) if tm else src
                tree = ast.parse(src)
            except (SyntaxError, ValueError):
                continue
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports[alias.name.split(".")[0]] += 1
                elif isinstance(node, ast.ImportFrom) and node.module:
                    imports[node.module.split(".")[0]] += 1
    declared_names = declared()
    missing=[]
    for module,count in sorted(imports.items(), key=lambda item:(-item[1], item[0])):
        if module in sys.stdlib_module_names or module in local:
            continue
        dist=IMPORT_TO_DIST.get(module,module).lower().replace("_","-")
        if dist not in declared_names and module not in OPTIONAL:
            missing.append((module,dist,count))
    out=ROOT/"audit"/"DEPENDENCY_AUDIT.md"; out.parent.mkdir(exist_ok=True)
    lines=["# Dependency Audit","",f"Third-party import modules observed: **{sum(1 for m in imports if m not in sys.stdlib_module_names and m not in local)}**",f"Undeclared non-optional imports: **{len(missing)}**","","| Import | Distribution | Occurrences |","|---|---|---:|"]
    lines += [f"| `{m}` | `{d}` | {n} |" for m,d,n in missing]
    if not missing: lines += ["","All non-optional notebook imports are represented in the declared dependency surface."]
    out.write_text("\n".join(lines)+"\n",encoding="utf-8")
    print(f"Undeclared non-optional imports: {len(missing)}")
    for row in missing: print(*row)
    return 1 if missing else 0

if __name__ == "__main__":
    raise SystemExit(main())
