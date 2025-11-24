# Comprehensive Improvement Roadmap

This document outlines the master plan for elevating the entire course repository to a "Gold Standard" of pedagogical, visual, and technical excellence. It addresses the 6 core tasks requested by the user, broken down into a granular, actionable checklist for every module.

## 1. Executive Summary & Philosophy
The goal is to transform the repository into a cohesive, self-contained, and visually stunning educational resource. The `01-Foundations` module (specifically `01_Introduction.ipynb`) serves as the benchmark.

**The "Gold Standard" Philosophy:**
1.  **Context before Code:** Every notebook must start with a narrative introduction (The "Lens").
2.  **No Magic:** Remove helper functions that hide logic (e.g., `sec()`, `note()`). Use Markdown.
3.  **Self-Containment:** Every notebook runs from top to bottom without external hidden dependencies.
4.  **Visual Consistency:** All plots use a unified style context; all diagrams have metadata.
5.  **Rigor:** Derivations are complete; code is robust (e.g., no `inv(A)`).

---

## 2. Global Technical Standards
*These standards apply to every single notebook in the repository.*

### A. Standard Header
Every notebook must begin with this cell (Markdown):
```markdown
# [Module Name]
## [Chapter Number]: [Chapter Title]

[![Code License: MIT](https://img.shields.io/badge/Code%20License-MIT-yellow.svg)](../LICENSE)
[![Content License: CC BY 4.0](https://img.shields.io/badge/Content%20License-CC%20BY%204.0-blue.svg)](https://creativecommons.org/licenses/by/4.0/)
```

### B. Standard Imports & Setup
Replace the complex `sec()`, `note()` setups with this standard block:
```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
# Module specific imports...

# Visual Configuration
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams.update({
    'figure.figsize': (10, 6),
    'font.size': 12,
    'axes.titlesize': 14,
    'axes.grid': True
})
```

### C. Formatting & Tone (Task 6)
*   **Remove:** `def sec(title): print(...)` -> Use `### Title` in Markdown.
*   **Remove:** `def note(msg): ...` -> Use `> **Note:** [Message]` in Markdown.
*   **Math:** Ensure all LaTeX equations are properly rendered (use `$$` for block math).

---

## 3. Module-Specific Action Plan (The Checklist)

### Module 01: Foundations (The Benchmark)
*   [ ] **Audit:** Ensure `finance_utils.py` is documented.
*   [ ] **Task 2:** Verify all images in `01_Introduction` have high-quality descriptions in `metadata.json`.

### Module 02: Numerical Methods
*   **Current State:** Uses `sec/note` helpers; good use of Scipy.
*   **Action Items:**
    *   [ ] **Refactor:** Remove `sec()` and `note()` from all 8 notebooks.
    *   [ ] **Task 4 (Correctness):** In `01_Linear_Algebra.ipynb`, verify the "Condition Number" example uses a fixed seed.
    *   [ ] **Task 2 (Vis):** In `04_Root_Finding.ipynb`, replace generic plots with a "Bond Yield Calculation" visualization to ground it in economics.
    *   [ ] **Task 5 (Gap):** In `05_Optimization.ipynb`, add a section on "Constrained Optimization" using `scipy.optimize.minimize(constraints=...)`.

### Module 03: Economic Modeling
*   **Current State:** Good theory, but code sometimes hides complexity.
*   **Action Items:**
    *   [ ] **Task 1 (Structure):** Explicitly link `01_Dynamic_Programming` to the `Contraction Mapping Theorem` introduced in Module 01.
    *   [ ] **Refactor:** `dp_solver.py` should be imported or (better) explained step-by-step in `01_Dynamic_Programming.ipynb`.
    *   [ ] **Task 5 (Gap):** In `05_Optimal_Stopping.ipynb`, add a real-world example: "When to exercise an American Option".

### Module 04: Macro Models
*   **Current State:** High-level models, often hardcoded matrices (e.g., RBC).
*   **Action Items:**
    *   [ ] **Refactor:** In `03_RBC_Models.ipynb`, **remove hardcoded matrices** `P_sol`, `Q_sol`. Implement a basic solver (e.g., QZ decomposition) or import one from `scripts/` to show *how* the solution is found.
    *   [ ] **Task 6 (History):** Add a vignette on "Kydland & Prescott (1982)" to `03_RBC_Models.ipynb`.
    *   [ ] **Task 2 (Vis):** Replace standard IRF plots with interactive (or better static) plots showing "Surprise vs News" shocks clearly.

