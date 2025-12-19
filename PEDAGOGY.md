# Pedagogical Framework: Zero to Hero

This document defines the educational philosophy and structural standards for the Computational Economics repository.

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
    return c**(1 - gamma) / (1 - gamma)
```

**Requirements:**
*   Use LaTeX for all model equations.
*   Variable names in Python should match LaTeX notation (e.g., `beta` for $\beta$, `sigma` for $\sigma$).
*   Complex matrix operations should be commented with their mathematical equivalent (e.g., `# X'X`).

---

## IV. Testing & Verification Strategy

We adopt a "Trust but Verify" approach.

*   **Inline Assertions:** Critical functions must have `assert` statements checking shapes and bounds (e.g., `assert prices > 0`).
*   **Unit Tests:** Key algorithms (like VFI) should have a test cell verifying they recover a known analytical solution (e.g., compare numerical derivative to exact derivative).
*   **Visual Verification:** Every simulation must produce a plot that matches economic intuition (e.g., "Consumption smooths income shocks").
