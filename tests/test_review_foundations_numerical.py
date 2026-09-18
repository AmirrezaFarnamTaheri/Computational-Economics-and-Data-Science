"""Regression probes execute lesson source without network or notebook side effects."""

import ast
import json
import re
from contextlib import contextmanager
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from scipy.special import roots_hermite

ROOT = Path(__file__).resolve().parents[1]


def cell_source(path, cell_id):
    notebook = json.loads((ROOT / path).read_text(encoding="utf-8"))
    return "".join(
        next(cell for cell in notebook["cells"] if cell.get("id") == cell_id)["source"]
    )


def definitions(source, namespace):
    tree = ast.parse(source)
    tree.body = [
        node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.ClassDef))
    ]
    exec(compile(tree, "<lesson definitions>", "exec"), namespace)
    return namespace


def test_backprop_shared_intermediate_counts_each_contribution_once():
    source = cell_source(
        "02-Numerical-Methods/03_Numerical_Differentiation.ipynb", "ad_intro"
    )
    example = re.search(r"```python\n(.*?)```", source, re.S).group(1)
    node = definitions(example, {})["Node"]
    x = node(2.0)
    shared = x * x
    result = shared + shared
    result.backward()
    assert result.value == 8.0
    assert x.grad == 8.0  # d(2*x**2)/dx = 4*x


@pytest.mark.parametrize("initial", [0.0, np.array([0.0]), np.array([0.0, 4.0])])
def test_anderson_accepts_scalar_and_vector_initial_guesses(initial):
    source = cell_source("02-Numerical-Methods/04_Root_Finding.ipynb", "imports")
    solve = definitions(source, {"np": np})["anderson_acceleration"]
    result, iterations = solve(lambda x: 0.5 * x + 1, initial)
    np.testing.assert_allclose(result, 2.0, atol=1e-6)
    assert np.linalg.norm(0.5 * np.asarray(result) + 1 - result) < 1e-6
    assert iterations < 100


def test_gauss_hermite_crra_example_has_positive_support_and_analytic_reference():
    source = cell_source(
        "02-Numerical-Methods/07_Numerical_Integration.ipynb", "gauss_hermite"
    )
    namespace = {
        "np": np,
        "roots_hermite": roots_hermite,
        "rng": np.random.default_rng(42),
    }
    exec(compile(source, "<gauss-hermite lesson>", "exec"), namespace)
    assert np.all(namespace["c_nodes"] > 0)
    assert np.all(namespace["mc_draws"] > 0)
    expected = -np.exp(-namespace["mu"] + namespace["sigma"] ** 2 / 2)
    assert namespace["expected_u"] == pytest.approx(expected, abs=1e-12)
    mc_se = np.std(namespace["utility"](namespace["mc_draws"]), ddof=1) / 1000
    assert abs(namespace["mc_u"] - expected) < 5 * mc_se


def test_temporary_seed_restores_generator_after_nested_exception():
    namespace = {
        "np": np,
        "rng": np.random.default_rng(42),
        "contextmanager": contextmanager,
    }
    definitions(
        cell_source(
            "01-Foundations/09_Control_Flow_and_Error_Handling.ipynb", "0d6e2d7e"
        ),
        namespace,
    )
    original = namespace["rng"]
    with namespace["temporary_seed"](123):
        expected = np.random.default_rng(123)
        assert namespace["rng"].random() == expected.random()
        with pytest.raises(RuntimeError):
            with namespace["temporary_seed"](7):
                raise RuntimeError("exercise finally")
        assert namespace["rng"].random() == expected.random()
    assert namespace["rng"] is original
    assert original.random() == np.random.default_rng(42).random()


def test_vectorized_pi_uses_generator_shape_tuple():
    source = cell_source("01-Foundations/12_NumPy.ipynb", "fb6f5936")
    source = re.search(
        r"def monte_carlo_pi_vectorized.*?(?=\nif not LINE_PROFILER_AVAILABLE)",
        source,
        re.S,
    ).group()
    calculate = definitions(source, {"np": np, "rng": np.random.default_rng(42)})[
        "monte_carlo_pi_vectorized"
    ]
    assert abs(calculate(100_000) - np.pi) < 0.03


def test_acquisition_setup_imports_numpy_before_generator_and_chunk_shape():
    setup = ast.parse(
        "\n".join(
            line
            for line in cell_source(
                "01-Foundations/14_Introduction_to_Data_Acquisition.ipynb", "ffb9efec"
            ).splitlines()
            if not line.startswith("%")
        )
    )
    namespace = {"pd": pd}
    for node in setup.body:
        if isinstance(node, ast.Import) and any(
            alias.name == "numpy" for alias in node.names
        ):
            exec(
                compile(
                    ast.Module(body=[node], type_ignores=[]), "<numpy import>", "exec"
                ),
                namespace,
            )
        elif isinstance(node, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id == "rng"
            for target in node.targets
        ):
            exec(
                compile(
                    ast.Module(body=[node], type_ignores=[]),
                    "<generator setup>",
                    "exec",
                ),
                namespace,
            )
    chunk = ast.parse(
        cell_source(
            "01-Foundations/14_Introduction_to_Data_Acquisition.ipynb", "code-chunking"
        )
    )
    exec(
        compile(
            ast.Module(body=[chunk.body[0]], type_ignores=[]), "<chunk data>", "exec"
        ),
        namespace,
    )
    assert namespace["large_df"].shape == (10_000, 3)


def test_phillips_inflation_is_percent_not_fraction():
    tree = ast.parse(
        cell_source(
            "01-Foundations/15_Accessing_Economic_Data_via_APIs.ipynb", "bf935389"
        )
    )
    assignment = next(
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Assign)
        and any(
            isinstance(target, ast.Name) and target.id == "inflation_data"
            for target in node.targets
        )
    )
    namespace = {"cpi_data": pd.Series([100.0] * 12 + [105.0] * 12)}
    exec(
        compile(
            ast.Module(body=[assignment], type_ignores=[]),
            "<inflation calculation>",
            "exec",
        ),
        namespace,
    )
    np.testing.assert_allclose(namespace["inflation_data"], 5.0)


def test_rck_jacobian_trace_for_nondefault_growth_rates():
    source = cell_source(
        "02-Numerical-Methods/08_Differential_Equations.ipynb", "rck_solver"
    )
    rhs = definitions(source, {})["rck_system"]
    p = dict(alpha=0.3, n=0.015, g=0.02, delta=0.05, rho=0.02, theta=2.0)
    k = (p["alpha"] / (p["delta"] + p["rho"] + p["theta"] * p["g"])) ** (
        1 / (1 - p["alpha"])
    )
    c = k ** p["alpha"] - (p["n"] + p["g"] + p["delta"]) * k
    h = 1e-5
    observed = (np.array(rhs(0, [k + h, c], p)) - np.array(rhs(0, [k - h, c], p))) / (
        2 * h
    )
    assert observed[0] == pytest.approx(
        p["rho"] + p["theta"] * p["g"] - p["n"] - p["g"], abs=1e-9
    )
