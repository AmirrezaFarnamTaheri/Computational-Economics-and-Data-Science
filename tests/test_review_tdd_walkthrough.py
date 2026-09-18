"""The teaching walkthrough must not overwrite a learner's project files."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "01-Foundations/02_Professional_Development_Environment.ipynb"


def test_tdd_walkthrough_is_isolated_and_checks_red_green(tmp_path, monkeypatch):
    notebook = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    protected = tmp_path / "finance_utils.py"
    original = "# Existing learner work must survive the demonstration.\n"
    protected.write_text(original, encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    namespace = {}
    for index in (18, 21, 23, 25, 27):
        source = "".join(notebook["cells"][index]["source"])
        exec(compile(source, f"{NOTEBOOK.name}:cell-{index}", "exec"), namespace)
        assert protected.read_text(encoding="utf-8") == original
    assert namespace["red_result"].returncode == 1
    assert namespace["green_result"].returncode == 0
