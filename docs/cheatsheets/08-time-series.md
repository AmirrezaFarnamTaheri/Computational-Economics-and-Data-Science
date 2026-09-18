# Time Series Cheat Sheet

> Quick reference for Module 08. Details: [ARMA](../modules/08-time-series/02-arma.md), [ARIMA](../modules/08-time-series/03-arima.md), [VAR](../modules/08-time-series/04-var.md), [GARCH](../modules/08-time-series/05-garch.md).

## Core objects & dimensions

| Object | Notation | Dimensions |
|---|---|---|
| Series | $y_t$ | scalar (univariate) or $\mathbb{R}^n$ (VAR) |
| AR/MA coefficients | $\phi_i, \theta_j$ | scalars; $p$ and $q$ of them |
| Innovation | $\epsilon_t$ | white noise, variance $\sigma^2$ |
| VAR companion | $A \in \mathbb{R}^{np \times np}$ | companion matrix |

## Univariate workhorse formulas

- **ARMA(p, q)**: $\underbrace{y_t - \sum_{i=1}^p \phi_i y_{t-i}}_{AR} = \underbrace{\epsilon_t + \sum_{j=1}^q \theta_j \epsilon_{t-j}}_{MA}$.
- Stationarity: AR roots outside the unit circle; invertibility: MA roots outside. AR(1) ACF: $\rho_k = \phi^k$.
- ARIMA(p, d, q): difference $d$ times to model a stationary series. Stationary ARMA forecasts approach the unconditional mean; integrated level forecasts need not mean-revert (a random walk forecasts its last observed level).
- **GARCH(1,1)**: $\sigma_t^2 = \omega + \alpha u_{t-1}^2 + \beta \sigma_{t-1}^2$; need $\omega > 0$, $\alpha + \beta < 1$; unconditional variance $\frac{\omega}{1-\alpha-\beta}$; persistence $\alpha + \beta$.
- Wold: a purely nondeterministic covariance-stationary series is $\mu + \sum_{j=0}^\infty \psi_j \epsilon_{t-j}$, $\sum \psi_j^2 < \infty$. In general, a deterministic component must also be included.

## Multivariate (VAR)

- Reduced form: $\mathbf{y}_t = c + A_1 \mathbf{y}_{t-1} + \dots + A_p \mathbf{y}_{t-p} + u_t$, $u_t \in \mathbb{R}^n$, $\Sigma_u \in \mathbb{R}^{n \times n}$.
- Structural shocks: $A u_t = B \epsilon_t$; Cholesky = recursive identification (order matters).
- IRFs: coefficients of the VMA($\infty$) representation; FEVD decomposes forecast variance.
- Granger causality: lags of $y_2$ help predict $y_1$ (F-test) — *predictive* causality only.
- Cointegration: $y_t \sim I(1)$ with $\beta' y_t \sim I(0)$; ECM: $\Delta y_t = \alpha \beta' y_{t-1} + \Gamma \Delta y_{t-1} + \epsilon_t$; Engle-Granger two-step or Johansen trace test.

## Workflow & complexity

1. Stationarity (ADF) → 2. identify orders (ACF/PACF, AIC/BIC) → 3. estimate → 4. diagnose residuals (Ljung-Box) → 5. forecast.
ARMA MLE via Kalman filter/CSS: $O(T)$ per likelihood evaluation; VAR OLS: equation-by-equation $O(T n^2 p^2)$.
