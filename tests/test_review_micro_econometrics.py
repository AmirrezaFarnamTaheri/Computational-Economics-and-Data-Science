"""Regression probes of the notebook sources changed by the curriculum review."""

import ast
import json
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]


def source(relative, cell_id):
    notebook = json.loads((ROOT / relative).read_text(encoding="utf-8"))
    return next(
        "".join(cell["source"])
        for cell in notebook["cells"]
        if cell.get("id") == cell_id
    )


def definitions(relative, cell_id, namespace):
    tree = ast.parse(source(relative, cell_id))
    tree.body = [
        node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.ClassDef))
    ]
    for node in tree.body:
        node.decorator_list = []
    exec(compile(tree, relative, "exec"), namespace)
    return namespace


def test_probit_matches_independent_likelihood():
    sm = pytest.importorskip("statsmodels.api")
    scipy = pytest.importorskip("scipy")
    from scipy.optimize import minimize
    from scipy.stats import norm

    relative = "06-Econometrics/02B_MLE_Optimization_and_Applications.ipynb"
    ns = {"np": np, "minimize": minimize, "norm": norm}
    definitions(relative, "ea22e4c0", ns)
    definitions(relative, "probit_example", ns)
    rng = np.random.default_rng(42)
    x = sm.add_constant(rng.normal(size=(1000, 2)))
    y = (x @ [-0.5, 1.2, -0.8] + rng.normal(size=1000) > 0).astype(int)
    fitted = ns["MLEstimator"](ns["loglike_probit"], {"X": x, "y": y}).fit([0, 0, 0])
    reference = sm.Probit(y, x).fit(disp=0)
    np.testing.assert_allclose(fitted.mle_params, reference.params, atol=1e-6)
    np.testing.assert_allclose(fitted.loglike_val, reference.llf, atol=1e-8)
    assert scipy is not None
    tail = ns["loglike_probit"]([100], {"X": np.ones((2, 1)), "y": np.array([0, 1])})
    assert np.isfinite(tail) and tail < -5000


def test_mle_does_not_publish_failed_optimizer_result():
    from scipy.optimize import minimize

    ns = {"np": np, "minimize": minimize}
    definitions(
        "06-Econometrics/02B_MLE_Optimization_and_Applications.ipynb", "ea22e4c0", ns
    )
    model = ns["MLEstimator"](lambda theta, data: np.nan, None)
    with pytest.raises(RuntimeError, match="optimization failed"):
        model.fit([0.0])
    assert model.results is None


def test_2sls_structural_covariance_matches_statsmodels():
    sm = pytest.importorskip("statsmodels.api")
    from statsmodels.sandbox.regression.gmm import IV2SLS

    ns = {"np": np, "sm": sm}
    definitions("06-Econometrics/05_Instrumental_Variables.ipynb", "372eb970", ns)
    rng = np.random.default_rng(42)
    z = rng.normal(size=(1000, 2))
    u = rng.normal(size=1000)
    x = z @ [0.7, 0.3] + 0.5 * u + rng.normal(size=1000)
    y = 1 + 2 * x + u
    fitted = ns["TwoStageLeastSquares"]().fit(y, x, z)
    reference = IV2SLS(y, sm.add_constant(x), sm.add_constant(z)).fit()
    np.testing.assert_allclose(fitted.second_stage_params, reference.params, atol=1e-10)
    np.testing.assert_allclose(fitted.se, reference.bse, atol=1e-10)


def test_iv_simulation_instruments_do_not_enter_structural_error():
    sm = pytest.importorskip("statsmodels.api")
    ns = {"np": np, "sm": sm}
    code = source("06-Econometrics/04_GMM.ipynb", "fdbc21eb")
    # A larger draw distinguishes population exogeneity from small-sample luck.
    exec(code.replace("N = 1000", "N = 200000"), ns)
    moments = ns["Z"].T @ ns["u"] / ns["N"]
    assert np.max(np.abs(moments)) < 0.01
    assert np.corrcoef(ns["x"], ns["u"])[0, 1] > 0.1


def test_ccapm_true_moments_and_identifying_rank():
    ns = {"np": np}
    code = source("06-Econometrics/04_GMM.ipynb", "17226091")
    exec(code.replace("T = 500", "T = 200000"), ns)
    data = ns["data_ccapm"]
    moments = ns["ccapm_moment_conditions"]([0.99, 2.5], data)
    assert np.max(np.abs(moments.mean(axis=0))) < 0.0002
    sdf_return = 0.99 * data["c_growth"] ** (-2.5) * data["returns"]
    jacobian = (
        data["instruments"].T
        @ np.column_stack([sdf_return / 0.99, -sdf_return * np.log(data["c_growth"])])
        / len(sdf_return)
    )
    assert np.linalg.svd(jacobian, compute_uv=False).min() > 0.02


@pytest.mark.parametrize(
    "relative,cell_id",
    [
        ("03_Causal_Inference", "72d0bf27"),
        ("05_Instrumental_Variables", "5d3d4f05"),
        ("12_Panel_Data_Methods", "2b220f7b"),
    ],
)
def test_rng_setup_follows_numpy_import(relative, cell_id):
    code = source(f"06-Econometrics/{relative}.ipynb", cell_id)
    assert code.index("import numpy as np") < code.index("rng = np.random.default_rng")


def test_rd_effect_display_is_inside_callback():
    tree = ast.parse(
        source("06-Econometrics/06_Regression_Discontinuity.ipynb", "48223728")
    )
    function = next(n for n in tree.body if isinstance(n, ast.FunctionDef))
    assert isinstance(function.body[-1], ast.Expr)
    assert isinstance(function.body[-1].value, ast.Call)
    assert function.body[-1].value.func.id == "display"
    assert not any(
        isinstance(n, ast.Name) and n.id == "rd_model"
        for node in tree.body
        if not isinstance(node, ast.FunctionDef)
        for n in ast.walk(node)
    )


def test_normal_gmm_second_step_keeps_variance_in_bounds():
    tree = ast.parse(source("06-Econometrics/04_GMM.ipynb", "b4c0d7ae"))
    calls = [
        n
        for n in ast.walk(tree)
        if isinstance(n, ast.Call) and getattr(n.func, "id", "") == "minimize"
    ]
    assert len(calls) == 2
    for call in calls:
        assert {"args", "bounds"} <= {k.arg for k in call.keywords if k.arg}
