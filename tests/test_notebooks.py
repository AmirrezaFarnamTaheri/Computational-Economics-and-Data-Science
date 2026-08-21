"""
Smoke tests for notebook integrity — verifies JSON validity and basic structure.
"""

import json

import pytest


def test_all_notebooks_valid_json(all_notebook_paths):
    """Every .ipynb file must be valid JSON."""
    errors = []
    for nb_path in all_notebook_paths:
        try:
            with open(nb_path, "rb") as f:
                json.loads(f.read())
        except json.JSONDecodeError as e:
            errors.append(f"{nb_path.name}: {e}")
    if errors:
        pytest.fail(f"{len(errors)} notebooks have invalid JSON:\n" + "\n".join(errors))


def test_all_notebooks_have_cells(all_notebook_paths):
    """Every notebook must have at least one cell."""
    empty = []
    for nb_path in all_notebook_paths:
        try:
            with open(nb_path, "rb") as f:
                nb = json.loads(f.read())
            if not nb.get("cells"):
                empty.append(nb_path.name)
        except json.JSONDecodeError:
            pass  # Caught by test_all_notebooks_valid_json
    if empty:
        pytest.fail(f"{len(empty)} notebooks have no cells:\n" + "\n".join(empty))


def test_no_duplicate_badges(all_notebook_paths):
    """Header cell should have at most 1 badge line."""
    import re

    badge_re = re.compile(r"\[!\[(Code|Content) License")
    dupes = []
    for nb_path in all_notebook_paths:
        try:
            with open(nb_path, "rb") as f:
                nb = json.loads(f.read())
        except json.JSONDecodeError:
            continue
        if not nb.get("cells"):
            continue
        cell = nb["cells"][0]
        if cell.get("cell_type") != "markdown":
            continue
        source = cell.get("source", [])
        badge_count = sum(1 for line in source if badge_re.search(line))
        if badge_count > 1:
            dupes.append(f"{nb_path.name}: {badge_count} badge lines")
    if dupes:
        pytest.fail(
            f"{len(dupes)} notebooks have duplicate badges:\n" + "\n".join(dupes)
        )


def test_no_boilerplate_cells(all_notebook_paths):
    """No notebook should contain boilerplate template cells."""
    import re

    patterns = [
        re.compile(r"###\s*Concept Overview:"),
        re.compile(r"###\s*Implementation Detail\b"),
        re.compile(r"\(Introduction text to be added\)"),
    ]
    hits = []
    for nb_path in all_notebook_paths:
        try:
            with open(nb_path, "rb") as f:
                nb = json.loads(f.read())
        except json.JSONDecodeError:
            continue
        for cell in nb.get("cells", []):
            if cell.get("cell_type") != "markdown":
                continue
            source = "".join(cell.get("source", []))
            for pat in patterns:
                if pat.search(source):
                    hits.append(f"{nb_path.name}: {pat.pattern}")
                    break
    if hits:
        pytest.fail(f"{len(hits)} boilerplate cells remain:\n" + "\n".join(hits))
