# Computational Economics & Data Science: The "Gold Standard" Roadmap

**Status:** 🚧 In Progress
**Target:** Production-Ready Open Source Course
**Author:** [Agent Name]
**Date:** October 2025

---

## 1. Executive Summary

This document serves as the **definitive execution plan** to elevate the `Computational-Economics-and-Data-Science` repository to a world-class educational resource. The goal is not merely "functional" code, but a cohesive, rigorously interconnected, and aesthetically professional curriculum that rivals top-tier university courses.

**The "Gold Standard" Philosophy:**
*   **Narrative First:** Code follows context. Every notebook begins with an economic question, not a library import.
*   **No "Magic":** Helper functions like `sec()` or `note()` that obscure standard behaviors are banned. We use standard Markdown and Python.
*   **Visual Excellence:** All plots use a unified, publication-quality style. Diagrams are localized and metadata-rich.
*   **Mathematical Rigor:** Derivations are explicit. Solvers are robust (no hardcoding).
*   **Self-Containment:** Every notebook runs top-to-bottom without hidden local dependencies.

---

## 2. Global Standards & Design System

These rules apply to **every single notebook** (116 files).

### A. Visual & Structural Design (Task 3)
1.  **Removal of Anti-Patterns (High Priority):**
    *   **Target:** ~202 instances of `def sec(title):` and `def note(msg):` across all modules.
    *   **Action:** Replace `sec(title)` calls with standard Markdown headers (`##`, `###`).
    *   **Action:** Replace `note(msg)` calls with standard Markdown blockquotes (`> **Note:** ...`) or info alerts (`<div class="alert alert-info">...</div>`).
2.  **Plot Styling:**
    *   **Action:** Enforce a unified Matplotlib style context in every notebook setup cell:
        ```python
        import matplotlib.pyplot as plt
        import seaborn as sns
        plt.style.use('seaborn-v0_8-whitegrid')
        plt.rcParams.update({'figure.figsize': (10, 6), 'font.size': 12})
        ```
3.  **Standard Headers:**
    *   **Action:** Ensure every notebook starts with the Title, Author, and Dual-License Badge (MIT Code / CC-BY Content).

### B. Writing & Tone (Task 6)
1.  **Banned Jargon:** Remove words like "deep dive", "unleash", "comprehensive", "demystify", "step-by-step".
2.  **Active Voice:** Use direct, active language (e.g., "We solve for X" instead of "X is solved for").
3.  **Transitions:** Ensure smooth narrative flow between code cells and markdown. No "wall of code" without explanation.

---

## 3. Module-Specific Execution Plan

### **Module 01: Foundations (The Benchmark)**
*   **Goal:** Polish to perfection as the template for all others.
*   **Task 1 (Structure):**
    *   Add `# Summary` sections to all 24 notebooks (currently missing).
    *   Refine `01_Introduction.ipynb` to include the "Four Revolutions" historical narrative.
*   **Task 2 (Components):**
    *   Check `02_Professional_Development_Environment.ipynb` for outdated installation instructions.

### **Module 02: Numerical Methods**
*   **Task 4 (Correctness):**
    *   `01_Linear_Algebra.ipynb`: Verify the condition number explanation and stability of `inv()` vs `solve()`.
    *   `04_Root_Finding.ipynb`: Ensure Newton's method implementation handles non-convergence gracefully.
*   **Task 3 (Design):**
    *   Replace all `sec()` calls in `03_Numerical_Differentiation.ipynb` and others.

### **Module 03: Economic Modeling**
*   **Task 5 (Gaps):**
    *   `04_Estimation_and_Calibration.ipynb`: **CRITICAL.** Replace the "Dummy Objective" in the `SMM` class with a real estimation using simulated data (e.g., estimating $\beta$ and $\gamma$ for an Aiyagari model).
    *   `01_Dynamic_Programming.ipynb`: Replace custom `tauchen` discretization with a robust implementation or `quantecon` library call (if permitted), or write a robust `tauchen` function in `scripts/`.

### **Module 04: Macro Models**
*   **Task 4 (Correctness):**
    *   `03_RBC_Models.ipynb`: **CRITICAL.** The solutions `P_sol` and `Q_sol` are hardcoded strings/arrays.
        *   **Action:** Implement a real QZ Decomposition or Schur Decomposition solver (using `scipy.linalg.ordqz`) to solve the linearized system dynamically.
