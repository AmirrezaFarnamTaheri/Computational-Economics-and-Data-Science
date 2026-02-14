"""
Shared pytest fixtures for the Computational Economics test suite.
"""

import os
import sys
from pathlib import Path

import pytest
import numpy as np

# Ensure the project root is on sys.path so modules can be imported
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# --- Path fixtures ---

@pytest.fixture
def project_root():
    """Return the project root directory as a Path."""
    return PROJECT_ROOT


@pytest.fixture
def data_dir(project_root):
    """Return the data/ directory as a Path."""
    return project_root / "data"


@pytest.fixture
def scripts_dir(project_root):
    """Return the scripts/ directory as a Path."""
    return project_root / "scripts"


# --- Tolerance fixtures ---

@pytest.fixture
def rtol():
    """Default relative tolerance for floating-point comparisons."""
    return 1e-6


@pytest.fixture
def atol():
    """Default absolute tolerance for floating-point comparisons."""
    return 1e-8


# --- Sample data fixtures ---

@pytest.fixture
def rng():
    """Seeded random number generator for reproducible tests."""
    return np.random.default_rng(42)


@pytest.fixture
def sample_grid():
    """A simple 1D grid for testing numerical methods."""
    return np.linspace(0, 1, 100)


@pytest.fixture
def sample_transition_matrix():
    """A valid 5x5 Markov transition matrix (rows sum to 1)."""
    rng = np.random.default_rng(123)
    P = rng.random((5, 5))
    P = P / P.sum(axis=1, keepdims=True)
    return P


# --- Notebook discovery ---

NOTEBOOK_DIRS = [
    "01-Foundations", "02-Numerical-Methods", "03-Economic-Modeling",
    "04-Macro-Models", "05-Micro-Models", "06-Econometrics",
    "07-Machine-Learning", "08-Time-Series", "09-Finance",
    "10-Specialized-Models", "Appendix", "high_performance_python",
]


@pytest.fixture
def all_notebook_paths(project_root):
    """Return a list of all .ipynb files in module directories."""
    notebooks = []
    for d in NOTEBOOK_DIRS:
        module_dir = project_root / d
        if module_dir.exists():
            notebooks.extend(sorted(module_dir.glob("*.ipynb")))
    return notebooks
