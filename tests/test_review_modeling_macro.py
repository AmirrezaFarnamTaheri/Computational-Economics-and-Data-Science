"""Regression probes for reviewed economic mechanisms, using notebook sources."""

import ast
import json
import math
from pathlib import Path

import numpy as np
import pytest
from numpy.polynomial import chebyshev
from scipy.integrate import quad
from scipy.optimize import brentq, minimize_scalar
from scipy.sparse import bmat, diags, eye
from scipy.sparse.linalg import spsolve

ROOT = Path(__file__).resolve().parents[1]


def load_definitions(path, cell_id, preserve_decorators=False, **extra):
    notebook = json.loads((ROOT / path).read_text(encoding="utf-8"))
    source = "".join(
        next(c for c in notebook["cells"] if c.get("id") == cell_id)["source"]
    )
    tree = ast.parse(source)
    nodes = [
        node
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.Import, ast.ImportFrom))
    ]
    for node in nodes:
        if not preserve_decorators and isinstance(
            node, (ast.FunctionDef, ast.ClassDef)
        ):
            node.decorator_list = []
    namespace = {
        "np": np,
        "math": math,
        "prange": range,
        "chebyshev": chebyshev,
        "brentq": brentq,
        "minimize_scalar": minimize_scalar,
        "quad": quad,
    }
    namespace.update(extra)
    exec(compile(ast.Module(body=nodes, type_ignores=[]), path, "exec"), namespace)
    return namespace


def test_howard_checks_value_residual_not_just_unchanged_policy():
    ns = load_definitions(
        "03-Economic-Modeling/01_Dynamic_Programming.ipynb", "17728f84"
    )
    value, policy = ns["howard_policy_iteration"](
        np.ones((1, 1, 1)), np.ones((1, 1, 1, 1)), 0.96, tol=1e-9
    )
    assert value.item() == pytest.approx(25.0, abs=3e-8)
    assert policy.item() == 0


def test_continuous_tauchen_preserves_tail_mass():
    ns = load_definitions(
        "03-Economic-Modeling/02_DP_with_Continuous_States.ipynb",
        "eb487d4f",
        PARAMS={"GAMMA": 2},
    )
    _, transition = ns["tauchen"](0.95, 0.1, 7, 3)
    np.testing.assert_allclose(transition.sum(axis=1), 1, atol=1e-14)
    assert np.min(transition) >= 0


def test_egm_uses_beginning_assets_and_respects_budget():
    numba = pytest.importorskip("numba")
    ns = load_definitions(
        "03-Economic-Modeling/02_DP_with_Continuous_States.ipynb",
        "f3654025",
        preserve_decorators=True,
        njit=numba.njit,
        prange=numba.prange,
    )
    assets = np.linspace(0.01, 10, 300)
    income = np.array([0.5, 1.5])
    transition = np.array([[0.8, 0.2], [0.2, 0.8]])
    consumption = ns["egm_solver"](0.03, 0.96, 2, income, transition, assets)
    cash = 1.03 * assets[None, :] + income[:, None]
    savings = cash - consumption
    assert consumption.min() > 0
    assert savings.min() >= assets[0] - 1e-10
    assert savings.max() <= assets[-1] + 1e-10
    # A borrowing-constrained household consumes income, not just its tiny assets.
    assert consumption[0, 0] > 0.4


def test_robust_savings_is_pessimistic_and_stable():
    ns = load_definitions(
        "03-Economic-Modeling/06_Robust_Control.ipynb",
        "145fc71a",
        W0=100,
        R=1.02,
        BETA=0.96,
        GAMMA=2,
        Y_H=15,
        Y_L=5,
        P0_H=0.5,
    )
    solve = ns["solve_savings_problem"]
    expected_utility = solve()
    assert solve(0.001) < solve(1.0) < expected_utility
    assert np.isfinite(solve(1e-8))
    with pytest.raises(ValueError, match="theta"):
        solve(0)


