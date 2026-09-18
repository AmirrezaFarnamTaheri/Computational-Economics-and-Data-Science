# Econometrics Cheat Sheet

> Quick reference for Module 06. Details: [OLS](../modules/06-econometrics/01-ols.md), [MLE](../modules/06-econometrics/02-mle.md), [Causal Inference](../modules/06-econometrics/03-causal-inference.md), [GMM & IV](../modules/06-econometrics/04-05-gmm-iv.md).

## Core objects & dimensions

| Object | Notation | Dimensions |
|---|---|---|
| Data | $\mathbf{y} \in \mathbb{R}^n$, $\mathbf{X} \in \mathbb{R}^{n \times k}$ | $n$ obs, $k$ regressors |
| Coefficients | $\beta \in \mathbb{R}^k$ | $k$-vector |
| Residuals | $\mathbf{u} \in \mathbb{R}^n$ | $n$-vector |
| Moments | $g(W_i, \theta)$ | $\mathbb{R}^r$, $r \ge k$ |

## Estimation

| Estimator | Formula | Key condition |
|---|---|---|
| OLS | $\hat{\beta} = (\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'\mathbf{y}$ | $\mathrm{rank}(\mathbf{X}) = k$ |
| 2SLS | $\hat{\beta} = (\mathbf{X}'P_Z\mathbf{X})^{-1}\mathbf{X}'P_Z\mathbf{y}$, $P_Z = Z(Z'Z)^{-1}Z'$ | instruments exogenous + relevant |
| MLE | $\hat{\theta} = \arg\max \sum_i \ln f(y_i \mid \theta)$ | interior, regular optimum |
| GMM | $\hat{\theta} = \arg\min\, g_N' W g_N$ | $E[g(W_i, \theta_0)] = 0$ |
| FE (panel) | within transformation | strict exogeneity |

## Inference

- OLS se: $\mathrm{Var}(\hat{\beta}) = \sigma^2 (\mathbf{X}'\mathbf{X})^{-1}$; heteroskedasticity-robust (White 1980); HAC (Newey-West, lag $\sim T^{1/3}$) for time series.
- Trinity: $LR = 2(\ell_1 - \ell_0) \sim \chi^2_q$; Wald and LM are asymptotically equivalent.
- GMM J-test: $J = N g_N' \hat{S}^{-1} g_N \sim \chi^2_{r-k}$ under overidentification.
- Weak instruments: first-stage $F < 10$ ⇒ 2SLS biased toward OLS; use Anderson-Rubin CIs.
- Nickell bias: lagged $y$ in FE panels biased $O(1/T)$ — use Arellano-Bond.

## Causal designs

| Design | Estimand | Threat to kill |
|---|---|---|
| RCT / DiD | ATT (scalar) | parallel trends (pre-trends necessary, not sufficient); staggered TWFE → Callaway-Sant'Anna |
| IV | LATE (compliers) | exclusion (untestable), weak instruments |
| RDD | $\tau = E[Y(1)-Y(0) \mid X = c]$ | manipulation of running variable (McCrary density test) |
| DAG rules | — | control for confounders, never colliders |

## Complexity

OLS via QR: $O(nk^2 + k^3)$. GMM adds an $r \times r$ long-run variance estimate.
