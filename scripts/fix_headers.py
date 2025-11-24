"""
Notebook Header Standardizer
----------------------------
This script walks through all Jupyter notebooks in the repository and ensures
they start with the standard License Notice header.

Usage:
    python scripts/fix_headers.py [directory] [--check]

Options:
    --check     Only check for missing headers, do not modify files.
"""

import os
import sys
import json
import argparse
from pathlib import Path

# The standard header content
HEADER_SOURCE = [
    "> **License Notice**\\n",
    "> \\n",
    "> This notebook is part of the *Computational Economics and Data Science* course.\\n",
    "> \\n",
    "> - Code cells are released under the MIT License. You are free to use and adapt the code with attribution.\\n",
    "> - Text, figures, and other non-code content are released under the Creative Commons Attribution 4.0 International License.\\n",
    "> \\n",
    "> Please retain this notice and credit the repository when sharing adaptations."
]

HEADER_CELL = {
    "cell_type": "markdown",
    "metadata": {},
    "source": HEADER_SOURCE
}

def is_header(cell):
    """Checks if a cell is the license header."""
    if cell['cell_type'] != 'markdown':
        return False
    source = cell.get('source', [])
    if not source:
        return False
    # Check for key phrase
    first_line = source[0]
    return "> **License Notice**" in first_line

def process_notebook(filepath, check_only=False):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            nb = json.load(f)
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return False

    cells = nb.get('cells', [])
    if not cells:
        return False

    first_cell = cells[0]

    if is_header(first_cell):
        # Header exists. Check if it's up to date?
        # For now, just assume if it has the title, it's fine.
        return True

    if check_only:
        print(f"[MISSING] {filepath}")
        return False

    # Insert header
    print(f"[FIXING] {filepath}")
    cells.insert(0, HEADER_CELL)
    nb['cells'] = cells

    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(nb, f, indent=1)
        return True
    except Exception as e:
        print(f"Error writing {filepath}: {e}")
        return False

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", nargs="?", default=".", help="Directory to scan")
    parser.add_argument("--check", action="store_true", help="Check only")
    args = parser.parse_args()

    root_dir = Path(args.directory)
    notebooks = list(root_dir.rglob("*.ipynb"))

    # Exclude checkpoints
    notebooks = [p for p in notebooks if ".ipynb_checkpoints" not in str(p)]

    print(f"Scanning {len(notebooks)} notebooks in {root_dir}...")

    fixed_count = 0
    missing_count = 0

    for nb_path in notebooks:
        if args.check:
            if not process_notebook(nb_path, check_only=True):
                missing_count += 1
        else:
            # Check if it needs fixing (process_notebook returns True if fixed or already good)
            # We want to count how many we ACTUALLY fixed.
            # So let's check first.
             with open(nb_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if data['cells'] and is_header(data['cells'][0]):
                    continue # Already good

             process_notebook(nb_path, check_only=False)
             fixed_count += 1

    if args.check:
        print(f"Found {missing_count} notebooks missing headers.")
        if missing_count > 0:
            sys.exit(1)
    else:
        print(f"Fixed headers in {fixed_count} notebooks.")

if __name__ == "__main__":
    main()
