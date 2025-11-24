# Comprehensive Improvement Roadmap

This document is the **definitive master plan** for elevating the Computational Economics course repository to a "Gold Standard" of pedagogical, visual, and technical excellence. It is the result of a deep, multi-phase audit of the codebase.

## 1. Executive Summary & Philosophy

The goal is to transform the repository into a cohesive, self-contained, and visually stunning educational resource. The `01-Foundations` module (specifically `01_Introduction.ipynb`) acts as the benchmark for tone, structure, and depth.

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

## 3. Module-Specific Manifest & Action Plan

### Module 01: Foundations
*   **Status:** Gold Standard.
*   **Actions:**
    *   [ ] **Task 2:** Verify all images in `01_Introduction` have high-quality descriptions in `metadata.json`.
    *   [ ] **Refactor:** Move `finance_utils.py` to a central `utils/` folder or deprecate if unused elsewhere.

### Module 02: Numerical Methods
*   **Audit Findings:** Heavy use of `sec()/note()`; global style setting.
*   **Checklist:**
    *   [ ] **Refactor:** Remove `sec()` and `note()` from all 8 notebooks.
    *   [ ] **Task 4 (Correctness):** In `01_Linear_Algebra.ipynb`, fix the "Condition Number" example to use a fixed seed for reproducibility.
    *   [ ] **Task 2 (Vis):** In `04_Root_Finding.ipynb`, add a "Bond Yield Calculation" visualization.
    *   [ ] **Task 5 (Gap):** In `05_Optimization.ipynb`, add a section on `scipy.optimize.minimize(constraints=...)`.

### Module 03: Economic Modeling
*   **Audit Findings:** Good use of Numba, but redundant static image display; custom `tauchen` implementation.
*   **Checklist:**
    *   [ ] **Refactor:** Remove `sec()/note()`.
    *   [ ] **Technical Debt:** In `01_Dynamic_Programming.ipynb`, replace the custom `tauchen` function with a robust import from `quantecon` or a dedicated `utils.py` module that handles Numba compatibility correctly.
    *   [ ] **Task 2 (Vis):** Replace `display(Image(...))` with direct plot generation where feasible, or use high-quality SVG diagrams.
    *   [ ] **Task 1 (Structure):** Explicitly link the "Contraction Mapping" section to the theory in Module 01.

### Module 04: Macro Models
*   **Audit Findings:** Hardcoded solution matrices (`P_sol`) in RBC model.
*   **Checklist:**
    *   [ ] **Refactor:** In `03_RBC_Models.ipynb`, **implement or import a real linear rational expectations solver** (e.g., QZ decomposition). Show *how* `P` and `Q` are derived.
    *   [ ] **Task 6 (History):** Add a vignette on "Kydland & Prescott (1982)" and the "Calibration vs. Estimation" debate.
    *   [ ] **Task 2 (Vis):** Upgrade IRF plots to use interactive Plotly charts for better exploration of shock horizons.

### Module 05: Micro Models
*   **Audit Findings:** Missing `nashpy` in requirements; lack of visual game trees.
*   **Checklist:**
    *   [ ] **Dependencies:** Add `nashpy` to `requirements.txt`.
    *   [ ] **Task 2 (Vis):** In `03_Game_Theory.ipynb`, use `graphviz` to generate extensive form game trees.
    *   [ ] **Refactor:** Convert the GSP Auction simulation into a clean `class GSPAuction`.

### Module 06: Econometrics
*   **Audit Findings:** `econometrics_utils.py` contains excellent pedagogical classes (`MLEstimator`) that are hidden.
*   **Checklist:**
    *   [ ] **Pedagogy:** In `02_Maximum_Likelihood.ipynb`, explicitly import and explain the `MLEstimator` class. Don't hide it.
    *   [ ] **Refactor:** Remove `sec()/note()` from all 12 notebooks.
    *   [ ] **Task 4 (Correctness):** Ensure `Guerry` dataset loading is robust (check local path vs internet fetch).

