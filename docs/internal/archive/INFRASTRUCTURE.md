# Infrastructure & Technology Strategy

To support the "Zero to Hero" pedagogical goals, the repository requires a robust technical infrastructure. This document outlines the strategy for data management, testing, and environment consistency.

## I. Data Management Strategy

Real-world data is the lifeblood of modern economics. We will move away from synthetic random data to "Real Data by Default".

### 1. `econometrics_data` Utility Module
We will create a lightweight local Python module `scripts/data_loader.py` to abstract data fetching complexity.

*   **Capabilities:**
    *   **API Wrapper:** unified interface for `pandas-datareader` (FRED), `wbdata` (World Bank), and `yfinance`.
    *   **Caching:** Decorators to cache API responses locally (pickle/parquet). This prevents rate-limiting during repeated notebook runs and allows offline work.
    *   **normalization:** Helper functions to standardize date formats and column names (e.g., converting 'DATE' to DateTime Index).

### 2. Standard Datasets
We will curate a set of standard datasets to be used across multiple modules, ensuring continuity.
*   **Macro:** US GDP, Inflation (CPI/PCE), Unemployment (FRED).
*   **Micro:** Penn World Table (PWT 10.0), Chetty Mobility Data (cleaned subset).
*   **Finance:** Fama-French Factors, S&P 500 OHLCV.

---

## II. Testing & Quality Assurance

A broken notebook is a broken lesson. We will implement a rigorous testing regime.

### 1. Automated Notebook Testing (`nbval`)
*   **Tool:** `pytest` with the `nbval` plugin.
*   **Policy:** Every notebook must execute from top to bottom without error.
*   **Sanity Checks:** "Smoke tests" will be added to `scripts/` to verify that key simulations produce results within expected bounds (e.g., Savings Rate $\in (0, 1)$).

### 2. Linting and Formatting
*   **Tools:** `black` (formatting), `ruff` (linting), `isort` (imports).
*   **Pre-commit Hooks:** A `.pre-commit-config.yaml` is already present. We will enforce strict compliance to the **Code Style Guide** defined in `PEDAGOGY.md`.

---

## III. Environment Management

Reproducibility is a core tenet of the course.

### 1. Dependency Specification
*   **`environment.yml`:** The source of truth for Conda environments.
*   **`requirements.txt`:** For pip users.
*   **Versioning:** All major libraries (`numpy`, `pandas`, `scipy`, `matplotlib`, `statsmodels`) will be pinned to specific minor versions to prevent API breakage.

### 2. Interactive Environment
*   **Binder:** The repository will be configured for launch on MyBinder.org, allowing students to run code in the browser without local installation.
*   **Colab Compatibility:** A "Open in Colab" badge will be added to all headers. We will ensure code cells do not rely on local file paths that break in Colab (using the Data Loader to handle remote fetching).

---

## IV. Documentation & Publishing

### 1. Quarto Integration
*   The entire repository will be structured to render as a cohesive **Quarto Book**.
*   **Cross-Referencing:** We will use Quarto's `@ref` syntax to link between chapters.
*   **Equations:** Mathjax compatibility will be verified.

### 2. Navigation
*   A `_quarto.yml` file will define the sidebar structure, matching the Module hierarchy defined in `FULL_ROADMAP.md`.
