# Notation Glossary

This page is the project-wide reference for mathematical notation. Every
notebook uses the symbols below with the meanings stated here; where a
notebook must deviate (for example, when replicating a paper that uses
different conventions), the deviation is declared explicitly at the point
of first use.

The tables also give the canonical **code variable name** for each symbol,
so that the mapping between the mathematics and the Python implementation
is one-to-one.

---

## 1. Core Conventions

| Convention | Rule |
|---|---|
| Discount factor | Always $\beta \in (0,1)$. Never $\delta$, which is reserved for depreciation. |
| Time subscripts | $x_t$ is the value in period $t$; $x_{t+1}$ (or $x'$ in recursive notation) is next period. |
| Steady states | A bar: $\bar{k}$, or the subscript $ss$ in code (`k_ss`). |
| Log-deviations | A hat: $\hat{x}_t = \log x_t - \log \bar{x}$. |
| Estimators | A hat on the parameter: $\hat{\beta}_{OLS}$. Context (econometrics vs. macro) disambiguates from log-deviations. |
| Vectors / matrices | Lowercase bold or plain italic for vectors ($x$), uppercase for matrices ($A$). |
| Transpose | $A^\top$ (code: `A.T`). |
| Expectations | $\mathbb{E}_t[\cdot]$ denotes expectation conditional on time-$t$ information. |
| Counts in code | `n_<thing>`: `n_states`, `n_actions`, `n_obs`, `n_features`. |
| Random draws in code | `rng = np.random.default_rng(seed)` — never the legacy `np.random.seed`. |

**Terminology rule:** the first use of a term in a notebook spells it out with
its abbreviation — "Value Function Iteration (VFI)" — and later uses employ
the abbreviation only.

---

## 2. General Mathematics & Analysis

| Symbol | Definition | Plain English | Code |
|---|---|---|---|
| $\mathbb{R}^n$ | $n$-dimensional Euclidean space | The set of real vectors of length $n$ | — |
| $f: X \to Y$ | Function from domain $X$ to codomain $Y$ | A rule mapping inputs to outputs | `def f(x):` |
| $\|x\|_\infty$ | $\max_i \lvert x_i \rvert$ | Sup norm: the largest entry in absolute value | `np.max(np.abs(x))` |
| $\nabla f(x)$ | Gradient vector of $f$ at $x$ | Direction of steepest ascent | `grad` |
| $H_f(x)$ | Hessian matrix of second derivatives | Local curvature of $f$ | `hess` |
| $J_f(x)$ | Jacobian matrix of a vector-valued $f$ | All first derivatives, stacked | `jac` |
| $\mathcal{O}(g(n))$ | Big-O asymptotic upper bound | "Grows no faster than $g$" | — |
| $x^*$ | Fixed point or optimum | The solution the algorithm seeks | `x_star` |

---

## 3. Probability & Statistics

| Symbol | Definition | Plain English | Code |
|---|---|---|---|
| $\Pr(A)$ | Probability of event $A$ | How likely $A$ is | — |
| $\mathbb{E}[X]$, $\text{Var}(X)$ | Expectation, variance | Long-run average; spread | `x.mean()`, `x.var()` |
| $X \sim N(\mu, \sigma^2)$ | Normal with mean $\mu$, **variance** $\sigma^2$ | Bell curve | `rng.normal(mu, sigma)` (takes the **standard deviation**) |
| $\Phi(\cdot)$, $\phi(\cdot)$ | Standard normal CDF, PDF | Cumulative and density functions | `norm.cdf`, `norm.pdf` |
| $\varepsilon_t$ | Innovation / shock at time $t$ | The unpredictable part | `eps` |
| $\sigma_\varepsilon$ | Standard deviation of the innovation | Typical shock size | `sigma_e` |
| $\rho$ | AR(1) persistence, $z' = \rho z + \varepsilon$ | How much of today carries into tomorrow | `rho` |
| $\pi$ (distribution) | Stationary distribution of a Markov chain | Long-run occupancy of each state | `pi_stat` |
| $P$, $P_{ij}$ | Markov transition matrix; $\Pr(s'=j \mid s=i)$ | Rows = today, columns = tomorrow; rows sum to 1 | `P` |

---

## 4. Dynamic Programming & Macro

| Symbol | Definition | Plain English | Code |
|---|---|---|---|
| $\beta$ | Discount factor, $\beta \in (0,1)$ | How much the future is worth today | `beta` |
| $V(s)$ | Value function | Best attainable lifetime payoff from state $s$ | `V` |
| $T$ | Bellman operator, $TV = \max_a \{R + \beta \mathbb{E} V\}$ | One round of "optimize given tomorrow's guess" | `bellman_operator` |
| $\pi(s)$ (policy) | Policy function | The optimal action in each state | `policy` |
| $R(s,a)$ | Reward / period payoff | Immediate payoff of action $a$ in state $s$ | `R` |
| $Q(s,a,s')$ | Transition kernel | Probability of landing in $s'$ | `Q` |
| $k_t$ | Capital stock (predetermined state) | Machines available for production | `k` |
| $c_t$ | Consumption (control/jump variable) | What households consume | `c` |
| $a_t$ / $z_t$ | (Log) TFP / productivity state | The economy's technology level | `a`, `z` |
| $\alpha$ | Capital share in $Y = A K^\alpha L^{1-\alpha}$ | Output elasticity of capital ($\approx 0.33$) | `alpha` |
| $\delta$ | Depreciation rate | Fraction of capital that wears out per period | `delta` |
| $\sigma$ (preferences) | CRRA / inverse IES | Curvature of utility, appetite for smoothing | `sigma` |
| $u(c)$ | Period utility | Happiness from consumption now | `u` |
| $\lambda_i$ | Generalized eigenvalue of the linearized system | Stability of a direction: $\lvert\lambda\rvert<1$ decays | `eigenvalues` |

**Interest rate convention:** $r$ is the *net real* rate, $R = 1 + r$ the
*gross* rate, and $i$ the *net nominal* rate. Code uses `r`, `R_gross`,
`i_nom` respectively.

**Linear RE models** (Klein/QZ solver): the system is
$AA\,\mathbb{E}_t[x_{t+1}] = BB\,x_t$ with $x = [\,\text{states};\,\text{jumps}\,]$;
the solution is a policy $u_t = P k_t$ and transition $k_{t+1} = M k_t$
(code: `Policy`, `Transition` in `scripts/macro_utils.py`).

---

## 5. Econometrics

| Symbol | Definition | Plain English | Code |
|---|---|---|---|
| $y$, $X$ | Outcome vector, regressor matrix | What we explain; what we explain it with | `y`, `X` |
| $\hat{\beta}_{OLS} = (X^\top X)^{-1} X^\top y$ | OLS estimator | Best linear fit coefficients | `beta_hat` |
| $u_i$ / $e_i$ | Population error / sample residual | Unobserved noise / leftover fit error | `resid` |
| $\sigma^2$ | Error variance | Spread of the noise | `sigma2` |
| $\mathcal{L}(\theta)$, $\ell(\theta)$ | Likelihood, log-likelihood | Plausibility of parameters given data | `log_lik` |
| $Y_i(1), Y_i(0)$ | Potential outcomes | Outcome with vs. without treatment | `y1`, `y0` |
| $\tau$ / ATE | Average treatment effect $\mathbb{E}[Y(1)-Y(0)]$ | Causal effect on average | `tau`, `ate` |
| $D_i$ | Treatment indicator | 1 if treated, 0 if not | `d` |
| $Z_i$ | Instrumental variable | Shifts treatment, untainted by confounding | `z` |

---

## 6. Time Series & Finance

| Symbol | Definition | Plain English | Code |
|---|---|---|---|
| $L$ | Lag operator, $L x_t = x_{t-1}$ | Shift a series back one period | `x.shift(1)` |
| $\phi_i$, $\theta_j$ | AR and MA coefficients | Memory of past values; of past shocks | `ar_params`, `ma_params` |
| $\Sigma$ | Covariance matrix (returns, shocks) | Joint variability | `Sigma` |
| $w$ | Portfolio weight vector, $\sum_i w_i = 1$ | Fraction of wealth in each asset | `w` |
| $\mu$ | Expected-return vector | Average payoff of each asset | `mu` |
| $S_t$ | Underlying asset price | The stock price today | `S` |
| $K$, $T$ (options) | Strike price, maturity | Contract terms of an option | `K`, `T` |
| $W_t$ | Brownian motion / Wiener process | Continuous-time random walk | `W` |
| $h_t$ / $\sigma_t^2$ | Conditional variance (GARCH) | Today's volatility given the past | `h` |

---

## 7. Machine Learning

| Symbol | Definition | Plain English | Code |
|---|---|---|---|
| $\theta$ / $w, b$ | Model parameters / weights and bias | The knobs training adjusts | `theta`, `w`, `b` |
| $\mathcal{L}(\theta)$ | Loss function | What training minimizes | `loss` |
| $\eta$ | Learning rate | Step size of gradient descent | `lr` |
| $\hat{y}$ | Model prediction | The model's guess for $y$ | `y_pred` |
| $\sigma(\cdot)$ (activation) | Sigmoid / activation function | Nonlinearity between layers | `activation` |
| $\lambda$ (regularization) | Penalty strength (ridge/lasso) | How hard complexity is punished | `lam` (never `lambda`, a Python keyword) |

---

## 8. Symbol Collisions to Watch

Some symbols are standard in *two* fields at once. The course keeps both
standards and disambiguates by context, stating the intended meaning at
first use in each notebook:

| Symbol | Meaning A | Meaning B |
|---|---|---|
| $\beta$ | Discount factor (macro/DP) | Regression coefficient (econometrics) |
| $\sigma$ | CRRA / inverse IES (preferences) | Standard deviation (statistics); activation (ML) |
| $\pi$ | Policy function (DP) | Inflation (macro); stationary distribution (Markov); 3.14159… |
| $\lambda$ | Eigenvalue (linear algebra) | Regularization strength (ML); Lagrange multiplier (optimization) |
| $\theta$ | ML parameter vector | MA coefficient (time series); generic structural parameter |
| $T$ | Bellman operator (DP) | Sample size / horizon (econometrics); maturity (finance) |

> **Rule of thumb:** if a notebook mixes two fields (e.g., *ML for Macro
> Forecasting*), it must rename one of the colliding symbols and say so.
