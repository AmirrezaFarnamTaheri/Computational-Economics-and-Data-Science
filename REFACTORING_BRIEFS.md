# Refactoring Briefs: The "Decimation" Phase

**Purpose:** This document contains specific, granular, and technically rigorous instructions for refactoring the key notebooks in the repository. These instructions are derived from a deep audit of the codebase and are designed to elevate the project to a "Gold Standard" of educational quality.

---

## 🌎 Module 01: Foundations
**Target:** `01_Introduction.ipynb` (and all foundational notebooks)

*   **Narrative Arc:** The current introduction jumps too quickly into syntax.
    *   *Action:* Rewrite the opening to focus on the *computational mindset* in economics. Why do we need code? (e.g., "Analytical solutions are rare; numerical methods are the rule.").
*   **Anti-Patterns:** Remove all `sec()` and `note()` calls. Replace with standard Markdown headers (`##`) and Alert blocks (`> **Note:**`).
*   **Code Quality:**
    *   Replace `from numpy import *` with explicit `import numpy as np`.
    *   Ensure all variable names are descriptive (e.g., `interest_rate` instead of `r` where possible, or document `r` clearly).

## 🧮 Module 02: Numerical Analysis
**Target:** `05_Optimization.ipynb`

*   **Conceptual Gap:** The link between convexity and optimization success is stated but not *felt*.
    *   *Action:* Add a 3D surface plot comparing a convex function ($x^2 + y^2$) vs. a non-convex function (Rosenbrock or Rastrigin). Visually demonstrate a gradient descent path getting stuck in a local minimum on the non-convex surface.
*   **Visuals:** Standardize the "BFGS vs. Newton" comparison plot. Use `matplotlib` contours with clear labels for the steps taken by each algorithm.

## 💰 Module 03: Economic Modeling
**Target:** `01_Dynamic_Programming.ipynb`

*   **Math Rigor:** The Bellman equation derivation is abrupt.
    *   *Action:* Insert a step-by-step derivation showing the expansion of the infinite sum $\sum \beta^t u(c_t)$ into $u(c_0) + \beta V(k_1)$. Explicitly state the conditions for the Contraction Mapping Theorem (Discounting + Boundedness).
*   **Code Refactor:** The Value Function Iteration (VFI) loop is likely slow python.
    *   *Action:* Vectorize the Bellman operator using broadcasting.
    *   *Code Snippet:*
        ```python
        # Bad: Double loop
        for i in range(N):
            for j in range(N):
                val[i, j] = u(k[i], k[j]) + beta * v[j]
        # Good: Broadcasting
        X, Y = np.meshgrid(k, k)
        return u(X, Y) + beta * v_guess
        ```
*   **Visuals:** Add a plot showing the *convergence error* ($\|V_{n+1} - V_n\|_\infty$) on a log-scale y-axis against iterations.

## 📈 Module 04: Macro Models
**Target:** `03_RBC_Models.ipynb` & `05_New_Keynesian_Models.ipynb`

*   **Critical Fix (RBC):** The code currently relies on pre-computed solution matrices (`P_sol`). This is "magic" and breaks the learning arc.
    *   *Action:* Implement a `solve_linear_rational_expectations(A, B, C, ...)` function (wrapping `scipy.linalg.ordqz` or `klein_solver.py`) that takes the linearized system matrices and *computes* the policy function live.
*   **Theory (NK):** The Calvo pricing derivation is often a black box.
    *   *Action:* Add a "Derivation Note" (collapsed markdown) showing how the infinite sum of reset prices leads to the New Keynesian Phillips Curve (NKPC).
*   **Visuals:** Impulse Response Functions (IRFs) must be combined into a single $2 \times 2$ or $3 \times 2$ subplot grid with shared x-axes, not scattered individual plots.

## 🏪 Module 05: Micro Models
**Target:** `03_Game_Theory_and_Auctions.ipynb`

