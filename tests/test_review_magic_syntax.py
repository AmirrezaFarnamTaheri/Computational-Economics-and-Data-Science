"""Regression for the %%time syntax-audit blind spot found in review."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from audit_curriculum_ast import _parseable_source  # noqa: E402


def test_time_magic_body_is_parsed_as_python():
    source = "%%time\nx = 1 + 1\nprint(x)\n"
    transformed = _parseable_source(source)
    # The body must survive as real Python, not vanish into a string literal
    # or a bare placeholder.
    assert "x = 1 + 1" in transformed or "print(x)" in transformed
    compile(transformed, "<probe>", "exec")


def test_broken_python_under_time_magic_is_detected():
    source = "%%time\ndef broken(:\n    pass\n"
    transformed = _parseable_source(source)
    import ast

    with_error = False
    try:
        ast.parse(transformed, filename="<probe>")
    except SyntaxError:
        with_error = True
    assert with_error, "invalid Python under %%time must fail the syntax gate"


def test_valid_notebook_cells_still_parse():
    for source in (
        "%matplotlib inline\nimport numpy as np\n",
        "!ls\n",
        "%config InlineBackend.figure_format = 'retina'\n",
    ):
        import ast

        ast.parse(_parseable_source(source), filename="<probe>")
