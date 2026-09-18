"""Repair stale in-notebook Table of Contents anchors.

During the WP-7 pass many section headings were renamed ('The Lens: ...'
prefixes, renumbering) without updating the TOC cells that link to them, so most
TOC anchors point at headings that no longer exist.

Resolution is deliberately CONSERVATIVE: a link is rewritten only when its own
label names a heading unambiguously (exact normalized-text match, or the fragment
already resolves). There is deliberately NO positional fallback -- an earlier
revision mapped the i-th TOC entry to the i-th section heading, but TOC entries
skip headings (Prerequisites, Summary, Exercises), so the indices drift and links
land on the wrong section. Unmatched entries are left untouched (dead, but not
actively wrong) and reported for a human pass.

Regexes are paren-balanced so anchors containing parens -- '#The-(Emerging)-...',
'...-(c.-1940s-1970s)' -- are matched in full instead of truncated at the first
')' (which left junk like '...1970s))' behind).

Dry-run mode reports what would change without writing.
"""

import argparse
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACKS = [
    "01-Foundations",
    "02-Numerical-Methods",
    "03-Economic-Modeling",
    "04-Macro-Models",
    "05-Micro-Models",
    "06-Econometrics",
    "07-Machine-Learning",
    "08-Time-Series",
    "09-Finance",
    "10-Specialized-Models",
    "Appendix",
    "high_performance_python",
]
# The destination may contain one level of balanced parens ('#The-(Emerging)-...',
# '...-(c.-1940s-1970s)'). The pattern below matches those in full instead of
# stopping at the first ')', which would leave the markdown link's own closing
# paren behind as junk ('...1970s))').
LINK_RE = re.compile(r"\[([^\]]*)\]\(#((?:[^()\s]|\([^()\s]*\))*)\)")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")


def _slugify(title: str) -> str:
    """Slugify like Python-Markdown's toc extension (matches the docs build)."""
    value = unicodedata.normalize("NFKD", title)
    value = value.encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^\w\s-]", "", value.lower())
    return re.sub(r"[-\s]+", "-", value).strip("-")


def _norm(text: str) -> str:
    """Comparison key for a heading vs a link label.

    Ignores the WP-7 decorations that broke the original anchors: the 'The Lens:'
    prefix and leading section numbers.
    """
    text = re.sub(r"^#+\s*", "", text)
    text = re.sub(r"^The Lens:?\s*", "", text, flags=re.I)
    text = re.sub(r"^\d+[-.]?\s*", "", text)
    text = re.sub(r"[^\w\s]", " ", text.lower())
    return re.sub(r"\s+", " ", text).strip()


def _headings(nb) -> tuple[dict[str, str], dict[str, str]]:
    """(slug -> heading, normalized-text -> heading) for real headings.

    Headings inside fenced code blocks are prose, not structure, and are excluded.
    """
    slug2head: dict[str, str] = {}
    norm2head: dict[str, str] = {}
    for cell in nb.get("cells", []):
        if cell.get("cell_type") != "markdown":
            continue
        in_fence = False
        for line in "".join(cell.get("source", [])).split("\n"):
            if line.lstrip().startswith("```"):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            m = HEADING_RE.match(line)
            if m and "Table of Contents" not in line:
                title = m.group(2)
                slug2head.setdefault(_slugify(title), title)
                norm2head.setdefault(_norm(title), title)
    return slug2head, norm2head


def repair_notebook(nb_path: Path, dry_run: bool = False):
    nb = json.loads(nb_path.read_bytes().decode("utf-8"))
    slug2head, norm2head = _headings(nb)

    changed_cells = 0
    fixed = 0
    left_dead = []
    for cell in nb.get("cells", []):
        if cell.get("cell_type") != "markdown":
            continue
        src = "".join(cell.get("source", []))
        if "Table of Contents" not in src:
            continue

        def repl(m: re.Match) -> str:
            nonlocal fixed, left_dead
            label, frag = m.group(1), m.group(2)
            # Already resolves -> leave exactly as is.
            if frag in slug2head:
                return m.group(0)
            # Label names a real heading -> rewrite to that heading's slug.
            target = norm2head.get(_norm(label))
            if target is None and len(_norm(label).split()) >= 3:
                # Shortened form: the label is a prefix of a longer heading
                # ('Garbage Collection' vs 'Garbage Collection: How Python
                # Reclaims Memory'). Only safe when exactly one heading matches.
                hits = [h for n, h in norm2head.items() if n.startswith(_norm(label))]
                if len(hits) == 1:
                    target = hits[0]
            if target is not None:
                new = _slugify(target)
                if new != frag:
                    fixed += 1
                    return f"[{label}](#{new})"
                return m.group(0)
            # No confident match -> leave it; record for the human pass.
            left_dead.append((label, frag))
            return m.group(0)

        new_src = LINK_RE.sub(repl, src)
        if new_src != src:
            cell["source"] = new_src.splitlines(keepends=True)
            changed_cells += 1

    if changed_cells and not dry_run:
        nb_path.write_text(
            json.dumps(nb, indent=1, ensure_ascii=False) + "\n", encoding="utf-8"
        )
    return changed_cells, fixed, left_dead


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--apply", action="store_true", help="write changes (default: dry run)"
    )
    args = ap.parse_args()

    total_cells = total_fixed = 0
    all_dead = []
    for track in TRACKS:
        for nb_path in sorted((ROOT / track).glob("*.ipynb")):
            cells, fixed, dead = repair_notebook(nb_path, dry_run=not args.apply)
            total_cells += cells
            total_fixed += fixed
            all_dead.extend((nb_path.name, *d) for d in dead)

    verb = "repaired" if args.apply else "would repair"
    print(f"{verb}: {total_cells} TOC cells, {total_fixed} anchors")
    print(f"left dead (no confident match): {len(all_dead)}")
    for name, label, frag in all_dead[:20]:
        print(f"  {name}: {label!r} -> {frag!r}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
