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


def test_all_notebooks_are_accounted_for():
    audited = results()
    assert len(audited) >= 127
    assert len(audited) == len(list(module.iter_notebooks(ROOT)))


def test_notebook_structural_contract():
    failures = [(r.path, r.missing_sections, r.missing_badges) for r in results() if r.missing_sections or r.missing_badges]
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