def test_rust_likelihood_extreme_costs_and_inner_residual():
    ns = load_definitions(
        "03-Economic-Modeling/07_Structural_Estimation.ipynb", "3c7cb159"
    )
    transition = np.array([[0, 1, 0], [0, 0, 1], [0, 0, 1]])
    reset = np.zeros((3, 3))
    reset[:, 0] = 1
    model = ns["RustNFXPSolver"](3, 0.95, {"maintain": transition, "replace": reset})
    params = [1000, 100]
    value = model.solve_dp_problem(params)
    um, ur = model._get_flow_utilities(params)
    bellman = np.logaddexp(um + 0.95 * transition @ value, ur + 0.95 * reset @ value)
    np.testing.assert_allclose(value, bellman, atol=1e-8)
    loss = model._log_likelihood(params, np.array([0, 1]), np.array([0, 2]))
    assert np.isfinite(loss)
    with pytest.raises(RuntimeError, match="converge"):
        model.solve_dp_problem(params, max_iter=1)


def test_olg_savings_satisfies_euler_and_log_limit():
    ns = load_definitions("04-Macro-Models/04_OLG_Models.ipynb", "73b7f73f")
    for sigma in [1, 2, 4]:
        model = ns["GeneralOLGModel"](sigma=sigma)
        k = model.k_star
        wage = model.wage_f(k)
        gross_return = 1 + model.interest_f(k)
        saving = (1 + model.n) * k
        assert (wage - saving) ** (-sigma) == pytest.approx(
            model.beta * gross_return * (gross_return * saving) ** (-sigma)
        )
        if sigma == 1:
            assert saving == pytest.approx(model.beta * wage / (1 + model.beta))


def test_news_pipeline_and_impact_resource_constraints():
    pd = pytest.importorskip("pandas")
    from macro_utils import solve_qz

    path = "04-Macro-Models/03D_RBC_News_Shocks_and_Expectations.ipynb"
    ns = load_definitions(path, "c8da7ef9", pd=pd, solve_qz=solve_qz)
    ns = load_definitions(path, "e3879ed5", **ns)
    model = ns["RBCNewsModel"]()
    state = np.zeros(6)
    state[-1] = 0.01
    c = (model.solution["Policy"] @ state).item()
    labor, output, investment, _, _ = model.reconstruct_variables(0, 0, c)
    assert c > 0 and labor < 0 and output < 0 and investment < 0
    np.testing.assert_allclose(
        model.ss.Y * output, model.ss.C * c + model.ss.I * investment
    )
    productivity = []
    for _ in range(5):
        productivity.append(state[1])
        state = model.solution["Transition"] @ state
    np.testing.assert_allclose(productivity, [0, 0, 0, 0, 0.01], atol=1e-12)


def test_zlb_levels_and_last_period_shock():
    pd = pytest.importorskip("pandas")
    path = "04-Macro-Models/05_New_Keynesian_Models.ipynb"
    ns = load_definitions(path, "bf9c34b1", pd=pd)
    params = ns["NKModel"]().__dict__
    solve = load_definitions(path, "b25ab7d0", pd=pd)["simulate_zlb"]
    baseline = solve(params, np.zeros(3))
    np.testing.assert_allclose(baseline["Output Gap"], 0)
    np.testing.assert_allclose(baseline["Nominal Rate"], -np.log(params["beta"]))
    shock = solve(params, np.array([0, 0, -0.05]))
    assert shock.iloc[-1]["Output Gap"] < 0
    assert shock.iloc[-1]["Nominal Rate"] == 0
    with pytest.raises(ValueError, match="Indeterminate"):
        ns["NKModel"](phi_pi=0.8)


def test_hjb_log_utility_and_generator_conservation():
    ns = load_definitions(
        "04-Macro-Models/08_Continuous_Time_Macro_HJB.ipynb",
        "ffcc1af3",
        bmat=bmat,
        diags=diags,
        eye=eye,
        spsolve=spsolve,
    )
    with np.errstate(divide="raise", invalid="raise"):
        result = ns["solve_two_state_hjb"](n_assets=60, gamma=1)
    assert result["max_hjb_residual"] < 1e-7
    np.testing.assert_allclose(
        np.asarray(result["generator"].sum(axis=1)), 0, atol=1e-12
    )
    assert np.min(result["consumption"]) > 0
