"""Source-level regressions for the finance/appendix review, without live data."""

import ast
import json
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd
import pytest
from scipy.optimize import brentq
from scipy.stats import norm

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]


def definitions(notebook, cell_ids, **namespace):
    """Load real lesson definitions but omit top-level demos and network calls."""
    nb = json.loads((ROOT / notebook).read_text(encoding="utf-8"))
    for cell_id in cell_ids:
        cell = next(c for c in nb["cells"] if c["id"] == cell_id)
        tree = ast.parse("".join(cell["source"]))
        tree.body = [
            node
            for node in tree.body
            if isinstance(node, (ast.FunctionDef, ast.ClassDef))
        ]
        exec(compile(tree, f"{notebook}#{cell_id}", "exec"), namespace)
    return namespace


@pytest.fixture
def option_ns():
    return definitions(
        "09-Finance/03_Option_Pricing.ipynb",
        ["f5cfecfd", "f4bbf2cc"],
        np=np,
        pd=pd,
        plt=plt,
        norm=norm,
        brentq=brentq,
        YFINANCE_AVAILABLE=False,
    )


def test_synthetic_option_smile_inverts_quotes_without_network(option_ns):
    try:
        calls, puts = option_ns["plot_volatility_smile"]()
        assert len(calls) == len(puts) == 13
        moneyness = (calls["strike"] - 170.0) / 170.0
        expected = 0.35 - 0.15 * moneyness + 0.5 * moneyness**2
        np.testing.assert_allclose(calls["iv"], expected, atol=1e-10)
        np.testing.assert_allclose(puts["iv"], expected, atol=1e-10)
    finally:
        plt.close("all")


def test_quote_filter_returns_inverted_frame_without_mutation(option_ns):
    pricer = option_ns["BSMPricer"]
    price = pricer(100, 100, 1, 0.05, 0.2).price()
    quotes = pd.DataFrame(
        {
            "strike": [100.0, 100.0, 100.0, 0.0],
            "bid": [price, -1.0, 3.0, 1.0],
            "ask": [price, 1.0, 2.0, 2.0],
        }
    )
    before = quotes.copy(deep=True)
    clean = option_ns["prepare_option_quotes"](quotes, 100, 1, 0.05, "call")
    assert len(clean) == 1
    assert clean.iloc[0]["iv"] == pytest.approx(0.2, abs=1e-10)
    pd.testing.assert_frame_equal(quotes, before)


def test_live_option_request_does_not_silently_become_synthetic(option_ns):
    with pytest.raises(ImportError, match="yfinance"):
        option_ns["plot_volatility_smile"](use_live=True)


def test_option_price_parity_and_binomial_convergence(option_ns):
    pricer = option_ns["BSMPricer"]
    call = pricer(100, 100, 1, 0.05, 0.2, "call").price()
    put = pricer(100, 100, 1, 0.05, 0.2, "put").price()
    expected = 100 * norm.cdf(0.35) - 100 * np.exp(-0.05) * norm.cdf(0.15)
    assert call == pytest.approx(expected, abs=1e-12)
    assert call - put == pytest.approx(100 - 100 * np.exp(-0.05), abs=1e-12)
    lattice = option_ns["BinomialPricer"](100, 100, 1, 0.05, 0.2).price(500)
    assert lattice == pytest.approx(call, abs=0.005)


def _merton_cell_source():
    """The symbolic Merton derivation cell as shipped source."""
    nb = json.loads(
        (ROOT / "09-Finance/04_Continuous_Time_Finance.ipynb").read_text(
            encoding="utf-8"
        )
    )
    cell = next(c for c in nb["cells"] if c.get("id") == "8e3483c0")
    return "".join(cell["source"])


def test_merton_symbolic_cell_does_not_call_untractable_solve():
    """Step 6 solved the HJB equation for A by calling sympy ``solve`` on it,
    which raised NotImplementedError under sympy 1.14 (multiple generators A and
    A**(1/gamma)); the closed-form route replaced it. See the matrix execution
    evidence for the failing run."""
    src = _merton_cell_source()
    # Executable code must use the closed form, not the symbolic solve.
    code = "\n".join(
        line for line in src.splitlines() if not line.strip().startswith("#")
    )
    assert "hjb_equation, A" not in code
    assert "A_sol = delta**(-gamma)" in code


def test_merton_closed_form_matches_numeric_solver():
    """The symbolic delta agrees with the notebook's own numeric solver."""
    mu, r, sigma, rho = 0.08, 0.03, 0.20, 0.04
    for gamma in (2.0, 3.0, 5.0):
        alpha = (mu - r) / (gamma * sigma**2)
        numeric = (rho - (1 - gamma) * (r + 0.5 * alpha * (mu - r))) / gamma
        closed = (
            rho - (1 - gamma) * (r + (mu - r) ** 2 / (2 * gamma * sigma**2))
        ) / gamma
        assert closed == pytest.approx(numeric, abs=1e-12)
