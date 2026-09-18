"""SDID weighting-problem regression coverage.

The original notebook estimated unit (omega) and time (lambda) simplex
weights by matching *levels* with no free intercept. SDID is specifically
built to tolerate permanent additive level differences while balancing
trajectories, and the reference implementation defaults to
``omega.intercept = TRUE`` and ``lambda.intercept = TRUE``. Matching levels
without an intercept forces the weighted controls to reproduce the treated
unit's level, not just its path.

These tests pin the property the reviewer asked for: a constant additive
shift in the unit or time level must not move the estimate.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest
from scipy.optimize import minimize

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "06-Econometrics" / "13_Modern_Causal_Frontiers_SDID.ipynb"


@pytest.fixture(scope="module")
def simplex_ridge():
    """Load simplex_ridge straight out of the notebook source."""
    nb = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    for cell in nb["cells"]:
        if cell.get("cell_type") == "code":
            src = "".join(cell["source"])
            if "def simplex_ridge" in src:
                ns = {"np": np, "minimize": minimize}
                exec(compile(src, "sdid-notebook", "exec"), ns)
                return ns["simplex_ridge"]
    pytest.fail("simplex_ridge not found in the SDID notebook")


@pytest.fixture(scope="module")
def panel():
    """An (N x T) panel with permanent additive unit and time level effects."""
    rng = np.random.default_rng(0)
    n_units, n_periods = 30, 15
    unit_fe = rng.normal(scale=1.0, size=n_units)
    time_fe = rng.normal(scale=0.5, size=n_periods)
    noise = rng.normal(scale=0.2, size=(n_units, n_periods))
    return unit_fe[:, None] + time_fe[None, :] + noise


def _control_and_treated(panel):
    """Split into a control block (N0 x T0) and a treated pre-period path."""
    controls = panel[:20]  # N0=20 control units
    treated = panel[20:25]  # 5 treated units
    co_pre = controls[:, :10]  # N0 x T0 pre-period block
    tr_pre = treated[:, :10].mean(axis=0)  # T0: treated average pre-period path
    return co_pre.T, tr_pre  # A is T0 x N0, b is T0


def test_weights_sum_to_one(simplex_ridge, panel):
    """The simplex constraint is preserved once centering is applied."""
    A, b = _control_and_treated(panel)
    w = simplex_ridge(A, b, ridge=0.05)
    assert np.isclose(w.sum(), 1.0, atol=1e-8)
    assert (w >= -1e-9).all()


def test_level_shift_leaves_weights_unchanged(simplex_ridge, panel):
    """Adding a constant to the target must not move the weights.

    This is the defining consequence of the free intercept: the matching
    problem balances trajectory, not level. Without the intercept the same
    shift forces the weights to chase the level and they move.
    """
    A, b = _control_and_treated(panel)
    w0 = simplex_ridge(A, b, ridge=0.05)
    w1 = simplex_ridge(A, b + 100.0, ridge=0.05)
    assert np.allclose(w0, w1, atol=1e-8), (
        "weights are not level-shift invariant; the intercept correction is "
        "missing from the weight estimation problem"
    )


def test_no_intercept_version_differs(simplex_ridge, panel):
    """Documents why the intercept is required.

    Without it the matching problem must reproduce the treated level from
    control levels alone; on a panel where the treated block carries a
    permanent additive offset that is not achievable, so the weights move
    chasing the level. This test only asserts the no-intercept problem
    differs from the invariant one -- it never claims the no-intercept
    weights are meaningful.
    """
    A, b = _control_and_treated(panel)
    w0 = simplex_ridge(A, b, ridge=0.05, intercept=False)
    w1 = simplex_ridge(A, b, ridge=0.05)
    assert not np.allclose(w0, w1, atol=1e-8)


def test_notebook_states_the_intercept(simplex_ridge):
    """The notebook's balancing section must specify the intercept term."""
    nb = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    markdown = "\n".join(
        "".join(c["source"]) for c in nb["cells"] if c.get("cell_type") == "markdown"
    )
    balancing = markdown.split("## 2. Unit and Time Balancing")[1]
    assert r"\alpha_\omega" in balancing
    assert r"\alpha_\lambda" in balancing
    # The dimension error in the original prose is corrected.
    assert r"N_0 \times T_0" in balancing
    assert r"T_0 \times N_0" not in balancing
