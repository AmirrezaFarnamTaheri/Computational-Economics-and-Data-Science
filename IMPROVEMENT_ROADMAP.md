# Comprehensive Improvement Roadmap

This document outlines the "Master Plan" for elevating the Computational Economics repository to a "Gold Standard" of pedagogical, visual, and technical excellence. It is the result of a deep, file-by-file audit of all 116 notebooks.

**Status:** 🚧 In Progress
**Target:** Production-Ready Open Source Course
**Author:** [Agent Name]
**Date:** October 2025

---

## 1. Executive Summary & Philosophy

The goal is to transform the repository into a cohesive, self-contained, and visually stunning educational resource. The "Production Ready" status claimed in `FINAL_PROJECT_REPORT.md` is aspirational; this roadmap bridges the gap to reality.

**The "Gold Standard" Philosophy:**
1.  **Context before Code:** Every notebook must start with a narrative introduction (The "Lens") that motivates the economic problem before any code is written.
2.  **No Magic:** Remove custom helper functions (e.g., `sec()`, `note()`) that hide logic or non-standard styling. Use standard Markdown and standard library calls.
3.  **Self-Containment:** Every notebook runs from top to bottom. External dependencies (data, scripts) must be explicitly handled with robust fallbacks.
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
Replace the ad-hoc `sec()`, `note()` setups with this standard block:
```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
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

## 3. Module-by-Module Audit & Action Plan

### Module 01: Foundations
*   **Status:** Strong content, missing summaries.
*   **Anti-Patterns:** `sec()`/`note()` helpers found in most files.
*   **Action Items:**
    *   [ ] **Structure:** Add explicit `# Summary` sections to all 24 notebooks.
    *   [ ] **Refactor:** Move `finance_utils.py` to `utils/` and document it.
    *   [ ] **Metadata:** Ensure all 22 images in this module have descriptions in `metadata.json`.

### Module 02: Numerical Methods
*   **Status:** Code-heavy, needs visual uplift.
*   **Anti-Patterns:** `sec()` found in all 8 notebooks.
*   **Action Items:**
    *   [ ] **01_Linear_Algebra:** Fix "Condition Number" seed.
    *   [ ] **04_Root_Finding:** Replace generic plots with "Bond Yield" visualization.
    *   [ ] **05_Optimization:** Add `scipy.optimize.minimize(constraints=...)` example.
    *   [ ] **Global:** Remove `sec()`/`note()` definitions.

### Module 03: Economic Modeling
*   **Status:** Good theory, technical debt in utils.
*   **Action Items:**
    *   [ ] **01_Dynamic_Programming:** Replace custom `tauchen` with `quantecon` or robust utility.
    *   [ ] **01_Dynamic_Programming:** Remove `display(Image(...))` for `cake_eating_solution.png` -> Generate plot inline.
    *   [ ] **04_Estimation:** Remove "Dummy Objective" in SMM class -> Implement real estimation logic with simulated data (e.g., Aiyagari).

### Module 04: Macro Models
*   **Status:** Hardcoding issues.
*   **Action Items:**
    *   [ ] **03_RBC_Models:** **CRITICAL:** Remove hardcoded `P_sol`, `Q_sol`. Implement QZ decomposition solver.
    *   [ ] **05_New_Keynesian:** Upgrade IRF plots to interactive Plotly.
    *   [ ] **06_Heterogeneous_Agents:** Ensure `macro_vfi_utils` import is clean.

### Module 05: Micro Models
*   **Status:** Visual gaps.
*   **Action Items:**
    *   [ ] **02_General_Equilibrium:** **CRITICAL:** Implement the Heckscher-Ohlin trade solver (currently missing logic).
    *   [ ] **03_Game_Theory:** Add `graphviz` game trees.
    *   [ ] **Dependency:** Add `nashpy` to `requirements.txt`.

