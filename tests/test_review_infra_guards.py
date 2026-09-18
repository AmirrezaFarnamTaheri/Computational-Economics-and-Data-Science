"""Regression guards for review findings in shared audit infrastructure."""

import shutil
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import generate_release_audit as release  # noqa: E402
import test_stub_inventory as stubs  # noqa: E402


@pytest.fixture()
def isolated_tree(tmp_path):
    """A tree with one source notebook and one executed artifact copy."""
    source = ROOT / "01-Foundations/12_NumPy.ipynb"
    (tmp_path / "01-Foundations").mkdir()
    (tmp_path / "build" / "exec").mkdir(parents=True)
    shutil.copy2(source, tmp_path / "01-Foundations" / source.name)
    shutil.copy2(source, tmp_path / "build" / "exec" / source.name)
    return tmp_path


def test_release_audit_counts_source_notebooks_once(isolated_tree):
    assert [p.name for p in release.notebooks(isolated_tree)] == ["12_NumPy.ipynb"]


def test_release_audit_hash_manifest_excludes_artifacts(isolated_tree):
    hashes = release.file_hashes(isolated_tree)
    assert "01-Foundations/12_NumPy.ipynb" in hashes
    assert not any(key.startswith("build/") for key in hashes)


@pytest.mark.parametrize(
    "body,expected",
    [
        ("pass", "pass"),
        ("...", "ellipsis"),
        ('"""Implement me."""\npass', "pass"),
        ('"""Implement me."""\n...', "ellipsis"),
        ("raise NotImplementedError", "not-implemented"),
        ('"""Implement me."""\nraise NotImplementedError', "not-implemented"),
        ('"""Docstring only."""', "docstring-only"),
        ("return 1", None),
        ('"""Docstring."""\nreturn 1', None),
    ],
)
def test_stub_kind_recognises_documented_stubs(body, expected):
    import ast

    module = ast.parse(
        "def probe():\n" + "\n".join("    " + line for line in body.splitlines())
    )
    assert stubs.stub_kind(module.body[0]) == expected
