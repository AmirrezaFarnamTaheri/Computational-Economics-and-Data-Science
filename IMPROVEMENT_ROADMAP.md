# Comprehensive Improvement Roadmap

This document outlines the master plan for the "Gold Standard" overhaul of the Computational Economics repository. It is a living document that tracks the status of the 6 major tasks defined for the project.

## 1. Executive Summary & Status

The project is currently in the **Refinement & Correction** phase. The repository structure is solid, but there are significant gaps in consistency, content validation, and specific technical debt that must be addressed to reach the "Production Ready" state claimed in the report.

**Current Focus:**
1.  **Standardization:** Eliminating ad-hoc `sec()`/`note()` helpers and unifying visual styles (Task 3).
2.  **Correctness:** Fixing identified model errors (RBC, HO, SMM) and validating math/code (Task 4).
3.  **Completeness:** Filling logic gaps and enhancing explanations (Task 5).
4.  **Flow:** Improving the narrative arc and "Lens" introductions (Task 1).

---

## 2. Detailed Task Breakdown

### **TASK 1: Structure & Coherence**
*Goal: Strengthen the learning arc and ensure a smooth narrative flow.*

*   **Action 1.1: Audit & Narrative Alignment**
    *   [ ] **Review:** Scan all 116 notebooks for the "Context before Code" principle.
    *   [ ] **Gap Fill:** Ensure every notebook starts with a clear "Lens" introduction motivating the economic problem.
    *   [ ] **Flow:** Verify that `01_Introduction.ipynb` in Module 1 acts as the "Gold Standard" anchor.
*   **Action 1.2: Standardize Headers & Licensing**
    *   [ ] **Check:** Ensure all notebooks have the standard dual-license badge header (MIT/CC-BY).
    *   [ ] **Fix:** Update `validate_notebooks.py` or a new script to enforce this header.
*   **Action 1.3: Explicit Summaries**
    *   [ ] **Audit:** Identify notebooks missing a final `# Summary` or `## Conclusion` section.
    *   [ ] **Implement:** Add comprehensive summaries to all Module 01 notebooks (currently missing).

### **TASK 2: High-Value Components**
*Goal: Rework low-value cells and unify image assets.*

*   **Action 2.1: Image Generation & Management**
    *   [ ] **Migration:** Move inline Matplotlib plotting code for educational diagrams (e.g., payoff diagrams, trees) to `scripts/` to keep notebooks clean.
    *   [ ] **Metadata:** Complete `images/metadata.json` for all images, ensuring every file has a description, source, and license.
    *   [ ] **Replacement:** Identify low-quality schematic images and replace them with high-quality web assets or better Python-generated alternatives.
*   **Action 2.2: Interactive Elements**
    *   [ ] **Refinement:** Review interactive widgets (if any) to ensure they are robust and add pedagogical value.

### **TASK 3: Visual & Structural Design**
*Goal: Clean, modern, and cohesive layout.*

*   **Action 3.1: Anti-Pattern Removal (CRITICAL)**
    *   [ ] **Search:** Locate all instances of `def sec(title)` and `def note(msg)` (~202 files affected).
    *   [ ] **Replace:** Convert `sec()` calls to standard Markdown headers (`##`, `###`).
    *   [ ] **Replace:** Convert `note()` calls to standard Markdown blockquotes (`> **Note:**`).
*   **Action 3.2: Visual Unification**
    *   [ ] **Style:** Enforce `plt.style.use('seaborn-v0_8-whitegrid')` context managers for all plots to prevent side effects.
    *   [ ] **Typography:** Standardize Markdown usage for equations ($...$) and block math ($$ ... $$).

### **TASK 4: Correctness & Validation**
*Goal: Verify math, proofs, and code.*

*   **Action 4.1: Specific Model Fixes (Identified Issues)**
    *   [ ] **Module 04 (Macro):** Remove hardcoded RBC solutions (`P_sol`, `Q_sol` in `03_RBC_Models.ipynb`) and implement a robust QZ decomposition solver.
    *   [ ] **Module 05 (Micro):** Implement the missing Heckscher-Ohlin trade solver in `02_General_Equilibrium.ipynb`.
    *   [ ] **Module 09 (Finance):** Replace any hardcoded Black-Scholes implementations with a robust `OptionPricer` class (if not already done).
*   **Action 4.2: Utility Refactoring**
    *   [ ] **Econometrics:** Verify `MLEstimator` in `06-Econometrics/econometrics_utils.py` and ensure it is correctly imported/used in notebooks.
    *   [ ] **Finance:** Move `finance_utils.py` logic to a proper `utils/` module if it creates circular dependencies or path issues.
*   **Action 4.3: Deprecation & Ethical Standards**
    *   [ ] **Machine Learning:** Replace the "Boston Housing" dataset in `07-Machine-Learning` with "California Housing" due to ethical concerns.
    *   [ ] **Libraries:** Remove inline `!pip install` calls; move dependencies to `requirements.txt`.

### **TASK 5: Filling Conceptual Gaps**
*Goal: Deepen the content and add missing links.*

*   **Action 5.1: Content Enrichment**
    *   [ ] **Module 03:** Replace the "Dummy Objective" in the SMM class in `04_Estimation_and_Calibration.ipynb` with a real estimation example.
    *   [ ] **Module 05:** Add `graphviz` game trees to Game Theory notebooks.
    *   [ ] **Module 06:** Ensure `MLEstimator` is fully explained and demonstrated.
    *   [ ] **Module 09:** Add 3D Greeks surface plots to Option Pricing.
*   **Action 5.2: Historical Context**
    *   [ ] **Enrich:** Add historical notes (e.g., about Black-Scholes, Arrow-Debreu, Nash) to relevant notebooks where missing.

### **TASK 6: Writing & Refinement**
*Goal: Polished, professional, and direct tone.*

*   **Action 6.1: Tone Check**
    *   [ ] **Review:** Ensure avoiding jargon like "deep dive", "unleash", "comprehensive" (per memory instructions).
    *   [ ] **Edit:** Refine the introductions and transitions of all modified notebooks.
*   **Action 6.2: Code Comments**
    *   [ ] **Annotate:** Ensure complex code blocks (especially solvers) have clear, instructional comments.

---

## 3. Immediate Execution Plan (Batch 1)

1.  **Roadmap Approval:** Get user sign-off on this document.
2.  **Anti-Pattern Sweep (Task 3):** Run a script to replace `sec()` and `note()` across the entire codebase. This is a high-volume change that clears the way for manual refinement.
3.  **Module 01 Refinement (Task 1):** Manually polish `01-Foundations` to establish it as the "Gold Standard" benchmark, adding summaries and checking headers.
4.  **Critical Fixes (Task 4):**
    *   Implement RBC Solver (Module 04).
    *   Implement HO Solver (Module 05).
    *   Swap Boston -> California (Module 07).
5.  **Validation:** Run `validate_notebooks.py` to ensure JSON integrity after changes.

---

## 4. Verification Standards

*   **Code:** Must run error-free from top to bottom.
*   **Visuals:** All plots must have labels, titles, and legends.
*   **Style:** No `sec()` or `note()` functions defined in the notebook.
*   **Data:** No reliance on external API keys without fallbacks; no deprecated datasets.
