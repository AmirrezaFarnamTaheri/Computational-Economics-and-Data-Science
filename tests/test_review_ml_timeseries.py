"""Focused regressions executing the reviewed notebooks' own source cells."""

import ast
import json
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]


def source(path, cell):
    notebook = json.loads((ROOT / path).read_text(encoding="utf-8"))
    return "".join(notebook["cells"][cell]["source"])


def test_boosting_synthetic_data_shapes():
    """Execute the actual dataset statements, without importing optional XGBoost."""
    code = source("07-Machine-Learning/02_Gradient_Boosting_Machines.ipynb", 10)
    tree = ast.parse(code)
    statements = tree.body[:2]
    namespace = {"np": np, "rng": np.random.default_rng(42)}
    exec(
        compile(ast.Module(body=statements, type_ignores=[]), "boosting-data", "exec"),
        namespace,
    )
    assert namespace["X"].shape == (100, 5)
    assert namespace["y"].shape == (100,)
    assert np.isfinite(namespace["y"]).all()


def test_macro_lstm_split_has_disjoint_targets_and_training_only_scaling():
    pytest.importorskip("sklearn")
    pd = pytest.importorskip("pandas")
    from sklearn.preprocessing import StandardScaler

    code = source("07-Machine-Learning/09_LSTMs_and_GRUs.ipynb", 21)
    code = code[code.index("# --- Prepare data for LSTM ---") :]
    # A large distribution shift exposes full-sample fitting immediately.
    data = np.column_stack([np.arange(100), np.arange(100) ** 2, np.ones(100)])
    data[80:, 0] += 10000
    frame = pd.DataFrame(data)
    namespace = {"np": np, "StandardScaler": StandardScaler, "macro_data": frame}
    exec(compile(code, "macro-lstm-preprocessing", "exec"), namespace)
    np.testing.assert_allclose(namespace["scaler"].mean_, frame.iloc[:80].mean())
    train_targets = namespace["y_train"]
    test_targets = namespace["y_test"]
    scaler = namespace["scaler"]
    train_raw = train_targets * scaler.scale_[0] + scaler.mean_[0]
    test_raw = test_targets * scaler.scale_[0] + scaler.mean_[0]
    assert train_raw.max() < 80
    assert test_raw.min() >= 10080
    assert namespace["X_train"].shape[1:] == (8, 3)
    assert train_targets.shape[1] == 4


def test_granger_calculation_matches_statsmodels_not_a_guaranteed_nonrejection():
    pytest.importorskip("statsmodels")
    namespace = {"np": np}
    code = source("08-Time-Series/04A_VAR_Estimation_and_Granger.ipynb", 11)
    exec(compile(code, "granger-directionality", "exec"), namespace)
    assert namespace["k_u2"] - namespace["k_r2"] == 1
    np.testing.assert_allclose(
        [namespace["F2"], namespace["p2"]], namespace["reference"][:2]
    )
    assert 0 < namespace["p2"] < 1


def test_var_fevd_notebook_runs_and_normalizes_shock_axis():
    pytest.importorskip("statsmodels")
    pd = pytest.importorskip("pandas")
    matplotlib = pytest.importorskip("matplotlib")
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from statsmodels.tsa.api import VAR

    namespace = {
        "np": np,
        "pd": pd,
        "plt": plt,
        "VAR": VAR,
        "rng": np.random.default_rng(42),
    }
    path = "08-Time-Series/04C_VAR_Impulse_Responses_and_FEVD.ipynb"
    try:
        for cell in (5, 7):
            exec(compile(source(path, cell), f"fevd-cell-{cell}", "exec"), namespace)
        decomposition = namespace["fevd_array"]
        assert decomposition.shape == (2, 10, 2)
        np.testing.assert_allclose(decomposition.sum(axis=2), 1, atol=1e-8)
        assert (decomposition >= 0).all()
        assert len(namespace["fig"].axes) == 2
    finally:
        plt.close("all")
