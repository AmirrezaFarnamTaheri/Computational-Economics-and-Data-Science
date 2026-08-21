import argparse
import os
import re

import nbformat
from nbformat.v4 import new_markdown_cell

# --- Constants ---
LICENSE_BADGE = "[![Code License: MIT](https://img.shields.io/badge/Code%20License-MIT-yellow.svg)](LICENSE) [![Content License: CC BY 4.0](https://img.shields.io/badge/Content%20License-CC%20BY%204.0-blue.svg)](https://creativecommons.org/licenses/by/4.0/)"

# Regex to find existing badges (loose match to catch variations)
BADGE_REGEX = r"\[!\[.*License.*\]\(.*\)\]\(.*\)"


def normalize_badges(nb, filename):
    """
    Ensures exactly one license badge block exists in the first cell.
    Removes badges from all other cells.
    """
    changes = []

    # 1. Remove badges from ALL cells
    for i, cell in enumerate(nb.cells):
        if cell.cell_type == "markdown":
            lines = cell.source.split("\n")
            new_lines = []
            cell_changed = False
            for line in lines:
                if re.search(BADGE_REGEX, line):
                    cell_changed = True
                    continue  # Skip badge line
                new_lines.append(line)

            if cell_changed:
                cell.source = "\n".join(new_lines).strip()
                if (
                    not cell.source and i > 0
                ):  # If cell became empty and not first cell, maybe mark for deletion?
                    # For now, just leave empty or stripping handles it
                    pass
                changes.append(f"Removed badge from cell {i}")

    # 2. Insert Canonical Badge in Cell 0
    if not nb.cells:
        nb.cells.append(
            new_markdown_cell(
                f"# {os.path.splitext(os.path.basename(filename))[0]}\n\n{LICENSE_BADGE}"
            )
        )
        changes.append("Created cell 0 with title and badge")
    else:
        cell0 = nb.cells[0]
        if cell0.cell_type == "markdown":
            # Check if it has a title
            lines = cell0.source.split("\n")

            # Find where to insert badge (after Title)
            insert_idx = 0
            for j, line in enumerate(lines):
                if line.strip().startswith("# "):
                    insert_idx = j + 1
                    break

            # If no title found, insert at top or keep existing structure?
            # Ideally we want Title then Badge.

            # Insert Badge
            if insert_idx < len(lines) and lines[insert_idx].strip() == "":
                # Reuse empty line
                pass
            else:
                lines.insert(insert_idx, "")

            lines.insert(insert_idx + 1, LICENSE_BADGE)

            # Clean up: multiple empty lines
            final_lines = []
            for line in lines:
                if line.strip() == "" and final_lines and final_lines[-1].strip() == "":
                    continue
                final_lines.append(line)

            cell0.source = "\n".join(final_lines).strip()
            changes.append("Inserted canonical badge in cell 0")
        else:
            # Cell 0 is code, insert new markdown cell at top
            nb.cells.insert(
                0,
                new_markdown_cell(
                    f"# {os.path.splitext(os.path.basename(filename))[0]}\n\n{LICENSE_BADGE}"
                ),
            )
            changes.append("Inserted new markdown cell 0 with badge")

    return changes


def ensure_structure_placeholders(nb):
    """
    Checks for presence of Lens, Objectives, Prerequisites.
    Does NOT overwrite existing content, just reports or adds placeholder if requested.
    For this implementation, we just REPORT missing sections to avoid "template contamination".
    """
    # Scan for headers
    has_lens = False
    has_objectives = False
    has_prereqs = False
    has_toc = False

    for cell in nb.cells:
        if cell.cell_type == "markdown":
            src = cell.source.lower()
            if "the lens" in src and "#" in src:
                has_lens = True
            if "learning objectives" in src and "#" in src:
                has_objectives = True
            if "prerequisites" in src and "#" in src:
                has_prereqs = True
            if "table of contents" in src and "#" in src:
                has_toc = True

    missing = []
    if not has_lens:
        missing.append("The Lens")
    if not has_objectives:
        missing.append("Learning Objectives")
    if not has_prereqs:
        missing.append("Prerequisites")
    if not has_toc:
        missing.append("Table of Contents")

    return missing


def process_notebook(filepath, fix_badges=True):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            nb = nbformat.read(f, as_version=4)

        changes = []
        filename = os.path.basename(filepath)

        if fix_badges:
            badge_changes = normalize_badges(nb, filename)
            changes.extend(badge_changes)

        # Structure check
        missing_sections = ensure_structure_placeholders(nb)

        # Save if changed
        if changes:
            with open(filepath, "w", encoding="utf-8") as f:
                nbformat.write(nb, f)
            print(f"Updated {filepath}:")
            for c in changes:
                print(f"  - {c}")
        else:
            print(f"No changes for {filepath}")

        if missing_sections:
            print(f"  [MISSING SECTIONS]: {', '.join(missing_sections)}")

    except Exception as e:
        print(f"Error processing {filepath}: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Standardize notebook headers and badges."
    )
    parser.add_argument("target", help="File or directory to process")
    parser.add_argument(
        "--fix-badges",
        action="store_true",
        default=True,
        help="Normalize license badges",
    )

    args = parser.parse_args()

    if os.path.isfile(args.target):
        process_notebook(args.target, args.fix_badges)
    elif os.path.isdir(args.target):
        for root, dirs, files in os.walk(args.target):
            if ".ipynb_checkpoints" in root:
                continue
            for file in files:
                if file.endswith(".ipynb"):
                    process_notebook(os.path.join(root, file), args.fix_badges)
    else:
        print(f"Invalid target: {args.target}")
