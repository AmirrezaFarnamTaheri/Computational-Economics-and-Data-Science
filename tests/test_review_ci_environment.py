"""Check the exact lock-extraction code embedded in the CI workflow."""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_ci_exports_only_pip_requirements(tmp_path, monkeypatch):
    workflow = (ROOT / ".github/workflows/CI.yml").read_text(encoding="utf-8")
    match = re.search(r"python - <<'PY'\n(.*?)^          PY$", workflow, re.M | re.S)
    assert match is not None
    code = "\n".join(line[10:] for line in match.group(1).splitlines())
    lock = {"dependencies": ["python=3.13", "pip", {"pip": ["numpy==2.5.2"]}]}
    (tmp_path / "environment.lock.yml").write_text(json.dumps(lock), encoding="utf-8")
    # json is a YAML subset. A tiny yaml adapter keeps the minimal test job
    # independent of PyYAML while exercising the workflow's real extraction.
    (tmp_path / "yaml.py").write_text(
        "import json\nsafe_load = json.loads\n", encoding="utf-8"
    )
    monkeypatch.chdir(tmp_path)
    import subprocess
    import sys

    result = subprocess.run(
        [sys.executable, "-c", code], cwd=tmp_path, capture_output=True, text=True
    )
    assert result.returncode == 0, result.stderr
    assert (tmp_path / "requirements-ci.txt").read_text() == "numpy==2.5.2\n"


def test_deterministic_python_matches_lock():
    workflow = (ROOT / ".github/workflows/CI.yml").read_text(encoding="utf-8")
    deterministic = workflow.split("  deterministic-execution:", 1)[1].split(
        "  docs-strict:", 1
    )[0]
    lock = (ROOT / "environment.lock.yml").read_text(encoding="utf-8")
    python = re.search(r"^  - python=([\d.]+)$", lock, re.M).group(1)
    assert f"python-version: '{python}'" in deterministic
    assert tuple(map(int, python.split("."))) >= (3, 12)
