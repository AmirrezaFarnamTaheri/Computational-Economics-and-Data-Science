# Course Structure

The repository currently contains **129 notebooks**: **116 core-module notebooks** across ten modules, plus **9 Appendix notebooks** and **4 High-Performance Python notebooks**. Counts below are generated from the live source tree.

## Core Modules

| Module | Notebooks | Focus |
|---|---:|---|
| **01-Foundations — Foundations** | 25 | Python, reproducibility, data tools, visualization, profiling |
| **02-Numerical-Methods — Numerical Methods** | 8 | Linear algebra, root finding, optimization, approximation, integration, ODEs |
| **03-Economic-Modeling — Economic Modeling** | 8 | Dynamic programming, calibration/estimation, optimal stopping, robust control, structural estimation |
| **04-Macro-Models — Macro Models** | 11 | Search, growth, RBC, OLG, New Keynesian, heterogeneous agents, endogenous and continuous-time macro |
| **05-Micro-Models — Micro Models** | 7 | Consumer/producer theory, equilibrium, games, discrete choice, information, BLP demand |
| **06-Econometrics — Econometrics** | 14 | OLS, MLE, causal inference, GMM/IV/RDD, synthetic control, DiD/SDID, Bayesian and panel methods |
| **07-Machine-Learning — Machine Learning** | 22 | Prediction, deep learning, reinforcement learning, causal ML, NLP, GNNs |
| **08-Time-Series — Time Series** | 9 | ARMA/ARIMA, VAR, GARCH, cointegration, particle filtering and nonlinear state-space models |
| **09-Finance — Finance** | 8 | Portfolio theory, asset pricing, options, continuous time, credit risk, market microstructure and Hawkes models |
| **10-Specialized-Models — Specialized Models** | 4 | Agent-based, heterogeneous-agent GE, networks, climate-macro integrated assessment |

## Supplementary Tracks

- **Appendix:** 9 notebooks covering mathematical foundations, publishing, autograding, and empirical replications (Chetty, Card–Krueger, and Fama–French).
- **High-Performance Python:** 4 notebooks covering profiling, Numba, Dask, and GPU acceleration.

## Recommended Learning Paths

1. **Full computational economics:** 01 → 02 → 03 → 04/05 → 06 → 08 → 09/10, using 07 where ML methods are needed.
2. **Causal/empirical:** 01 → 02 → 06 → 07 (causal ML) → 08.
3. **Macro/heterogeneous agents:** 01 → 02 → 03 → 04 → 10, with HJB/HANK and HPC as advanced extensions.
4. **Finance:** 01 → 02 → 06/08 → 09.

## Repository Layout

```text
01-Foundations/
02-Numerical-Methods/
03-Economic-Modeling/
04-Macro-Models/
05-Micro-Models/
06-Econometrics/
07-Machine-Learning/
08-Time-Series/
09-Finance/
10-Specialized-Models/
Appendix/
high_performance_python/
data/
images/
scripts/
docs/
tests/
audit/
```

For the live notebook inventory and searchable reading views, see [All Modules](../modules/index.md).
