# Pedagogical Framework: Zero to Hero

This document defines the educational philosophy, structural standards, and technical guidelines for the Computational Economics repository. It serves as the constitution for content creation.

## I. The "Zero to Hero" Philosophy

The goal is to take a student with basic Python knowledge and guide them to the research frontier. This requires a carefully structured journey across four stages:

1.  **Novice (Modules 1-2):**
    *   *Focus:* Syntax, basic libraries (NumPy/Pandas), and foundational numerical methods.
    *   *Approach:* "Code from Scratch". Implement OLS, Gradient Descent, and Root Finding manually before using libraries.
    *   *Outcome:* Can translate a simple mathematical formula into a Python function.

2.  **Apprentice (Modules 3-5):**
    *   *Focus:* Core economic models (Consumer Theory, Solow, Simple DP).
    *   *Approach:* "Model as Object". Use Python Classes to represent agents and markets.
    *   *Outcome:* Can build and simulate a standard dynamic model.

3.  **Practitioner (Modules 6, 8, 9):**
    *   *Focus:* Empirical rigor and financial applications.
    *   *Approach:* "Professional Tooling". Use `statsmodels`, `arch`, `pandas-datareader`. Focus on identification and forecasting accuracy.
    *   *Outcome:* Can replicate a paper's results using real-world data.

4.  **Expert (Modules 7, 10):**
    *   *Focus:* Complexity, High Performance, and AI.
    *   *Approach:* "Frontier Methods". Use `jax`, `numba`, `pytorch`. Solve intractable problems (HANK, High-dim Causal ML).
    *   *Outcome:* Can contribute to the scientific literature.

---

## II. The "Lens" Structure

Every notebook must begin with **"The Lens"**. This section serves as the bridge between economic intuition and computational implementation.

**Structure of "The Lens":**
1.  **The Hook:** A real-world economic question (e.g., "Why do stock markets crash?", "How does the Fed control inflation?").
2.  **The Intuition:** A non-mathematical explanation of the mechanism.
3.  **The Formalism:** The specific equation or model we will solve (e.g., $Supply = Demand$).
4.  **The Code:** Why we need computation (e.g., "This equation has no analytical solution").

---

## III. Math-Code Parity Standard

To reduce cognitive load, mathematical notation must map 1:1 to code variables.

**Bad Example:**
$$ U(c) = \frac{c^{1-\gamma}}{1-\gamma} $$
```python
def util(x, g):
    return x**(1-g) / (1-g)
```

**Good Example:**
$$ U(c) = \frac{c^{1-\gamma}}{1-\gamma} $$
```python
def utility(c: float, gamma: float) -> float:
    """
    CRRA Utility Function.

    Parameters:
    c (float): Consumption level.
    gamma (float): Coefficient of relative risk aversion.
    """
    return c**(1 - gamma) / (1 - gamma)
```

**Requirements:**
*   Use LaTeX for all model equations.
*   Variable names in Python should match LaTeX notation (e.g., `beta` for $\beta$, `sigma` for $\sigma$).
*   Complex matrix operations should be commented with their mathematical equivalent (e.g., `# X'X`).

---

## IV. Code Style Guide

Consistency is key for readability and professional habit formation.

1.  **Naming Conventions:**
    *   Variables: `snake_case` (e.g., `consumption_growth`).
    *   Classes: `CamelCase` (e.g., `RepresentativeAgent`).
    *   Constants: `UPPER_CASE` (e.g., `MAX_ITERATIONS`).
    *   Avoid single-letter variables unless they match standard math notation (e.g., `X`, `y` in OLS is acceptable; `a`, `b` in a complex function is not).

2.  **Type Hinting:**
    *   All function signatures must include type hints.
    *   Use `typing.List`, `typing.Tuple`, `numpy.typing.NDArray` for clarity.

3.  **Documentation:**
    *   Use NumPy-style docstrings for all functions and classes.
    *   Explain *economic* meaning of parameters, not just data types.

4.  **Vectorization:**
    *   Explicit `for` loops over data are forbidden unless necessary for the algorithm (e.g., time stepping). Use NumPy broadcasting.

---

## V. Visual Style Guide

All plots must look professional and be publication-ready.

1.  **Libraries:** Use `matplotlib` as the primary engine, `seaborn` for statistical plots.
2.  **Configuration:** Set global defaults at the top of the notebook:
    ```python
    plt.style.use('seaborn-v0_8-whitegrid')
    plt.rcParams.update({'figure.figsize': (10, 6), 'font.size': 12})
    ```
3.  **Requirements:**
    *   **Titles:** Every plot must have a descriptive title.
    *   **Labels:** All axes must be labeled with variable names and units.
    *   **Legends:** Mandatory if more than one series is plotted.
    *   **Color:** Use colorblind-friendly palettes (e.g., `viridis`, `plasma`, or specific Seaborn palettes).

---

## VI. Assessment Taxonomy

Each notebook must conclude with three graded exercises, increasing in difficulty.

1.  **Conceptual (The "Why"):**
    *   *Goal:* Check understanding of the economic logic.
    *   *Format:* Short answer, modification of a markdown cell, or simple calculation.
    *   *Example:* "Explain why the equilibrium price increases when $\beta$ increases."

2.  **Applied (The "How"):**
    *   *Goal:* Verify ability to use the code.
    *   *Format:* Modify the existing code to handle a new case.
    *   *Example:* "Change the utility function to Log Utility and re-run the simulation. How does the savings rate change?"

3.  **Challenge (The "What If"):**
    *   *Goal:* Synthesis and extension.
    *   *Format:* Open-ended coding task requiring new logic or external data.
    *   *Example:* "Download real GDP data for Japan. Calibrate the Solow model to match Japan's capital-output ratio."
