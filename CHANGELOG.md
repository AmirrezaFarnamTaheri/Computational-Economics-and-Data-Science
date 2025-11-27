# Changelog

## Session 7: Critical Module Refactoring and Feature Implementation
*   **Refactor:** `04-Macro-Models/03_RBC_Models.ipynb`
    *   **Structure:** Implemented "The Lens" introduction ("Microfoundations of Aggregates") and "Summary".
    *   **Correctness:** Re-implemented the QZ solver cleanly within the `RBCModel` class, ensuring robust handling of singular matrices.
    *   **Features:** Implemented a new `RBCNewsModel` class that rigorously extends the state space to simulate anticipated "news" shocks.
    *   **Visuals:** Added direct comparison plots of Surprise vs. News shocks to demonstrate the "investment-led boom" phenomenon.
*   **Refactor:** `05-Micro-Models/02_General_Equilibrium.ipynb`
    *   **Structure:** Implemented "The Lens" introduction ("The Invisible Hand Calculated") and "Summary".
    *   **Correctness:** Replaced placeholder code with a robust `CGEModel` class that solves the 2x2x2 General Equilibrium system using `scipy.optimize.root`.
    *   **Features:** Implemented a `HeckscherOhlinSystem` class to numerically verify the Heckscher-Ohlin trade theorem.
*   **Refactor:** `03-Economic-Modeling/04_Estimation_and_Calibration.ipynb`
    *   **Structure:** Implemented "The Lens" introduction ("From Theory to Reality") and "Summary".
    *   **Correctness:** Replaced dummy objective function with a real SMM estimator.
    *   **Performance:** Implemented a JIT-compiled Aiyagari solver using `numba` to enable live estimation within the notebook.
    *   **Verification:** Added a Monte Carlo test to verify parameter recovery and visualized the identification surface.
*   **Refactor:** `09-Finance/02_Portfolio_Theory.ipynb`
    *   **Structure:** Implemented "The Lens" introduction ("The Mathematics of Diversification") and "Summary".
    *   **Robustness:** Implemented a fail-safe data loading system that uses local CSVs (`fama_french_5_factors.csv`) and falls back to synthetic data generation if files are missing, ensuring offline functionality.
*   **Refactor:** `08-Time-Series/05_Volatility_Modeling_ARCH_GARCH.ipynb`
    *   **Structure:** Implemented "The Lens" introduction ("The Pulse of Fear") and "Summary".
    *   **Robustness:** Implemented robust data loading for S&P 500 data with synthetic fallback.
    *   **Visuals:** Standardized Q-Q plots and conditional volatility charts using the project's visual style.

## Session 6: Global Standardization and Core Module Refactors
*   **Global Standardization (All Modules):**
    *   Executed `scripts/remove_antipatterns.py` across all remaining modules (`02-10`, `Appendix`, `high_performance_python`) to replace custom `sec()` and `note()` calls with standard Markdown.
    *   Executed `scripts/standardize_notebooks.py` across all remaining modules to enforce consistent license headers and Matplotlib styling.
    *   Validated all 116 notebooks using `validate_notebooks.py` to ensure JSON integrity.
*   **Refactor:** `02-Numerical-Methods/01_Linear_Algebra.ipynb`
    *   **Structure:** Implemented the "Lens" introduction ("The Engine of Computational Economics") and a robust "Summary".
    *   **Content:** Clarified the geometric intuition of linear algebra and emphasized numerical stability (e.g., condition numbers, avoiding `inv(A)`).
    *   **Design:** Cleaned up code/markdown mixing and standardized imports.
*   **Refactor:** `03-Economic-Modeling/01_Dynamic_Programming.ipynb`
    *   **Structure:** Implemented the "Lens" introduction ("The Recursive Structure of Choice") and "Summary".
    *   **Content:** Strengthened the explanation of the Bellman Equation and Contraction Mapping Theorem.
    *   **Design:** Standardized visual configuration and imports.
*   **Refactor:** `04-Macro-Models/01_Job_Search.ipynb`
    *   **Structure:** Implemented the "Lens" introduction ("Frictions in the Labor Market") and "Summary".
    *   **Content:** Unified the narrative around search and matching frictions (McCall, DMP, Burdett-Mortensen).
    *   **Design:** Standardized visual configuration and imports.

## Session 5: Foundations Module Overhaul (Module 01)
*   **Refactor:** `01-Foundations/01_Introduction.ipynb`
    *   **Structure:** Strengthened the "Lens" introduction to strictly answer "What problem are we solving?" and "Why this method?". Added a robust "Summary" section.
    *   **Visuals:** Audited images and ensured metadata compliance. Improved visual layout and rhythm.
    *   **Writing:** Polished narrative tone for professional clarity.
    *   **Code:** Refined the Lucas Critique simulation code for better robustness and clarity.
*   **Refactor:** `01-Foundations/02_Professional_Development_Environment.ipynb`
    *   **Structure:** Added "The Lens" introduction: "From Disposable Scripts to Durable Scientific Artifacts". Added "Summary" section.
    *   **Standards:** Replaced custom helpers with standard Markdown. Cleaned up imports and visual configuration.
