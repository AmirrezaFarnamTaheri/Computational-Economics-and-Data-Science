# Prerequisites

What you need to know before starting the course.

---

## Mathematics

### Required (Modules 1–6)

- **Calculus** — Derivatives, integrals, chain rule, Taylor expansions, constrained optimization (Lagrangians)
- **Linear Algebra** — Matrix operations, systems of linear equations, eigenvalues/eigenvectors, positive definiteness
- **Probability & Statistics** — Random variables, expectation, variance, common distributions (Normal, Bernoulli), Bayes' rule, law of large numbers, central limit theorem

### Recommended (Modules 7–10)

- **Real Analysis** — Metric spaces, contraction mappings, fixed-point theorems (used in dynamic programming proofs; see Appendix A1)
- **Optimization** — Convexity, KKT conditions, duality (used in consumer/producer theory and ML)
- **Stochastic Processes** — Markov chains, stationarity, ergodicity (used in time series and macro models)
- **Measure-Theoretic Probability** — Helpful for continuous-time finance (Module 9)

### Self-Assessment

If you can answer these, you're ready for the core modules:

1. Compute $\frac{\partial}{\partial x} \ln(x^2 + y)$
2. Find the eigenvalues of $\begin{pmatrix} 2 & 1 \\ 0 & 3 \end{pmatrix}$
3. If $X \sim N(0, 1)$, what is $P(X > 1.96)$?

If not, review the **Appendix** notebooks on calculus, linear algebra, and probability before starting Module 2.

---

## Economics

### Required

- **Intermediate Microeconomics** — Utility maximization, firm theory, market equilibrium, welfare theorems
- **Intermediate Macroeconomics** — IS-LM, Solow growth model, monetary policy basics

### Recommended

- **Graduate Microeconomics** — Game theory, mechanism design, general equilibrium (for Modules 5, 10)
- **Graduate Macroeconomics** — Dynamic optimization, RBC/DSGE intuition (for Modules 3, 4)
- **Introductory Econometrics** — OLS, hypothesis testing, regression diagnostics (for Module 6)

### No Economics Background?

Modules 1–2 (Foundations, Numerical Methods) and Module 7 (Machine Learning) are accessible without economics training. Start there and pick up economics concepts as you encounter them.

---

## Programming

**No prior Python experience required.** Module 1 teaches Python from scratch, covering:

- Variables, data types, control flow, functions
- NumPy for numerical computing
- Pandas for data manipulation
- Matplotlib for visualization

### Helpful (but not required)

- Any prior programming experience (R, MATLAB, Julia, etc.)
- Familiarity with Jupyter notebooks
- Basic command-line usage (for installation)

---

## Software

See the [Installation Guide](installation.md) for detailed setup instructions. In brief, you need:

- **Python 3.11+** (via Anaconda or pip)
- **Jupyter Notebook/Lab**
- Core packages: NumPy, Pandas, Matplotlib, SciPy, scikit-learn

Optional (for specific modules):
- TensorFlow/PyTorch (Module 7: Deep Learning)
- Graphviz (diagram generation)
- statsmodels (Module 6, 8: Econometrics, Time Series)

---

## Module-Level Requirements

| Module | Math Level | Econ Level | Programming Level |
|--------|-----------|-----------|-------------------|
| 01 Foundations | Basic | None | Beginner |
| 02 Numerical Methods | Calculus + LinAlg | None | Intermediate |
| 03 Economic Modeling | Real Analysis | Grad Macro | Intermediate |
| 04 Macro Models | Calculus | Intermediate Macro | Intermediate |
| 05 Micro Models | Optimization | Intermediate Micro | Intermediate |
| 06 Econometrics | Statistics | Intro Econometrics | Intermediate |
| 07 Machine Learning | LinAlg + Prob | None | Intermediate |
| 08 Time Series | Stochastic Processes | Macro basics | Intermediate |
| 09 Finance | Stochastic Calculus | None | Advanced |
| 10 Specialized | Varies | Varies | Advanced |

---

For installation instructions, see [Installation Guide](installation.md).