*   **Task 1 (Flow):**
    *   Ensure the transition from Solow (Mod 4.1) to Ramsey (Mod 4.2) to RBC (Mod 4.3) is seamless.

### **Module 05: Micro Models**
*   **Task 5 (Gaps):**
    *   `02_General_Equilibrium.ipynb`: **CRITICAL.** The Heckscher-Ohlin solver is missing logic. Implement a 2-good, 2-factor CGE solver using `scipy.optimize.root`.
    *   `03_Game_Theory.ipynb`: Add `graphviz` visualizations for extensive form games (Game Trees).
*   **Task 3 (Visuals):**
    *   Generate static images for the Edgeworth Box if dynamic plotting is unstable.

### **Module 06: Econometrics**
*   **Task 2 (Refactor):**
    *   `econometrics_utils.py`: Verify this file is imported correctly in `02_Maximum_Likelihood.ipynb`. If it defines `MLEstimator`, ensure the notebook demonstrates it clearly.
*   **Task 5 (Enrichment):**
    *   `01_Linear_Model_and_OLS.ipynb`: Add the "Frisch-Waugh-Lovell" theorem proof/demonstration if missing.

### **Module 07: Machine Learning**
*   **Task 4 (Data Ethics):**
    *   Verify `01_Introduction_to_ML_for_Economists.ipynb` uses `fetch_california_housing` (DONE). Ensure text description matches the code (remove references to "Boston").
*   **Task 2 (Cleanup):**
    *   Delete `08_Recurrent_Neural_Networks_executed.ipynb` and `09_LSTMs_and_GRUs_executed.ipynb` (duplicate artifacts).

### **Module 08: Time Series**
*   **Task 4 (Robustness):**
    *   `04_Vector_Autoregression.ipynb`: Wrap `pandas_datareader` calls in `try/except` blocks. Provide a fallback to local CSV data (in `data/`) if the API fails.
    *   **Action:** Create a `scripts/download_macro_data.py` to fetch and save these CSVs for offline use.

### **Module 09: Finance**
*   **Task 5 (Enrichment):**
    *   `04_Option_Pricing.ipynb`: Add a 3D surface plot of the "Greeks" (Delta/Gamma) vs. Spot Price and Time to Maturity.
    *   **Refactor:** Ensure Black-Scholes logic is encapsulated in a class `OptionPricer` for reusability.

### **Module 10: Specialized Models**
*   **Task 4 (Dependencies):**
    *   `01_Agent_Based_Models.ipynb`: Remove inline `!pip install networkx`. Ensure `networkx` is in `requirements.txt`.
    *   **Action:** Verify `03_Network_Economics.ipynb` for similar issues.

---

## 4. Technical Debt & Cleanup Strategy

1.  **Image Localization (Task 2):**
    *   **Audit:** Scan `images/metadata.json`. Any image without a "Source" or "License" needs to be fixed.
    *   **Action:** Move inline plot generation code (that produces static educational diagrams) to `scripts/generate_diagrams.py`.
2.  **Requirements Management:**
    *   **Action:** Consolidate all imports from all notebooks into a single `requirements.txt`. Remove unused libs.
3.  **Git Hygiene:**
    *   **Action:** Ensure `.gitignore` excludes `__pycache__`, `.ipynb_checkpoints`, and `*.csv` (unless they are small example datasets).

---

## 5. Verification Protocol (The "Pre-Flight Check")

Before marking any task as "Complete", the following must be true:
1.  **Kernel Restart & Run All:** The notebook executes from top to bottom without errors.
2.  **No Custom Prints:** `sec()` and `note()` functions are undefined and unused.
3.  **Visual Check:** All plots have titles, axis labels, and legends.
4.  **Data Check:** No API keys are hardcoded. Data loading falls back gracefully.
5.  **Lint:** Markdown is clean (no broken LaTeX `$$`).

---

## 6. Phased Execution

*   **Phase 1:** Global Search & Replace (`sec`/`note`), Style Headers. (Automated + Manual)
*   **Phase 2:** Critical Model Fixes (RBC, HO, SMM). (Deep Coding)
*   **Phase 3:** Content Enrichment & Historical Context. (Writing & Derivation)
*   **Phase 4:** Final Polish & Website Generation. (Documentation)
