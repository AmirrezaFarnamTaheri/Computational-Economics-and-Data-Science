# Project Instructions: Computational Economics and Data Science

Graduate-level course repository on modern computational methods in economics, econometrics, dynamic modeling, machine learning, and quantitative finance.

## Tech Stack
- **Language & Runtime:** Python 3.10+ (tested against Python 3.11)
- **Environment Management:** Conda / Mamba (`environment.yml`), `uv` / `pip` (`requirements.txt`, `pyproject.toml`)
- **Computational Core:** `numpy`, `scipy`, `pandas`, `sympy`, `numba`, `dask`, `cupy`
- **Econometrics & Time Series:** `statsmodels`, `linearmodels`, `arch`
- **Machine Learning & Deep Learning:** `scikit-learn`, `torch` (PyTorch), `keras` / `tensorflow`
- **Documentation & Publishing:** `mkdocs-material`, `pymdown-extensions`, `quarto`, `nbformat`
- **Testing & Quality Assurance:** `pytest`, `black` (line-length 88), `ruff`

## Code Style & Formatting
- **Python Code Standards:** Conform to PEP 8, formatted with Black (`line-length = 88`) and linted with Ruff (`select = ["E", "F", "W", "I"]`, `ignore = ["E501"]`).
- **Notebook Hygiene:** 
  - Each `.ipynb` must be self-contained with explicit imports and seed initialization (`np.random.seed(...)`).
  - No deprecated helper calls (e.g. `sec()`, `note()`) — use native Markdown headers (H2/H3) and blockquotes (`> **Note:**`).
  - Header badges must link correctly (`../LICENSE` for subdirectories).
  - Notebooks should feature a pedagogical **"The Lens"** (economic intuition/problem) and a concluding **"Summary and Key Takeaways"**.
- **Mathematical Conventions:** Standardize mathematical notation against [`docs/resources/notation.md`](docs/resources/notation.md).

## Testing & Validation
- **Run Unit Tests:** `pytest tests/ -v --tb=short`
- **Audit Notebooks JSON & Structure:** `python scripts/audit_notebooks.py`
- **Check Formatting:** `black --check --diff .`
- **Run Linter:** `ruff check .`

## Project Structure
- `01-Foundations/`: Python fundamentals, data structures, data acquisition (APIs/SQL), NumPy, Pandas, SymPy, SciPy, Complexity (25 notebooks).
- `02-Numerical-Methods/`: Linear algebra, differentiation, root-finding, optimization, interpolation, integration, ODEs (8 notebooks).
- `03-Economic-Modeling/`: Dynamic programming (VFI/PFI), continuous state DP, discrete choice, structural estimation (`DiscreteDP`, `dp_solver.py`) (8 notebooks).
- `04-Macro-Models/`: Job search, Neoclassical growth, RBC models (foundations, solution, surprise shocks, news shocks), OLG, New Keynesian, HANK (10 notebooks).
- `05-Micro-Models/`: Consumer/producer theory, General Equilibrium (welfare theorems, Brouwer fixed point), game theory, auctions, discrete choice, principal-agent (6 notebooks).
- `06-Econometrics/`: OLS, MLE, Causal inference ($d$-separation, DAGs), GMM, IV, RDD, Synthetic controls, DiD, Bayesian, Panel data (13 notebooks).
- `07-Machine-Learning/`: SML, GBM, SVM, Ensembles, Deep Learning (Universal Approximation), CNNs, RNNs, LSTMs, Transformers, VAEs, SSL, RL, Causal ML, NLP, GNNs (22 notebooks).
- `08-Time-Series/`: ARMA, ARIMA, VAR (identification, IRF, FEVD), GARCH, Cointegration / VECM, Stationarity tests (ADF / KPSS) (8 notebooks).
- `09-Finance/`: Portfolio theory, Asset pricing, Option pricing, Continuous-time finance (Itô calculus, Black-Scholes), Credit risk, BGG financial frictions (7 notebooks).
- `10-Specialized-Models/`: Agent-based models, HANK general equilibrium, network economics (3 notebooks).
- `Appendix/`: Mathematical foundations (Real Analysis A1, Multivariate Calculus A2, Probability Theory A3, Linear Algebra A4) & Tooling tutorials (T1 Quarto, T2 Chetty replication, T3 Otter) (7 notebooks).
- `high_performance_python/`: HPC, Numba JIT, Dask distributed computing, CuPy GPU acceleration (4 notebooks).
- `scripts/`: Image generators, macro solvers (`macro_utils.py`), data downloaders, notebook auditors.
- `tests/`: Pytest suites for dynamic programming (`test_dp_solver.py`), macroeconomic QZ solvers (`test_macro_utils.py`), Tauchen discretization (`test_macro_vfi_utils.py`), and notebook JSON integrity (`test_notebooks.py`).
- `docs/`: MkDocs documentation site source.