### Module 05: Micro Models
*   **Current State:** Needs more game theory visualizations.
*   **Action Items:**
    *   [ ] **Task 2 (Vis):** In `03_Game_Theory.ipynb`, use `graphviz` to generate extensive form game trees instead of static images.
    *   [ ] **Task 5 (Gap):** In `02_General_Equilibrium.ipynb`, add a pure exchange Edgeworth Box simulation (Python code to draw contract curve).

### Module 06: Econometrics
*   **Current State:** Heavy use of `sec/note` helpers; assumes external data.
*   **Action Items:**
    *   [ ] **Refactor:** Remove `sec/note` from all 12 notebooks.
    *   [ ] **Task 4 (Correctness):** In `01_Linear_Model.ipynb`, explicitly load `Guerry` dataset (do not assume it's in env).
    *   [ ] **Task 2 (Vis):** In `03_Causal_Inference.ipynb`, create a DAG visualization using `networkx` or `graphviz`.

### Module 07: Machine Learning
*   **Current State:** Some duplicate "executed" notebooks; older library versions?
*   **Action Items:**
    *   [ ] **Cleanup:** Delete `*_executed.ipynb` files.
    *   [ ] **Update:** Ensure PyTorch/TensorFlow code is compatible with latest stable versions.
    *   [ ] **Task 5 (Gap):** In `10_Transformers.ipynb`, add a diagram explaining "Self-Attention" (generate via script).

### Module 08: Time Series
*   **Current State:** Good coverage, check stationarity tests.
*   **Action Items:**
    *   [ ] **Task 4 (Correctness):** In `02_ARMA_Models.ipynb`, ensure ADF test is explained and interpreted correctly (p-value logic).
    *   [ ] **Task 2 (Vis):** Standardize ACF/PACF plots using `statsmodels.graphics.tsaplots`.

### Module 09: Finance
*   **Current State:** Relies on external APIs (Yahoo Finance) which often break.
*   **Action Items:**
    *   [ ] **Robustness:** In `02_Portfolio_Theory.ipynb`, wrap `pandas_datareader` calls in try/except blocks. Provide a fallback `.csv` in `data/` if API fails.
    *   [ ] **Task 5 (Gap):** In `04_Option_Pricing.ipynb`, add a "Greeks" visualization surface plot (3D).

### Module 10: Specialized Models
*   **Current State:** Less polished.
*   **Action Items:**
    *   [ ] **Task 1 (Structure):** Ensure `01_Agent_Based_Models.ipynb` links back to "Emergence" concepts in Module 01.
    *   [ ] **Task 3 (Design):** Ensure the Schelling Segregation Model (if present) uses a clean grid visualization.

---

## 4. Metadata & Assets Strategy (Task 2)
*   **Goal:** 100% coverage in `images/metadata.json`.
*   **Action:**
    1.  Run `validate_notebooks.py` to identify all used images.
    2.  For every image:
        *   If it's a generic filename (`lp1.png`), rename to descriptive (`linear_programming_feasible_region.png`).
        *   Add valid "Description" (educational value) and "License" to JSON.
        *   If "Source" is "Course Repository", ensure the generating script exists in `scripts/`.

---

## 5. Phased Execution Plan

### Phase 1: The "Sweep" (Structure & Design)
*   **Target:** All Modules.
*   **Actions:**
    *   Replace Headers.
    *   Remove `sec()/note()`.
    *   Standardize Matplotlib `plt.style`.
    *   Delete `*_executed.ipynb` files.

### Phase 2: The "Fix" (Correctness & Refactoring)
*   **Target:** Modules 02, 04, 06 (High Priority).
*   **Actions:**
    *   Refactor RBC Model (Module 04).
    *   Fix Linear Algebra "Condition Number" seed (Module 02).
    *   Fix Data Loading in Econometrics (Module 06).

### Phase 3: The "Enrichment" (Gaps & Writing)
*   **Target:** All Modules.
*   **Actions:**
    *   Write "Big Picture" Introductions.
    *   Add Historical Vignettes.
    *   Fill identified Gaps (e.g., QZ Decomposition explanation).

### Phase 4: The "Polish" (Metadata & Assets)
*   **Target:** `images/` and `scripts/`.
*   **Actions:**
    *   Rename ambiguous images.
    *   Complete `metadata.json`.
    *   Verify all scripts run and produce the expected images.
