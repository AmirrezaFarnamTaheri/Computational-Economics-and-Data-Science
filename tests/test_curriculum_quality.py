"""Regression gates for repository-wide notebook quality invariants."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "audit_curriculum_ast.py"
spec = importlib.util.spec_from_file_location("audit_curriculum_ast", SCRIPT)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)


def results():
    return [module.audit_notebook(path, ROOT) for path in module.iter_notebooks(ROOT)]


# Release invariant: the curriculum ships exactly this set of lessons. The
# count must be updated deliberately when a lesson is added or removed -- a
# bare ">=" floor would stay green if one or two notebooks were accidentally
# deleted. Kept in sync with audit_curriculum_ast.iter_notebooks, which is the
# same source enumeration the strict CI gate audits.
EXPECTED_NOTEBOOK_COUNT = 129


def test_all_notebooks_are_accounted_for():
    audited = results()
    assert len(audited) == EXPECTED_NOTEBOOK_COUNT, (
        f"curriculum notebook count changed: {len(audited)} != "
        f"{EXPECTED_NOTEBOOK_COUNT}. If lessons were added or removed, update "
        "EXPECTED_NOTEBOOK_COUNT deliberately."
    )
    # The audit must cover every notebook the source iterator finds, so a gap
    # between the auditor's enumeration and the canonical one is caught.
    enumerated = list(module.iter_notebooks(ROOT))
    assert {Path(r.path) for r in audited} == {p.relative_to(ROOT) for p in enumerated}


def test_notebook_structural_contract():
    failures = [
        (r.path, r.missing_sections, r.missing_badges)
        for r in results()
        if r.missing_sections or r.missing_badges
    ]
    assert not failures


def test_notebook_integrity_contract():
    failures = [
        (r.path, r.missing_cell_ids, r.duplicate_cell_ids, r.syntax_errors)
        for r in results()
        if r.missing_cell_ids or r.duplicate_cell_ids or r.syntax_errors
    ]
    assert not failures


def test_notebook_placeholder_and_warning_contract():
    failures = [
        (r.path, r.placeholders, r.blanket_warning_suppression)
        for r in results()
        if r.placeholders or r.blanket_warning_suppression
    ]
    assert not failures


def test_notebook_local_images_resolve():
    failures = [(r.path, r.broken_images) for r in results() if r.broken_images]
    assert not failures