### Module 07: Machine Learning
*   **Audit Findings:** Legacy Keras code; "Executed" duplicate notebooks; Boston Housing dataset.
*   **Checklist:**
    *   [ ] **Cleanup:** Delete `*_executed.ipynb` files.
    *   [ ] **Ethics/Modernity:** In `01_Introduction_to_ML.ipynb` (or wherever Boston is used), replace **Boston Housing** dataset with **California Housing** to avoid ethical issues and `sklearn` warnings.
    *   [ ] **Task 5 (Gap):** In `10_Transformers.ipynb`, add a generated diagram explaining "Self-Attention".

### Module 08: Time Series
*   **Audit Findings:** Good data fallback strategy; static plots.
*   **Checklist:**
    *   [ ] **Task 2 (Vis):** Upgrade Impulse Response Functions (IRFs) in `04_Vector_Autoregression.ipynb` to use interactive plots.
    *   [ ] **Task 4 (Correctness):** Add a note about the sensitivity of Cholesky identification to variable ordering.

### Module 09: Finance
*   **Audit Findings:** Strong class-based design; `yfinance` dependency.
*   **Checklist:**
    *   [ ] **Robustness:** In `04_Option_Pricing.ipynb`, ensure the `yfinance` try/except block is applied to *all* fetch calls.
    *   [ ] **Task 5 (Gap):** Add a "Greeks Surface" 3D plot to visualize Delta/Gamma across Price/Time.

### Module 10: Specialized Models
*   **Audit Findings:** Inline `pip install`; good use of Widgets.
*   **Checklist:**
    *   [ ] **Cleanup:** Remove `!pip install networkx`.
    *   [ ] **Task 3 (Design):** Ensure the Schelling Model grid visualization uses a discrete colormap that is colorblind-friendly.

### Appendices & High Performance Python
*   **Audit Findings:** Excellent theory content; redundant HPC content; Otter grader dependency.
*   **Checklist:**
    *   [ ] **Style:** Refactor custom `theorem()` display functions in `A1-Real-Analysis` to use standard Markdown Blockquotes (`> **Theorem:**`).
    *   [ ] **Integration:** Link Module 02 (Numerical) directly to `high_performance_python/` for advanced readers.
    *   [ ] **Preservation:** Ensure `otter` tags (`# BEGIN QUESTION`) are preserved during any refactoring.

---

## 4. Technical Debt & Infrastructure (Task 4 & 5)

### Utilities Refactoring
*   **`finance_utils.py`:** Move to `utils/finance.py`.
*   **`econometrics_utils.py`:** Move to `utils/econometrics.py`.
*   **`macro_vfi_utils.py`:** Fix the `norm.cdf` Numba incompatibility and enable JIT.

### Scripts & Assets
*   **Script Strategy:**
    *   **Keep:** Animation generators (e.g., `generate_aiyagari_animation.py`).
    *   **Refactor:** Scripts that duplicate logic (like the Aiyagari solver) should import from the `utils` package instead of redefining functions.
    *   **Delete:** Scripts that generate simple static plots that can be inline code (unless they are very complex).
*   **Metadata:** Complete the `images/metadata.json` file.

### Environment
*   **`requirements.txt`:**
    *   Add `nashpy`.
    *   Resolve potential `torch` vs `tensorflow` conflicts (decide on primary DL framework or ensure compatibility).

---

## 5. Phased Execution Plan

### Phase 1: The "Sweep" (Structure & Design)
*   **Target:** All 100+ Notebooks.
*   **Action:** Apply Header, Imports, and Style standards. Remove `sec()/note()`.

### Phase 2: The "Fix" (Correctness & Refactoring)
*   **Target:** Modules 04, 06, 09.
*   **Action:** Fix RBC hardcoding, expose Econometrics classes, ensure Finance data robustness.

### Phase 3: The "Enrichment" (Gaps & Writing)
*   **Target:** Modules 01, 02, 03, 05, 07, 08, 10.
*   **Action:** Add Introductions, Historical Vignettes, and missing visualizations (Game Trees, 3D Greeks).

### Phase 4: The "Polish" (Assets & Metadata)
*   **Target:** `images/`, `scripts/`, `utils/`.
*   **Action:** Refactor utilities, clean up scripts, finalize metadata.
