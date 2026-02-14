# Course Structure

Overview of how the course is organized and recommended learning paths.

---

## Module Organization

The course consists of **10 comprehensive modules**, a **high-performance computing** track, and an **Appendix** with mathematical foundations and practical tooling.

### Core Modules (1–3): Foundations & Methods

| Module | Notebooks | Focus |
|--------|-----------|-------|
| **01 — Foundations** | 24 | Python fundamentals, NumPy, Pandas, data acquisition, visualization, profiling |
| **02 — Numerical Methods** | 8 | Linear systems, optimization, root finding, interpolation, integration, differentiation, ODEs |
| **03 — Economic Modeling** | 7 | Dynamic programming, continuous-state DP, optimal stopping, robust control, structural estimation |

### Application Modules (4–10): Economics, Finance & ML

| Module | Notebooks | Focus |
|--------|-----------|-------|
| **04 — Macro Models** | 7 | Job search, neoclassical growth, RBC, OLG, New Keynesian, heterogeneous agents, endogenous growth |
| **05 — Micro Models** | 6 | Consumer/producer theory, general equilibrium, game theory, discrete choice, principal-agent, information economics |
| **06 — Econometrics** | 12 | OLS, MLE, causal inference, GMM, IV, RDD, synthetic control, DiD, time series, VAR, Bayesian, panel data |
| **07 — Machine Learning** | 22 | Supervised/unsupervised learning, deep learning (CNN, RNN, Transformers), RL, causal ML, NLP, GNNs |
| **08 — Time Series** | 6 | Stationary processes, ARMA/ARIMA, VAR, GARCH, cointegration |
| **09 — Finance** | 7 | Portfolio theory, asset pricing, option pricing, continuous-time finance, credit risk, HFT, financial frictions (BGG) |
| **10 — Specialized Models** | 3 | Agent-based models, heterogeneous-agent GE, network economics |

### Supplementary

| Section | Notebooks | Focus |
|---------|-----------|-------|
| **High-Performance Python** | 4 | HPC, Numba, Dask, GPU acceleration |
| **Appendix** | 8 | Real analysis, multivariate calculus, probability theory, linear algebra, Quarto publishing, Otter grading, replication exercises |

---

## Recommended Learning Paths

### Path 1: Full Course (Sequential)

Work through modules 01 → 10 in order. Each module builds on skills from earlier ones.

### Path 2: Econometrics Focus

`01 Foundations` → `02 Numerical Methods` → `06 Econometrics` → `08 Time Series` → `07 ML (selected)`

### Path 3: Finance Focus

`01 Foundations` → `02 Numerical Methods` → `03 Economic Modeling` → `08 Time Series` → `09 Finance`

### Path 4: Machine Learning for Economists

`01 Foundations` → `06 Econometrics (01–03)` → `07 Machine Learning` → `07-ML/17 Causal ML`

---

## Repository Layout

```
├── 01-Foundations/          # Python, data tools, visualization
├── 02-Numerical-Methods/    # Computational algorithms
├── 03-Economic-Modeling/    # DP, estimation, calibration
├── 04-Macro-Models/         # Macroeconomic models
├── 05-Micro-Models/         # Microeconomic models
├── 06-Econometrics/         # Statistical methods
├── 07-Machine-Learning/     # ML and deep learning
├── 08-Time-Series/          # Time series analysis
├── 09-Finance/              # Financial economics
├── 10-Specialized-Models/   # ABM, networks, hetero-agent GE
├── Appendix/                # Math foundations & tools
├── high_performance_python/  # HPC, Numba, Dask, GPU
├── data/                    # Datasets (FRED, finance, research)
├── images/                  # Generated figures
├── scripts/                 # Utility & image generation scripts
├── docs/                    # MkDocs documentation source
└── tests/                   # Test suite
```

---

For detailed module information, see [All Modules](../modules/index.md).
