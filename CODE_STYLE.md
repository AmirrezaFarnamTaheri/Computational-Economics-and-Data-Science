# The Code Constitution: Python Style & Standards

**Purpose:** This document defines the technical standards for all code in the repository. It is the single source of truth for code quality, ensuring consistency, readability, and reproducibility across all modules.

---

## 1. General Philosophy

*   **Readability > Cleverness:** We write code for students, not compilers. Avoid "one-liners" that obscure logic.
*   **Explicit > Implicit:** Imports, variable names, and logic flows should be explicit.
*   **Vectorized > Looped:** Use NumPy vectorization wherever possible for performance and clarity.
*   **Self-Contained:** Notebooks should run from top to bottom without external hidden state.

---

## 2. Python Standards

### 2.1 Imports
*   **Standard Aliases:** Use the following standard aliases:
    ```python
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    import scipy.stats as stats
    import statsmodels.api as sm
    ```
*   **Grouping:** Group imports: Standard Library $\to$ Third Party $\to$ Local.
*   **Location:** All imports must be in the first code cell of the notebook.

### 2.2 Naming Conventions
*   **Variables:** `snake_case`. Descriptive (e.g., `interest_rate`, `gdp_growth`).
    *   *Exception:* Mathematical symbols that directly correspond to the LaTeX derivation are allowed (e.g., `alpha`, `beta`, `A`, `K`).
*   **Functions:** `snake_case`. Verb-noun pairs (e.g., `calculate_steady_state`, `plot_irf`).
*   **Classes:** `CamelCase`. Nouns (e.g., `RBCModel`, `MLEstimator`).
*   **Constants:** `UPPER_SNAKE_CASE` (e.g., `MAX_ITER`, `TOLERANCE`).

### 2.3 Type Hinting
*   All significant functions (solvers, estimators, models) **must** use type hints.
    ```python
    def calculate_utility(c: np.ndarray, gamma: float) -> np.ndarray:
        ...
    ```

### 2.4 Docstrings
*   Use **NumPy Style** docstrings for all functions and classes.
    ```python
    def solve_steady_state(params: dict) -> float:
        """
        Calculates the steady state capital stock.

        Parameters
        ----------
        params : dict
            Dictionary containing model parameters 'alpha', 'beta', 'delta'.

        Returns
        -------
        float
            The steady state capital stock k_ss.
        """
        ...
    ```

---

## 3. Visualization Standards

### 3.1 Setup
Every notebook must run this setup block:
```python
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams.update({
    'figure.figsize': (10, 6),
    'figure.dpi': 150,
    'axes.titlesize': 16,
    'axes.labelsize': 14,
    'xtick.labelsize': 12,
    'ytick.labelsize': 12,
    'lines.linewidth': 2
})
```

### 3.2 Plot Quality
*   **Labels:** Every plot must have `xlabel`, `ylabel`, and `title`.
*   **Legends:** Required if more than one series is plotted.
*   **Colorblindness:** Use distinct color palettes (e.g., `'viridis'`, `'deep'`). Avoid Red/Green contrasts for critical information.
*   **Grid:** Enabled by default (`whitegrid`).

---

## 4. Notebook Structure

### 4.1 The "Lens" (Introduction)
*   **Markdown:** Begins with `# Introduction` or `# The Lens`.
*   **Content:** Context (Why?), Theory (What?), and Goal (How?).

### 4.2 The "Engine" (Core Logic)
*   **Separation:** Define classes/functions in separate cells from the execution logic.
*   **Comments:** Use `#` comments to explain *why* a step is taken, not *what* the code does (unless complex).

### 4.3 The "Result" (Analysis)
*   **Interpretation:** Every plot or table must be followed by a Markdown cell interpreting the result economically. "As we see in Figure 1, the shock causes a persistent decline in consumption..."

### 4.4 The "Summary" (Conclusion)
*   **Recap:** Brief summary of the main takeaways.

---

## 5. Data Handling

### 5.1 Local First
*   Always check for local data in `data/` before attempting to download.
    ```python
    try:
        df = pd.read_csv('data/sp500.csv')
    except FileNotFoundError:
        # Download logic
        ...
    ```

### 5.2 Determinism
*   Set seeds for all random number generators.
    ```python
    rng = np.random.default_rng(seed=42)
    ```

---

## 6. Anti-Patterns (Forbidden)

*   ❌ **No** `from module import *` (Namespace pollution).
*   ❌ **No** `def sec()` or `def note()` (Custom formatting functions).
*   ❌ **No** hardcoded absolute paths (e.g., `C:/Users/Jules/...`).
*   ❌ **No** `var1`, `var2` (Meaningless names).
*   ❌ **No** giant code cells (> 50 lines). Break them up.