*   **Global Standardization (Batch 1):**
    *   Executed `scripts/remove_antipatterns.py` on `01-Foundations` to replace custom `sec()` and `note()` calls with standard Markdown.
    *   Executed `scripts/standardize_notebooks.py` on `01-Foundations` to enforce license headers and Matplotlib styling.
    *   Validated all notebooks in `01-Foundations` using `validate_notebooks.py`.

## Session 4: Deep Dive and Refactor - Macro Models (Module 04)
*   **Refactor:** `04-Macro-Models/03_RBC_Models.ipynb`
    *   Replaced manual and potentially unstable QZ solver with a robust implementation using `scipy.linalg.ordqz`.
    *   Implemented sorting of eigenvalues to satisfy Blanchard-Kahn conditions (2 stable eigenvalues for states K and A).
    *   Implemented `scripts/klein_solver.py` as a reference robust solver.
    *   Standardized notebook header and removed antipatterns.

## Session 3: Standardization of Foundations (Module 01)
*   **Fixes:**
    *   Repaired corrupted JSON structure in `01-Foundations/04_Python_Data_Model.ipynb`.
    *   Repaired corrupted JSON structure in `01-Foundations/15_Accessing_Economic_Data_via_APIs.ipynb`.
*   **Standardization:**
    *   Applied `scripts/fix_headers.py` to all notebooks in `01-Foundations/` to ensure consistent License headers.
    *   Applied `scripts/remove_antipatterns.py` to all notebooks in `01-Foundations/` to replace custom `sec()` and `note()` calls with standard Markdown.

## Session 2: Comprehensive Overhaul (Starting Nov 27)

*   **Infrastructure:**
    *   Initiated comprehensive audit of all 116 notebooks.
    *   Verified `images/metadata.json` integrity.
    *   Started standardization of License headers and removal of anti-patterns (`sec()`, `note()`).

## Session 1: Standardization and Overhaul

*   **Standardization:**
    *   Updated header for `01-Foundations/01_Introduction.ipynb`.
    *   Updated header for `01-Foundations/02_Professional_Development_Environment.ipynb`.
    *   Updated header for `01-Foundations/03_Python_Fundamentals_Data_Types.ipynb`.
    *   Updated header for `01-Foundations/04_Python_Data_Model.ipynb`.
    *   Updated header for `01-Foundations/05_Lists_and_Tuples.ipynb`.
    *   Updated header for `01-Foundations/06_Advanced_String_Processing.ipynb`.
    *   Updated header for `01-Foundations/07_Dictionaries.ipynb`.
    *   Updated header for `01-Foundations/08_Sets.ipynb`.
    *   Updated header for `01-Foundations/09_Control_Flow_and_Error_Handling.ipynb`.
    *   Updated header for `01-Foundations/10_Advanced_Functions.ipynb`.
    *   Updated header for `01-Foundations/11_Object_Oriented_Programming.ipynb`.
    *   Updated header for `01-Foundations/12_NumPy.ipynb`.
    *   Updated header for `01-Foundations/13_Pandas.ipynb`.
    *   Updated header for `01-Foundations/14_Introduction_to_Data_Acquisition.ipynb`.
    *   Updated header for `01-Foundations/15_Accessing_Economic_Data_via_APIs.ipynb`.
    *   Updated header for `01-Foundations/16_Data_Visualization.ipynb`.
    *   Updated header for `01-Foundations/17_Effective_Debugging.ipynb`.
    *   Updated header for `01-Foundations/18_Data_Acquisition_Web_Scraping.ipynb`.
    *   Updated header for `01-Foundations/19_Introduction_to_SQL.ipynb`.
    *   Updated header for `01-Foundations/20_Introduction_to_SciPy.ipynb`.
    *   Updated header for `01-Foundations/21_Symbolic_Computation_with_SymPy.ipynb`.
    *   Updated header for `01-Foundations/22_Computational_Complexity.ipynb`.
    *   Updated header for `01-Foundations/23_Profiling_and_Performance.ipynb`.
    *   Updated header for `01-Foundations/24_Production_Code_Standards.ipynb`.
    *   Removed `sec()` and `note()` from `01-Foundations/02_Professional_Development_Environment.ipynb`.
    *   Removed `sec()` and `note()` from `01-Foundations/04_Python_Data_Model.ipynb`.
    *   Removed `sec()` and `note()` from `01-Foundations/05_Lists_and_Tuples.ipynb`.
    *   Removed `sec()` and `note()` from `01-Foundations/06_Advanced_String_Processing.ipynb`.

- **Refactor:** Made `03-Economic-Modeling/01_Dynamic_Programming.ipynb` self-contained.
  - Embedded the `DynamicProgramming` class directly into the notebook.
  - Removed the external `finance_utils.py` file.
  - Replaced custom `sec()` and `note()` calls with standard Markdown headers and notes for better readability and portability.

- **Refactor:** Made `04-Macro-Models/01_Job_Search.ipynb` self-contained.
  - Embedded the `JobSearch` class directly into the notebook.
  - Removed the external `macro_utils.py` file.
  - Replaced custom `sec()` and `note()` calls with standard Markdown headers and notes for better readability and portability.

- **Refactor:** Made `06-Econometrics/02_Maximum_Likelihood.ipynb` self-contained.
  - Embedded the `MLEstimator` class directly into the notebook.
  - Removed the external `econometrics_utils.py` file.
  - Replaced custom `sec()` and `note()` calls with standard Markdown headers and notes for better readability and portability.
