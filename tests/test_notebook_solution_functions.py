"""WP-11 harness: pytest validation of notebook solution functions.

Loads the worked "student solution" code directly out of lecture notebooks
and runs parameterized edge-case contracts against it, so regressions in the
curriculum's executable content fail CI like any other code. The ABC/Protocol
interface stubs (``...`` bodies) are validated as contracts too: abstract
bases cannot be instantiated, and structural implementations satisfy the
protocol at runtime.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest
from scipy.optimize import linprog, minimize_scalar

ROOT = Path(__file__).resolve().parents[1]


def _cell_source(nb: dict, cell_ref: int | str) -> str:
    """Return the source of one cell, looked up by stable ID or by index.

    Notebooks carry a stable ``id`` on every cell. Tests should pass that ID
    (a string) so inserting or deleting prose elsewhere in the notebook cannot
    silently shift the target onto a different cell -- the exact failure that
    hit this PR when an authoring pass inserted markdown cells and four tests
    began executing prose as Python. An int is still accepted as a positional
    index for existing call sites, but new tests should use IDs.
    """
    if isinstance(cell_ref, str):
        for cell in nb.get("cells", []):
            if cell.get("id") == cell_ref:
                src = cell["source"]
                return "".join(src) if isinstance(src, list) else str(src)
        raise KeyError(f"no cell with id={cell_ref!r}")
    src = nb["cells"][cell_ref]["source"]
    return "".join(src) if isinstance(src, list) else str(src)


def load_cell(notebook: str, cell_ref: int | str, extra: dict | None = None) -> dict:
    """Execute one code cell of a notebook and return its namespace.

    ``cell_ref`` is a stable cell ID (preferred) or a positional index.
    """
    nb = json.loads((ROOT / notebook).read_text(encoding="utf-8"))
    src = _cell_source(nb, cell_ref)
    namespace: dict = {
        "np": np,
        "minimize_scalar": minimize_scalar,
        "linprog": linprog,
    }
    if extra:
        namespace.update(extra)
    exec(compile(src, f"{notebook}#cell{cell_ref}", "exec"), namespace)
    return namespace


# ---------------------------------------------------------------------------
# Foundations: OOP interface stubs and their implementations
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def oop_ns():
    from abc import ABC, abstractmethod
    from typing import List, Protocol, runtime_checkable

    return load_cell(
        "01-Foundations/11_Object_Oriented_Programming.ipynb",
        15,
        extra={
            "ABC": ABC,
            "abstractmethod": abstractmethod,
            "List": List,
            "Protocol": Protocol,
            "runtime_checkable": runtime_checkable,
        },
    )


def test_abstract_base_cannot_be_instantiated(oop_ns):
    with pytest.raises(TypeError):
        oop_ns["AbstractValuationModel"]()


@pytest.mark.parametrize(
    "cash_flows, rate, expected",
    [
        ([], 0.1, 0.0),
        ([100.0], 0.0, 100.0),
        ([100.0, 100.0], 0.1, 100 / 1.1 + 100 / 1.1**2),
        ([100.0, -40.0], 0.05, 100 / 1.05 - 40 / 1.05**2),
    ],
)
def test_dcf_npv_edge_cases(oop_ns, cash_flows, rate, expected):
    model = oop_ns["DCFModel"]()
    out = model.calculate_npv(cash_flows, rate)
    assert np.isclose(out, expected, rtol=1e-12)


def test_protocol_satisfied_structurally(oop_ns):
    ValuationProtocol = oop_ns["ValuationProtocol"]
    DividendDiscountModel = oop_ns["DividendDiscountModel"]
    assert isinstance(DividendDiscountModel(), ValuationProtocol)


# ---------------------------------------------------------------------------
# Foundations: exception contract of solve_model
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def control_flow_ns():
    return load_cell("01-Foundations/09_Control_Flow_and_Error_Handling.ipynb", 28)


def test_solve_model_valid_params(control_flow_ns):
    assert control_flow_ns["solve_model"]({"beta": 0.96}) == "Equilibrium found."


@pytest.mark.parametrize(
    "params",
    [{"beta": 1.05}, {"beta": 0.0}, {"beta": -0.5}, {"alpha": 0.3}],
)
def test_solve_model_raises_parameter_error(control_flow_ns, params):
    ParameterError = control_flow_ns["ParameterError"]
    with pytest.raises(ParameterError):
        control_flow_ns["solve_model"](params)


# ---------------------------------------------------------------------------
# Micro: correlated equilibrium LP
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def game_ns():
    # the cell's trailing demo call needs payoff matrices in scope
    demo = np.array([[2.0, 0.0], [0.0, 1.0]])
    return load_cell(
        "05-Micro-Models/03_Game_Theory_and_Auctions.ipynb",
        13,
        extra={"payoffs_A": demo, "payoffs_B": demo},
    )


def _ic_residuals(dist, u1, u2):
    """Worst incentive-to-deviate for each player (must be <= 0 at a CE).

    Given the recommendation i, a player's belief is p(i, .) / p(i), so the
    deviation gain is evaluated under the conditional distribution dist[i, :].
    """
    n1, n2 = dist.shape
    dev1 = max(
        dist[i, :] @ u1[i_prime, :] - dist[i, :] @ u1[i, :]
        for i in range(n1)
        for i_prime in range(n1)
    )
    dev2 = max(
        dist[:, j] @ u2[:, j_prime] - dist[:, j] @ u2[:, j]
        for j in range(n2)
        for j_prime in range(n2)
    )
    return dev1, dev2


def test_find_ce_prisoners_dilemma_is_defect_defect(game_ns):
    # Classic PD: T > R > P > S. The only correlated equilibrium is (D, D).
    T, R, P, S = 3.0, 2.0, 1.0, 0.0
    u1 = np.array([[R, S], [T, P]])
    u2 = np.array([[R, T], [S, P]])
    dist = game_ns["find_ce"](u1, u2)
    assert dist is not None
    assert np.isclose(dist.sum(), 1.0)
    assert (dist >= 0).all()
    assert np.isclose(dist[1, 1], 1.0)  # all mass on (Defect, Defect)


def test_find_ce_coordination_pure_profile(game_ns):
    # Pure coordination: (Top, Left) is an equilibrium and welfare-maximizing.
    u1 = np.array([[2.0, 0.0], [0.0, 1.0]])
    u2 = np.array([[2.0, 0.0], [0.0, 1.0]])
    dist = game_ns["find_ce"](u1, u2)
    assert dist is not None
    assert np.isclose(dist.sum(), 1.0)
    dev1, dev2 = _ic_residuals(dist, u1, u2)
    assert dev1 <= 1e-8 and dev2 <= 1e-8
    assert np.isclose(dist[0, 0], 1.0)


def test_find_ce_battle_of_sexes_mixture_is_a_ce(game_ns):
    # Any convex combination over the two pure NE is a CE; the LP must return
    # one of them (or a mixture) with satisfied incentives.
    u1 = np.array([[3.0, 0.0], [0.0, 2.0]])
    u2 = np.array([[2.0, 0.0], [0.0, 3.0]])
    dist = game_ns["find_ce"](u1, u2)
    assert dist is not None
    assert np.isclose(dist.sum(), 1.0)
    dev1, dev2 = _ic_residuals(dist, u1, u2)
    assert dev1 <= 1e-8 and dev2 <= 1e-8


# ---------------------------------------------------------------------------
# Economic Modeling: Tauchen + normal CDF (Numba)
# ---------------------------------------------------------------------------


def _em04_ns():
    pytest.importorskip("numba")
    import math

    from numba import njit

    return load_cell(
        "03-Economic-Modeling/04_Estimation_and_Calibration.ipynb",
        6,
        extra={"njit": njit, "math": math},
    )


def test_norm_cdf_edge_cases():
    ns = _em04_ns()
    norm_cdf = ns["norm_cdf"]
    assert np.isclose(norm_cdf(0.0), 0.5)
    assert norm_cdf(10.0) > 1.0 - 1e-9
    assert norm_cdf(-10.0) < 1e-9
    assert norm_cdf(-1.0) < norm_cdf(0.0) < norm_cdf(1.0)


@pytest.mark.parametrize("rho", [0.0, 0.5, 0.9])
@pytest.mark.parametrize("n", [3, 7, 21])
def test_tauchen_transition_properties(rho, n):
    ns = _em04_ns()
    tauchen = ns["tauchen"]
    grid, P = tauchen(rho, 1.0, n=n, m=3)
    P = np.asarray(P)
    grid = np.asarray(grid)
    assert P.shape == (n, n)
    assert np.allclose(P.sum(axis=1), 1.0)
    assert (P >= 0).all()
    if np.isclose(rho, 0.0):
        assert np.allclose(P, P[:, ::-1], atol=1e-10)  # symmetric transitions
    assert grid[0] < grid[-1] and np.isclose(grid[0], -grid[-1])


# ---------------------------------------------------------------------------
# Economic Modeling: Chebyshev VFI vs Euler iteration
# ---------------------------------------------------------------------------

PARAMS = {
    "BETA": 0.96,
    "R_INTEREST": 0.02,
    "A_MIN": 0.1,
    "A_MAX": 4.0,
    "N_DEGREE": 5,
    "N_Y_STATES": 2,
}
# the notebook's convention: a_nodes are the N_DEGREE Chebyshev nodes mapped
# onto [A_MIN, A_MAX] (chebfit fits exactly at these points)
from numpy.polynomial import chebyshev as _cheb  # noqa: E402

_CHEB_NODES = _cheb.chebgauss(PARAMS["N_DEGREE"])[0]  # in [-1, 1], ascending
A_NODES = (
    PARAMS["A_MIN"] + (PARAMS["A_MAX"] - PARAMS["A_MIN"]) * (_CHEB_NODES + 1.0) / 2.0
)
Y_STATES = np.array([1.0, 1.5])
P_TRANS = np.array([[0.9, 0.1], [0.2, 0.8]])


def _vfi_ns():
    from numpy.polynomial import chebyshev

    return load_cell(
        "03-Economic-Modeling/02_DP_with_Continuous_States.ipynb",
        11,
        extra={"chebyshev": chebyshev, "u": np.log},
    )


def _euler_ns():
    from numpy.polynomial import chebyshev
    from scipy.optimize import brentq

    return load_cell(
        "03-Economic-Modeling/02_DP_with_Continuous_States.ipynb",
        13,
        extra={"chebyshev": chebyshev, "u_prime": lambda c: 1.0 / c, "brentq": brentq},
    )


def test_vfi_chebyshev_returns_finite_coefficients():
    theta = _vfi_ns()["solve_vfi_chebyshev"](
        PARAMS, Y_STATES, P_TRANS, A_NODES, tol=1e-7, max_iter=400
    )
    assert theta.shape == (PARAMS["N_Y_STATES"], PARAMS["N_DEGREE"])
    assert np.isfinite(theta).all()
    # tighter tolerance changes the solution only slightly (converged)
    theta_tight = _vfi_ns()["solve_vfi_chebyshev"](
        PARAMS, Y_STATES, P_TRANS, A_NODES, tol=1e-9, max_iter=600
    )
    assert np.max(np.abs(theta_tight - theta)) < 1e-3


def test_euler_iteration_policy_is_feasible():
    from numpy.polynomial import chebyshev

    coeffs = _euler_ns()["solve_euler_residuals"](
        PARAMS, Y_STATES, P_TRANS, A_NODES, tol=1e-8, max_iter=400
    )
    assert coeffs.shape == (PARAMS["N_Y_STATES"], PARAMS["N_DEGREE"])
    assert np.isfinite(coeffs).all()
    for i, y in enumerate(Y_STATES):
        c_policy = chebyshev.Chebyshev(
            coeffs[i], domain=[PARAMS["A_MIN"], PARAMS["A_MAX"]]
        )(A_NODES)
        assert (c_policy > 0).all()
        # consumption cannot exceed cash on hand (1+r)a + y
        assert (c_policy <= (1 + PARAMS["R_INTEREST"]) * A_NODES + y + 1e-6).all()


def test_euler_time_iteration_residuals_are_small():
    """The time-iteration policy satisfies the Euler equation on a dense grid.

    This is the standard accuracy certificate in quantitative economics (max
    scaled Euler equation error). VFI's own policy is *not* used as the
    reference: its piecewise-linear EV interpolation plus a Chebyshev fit of
    the kinked value function is far cruder than time iteration, so the two
    are only expected to agree qualitatively (both imply positive saving that
    declines with wealth).
    """
    from numpy.polynomial import chebyshev

    a_dense = np.linspace(PARAMS["A_MIN"], PARAMS["A_MAX"], 25)
    # denser fit too: the notebook ties len(a_nodes) to N_DEGREE
    params_hi = {**PARAMS, "N_DEGREE": 12}
    coeffs = _euler_ns()["solve_euler_residuals"](
        params_hi, Y_STATES, P_TRANS, a_dense, tol=1e-9, max_iter=500
    )
    funcs = [
        chebyshev.Chebyshev(coeffs[i], domain=[PARAMS["A_MIN"], PARAMS["A_MAX"]])
        for i in range(PARAMS["N_Y_STATES"])
    ]

    worst = 0.0
    for a in np.linspace(PARAMS["A_MIN"] + 0.05, PARAMS["A_MAX"] - 0.05, 60):
        for i, y in enumerate(Y_STATES):
            cash = (1 + PARAMS["R_INTEREST"]) * a + y
            c_today = max(funcs[i](a), 1e-9)
            assert c_today <= cash + 1e-6, "policy violates the budget constraint"
            a_prime = np.clip(cash - c_today, PARAMS["A_MIN"], PARAMS["A_MAX"])
            c_next = np.maximum(np.array([fk(a_prime) for fk in funcs]), 1e-9)
            gap = 1.0 / c_today - PARAMS["BETA"] * (1 + PARAMS["R_INTEREST"]) * (
                P_TRANS[i] @ (1.0 / c_next)
            )
            worst = max(worst, abs(gap) * c_today)  # scaled Euler error
    assert worst < 0.05


# ---------------------------------------------------------------------------
# Economic Modeling: robust savings (Numba utility) and Rust NFXP
# ---------------------------------------------------------------------------


def _robust_ns():
    pytest.importorskip("numba")
    from numba import njit

    return load_cell(
        "03-Economic-Modeling/06_Robust_Control.ipynb", 11, extra={"njit": njit}
    )


def test_robust_savings_bounds_and_continuity_in_theta():
    ns = _robust_ns()
    solve = ns["solve_savings_problem"]
    W0 = ns["W0"]
    c0_eu = solve()  # theta = inf: standard expected utility
    c0_strong = solve(theta=1.0)
    c0_weak = solve(theta=50.0)
    for c0 in (c0_eu, c0_strong, c0_weak):
        assert 0.0 < c0 < W0
    # continuity: weak ambiguity ~ the EU benchmark; the operator moves
    # smoothly in theta (the direction of the small correction is governed by
    # the risk-sensitive sign convention coded in the lecture cell)
    assert abs(c0_weak - c0_eu) < 0.05
    assert abs(c0_strong - c0_eu) < 0.5


def test_rust_nfxp_flow_utilities_and_beta_zero_solution():
    from scipy.optimize import minimize

    ns = load_cell(
        "03-Economic-Modeling/07_Structural_Estimation.ipynb",
        14,
        extra={"minimize": minimize},
    )
    n_states, beta = 10, 0.0
    maintain = np.full((n_states, n_states), 0.0)
    for i in range(n_states):
        maintain[i, min(i + 1, n_states - 1)] = 0.7
        maintain[i, i] = 0.3
    replace = np.zeros((n_states, n_states))
    replace[:, 0] = 1.0
    solver = ns["RustNFXPSolver"](
        n_states, beta, {"maintain": maintain, "replace": replace}
    )

    u_maintain, u_replace = solver._get_flow_utilities((1.0, 2.0))
    assert u_maintain.shape == (n_states,) and u_replace.shape == (n_states,)
    assert (u_replace == -1.0).all()  # replacement cost is state-independent
    assert (np.diff(u_maintain) == -2.0).all()  # maintenance worsens with mileage

    EV = solver.solve_dp_problem((1.0, 2.0))
    assert EV.shape == (n_states,) and np.isfinite(EV).all()
    # with beta = 0 the Bellman operator is static: EV = logsumexp(u)
    expected = np.log(np.exp(u_maintain) + np.exp(u_replace))
    assert np.allclose(EV, expected, rtol=1e-10)
