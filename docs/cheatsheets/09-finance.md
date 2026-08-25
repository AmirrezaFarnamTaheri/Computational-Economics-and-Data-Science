# Finance Cheat Sheet

> Quick reference for Module 09. Details: [Portfolio Theory](../modules/09-finance/02-portfolio.md), [Asset Pricing](../modules/09-finance/03-asset-pricing.md), [Option Pricing](../modules/09-finance/04-options.md), [Continuous Time](../modules/09-finance/05-continuous-time.md).

## Core objects & dimensions

| Object | Notation | Dimensions |
|---|---|---|
| Returns | $R_i$, excess $R_i - R_f$ | scalars |
| Weight vector | $w \in \mathbb{R}^N$ | $N$ assets |
| Covariance | $\Sigma \in \mathbb{R}^{N \times N}$ | symmetric PSD |
| SDF | $m_{t+1}$ | scalar stochastic |
| Option value | $C(S, t)$ | scalar field |

## Portfolio theory

- Mean-variance: $\min_w \tfrac{1}{2} w'\Sigma w$ s.t. $\mu'w \ge \bar{r}$, $\mathbf{1}'w = 1$; FOC $\Sigma w = \lambda\mu + \gamma\mathbf{1}$ ⇒ $w^* = \Sigma^{-1}(\lambda\mu + \gamma\mathbf{1})$.
- Tangency portfolio: $w \propto \Sigma^{-1}(\mu - R_f \mathbf{1})$; Sharpe $= \frac{E[R] - R_f}{\sigma}$ (annualize mean by 12, vol by $\sqrt{12}$).
- Estimation error: sample means are noisy ⇒ corner solutions; shrink $\Sigma$ (Ledoit-Wolf) and constrain $w$.

## Asset pricing

- SDF pricing: $p_t = E_t[m_{t+1} x_{t+1}]$; CCAPM: $m_{t+1} = \beta (C_{t+1}/C_t)^{-\gamma}$ ⇒ $E[R_i] - R_f \approx \gamma\,\mathrm{Cov}(R_i, \Delta c)$.
- CAPM: $E[R_i] - R_f = \beta_i (E[R_m] - R_f)$, $\beta_i = \mathrm{Cov}(R_i, R_m)/\mathrm{Var}(R_m)$.
- Fama-MacBeth: first-pass betas, second-pass risk premia; Shanken-correct the standard errors (generated regressors).

## Derivatives

- Binomial: $p = \frac{e^{r\Delta t} - d}{u - d} \in (0,1)$; value by backward induction, $O(N^2)$ nodes for $N$ steps.
- **BSM** (European): $C = S_0 N(d_1) - K e^{-rT} N(d_2)$, $d_1 = \frac{\ln(S_0/K) + (r + \sigma^2/2)T}{\sigma\sqrt{T}}$, $d_2 = d_1 - \sigma\sqrt{T}$.
- Put-call parity: $C - P = S_0 - K e^{-rT}$.
- Greeks: $\Delta_{call} = N(d_1)$ (shares per option); Vega $= S_0 \sqrt{T}\, \phi(d_1)$.
- Itô: $df = f_t dt + f_S dS + \tfrac{1}{2} f_{SS} (dS)^2$ with $(dS)^2 = \sigma^2 S^2 dt$.

## Credit & microstructure

- Merton: equity $= V_A N(d_1) - F e^{-rT} N(d_2)$ (call on assets); default if $V_A(T) < F$; distance-to-default $= d_2$.
- Reduced form: survival $e^{-\lambda T}$; spread $\approx \lambda (1 - R)$ for recovery $R$.
- Hawkes: $\lambda(t) = \mu + \sum_{t_i < t} \alpha e^{-\beta (t - t_i)}$; stationary iff branching $n = \alpha/\beta < 1$; mean intensity $\frac{\mu}{1-n}$.
- Impact (square-root law): $I(Q) = Y \sigma \sqrt{Q/V}$, $Y = O(1)$.

## Monte Carlo discipline

Standard error falls as $1/\sqrt{N}$ — quote it; antithetic/control variates before brute force.
