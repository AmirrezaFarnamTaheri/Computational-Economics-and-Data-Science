#!/usr/bin/env python3
"""Synchronize module landing pages and navigation stubs with actual notebooks."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = (
    "https://github.com/AmirrezaFarnamTaheri/Computational-Economics-and-Data-Science"
)
MODULES = {
    "01-foundations": "01-Foundations",
    "02-numerical-methods": "02-Numerical-Methods",
    "03-economic-modeling": "03-Economic-Modeling",
    "04-macro-models": "04-Macro-Models",
    "05-micro-models": "05-Micro-Models",
    "06-econometrics": "06-Econometrics",
    "07-machine-learning": "07-Machine-Learning",
    "08-time-series": "08-Time-Series",
    "09-finance": "09-Finance",
    "10-specialized": "10-Specialized-Models",
}


def source(cell: dict) -> str:
    src = cell.get("source", "")
    return "".join(src) if isinstance(src, list) else str(src)


def notebook_meta(path: Path) -> dict[str, str]:
    nb = json.loads(path.read_text(encoding="utf-8"))
    markdown = [
        source(c) for c in nb.get("cells", []) if c.get("cell_type") == "markdown"
    ]
    title = path.stem.replace("_", " ")
    lens = ""
    objectives = ""
    for text in markdown:
        for line in text.splitlines():
            if line.startswith("# "):
                title = line[2:].strip()
                break
        if "## The Lens" in text and not lens:
            body = re.split(r"\n#{2,4}\s", text, maxsplit=1)[0]
            body = re.sub(r"^## The Lens[^\n]*\n+", "", body).strip()
            lens = re.sub(r"\s+", " ", body)[:420]
        if "Learning Objectives" in text and not objectives:
            match = re.search(
                r"#{2,4}\s+Learning Objectives[^\n]*\n(.*?)(?=\n#{2,4}\s|\Z)",
                text,
                re.S | re.I,
            )
            if match:
                objectives = match.group(1).strip()
    return {"title": title, "lens": lens, "objectives": objectives}


def selected_for_stub(stub: Path, notebooks: list[Path]) -> list[Path]:
    slug = stub.stem.lower()
    numbers = [int(n) for n in re.findall(r"\d+", slug)]
    selected = []
    if numbers:
        lo, hi = (numbers[0], numbers[-1])
        if len(numbers) >= 2 and hi >= lo:
            for nb in notebooks:
                m = re.match(r"(\d+)", nb.stem)
                if m and lo <= int(m.group(1)) <= hi:
                    selected.append(nb)
        else:
            for nb in notebooks:
                m = re.match(r"(\d+)", nb.stem)
                if m and int(m.group(1)) == lo:
                    selected.append(nb)
    if selected:
        return selected[:6]
    words = {w for w in re.findall(r"[a-z]+", slug) if len(w) > 2}
    scored = []
    for nb in notebooks:
        tokens = set(re.findall(r"[a-z]+", nb.stem.lower().replace("_", "-")))
        score = len(words & tokens)
        if score:
            scored.append((score, nb))
    ordered = sorted(scored, key=lambda item: (-item[0], str(item[1])))[:3]
    return [nb for _, nb in ordered] or notebooks[:1]


def page_for(paths: list[Path], heading: str) -> str:
    lines = [
        f"# {heading}",
        "",
        "> This page is synchronized from the authoritative notebooks. Use the generated reading view "
        "for searchable prose/code, or open the notebook for execution.",
        "",
    ]
    for path in paths:
        meta = notebook_meta(path)
        rel = path.relative_to(ROOT).as_posix()
        generated = f"../../notebooks/{path.parent.name}/{path.stem}.md"
        lines += [f"## {meta['title']}", ""]
        if meta["lens"]:
            lines += [meta["lens"], ""]
        lines += [
            f"[Read generated page]({generated}){{ .md-button }} "
            f"[Open notebook]({REPO}/blob/main/{rel}){{ .md-button }}",
            "",
        ]
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    total = 0
    module_rows = []
    for slug, track in MODULES.items():
        notebooks = sorted((ROOT / track).glob("*.ipynb"))
        module_rows.append((track, len(notebooks), slug))
        docs_dir = ROOT / "docs" / "modules" / slug
        docs_dir.mkdir(parents=True, exist_ok=True)
        index_lines = [
            f"# {track.replace('-', ' ')}",
            "",
            f"**{len(notebooks)} notebooks** form this module.",
            "",
            "| Notebook | Focus | Reading view |",
            "|---|---|---|",
        ]
        for nb in notebooks:
            meta = notebook_meta(nb)
            lens = meta["lens"] or "See the notebook for the full economic lens."
            escaped_lens = lens.replace("|", "\\|")
            reading_view = f"[Read](../../notebooks/{track}/{nb.stem}.md)"
            index_lines.append(f"| `{nb.name}` | {escaped_lens} | {reading_view} |")
        (docs_dir / "index.md").write_text(
            "\n".join(index_lines) + "\n", encoding="utf-8"
        )
        total += 1
        for stub in docs_dir.glob("*.md"):
            if stub.name == "index.md":
                continue
            stub_text = stub.read_text(encoding="utf-8")
            if stub.stat().st_size:
                heading = stub_text.splitlines()[0].lstrip("# ").strip()
            else:
                heading = stub.stem.replace("-", " ").title()
            if "Content coming soon" in stub_text:
                page = page_for(selected_for_stub(stub, notebooks), heading)
                stub.write_text(page, encoding="utf-8")
                total += 1
    overview = [
        "# Course Modules",
        "",
        "The live repository currently contains the following core modules. Counts are generated "
        "from the notebook source tree.",
        "",
        "| Module | Notebooks |",
        "|---|---:|",
    ]
    for track, count, slug in module_rows:
        overview.append(f"| [{track.replace('-', ' ')}]({slug}/index.md) | {count} |")
    (ROOT / "docs" / "modules" / "index.md").write_text(
        "\n".join(overview) + "\n", encoding="utf-8"
    )
    total += 1
    print(f"Synchronized {total} module documentation pages.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
