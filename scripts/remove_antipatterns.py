"""
Anti-Pattern Remover
--------------------
This script systematically removes the custom `sec()` and `note()` helper functions
found in many notebooks and replaces them with standard Markdown headers and blockquotes.

It performs two actions:
1. Removes the Python definitions of `sec` and `note` from code cells.
2. Converts code cells that *only* call these functions into Markdown cells.

Usage:
    python scripts/remove_antipatterns.py [directory]
"""

import os
import sys
import json
import re
import argparse
from pathlib import Path

# Regex patterns
# Definitions (multi-line, but we look for the start)
DEF_SEC_PATTERN = re.compile(r"def\s+sec\s*\(.*?\):")
DEF_NOTE_PATTERN = re.compile(r"def\s+note\s*\(.*?\):")

# Usages (standalone lines)
# Matches: sec("Title") or sec('Title')
USAGE_SEC_PATTERN = re.compile(r"^\s*sec\s*\(\s*[\"'](.*?)[\"']\s*\)\s*$")
# Matches: note("Message") or note('Message')
USAGE_NOTE_PATTERN = re.compile(r"^\s*note\s*\(\s*[\"'](.*?)[\"']\s*.*?\)\s*$") # ..*? handles kwargs if any

def clean_definitions(source_lines):
    """
    Removes the definition blocks for sec() and note().
    Returns (cleaned_lines, was_modified)
    """
    new_lines = []
    skip_mode = False
    modified = False

    for line in source_lines:
        # Check if we are starting a definition we want to remove
        if DEF_SEC_PATTERN.match(line) or DEF_NOTE_PATTERN.match(line):
            skip_mode = True
            modified = True
            continue

        # If we are in skip mode, we look for the next unindented line
        # (assuming 4-space indentation or similar for the function body)
        if skip_mode:
            # If line is indented, skip it
            if line.startswith(" ") or line.startswith("\t") or line.strip() == "":
                continue
            else:
                # We found the end of the function
                skip_mode = False
                new_lines.append(line)
        else:
            new_lines.append(line)

    return new_lines, modified

def process_notebook(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            nb = json.load(f)
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return False

    cells = nb.get('cells', [])
    modified_nb = False

    new_cells = []

    for cell in cells:
        if cell['cell_type'] == 'code':
            source = cell.get('source', [])

            # --- Check for standalone usage ---
            # We assume the source is a list of strings (lines)
            # If the cell has only 1 line (ignoring whitespace/comments), and it's a sec/note call
            code_str = "".join(source).strip()

            # Handle sec("Title")
            m_sec = USAGE_SEC_PATTERN.match(code_str)
            if m_sec:
                title = m_sec.group(1)
                # Convert to Markdown
                new_cells.append({
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": [f"## {title}"]
                })
                modified_nb = True
                continue

            # Handle note("Message")
            m_note = USAGE_NOTE_PATTERN.match(code_str)
            if m_note:
                msg = m_note.group(1)
                # Convert to Markdown
                new_cells.append({
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": [f"> **Note:** {msg}"]
                })
                modified_nb = True
                continue

            # --- Check for definitions ---
            # If not converted, check if we need to remove definitions inside the cell
            cleaned_source, modified_source = clean_definitions(source)
            if modified_source:
                cell['source'] = cleaned_source
                modified_nb = True

            new_cells.append(cell)

        else:
            new_cells.append(cell)

    if modified_nb:
        nb['cells'] = new_cells
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(nb, f, indent=1)
            print(f"[CLEANED] {filepath}")
            return True
        except Exception as e:
            print(f"Error writing {filepath}: {e}")
            return False

    return False

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", nargs="?", default=".", help="Directory to scan")
    args = parser.parse_args()

    root_dir = Path(args.directory)
    notebooks = list(root_dir.rglob("*.ipynb"))
    notebooks = [p for p in notebooks if ".ipynb_checkpoints" not in str(p)]

    print(f"Scanning {len(notebooks)} notebooks in {root_dir} for anti-patterns...")

    count = 0
    for nb_path in notebooks:
        if process_notebook(nb_path):
            count += 1

    print(f"Removed anti-patterns from {count} notebooks.")

if __name__ == "__main__":
    main()