*   **Refactor:** The VCG auction code is procedural and hard to reuse.
    *   *Action:* Encapsulate the auction logic in a `VCGAuction` class with methods `.bid()`, `.calculate_allocation()`, and `.calculate_payments()`.
*   **Visuals:** For the "Battle of the Sexes" or 2x2 games, use `seaborn.heatmap` to visualize the payoff matrix, making the Nash Equilibria visually obvious (e.g., highlight the cells).

## 📊 Module 06: Econometrics
**Target:** `02_Maximum_Likelihood.ipynb`

*   **Visuals:** The "Likelihood Surface" is a key concept.
    *   *Action:* Create a high-quality 3D surface plot (or interactive `plotly` if possible, otherwise static `matplotlib` with good perspective) showing the peak of the log-likelihood function. Mark the true parameter value and the MLE estimate.
*   **Code:** Ensure `MLEstimator` is defined in `econometrics_utils.py` and imported. The notebook should focus on *using* it, not defining the class boilerplates.

## 🧠 Module 07: Machine Learning
**Target:** `06_Deep_Learning_Foundations.ipynb`

*   **Robustness:** Deep Learning libraries (TensorFlow/PyTorch) are heavy.
    *   *Action:* Add a strict check at the top: `if not TENSORFLOW_AVAILABLE: print("Skipping execution..."); return`.
*   **Content:** The "DeepIV" section is advanced.
    *   *Action:* Add a diagram (using `graphviz` or static image) showing the Causal Graph (DAG) for IV: $Z \rightarrow D \rightarrow Y$ with confounder $U$ affecting $D$ and $Y$. Explain *why* standard NN fails here (it picks up the $U \rightarrow D \rightarrow Y$ path).

## ⏳ Module 08: Time Series
**Target:** `04_Vector_Autoregression.ipynb`

*   **Identification:** The Cholesky decomposition ordering is crucial but often glossed over.
    *   *Action:* Add a visual representation of the recursive structure implied by the ordering (e.g., "Shocks to GDP affect Rate immediately, but Rate shocks take a quarter to affect GDP").
*   **Data:** Replace `pandas_datareader` (which fails often) with a local CSV fallback (`data/us_macro_quarterly.csv`).

## 💹 Module 09: Finance
**Target:** `03_Asset_Pricing.ipynb`

*   **Visuals:** The Hansen-Jagannathan (HJ) bound is the centerpiece of this notebook.
    *   *Action:* Ensure the HJ bound plot is technically correct: Plot $\sigma(m)/E[m]$ vs Sharpe Ratio. Add points for different asset pricing models (CCAPM with various $\gamma$) to show they fail to enter the "admissible region".
*   **Code:** The Fama-MacBeth implementation should be explicitly checked against `linearmodels` or standard results to ensure the Newey-West standard error adjustment is correct (lag length choice).

## 🐜 Module 10: Specialized Models
**Target:** `01_Agent_Based_Models.ipynb`

*   **Interactive:** Schelling's model begs for animation.
    *   *Action:* Use `matplotlib.animation` to save a `.gif` of the segregation process and embed it. Do not rely on live runtime animation which often breaks in static views.
*   **Performance:** ABMs in Python can be slow. Use `numba` to accelerate the agent step loops if the grid size > 50x50.

---

## General Refactoring Rules (The "Codex")

1.  **Type Hinting:** All major functions must have Python type hints.
    *   *Example:* `def solve_model(alpha: float, beta: float) -> np.ndarray:`
2.  **Docstrings:** All functions must have NumPy-style docstrings (Parameters, Returns, Notes).
3.  **Variable Names:** No single-letter variables for complex objects (use `transition_matrix` not `P`). Math symbols ($A, \alpha$) are acceptable if they match the LaTeX derivation nearby.
4.  **Testing:** Every notebook should have a "Sanity Check" cell where the implemented model is tested against a known simple case (e.g., "If risk aversion is 0, price should equal expected discounted payoff").
