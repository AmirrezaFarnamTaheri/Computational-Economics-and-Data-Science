# Comprehensive Improvement Roadmap

This document outlines the master plan for elevating the entire course repository to a "Gold Standard" of pedagogical, visual, and technical excellence. It addresses the 6 core tasks requested.

## 1. Executive Summary
The goal is to transform the repository into a cohesive, self-contained, and visually stunning educational resource. The `01-Foundations` module (specifically `01_Introduction.ipynb`) serves as the benchmark for tone, structure, and depth. All other modules will be elevated to match this standard.

## 2. Global Standards (The "Gold Standard")
All notebooks must adhere to the following strict standards:

### A. Structure & Metadata (Tasks 1 & 2)
*   **Header:** Standard Markdown header with Title, License Badges (MIT/CC-BY-4.0).
*   **Table of Contents:** Markdown-based TOC (not hardcoded HTML if possible, or consistent HTML).
*   **Introduction:** A "Big Picture" narrative section before any code runs.
*   **Metadata:** All images must be logged in `images/metadata.json` with valid descriptions and licenses.

### B. Visual Design (Task 3)
*   **No Custom Utility Styling:** Remove ad-hoc functions like `sec()` or `note()` defined in code cells (seen in Module 06). Use standard Markdown blockquotes (`>`) or consistent HTML classes for "Notes" and "Warnings".
*   **Plot Styling:** Use a unified context manager for plots:
    ```python
    with plt.style.context('seaborn-v0_8-whitegrid'):
        fig, ax = plt.subplots(...)
    ```
*   **Typography:** Use consistent H1, H2, H3 hierarchy.

### C. Pedagogy & Code (Tasks 4, 5, 6)
*   **"Scratch" vs "Library":** Explicitly mark sections where we build from scratch vs using a library.
*   **Self-Containment:** Exercises must load their data explicitly. Do not assume `econometrics_utils.py` has magically loaded data into the namespace.
*   **Tone:** Academic yet accessible. "Computation as a Lens."

---

## 3. Module-Specific Action Plans

### Module 01: Foundations
*   **Status:** **Gold Standard.**
*   **Actions:**
    *   **Audit:** Verify `metadata.json` coverage for all images.
    *   **Refinement:** Ensure `finance_utils.py` is either documented or folded into notebooks if small enough.

### Module 02: Numerical Methods
*   **Focus:** Math/Code Correctness (Task 4) and Visuals (Task 2).
*   **Actions:**
    *   Review `scripts/` for generated plots (e.g., `generate_newton_method.py`).
    *   Replace static plot scripts with high-quality saved images to reduce cell clutter, OR refactor into a cleaner `Visualizer` class.
    *   Ensure "Convergence" proofs are rigorous.

### Module 03: Economic Modeling (Micro/Macro Foundations)
*   **Focus:** Learning Arc (Task 1).
*   **Actions:**
    *   Ensure smooth transition from "Numerical Methods" to "Economic Application".
    *   **Task 5 (Gap):** Add a "Motivating Example" for each model (e.g., *why* do we care about the Cobweb model? -> Price stability).

### Module 04 & 05: Macro & Micro Models
*   **Focus:** Depth & Completeness (Task 5).
*   **Actions:**
    *   **Refactor:** If models (like RBC) are complex, encapsulate them in Classes (e.g., `class RBCModel`) to separate logic from presentation.
    *   **History:** Add "Historical Notes" (Task 6) similar to Module 01 (e.g., "The Lucas Critique context" for Macro).

### Module 06: Econometrics
*   **Status:** Needs Standardization.
*   **Actions:**
    *   **Design:** Remove `def sec(title): print(...)` and `def note(msg): ...`. Replace with Markdown headers and Blockquotes.
    *   **Data:** Explicitly load the `Guerry` dataset in the `Exercises` section.
    *   **Math:** Verify OLS derivations. Add "Geometric Interpretation" visualization if missing (Task 2).

### Module 07: Machine Learning
*   **Focus:** Modernity & Relevance.
*   **Actions:**
    *   Update libraries (ensure `scikit-learn`, `pytorch` versions are current).
    *   **Metadata:** Check sources for neural net diagrams. Replace low-res web images with SVG or generated diagrams.

### Module 08, 09, 10 (Time Series, Finance, Specialized)
*   **Focus:** Rigor & Real-world Data.
*   **Actions:**
    *   **Finance:** Ensure `pandas_datareader` calls are robust (APIs often break). Provide fallback `.csv` data in `data/` folder.
    *   **Task 5:** Add "Real World Constraints" discussion (transaction costs, liquidity).

### Appendix & Scripts
*   **Actions:**
    *   **Script Audit:** Review all 60+ `generate_*.py` scripts.
        *   *Keep:* Complex animations (e.g., `generate_aiyagari_animation.py`).
        *   *Retire:* Simple static plots (generate once, save to `images/`, delete script).
    *   **Metadata:** Complete the `metadata.json` audit.

---

## 4. Implementation Strategy

### Phase 1: Standardization (The "Sweep")
*   **Goal:** Uniform look and feel.
*   **Steps:**
    1.  Apply standard Header/Footer to all notebooks.
    2.  Replace custom `sec/note` functions with Markdown.
    3.  Standardize Matplotlib styling.

### Phase 2: Content & Code (The "Deep Dive")
*   **Goal:** Correctness and Robustness.
*   **Steps:**
    1.  Run `validate_notebooks.py` and fix errors.
    2.  Refactor complex code into Classes.
    3.  Fill pedagogical gaps (missing derivations/data).

### Phase 3: Visuals & Narrative (The "Polish")
*   **Goal:** Engagement.
*   **Steps:**
    1.  Update `metadata.json`.
    2.  Enhance historical vignettes.
    3.  Final proofread for tone.