### Module 06: Econometrics
*   **Status:** Hidden pedagogy.
*   **Action Items:**
    *   [ ] **02_Maximum_Likelihood:** Expose `MLEstimator` class from `econometrics_utils.py` or define inline.
    *   [ ] **03_Causal_Inference:** Ensure `graphviz` fallback is robust.
    *   [ ] **Data:** Verify `Guerry` dataset loading (local vs remote).

### Module 07: Machine Learning
*   **Status:** Legacy code, ethical issues.
*   **Action Items:**
    *   [ ] **01_Intro_to_ML:** Replace **Boston Housing** with **California Housing**.
    *   [ ] **Cleanup:** Delete `*_executed.ipynb` duplicates.
    *   [ ] **Technical Debt:** Convert `tensorflow` code to `pytorch` or `sklearn` where appropriate (or mark as Legacy Keras).

### Module 08: Time Series
*   **Status:** Data dependency risks.
*   **Action Items:**
    *   [ ] **All Notebooks:** Wrap `pandas_datareader` in `try/except` blocks with local CSV fallbacks.
    *   [ ] **04_VAR:** Upgrade IRF plots to interactive.

### Module 09: Finance
*   **Status:** Strong, needs robustness.
*   **Action Items:**
    *   [ ] **04_Option_Pricing:** Ensure `yfinance` calls have try/except blocks.
    *   [ ] **04_Option_Pricing:** Add 3D Greeks Surface plot.
    *   [ ] **Refactor:** Create `OptionPricer` class for reusability.

### Module 10: Specialized Models
*   **Status:** Inline installs.
*   **Action Items:**
    *   [ ] **01_Agent_Based_Models:** Remove `!pip install networkx`.
    *   [ ] **03_Network_Economics:** Ensure Centrality visualizations use clear colormaps.

### Appendices
*   **Action Items:**
    *   [ ] **A1_Real_Analysis:** Standardize `theorem()` display function to Markdown.
    *   [ ] **02_Autograding:** Preserve `otter` tags.

---

## 4. Search & Destroy: Specific Technical Debt

### A. Remove Inline Pip Installs
*   `10-Specialized-Models/01_Agent_Based_Models.ipynb`
*   `07-Machine-Learning/06_Deep_Learning_Foundations.ipynb` (if present)
*   **Action:** Move all to `requirements.txt`.

### B. Fix Data Fetching (`pandas_datareader`)
*   `08-Time-Series/04_Vector_Autoregression.ipynb`
*   `09-Finance/02_Portfolio_Theory.ipynb`
*   **Action:** Ensure `data/` folder contains CSV mirrors for all fetched series.

### C. Refactor Utilities
*   `finance_utils.py` -> `utils/finance.py`
*   `econometrics_utils.py` -> `utils/econometrics.py`
*   `macro_vfi_utils.py` -> Fix Numba compatibility.

---

## 5. Phased Execution Plan

### Phase 1: The "Sweep" (Structure & Design)
*   **Target:** All 116 Notebooks.
*   **Action:**
    1.  Run script to replace Header cell.
    2.  Run script to replace Import/Setup cell (removing `sec`/`note`).
    3.  Run script to add `# Summary` if missing.

### Phase 2: The "Fix" (Correctness & Refactoring)
*   **Target:** Modules 04, 05, 07.
*   **Action:**
    1.  Implement RBC Solver (M04).
    2.  Implement HO Trade Solver (M05).
    3.  Swap Boston -> California Housing (M07).

### Phase 3: The "Enrichment" (Gaps & Writing)
*   **Target:** Modules 02, 03, 06, 09.
*   **Action:**
    1.  Add Bond Yield Vis (M02).
    2.  Refactor SMM estimation (M03).
    3.  Expose MLEstimator (M06).
    4.  Add 3D Greeks (M09).

### Phase 4: The "Polish" (Assets & Metadata)
*   **Target:** `images/`, `scripts/`, `utils/`.
*   **Action:**
    1.  Refactor utilities.
    2.  Complete `metadata.json`.
    3.  Generate missing static assets.
