"""Create the non-duplicative frontier lectures from the reconciled curriculum plan.

The 2026 plans proposed eight frontier directions. Two already have substantial
homes in the repository (HANK and advanced deep RL/PPO), so this script enriches
those canonical notebooks instead of creating duplicate lectures. Six genuinely
missing subjects are added as compact, executable advanced lectures.
"""
from __future__ import annotations

from pathlib import Path

import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook

ROOT = Path(__file__).resolve().parents[1]


def write_notebook(rel: str, cells: list, *, force: bool = False) -> bool:
    path = ROOT / rel
    if path.exists() and not force:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    nb = new_notebook(cells=cells)
    nb.metadata["kernelspec"] = {
        "display_name": "Python 3",
        "language": "python",
        "name": "python3",
    }
    nb.metadata["language_info"] = {"name": "python", "version": "3.11"}
    nbformat.write(nb, path)
    return True


def common_setup(extra: str = ""):
    src = """import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import Markdown, display

rng = np.random.default_rng(42)
plt.style.use("seaborn-v0_8-whitegrid")
plt.rcParams.update({"font.size": 12, "figure.figsize": (10, 6), "figure.dpi": 120})
np.set_printoptions(suppress=True, precision=5, linewidth=120)
"""
    if extra:
        src += "\n" + extra.strip() + "\n"
    return new_code_cell(src)


def create_hjb() -> bool:
    cells = [
        new_markdown_cell(r"""# 08 Continuous-Time Macroeconomics: HJB and Fokker-Planck Methods

## The Lens: Solving Household Behavior When Time Becomes Continuous

A discrete Bellman equation asks what an agent does between dates. Continuous time instead asks what infinitesimal drift is optimal at every state. This change is computationally valuable because the Hamilton-Jacobi-Bellman (HJB) equation becomes a differential equation and the stationary distribution is characterized by its adjoint Kolmogorov Forward (Fokker-Planck) equation. Together they form the workhorse numerical system behind modern continuous-time heterogeneous-agent macroeconomics.

The economic question is not simply whether we can solve a partial differential equation. It is whether the numerical discretization respects the direction of optimal asset drift, the borrowing boundary, probability conservation, and market-clearing objects. A centered difference can look smooth while violating monotonicity; an upwind scheme chooses the derivative implied by the direction of savings or dissavings. We therefore solve a two-income-state consumption-saving problem with a monotone upwind finite-difference method, verify the HJB residual, recover the invariant distribution from the generator's adjoint, and report aggregate assets.

### Learning Objectives
- **Derive** the stationary continuous-time HJB equation from the dynamic programming principle.
- **Implement** an upwind finite-difference discretization with explicit borrowing and upper-grid boundaries.
- **Recover** the stationary density from the transpose of the Markov generator.
- **Diagnose** a solution using HJB residuals, mass conservation, and boundary drift checks.

### Prerequisites
- `06_Heterogeneous_Agent_Models.ipynb`: incomplete-markets household problem and stationary equilibrium.
- `../03-Economic-Modeling/01_Dynamic_Programming.ipynb`: Bellman equations and contraction logic.
- `../02-Numerical-Methods/08_Differential_Equations.ipynb`: finite differences and stability.
"""),
        new_markdown_cell(r"""## Table of Contents

1. [Continuous-time Bellman equation](#continuous-time-bellman-equation)
2. [Upwind discretization](#upwind-discretization)
3. [Executable HJB solver](#executable-hjb-solver)
4. [Stationary Fokker-Planck distribution](#stationary-fokker-planck-distribution)
5. [Diagnostics and economic interpretation](#diagnostics-and-economic-interpretation)
6. [Exercises](#exercises)
"""),
        common_setup("""from scipy.sparse import bmat, diags, eye
from scipy.sparse.linalg import spsolve"""),
        new_markdown_cell(r"""<a id="continuous-time-bellman-equation"></a>
## 1. Continuous-Time Bellman Equation

Let assets evolve according to

$$da_t = [y(z_t) + r a_t - c_t]dt,$$

where the income state $z_t\in\{1,2\}$ jumps according to a continuous-time Markov chain with rates $\lambda_{12}$ and $\lambda_{21}$. With CRRA flow utility $u(c)=c^{1-\gamma}/(1-\gamma)$ and discount rate $\rho$, the stationary HJB equation is

$$\rho V_j(a)=\max_{c>0}\left\{u(c)+V_j'(a)[y_j+ra-c]+\lambda_{jk}[V_k(a)-V_j(a)]\right\}.$$

The first-order condition is $u'(c)=V_j'(a)$, hence

$$c_j(a)=\left[V_j'(a)\right]^{-1/\gamma}.$$

The derivative must be chosen consistently with the drift $s_j(a)=y_j+ra-c_j(a)$. If $s>0$, information should arrive from the lower asset node; if $s<0$, it should arrive from the upper node. This is the economic content of the **upwind** rule.
"""),
        new_markdown_cell(r"""<a id="upwind-discretization"></a>
## 2. Upwind Discretization

On a grid $a_0<\cdots<a_{N-1}$ with spacing $\Delta a$, define forward and backward derivatives

$$D^+V_i=\frac{V_{i+1}-V_i}{\Delta a},\qquad D^-V_i=\frac{V_i-V_{i-1}}{\Delta a}.$$

Candidate consumptions and drifts are $c^+=(D^+V)^{-1/\gamma}$, $s^+=y+ra-c^+$ and analogously for the backward derivative. We choose $D^+V$ where $s^+>0$, $D^-V$ where $s^-<0$, and the steady-state marginal utility $u'(y+ra)$ when neither direction is active. The resulting drift coefficients form a sparse Markov generator $A(V)$.

A false-transient step solves

$$\left[(\rho+\Delta^{-1})I-A(V^n)\right]V^{n+1}=u(c^n)+\Delta^{-1}V^n.$$

This implicit step is much more stable than naively marching the nonlinear HJB forward.
"""),
        new_markdown_cell(r"""<a id="executable-hjb-solver"></a>
## 3. Executable HJB Solver

The implementation below follows the discrete generator directly. The high-asset boundary is intentionally far from the mass of the stationary distribution; the low-asset boundary enforces the borrowing constraint by replacing the outward derivative with marginal utility from consuming cash-on-hand.
"""),
        new_code_cell(r'''def solve_two_state_hjb(
    n_assets=240,
    a_min=0.0,
    a_max=30.0,
    income=(0.8, 1.2),
    switch_rates=(0.15, 0.10),
    r=0.03,
    rho=0.05,
    gamma=2.0,
    false_step=1000.0,
    tol=1e-8,
    max_iter=500,
):
    """Solve a stationary two-income-state consumption-saving HJB."""
    if not (0 < r < rho < 1):
        raise ValueError("For this calibration require 0 < r < rho < 1.")
    if gamma <= 0 or n_assets < 20 or a_max <= a_min:
        raise ValueError("Invalid curvature or asset grid.")

    a = np.linspace(a_min, a_max, n_assets)
    da = a[1] - a[0]
    y = np.asarray(income, dtype=float)
    lam12, lam21 = map(float, switch_rates)
    if np.any(y <= 0) or min(lam12, lam21) <= 0:
        raise ValueError("Income and switching rates must be positive.")

    cash = y[:, None] + r * a[None, :]
    utility = lambda c: np.where(gamma == 1.0, np.log(c), c ** (1 - gamma) / (1 - gamma))
    marginal = lambda c: c ** (-gamma)

    # Consuming cash-on-hand forever is a stable initial value guess.
    V = utility(cash) / rho
    generator = None
    consumption = None

    for iteration in range(1, max_iter + 1):
        d_forward = np.empty_like(V)
        d_backward = np.empty_like(V)
        d_forward[:, :-1] = (V[:, 1:] - V[:, :-1]) / da
        d_backward[:, 1:] = (V[:, 1:] - V[:, :-1]) / da
        d_forward[:, -1] = marginal(cash[:, -1])
        d_backward[:, 0] = marginal(cash[:, 0])

        d_forward = np.maximum(d_forward, 1e-12)
        d_backward = np.maximum(d_backward, 1e-12)
        c_forward = d_forward ** (-1.0 / gamma)
        c_backward = d_backward ** (-1.0 / gamma)
        drift_forward = cash - c_forward
        drift_backward = cash - c_backward

        use_forward = drift_forward > 0
        use_backward = drift_backward < 0
        # If both one-sided candidates point inward, prefer the one with larger |drift|.
        conflict = use_forward & use_backward
        choose_forward = use_forward & (~conflict | (np.abs(drift_forward) >= np.abs(drift_backward)))
        choose_backward = use_backward & ~choose_forward
        d_steady = marginal(cash)
        derivative = np.where(choose_forward, d_forward, np.where(choose_backward, d_backward, d_steady))
        consumption = np.maximum(derivative, 1e-12) ** (-1.0 / gamma)
        drift = cash - consumption

        # Prevent probability flow out of the artificial grid.
        drift[:, 0] = np.maximum(drift[:, 0], 0.0)
        drift[:, -1] = np.minimum(drift[:, -1], 0.0)

        blocks = []
        for j, lam in enumerate((lam12, lam21)):
            up = np.maximum(drift[j], 0.0) / da
            down = np.maximum(-drift[j], 0.0) / da
            main = -(up + down + lam)
            blocks.append(diags([down[1:], main, up[:-1]], [-1, 0, 1], shape=(n_assets, n_assets), format="csr"))
        switch12 = lam12 * eye(n_assets, format="csr")
        switch21 = lam21 * eye(n_assets, format="csr")
        generator = bmat([[blocks[0], switch12], [switch21, blocks[1]]], format="csr")

        lhs = (rho + 1.0 / false_step) * eye(2 * n_assets, format="csr") - generator
        rhs = utility(consumption).reshape(-1) + V.reshape(-1) / false_step
        V_new = spsolve(lhs, rhs).reshape(2, n_assets)
        error = float(np.max(np.abs(V_new - V)))
        V = V_new
        if error < tol:
            break
    else:
        raise RuntimeError(f"HJB did not converge after {max_iter} iterations; final error={error:.3e}")

    # Residual using the final generator and consumption.
    residual = rho * V.reshape(-1) - (utility(consumption).reshape(-1) + generator @ V.reshape(-1))
    return {
        "assets": a,
        "value": V,
        "consumption": consumption,
        "generator": generator,
        "iterations": iteration,
        "value_change": error,
        "max_hjb_residual": float(np.max(np.abs(residual))),
    }

hjb = solve_two_state_hjb()
print({k: hjb[k] for k in ("iterations", "value_change", "max_hjb_residual")})
assert hjb["max_hjb_residual"] < 1e-4
'''),
        new_code_cell('''fig, ax = plt.subplots()
for j, label in enumerate(["low income", "high income"]):
    ax.plot(hjb["assets"], hjb["consumption"][j], label=label)
ax.plot(hjb["assets"], 0.8 + 0.03 * hjb["assets"], "--", alpha=0.6, label="low-state cash-on-hand")
ax.set(xlabel="assets", ylabel="consumption", title="Optimal consumption policies from the HJB")
ax.legend()
plt.show()
'''),
        new_markdown_cell(r"""<a id="stationary-fokker-planck-distribution"></a>
## 4. Stationary Fokker-Planck Distribution

The same generator that moves the value function moves probability mass in the opposite (adjoint) direction. If $g$ stacks probability mass over income and asset states, a stationary distribution satisfies

$$A^\top g=0,\qquad \mathbf{1}^\top g=1.$$

This duality is a powerful correctness check: if the HJB and Kolmogorov equations are discretized inconsistently, the implied distribution often leaks mass or places probability at the artificial grid boundary.
"""),
        new_code_cell('''def stationary_distribution(generator, da):
    """Solve A.T g = 0 with one row replaced by the normalization condition."""
    matrix = generator.T.tolil(copy=True)
    rhs = np.zeros(matrix.shape[0])
    matrix[0, :] = np.ones(matrix.shape[1])
    rhs[0] = 1.0
    mass = spsolve(matrix.tocsr(), rhs)
    mass = np.maximum(mass, 0.0)
    mass /= mass.sum()
    density = mass / da
    return mass, density

da = hjb["assets"][1] - hjb["assets"][0]
mass, density = stationary_distribution(hjb["generator"], da)
n = len(hjb["assets"])
aggregate_assets = float(np.dot(mass[:n] + mass[n:], hjb["assets"]))
boundary_mass = float((mass[0] + mass[n] + mass[n-1] + mass[-1]))
print(f"aggregate assets = {aggregate_assets:.4f}")
print(f"total mass = {mass.sum():.12f}; boundary mass = {boundary_mass:.4%}")
assert np.isclose(mass.sum(), 1.0, atol=1e-10)
assert np.all(mass >= -1e-12)
'''),
        new_code_cell('''fig, ax = plt.subplots()
ax.plot(hjb["assets"], density[:n], label="low income")
ax.plot(hjb["assets"], density[n:], label="high income")
ax.set(xlabel="assets", ylabel="stationary density", title="Invariant asset distribution")
ax.legend()
plt.show()
'''),
        new_markdown_cell(r"""<a id="diagnostics-and-economic-interpretation"></a>
## 5. Diagnostics and Economic Interpretation

Three checks should accompany every reported equilibrium:

1. **HJB residual:** a small nonlinear residual verifies the discretized optimality equation, not only successive-iteration convergence.
2. **Probability conservation:** stationary mass must be nonnegative and sum to one.
3. **Boundary mass:** substantial probability on the upper grid boundary is evidence that `a_max` is too low and the solution should be recomputed on a wider grid.

A full stationary general equilibrium would add an outer root finder for the interest rate so aggregate household assets equal the economy's asset supply. That extra equilibrium loop is intentionally separated from the household solver here so each numerical layer can be validated independently.
"""),
        new_markdown_cell(r"""## Exercises

**1. Upwind logic (Conceptual):** Derive why positive asset drift requires a backward-looking value derivative and negative drift requires a forward-looking derivative. What numerical pathology can a centered derivative create near a kink?

**2. Grid adequacy (Applied):** Re-solve the model with `a_max` equal to 10, 20, 30, and 50. Record aggregate assets, maximum HJB residual, and boundary mass. Identify the smallest grid that produces a stable aggregate statistic.

**3. Market clearing (Challenge):** Wrap `solve_two_state_hjb` in a scalar root finder for `r`. Specify an exogenous asset supply, solve for the clearing rate, and verify that both the household residual and market-clearing residual meet stated tolerances.
"""),
        new_markdown_cell(r"""## Summary & Key Takeaways

- Continuous-time household optimization is summarized by an HJB equation; distribution dynamics use the adjoint Kolmogorov equation.
- Upwinding is an economic as well as numerical restriction because the derivative must follow the direction of optimal drift.
- False-transient implicit steps produce a stable sparse linear solve inside the nonlinear fixed point.
- HJB residuals, mass conservation, and boundary mass provide independent evidence that the computed solution is usable.
"""),
        new_markdown_cell(r"""## References & Further Reading

- Achdou, Y., Han, J., Lasry, J.-M., Lions, P.-L. & Moll, B. (2022). Income and wealth distribution in macroeconomics: A continuous-time approach. *Review of Economic Studies*, 89(1), 45–86.
- Moll, B. Continuous-time heterogeneous-agent methods and numerical notes.
- Aiyagari, S. R. (1994). Uninsured idiosyncratic risk and aggregate saving. *Quarterly Journal of Economics*, 109(3), 659–684.
"""),
    ]
    return write_notebook("04-Macro-Models/08_Continuous_Time_Macro_HJB.ipynb", cells)


def create_blp() -> bool:
    cells = [
        new_markdown_cell(r"""# 07 BLP Demand Estimation: Random-Coefficients Logit and Share Inversion

## The Lens: Recovering Willingness to Pay from Market Shares

Product-level market shares compress millions of household choices into a few equilibrium outcomes. Structural demand estimation asks whether those outcomes can be inverted to recover latent mean utilities and, eventually, substitution patterns and willingness to pay. The Berry-Levinsohn-Pakes (BLP) framework extends multinomial logit by allowing heterogeneous tastes, which prevents every product from being an equally good substitute after conditioning on mean utility.

The computational core is a fixed point. Observed shares are held fixed while the mean utility vector $\delta$ is updated until simulated shares match them. That contraction is only one layer of the estimator: a production BLP analysis also instruments endogenous prices and searches over nonlinear taste parameters in an outer GMM objective. This notebook isolates the inner inversion, simulates data where the truth is known, verifies the share residual, and makes the nested structure explicit so the econometric identification problem is never confused with numerical convergence.

### Learning Objectives
- **Derive** the logit share equation and Berry share-inversion contraction.
- **Simulate** random-coefficient market shares with common consumer draws.
- **Recover** mean utilities by fixed-point iteration and diagnose convergence.
- **Distinguish** the inner contraction from the outer IV/GMM identification problem.

### Prerequisites
- `04_Discrete_Choice_Models.ipynb`: logit choice probabilities and random utility.
- `../03-Economic-Modeling/07_Structural_Estimation.ipynb`: structural estimation and nested fixed points.
- `../06-Econometrics/05_Instrumental_Variables.ipynb`: price endogeneity and instruments.
"""),
        new_markdown_cell(r"""## Table of Contents

1. [From random utility to market shares](#random-utility)
2. [Berry's contraction](#berry-contraction)
3. [Synthetic random-coefficients market](#synthetic-market)
4. [Inversion diagnostics](#inversion-diagnostics)
5. [From inversion to BLP GMM](#blp-gmm)
6. [Exercises](#exercises)
"""),
        common_setup("from scipy.special import logsumexp"),
        new_markdown_cell(r"""<a id="random-utility"></a>
## 1. From Random Utility to Market Shares

Consumer $i$ in market $t$ chooses product $j$ when

$$u_{ijt}=\delta_{jt}+\sigma x_{jt}\nu_i+\varepsilon_{ijt}$$

is maximal, where $\varepsilon$ is type-I extreme value and $\nu_i\sim N(0,1)$ creates taste heterogeneity. Conditional on $\nu_i$, the logit probability is

$$P_{ijt}=\frac{\exp(\delta_{jt}+\sigma x_{jt}\nu_i)}{1+\sum_{k=1}^J\exp(\delta_{kt}+\sigma x_{kt}\nu_i)}.$$

Integrating over $\nu$ gives simulated market shares. The outside good has normalized mean utility zero, so its share disciplines the absolute level of $\delta$.
"""),
        new_markdown_cell(r"""<a id="berry-contraction"></a>
## 2. Berry's Contraction

For a trial mean utility vector $\delta^h$, simulate shares $s(\delta^h;\sigma)$. The BLP inversion updates

$$\delta^{h+1}_{jt}=\delta^h_{jt}+\log s^{obs}_{jt}-\log s_{jt}(\delta^h;\sigma).$$

At a fixed point, simulated and observed shares coincide. Numerically, monitor the **share residual** as well as the update norm. The contraction solves for $\delta$ conditional on nonlinear taste parameters; it does not solve the endogeneity of price.
"""),
        new_markdown_cell(r"""<a id="synthetic-market"></a>
## 3. Synthetic Random-Coefficients Market

We generate many independent markets with known mean utilities and a common set of simulation draws. Reusing draws makes the contraction deterministic and prevents Monte Carlo noise from masquerading as non-convergence.
"""),
        new_code_cell('''def simulated_shares(delta, x_random, sigma, draws):
    """Simulate BLP inside-good shares for one market."""
    utilities = delta[:, None] + sigma * x_random[:, None] * draws[None, :]
    # Include outside-good utility 0 with a stable log denominator.
    log_denom = logsumexp(np.vstack([np.zeros(draws.size), utilities]), axis=0)
    probabilities = np.exp(utilities - log_denom)
    return probabilities.mean(axis=1)


def berry_inversion(observed, x_random, sigma, draws, tol=1e-12, max_iter=10_000):
    """Recover mean utilities from observed shares by Berry contraction."""
    observed = np.asarray(observed, dtype=float)
    if np.any(observed <= 0) or observed.sum() >= 1:
        raise ValueError("Inside shares must be positive and sum to less than one.")
    outside = 1.0 - observed.sum()
    delta = np.log(observed) - np.log(outside)  # simple-logit starting value
    for iteration in range(1, max_iter + 1):
        predicted = np.clip(simulated_shares(delta, x_random, sigma, draws), 1e-300, 1.0)
        delta_new = delta + np.log(observed) - np.log(predicted)
        update = float(np.max(np.abs(delta_new - delta)))
        delta = delta_new
        if update < tol:
            break
    else:
        raise RuntimeError(f"BLP contraction did not converge; update={update:.3e}")
    predicted = simulated_shares(delta, x_random, sigma, draws)
    return delta, iteration, update, float(np.max(np.abs(predicted - observed)))

n_markets, n_products, n_draws = 20, 5, 6_000
beta0, beta_x, alpha_price, sigma_true = -1.0, 1.2, 1.0, 0.8
draws = rng.normal(size=n_draws)
records = []
for market in range(n_markets):
    quality = rng.normal(size=n_products)
    price = 2.0 + 0.5 * quality + rng.normal(scale=0.35, size=n_products)
    xi = rng.normal(scale=0.15, size=n_products)
    delta_true = beta0 + beta_x * quality - alpha_price * price + xi
    shares = simulated_shares(delta_true, quality, sigma_true, draws)
    for j in range(n_products):
        records.append((market, j, quality[j], price[j], delta_true[j], shares[j]))

market_data = pd.DataFrame(records, columns=["market", "product", "quality", "price", "delta_true", "share"])
market_data.head()
'''),
        new_markdown_cell(r"""<a id="inversion-diagnostics"></a>
## 4. Inversion Diagnostics

Because the data were generated by the same model used in inversion, recovered mean utilities should match the latent truth up to numerical tolerance. In empirical work the truth is unavailable, so the observable diagnostic is the maximum share discrepancy together with fixed-point stability under tighter tolerances and more simulation draws.
"""),
        new_code_cell('''results = []
for market, group in market_data.groupby("market", sort=True):
    recovered, iterations, update, share_error = berry_inversion(
        group["share"].to_numpy(),
        group["quality"].to_numpy(),
        sigma_true,
        draws,
    )
    delta_error = float(np.max(np.abs(recovered - group["delta_true"].to_numpy())))
    results.append((market, iterations, update, share_error, delta_error))

diagnostics = pd.DataFrame(results, columns=["market", "iterations", "update", "share_error", "delta_error"])
display(diagnostics.describe().T)
assert diagnostics["share_error"].max() < 1e-9
assert diagnostics["delta_error"].max() < 1e-8
'''),
        new_code_cell('''sample = market_data.query("market == 0").copy()
sample["delta_recovered"], *_ = berry_inversion(sample["share"], sample["quality"], sigma_true, draws)
fig, ax = plt.subplots()
ax.scatter(sample["delta_true"], sample["delta_recovered"], s=70)
lo, hi = sample[["delta_true", "delta_recovered"]].to_numpy().min(), sample[["delta_true", "delta_recovered"]].to_numpy().max()
ax.plot([lo, hi], [lo, hi], "--", label="45° line")
ax.set(xlabel="true mean utility", ylabel="recovered mean utility", title="Berry inversion recovers the synthetic truth")
ax.legend()
plt.show()
'''),
        new_markdown_cell(r"""<a id="blp-gmm"></a>
## 5. From Share Inversion to BLP GMM

The full BLP estimator nests the contraction inside an outer objective. If prices are endogenous, mean utility is decomposed as

$$\delta_{jt}=x_{jt}'\beta-\alpha p_{jt}+\xi_{jt},$$

and instruments $Z$ satisfy $E[Z'\xi]=0$. For each candidate nonlinear parameter $\sigma$:

1. invert shares to obtain $\delta(\sigma)$;
2. estimate linear parameters $(\beta,\alpha)$ by IV/GMM;
3. recover $\xi(\sigma)$;
4. evaluate

$$Q(\sigma)=g(\sigma)'Wg(\sigma),\qquad g(\sigma)=\frac{1}{N}Z'\xi(\sigma);$$

5. optimize over $\sigma$ and then compute robust uncertainty.

Keeping the contraction and IV/GMM layers separate makes failures diagnosable: share mismatch is numerical; invalid instruments are an identification failure.
"""),
        new_markdown_cell(r"""## Exercises

**1. IIA versus random coefficients (Conceptual):** Explain why the simple logit model implies proportional substitution and how a random coefficient on product quality changes cross-price substitution patterns.

**2. Numerical inversion (Applied):** Repeat the experiment for `sigma` in `{0, 0.4, 0.8, 1.5}`. Record iteration counts and verify share errors. Explain why a harder substitution pattern can change contraction speed.

**3. Endogenous prices (Challenge):** Generate price using an unobserved cost shock correlated with `xi`, add an excluded cost shifter as an instrument, and implement the outer IV/GMM step. Compare OLS and IV estimates of the price coefficient.
"""),
        new_markdown_cell(r"""## Summary & Key Takeaways

- Random coefficients relax the simple-logit substitution pattern by allowing heterogeneous tastes.
- Berry's contraction recovers mean utilities by matching observed and simulated shares.
- Share inversion is a numerical fixed point; price endogeneity is a separate econometric identification problem.
- Reusing simulation draws and reporting share residuals make the inner loop reproducible and auditable.
"""),
        new_markdown_cell(r"""## References & Further Reading

- Berry, S. (1994). Estimating discrete-choice models of product differentiation. *RAND Journal of Economics*, 25(2), 242–262.
- Berry, S., Levinsohn, J. & Pakes, A. (1995). Automobile prices in market equilibrium. *Econometrica*, 63(4), 841–890.
- Nevo, A. (2000). A practitioner's guide to estimation of random-coefficients logit models of demand. *Journal of Economics & Management Strategy*, 9(4), 513–548.
"""),
    ]
    return write_notebook("05-Micro-Models/07_BLP_Demand_Estimation.ipynb", cells)


def create_sdid() -> bool:
    cells = [
        new_markdown_cell(r"""# 13 Modern Causal Frontiers: Synthetic Difference-in-Differences and Matrix Completion

## The Lens: Building a Credible Counterfactual When Parallel Trends Are Too Crude

Difference-in-differences (DiD) is persuasive when untreated units reveal the path the treated units would have followed. Synthetic control is persuasive when a weighted combination of controls reproduces the treated pre-period. Synthetic difference-in-differences (SDID) combines those ideas: it chooses unit weights and time weights to improve pre-treatment balance, then estimates a DiD-style contrast that retains an intercept correction.

This notebook focuses on the mechanism rather than presenting a package call as proof. We construct a latent-factor panel with known treatment effect, solve constrained ridge problems for unit and time weights, and compare classical DiD with an SDID-style estimator. The exercise is intentionally transparent: the implementation is an educational reconstruction of the weighting logic, not a substitute for the complete inference machinery in production SDID libraries. We close with matrix completion, where untreated potential outcomes are modeled as a low-rank panel, and with the diagnostics that determine whether either method has enough pre-treatment information to be credible.

### Learning Objectives
- **Explain** how SDID blends synthetic-control balancing with DiD intercept correction.
- **Solve** simplex-constrained ridge problems for unit and time weights.
- **Compare** estimators in a panel where the true effect is known.
- **Relate** SDID to low-rank matrix completion and modern sensitivity analysis.

### Prerequisites
- `08_Difference_in_Differences.ipynb`: potential-outcomes DiD and staggered adoption.
- `07_Synthetic_Control_Methods.ipynb`: synthetic-control weights and placebo logic.
- `../02-Numerical-Methods/05_Optimization.ipynb`: constrained optimization.
"""),
        new_markdown_cell(r"""## Table of Contents

1. [The SDID estimand](#sdid-estimand)
2. [Unit and time balancing](#unit-time-balancing)
3. [Synthetic panel experiment](#synthetic-panel)
4. [Estimator comparison](#estimator-comparison)
5. [Matrix completion and sensitivity](#matrix-completion)
6. [Exercises](#exercises)
"""),
        common_setup("from scipy.optimize import minimize"),
        new_markdown_cell(r"""<a id="sdid-estimand"></a>
## 1. The SDID Estimand

Let $Y_{it}$ be a balanced panel, with treated units observed after time $T_0$. Classical DiD gives equal weight to control units and pre-periods. SDID instead estimates nonnegative simplex weights $\omega_i$ for controls and $\lambda_t$ for pre-periods, then forms an intercept-corrected contrast. A transparent two-group version is

$$\hat\tau = \left(\bar Y^{tr}_{post}-\omega'\bar Y^{co}_{post}\right)
-\left(\lambda'\bar Y^{tr}_{pre}-\omega'Y^{co}_{pre}\lambda\right).$$

If uniform weights are used, this collapses toward ordinary DiD. If pre-treatment trajectories are highly informative, the learned weights make the counterfactual more local to the treated path.
"""),
        new_markdown_cell(r"""<a id="unit-time-balancing"></a>
## 2. Unit and Time Balancing

We use ridge-regularized simplex problems. Unit weights solve

$$\min_{\omega\ge 0,\;\mathbf{1}'\omega=1}
\|Y_{co,pre}'\omega-\bar Y_{tr,pre}\|_2^2+\zeta_\omega\|\omega\|_2^2.$$

Time weights reverse the regression: pre-period columns are combined to reproduce each control unit's average post-period outcome,

$$\min_{\lambda\ge0,\;\mathbf{1}'\lambda=1}
\|Y_{co,pre}\lambda-\bar Y_{co,post}\|_2^2+\zeta_\lambda\|\lambda\|_2^2.$$

The ridge terms prevent a near-perfect but fragile match from concentrating all weight on one unit or date.
"""),
        new_code_cell('''def simplex_ridge(A, b, ridge=1e-3):
    """Solve min ||A @ w - b||^2 + ridge*||w||^2 on the probability simplex."""
    A, b = np.asarray(A, float), np.asarray(b, float)
    n = A.shape[1]
    objective = lambda w: float(np.sum((A @ w - b) ** 2) + ridge * np.sum(w**2))
    gradient = lambda w: 2 * (A.T @ (A @ w - b) + ridge * w)
    result = minimize(
        objective,
        np.full(n, 1 / n),
        jac=gradient,
        bounds=[(0.0, 1.0)] * n,
        constraints={"type": "eq", "fun": lambda w: np.sum(w) - 1.0, "jac": lambda w: np.ones(n)},
        method="SLSQP",
        options={"ftol": 1e-12, "maxiter": 2_000},
    )
    if not result.success:
        raise RuntimeError(result.message)
    return result.x
'''),
        new_markdown_cell(r"""<a id="synthetic-panel"></a>
## 3. Synthetic Panel Experiment

The untreated outcome contains unit effects, time effects, and a latent factor whose loading differs across units. Treated units are selected partly on that loading, so equal-weight controls have imperfect pre-trends. The true treatment effect is known and constant after adoption.
"""),
        new_code_cell('''n_units, n_periods, n_treated, t0 = 40, 24, 6, 16
true_tau = 2.0
time = np.arange(n_periods)
unit_fe = rng.normal(scale=1.0, size=n_units)
loadings = rng.normal(size=n_units)
factor = 0.08 * time + 0.8 * np.sin(time / 4)
time_fe = 0.04 * time
noise = rng.normal(scale=0.25, size=(n_units, n_periods))
y0 = unit_fe[:, None] + time_fe[None, :] + loadings[:, None] * factor[None, :] + noise

treated_idx = np.argsort(loadings)[-n_treated:]
control_idx = np.setdiff1d(np.arange(n_units), treated_idx)
treated = np.zeros((n_units, n_periods), dtype=bool)
treated[np.ix_(treated_idx, np.arange(t0, n_periods))] = True
y = y0 + true_tau * treated

pre, post = np.arange(t0), np.arange(t0, n_periods)
tr_pre = y[np.ix_(treated_idx, pre)].mean(axis=0)
co_pre = y[np.ix_(control_idx, pre)]
co_post_mean = y[np.ix_(control_idx, post)].mean(axis=1)

omega = simplex_ridge(co_pre.T, tr_pre, ridge=0.05)
lambda_pre = simplex_ridge(co_pre, co_post_mean, ridge=0.05)
assert np.isclose(omega.sum(), 1.0) and np.isclose(lambda_pre.sum(), 1.0)
'''),
        new_markdown_cell(r"""<a id="estimator-comparison"></a>
## 4. Estimator Comparison

The pre-fit error is reported alongside the treatment effect. An estimator that happens to land near the truth but cannot reproduce the pre-period should not be treated as validated.
"""),
        new_code_cell('''treated_pre_mean = y[np.ix_(treated_idx, pre)].mean()
treated_post_mean = y[np.ix_(treated_idx, post)].mean()
control_pre_mean = y[np.ix_(control_idx, pre)].mean()
control_post_mean = y[np.ix_(control_idx, post)].mean()
did = (treated_post_mean - treated_pre_mean) - (control_post_mean - control_pre_mean)

tr_post = y[np.ix_(treated_idx, post)].mean(axis=0)
weighted_control_post = omega @ y[np.ix_(control_idx, post)].mean(axis=1)
weighted_treated_pre = lambda_pre @ tr_pre
weighted_control_pre = omega @ (co_pre @ lambda_pre)
sdid_style = float(tr_post.mean() - weighted_control_post - (weighted_treated_pre - weighted_control_pre))

pre_fit_uniform = float(np.sqrt(np.mean((co_pre.mean(axis=0) - tr_pre) ** 2)))
pre_fit_weighted = float(np.sqrt(np.mean((omega @ co_pre - tr_pre) ** 2)))
summary = pd.DataFrame({
    "estimate": [true_tau, did, sdid_style],
    "absolute_error": [0.0, abs(did - true_tau), abs(sdid_style - true_tau)],
}, index=["truth", "classical DiD", "SDID-style"])
display(summary)
print(f"pre-period RMSE: uniform={pre_fit_uniform:.4f}, weighted={pre_fit_weighted:.4f}")
assert pre_fit_weighted <= pre_fit_uniform + 1e-8
'''),
        new_code_cell('''fig, ax = plt.subplots()
tr_path = y[treated_idx].mean(axis=0)
co_uniform = y[control_idx].mean(axis=0)
co_weighted = omega @ y[control_idx]
ax.plot(time, tr_path, label="treated mean", lw=2.5)
ax.plot(time, co_uniform, label="uniform controls", alpha=0.8)
ax.plot(time, co_weighted, label="weighted controls", alpha=0.9)
ax.axvline(t0 - 0.5, color="black", ls="--", label="treatment begins")
ax.set(xlabel="period", ylabel="outcome", title="Pre-treatment balance and post-treatment divergence")
ax.legend()
plt.show()
'''),
        new_markdown_cell(r"""<a id="matrix-completion"></a>
## 5. Matrix Completion and Sensitivity

Synthetic weighting is one way to exploit low-dimensional structure. Matrix-completion approaches instead posit

$$Y_{it}(0)=\alpha_i+\gamma_t+L_{it}+\varepsilon_{it},$$

where $L$ is low rank and is estimated from untreated entries with nuclear-norm or factor regularization. The counterfactual is the completed treated-post block. This is most useful when many units and periods reveal stable latent factors.

Neither method repairs a design with no credible untreated information. Modern DiD work therefore complements flexible counterfactual models with **design diagnostics and sensitivity analysis**. In particular, Rambachan-Roth style analyses ask how much post-treatment deviation from extrapolated pre-trends is required to overturn a result. The right workflow separates (1) fit of untreated outcomes, (2) treatment-effect estimation, and (3) sensitivity to violations that the data cannot rule out.
"""),
        new_markdown_cell(r"""## Exercises

**1. Weight geometry (Conceptual):** Explain the roles of the simplex constraint and ridge penalty. What does a single control receiving weight one tell you about overlap and extrapolation risk?

**2. Selection strength (Applied):** Change the rule that selects treated units from random assignment to progressively stronger selection on the latent loading. Compare classical DiD and SDID-style error over at least 100 simulated panels.

**3. Low-rank counterfactual (Challenge):** Implement a rank-$k$ factor completion using only untreated observations. Choose rank using pre-treatment validation, estimate the treated-post counterfactual, and compare its bias with the weighting estimator.
"""),
        new_markdown_cell(r"""## Summary & Key Takeaways

- SDID improves on equal-weight DiD by learning both comparison-unit and pre-period weights while retaining an intercept correction.
- Weight concentration and pre-fit are diagnostics, not cosmetic outputs.
- Matrix completion attacks the same counterfactual problem through low-rank structure rather than convex weighting.
- Flexible counterfactual fitting does not eliminate the need for causal assumptions or sensitivity analysis.
"""),
        new_markdown_cell(r"""## References & Further Reading

- Arkhangelsky, D., Athey, S., Hirshberg, D. A., Imbens, G. W. & Wager, S. (2021). Synthetic difference-in-differences. *American Economic Review*, 111(12), 4088–4118.
- Athey, S., Bayati, M., Doudchenko, N., Imbens, G. & Khosravi, K. (2021). Matrix completion methods for causal panel data models. *Journal of the American Statistical Association*, 116(536), 1716–1730.
- Rambachan, A. & Roth, J. (2023). A more credible approach to parallel trends. *Review of Economic Studies*, 90(5), 2555–2591.
"""),
    ]
    return write_notebook("06-Econometrics/13_Modern_Causal_Frontiers_SDID.ipynb", cells)


def create_particle_filter() -> bool:
    cells = [
        new_markdown_cell(r"""# 07 Nonlinear Time Series and Particle Filters

## The Lens: Filtering When Gaussian Linearity Breaks

The Kalman filter is exact because linear state transitions and Gaussian shocks preserve a Gaussian filtering distribution. Many economic state-space models violate both assumptions: volatility is positive and nonlinear, regime changes are discrete, occasionally binding constraints kink policy rules, and measurement equations can be strongly non-Gaussian. Sequential Monte Carlo (SMC), usually called a particle filter in this setting, replaces a single Gaussian approximation with a weighted empirical distribution of simulated states.

The economic question is whether the hidden state can be learned from the sequence of observations without numerical collapse. A particle filter can fail even when the code runs: weights may concentrate on one particle, resampling may destroy diversity, or a likelihood may underflow to zero. This notebook therefore treats log-weight stabilization and effective sample size (ESS) as first-class diagnostics. We simulate a canonical nonlinear state-space process, implement a bootstrap filter, trigger systematic resampling adaptively, and compare the filtered-state RMSE with a naive observation-based proxy.

### Learning Objectives
- **Derive** the sequential importance-weighting recursion.
- **Implement** a numerically stable bootstrap particle filter with systematic resampling.
- **Diagnose** particle degeneracy using ESS and log-likelihood increments.
- **Connect** SMC to nonlinear DSGE, stochastic-volatility, and regime-switching applications.

### Prerequisites
- `01_Introduction_to_Time_Series.ipynb`: state-space representation and innovations.
- `../02-Numerical-Methods/02_Numerical_Preliminaries.ipynb`: log-sum-exp and floating-point stability.
- Probability distributions and Monte Carlo simulation.
"""),
        new_markdown_cell(r"""## Table of Contents

1. [Nonlinear state-space model](#nonlinear-state-space)
2. [Sequential importance sampling](#sequential-importance)
3. [Systematic resampling](#systematic-resampling)
4. [Bootstrap particle filter](#bootstrap-filter)
5. [Diagnostics](#diagnostics)
6. [Exercises](#exercises)
"""),
        common_setup("from scipy.special import logsumexp"),
        new_markdown_cell(r"""<a id="nonlinear-state-space"></a>
## 1. Nonlinear State-Space Model

We use the standard nonlinear filtering benchmark

$$x_t=\frac{x_{t-1}}{2}+\frac{25x_{t-1}}{1+x_{t-1}^2}+8\cos(1.2t)+\eta_t,$$

$$y_t=\frac{x_t^2}{20}+\varepsilon_t,$$

with Gaussian state and measurement shocks. The observation equation is many-to-one because $x$ and $-x$ imply the same conditional mean. A Gaussian linearization can therefore be seriously misleading.
"""),
        new_code_cell('''def simulate_nonlinear_state_space(n=80, state_sd=np.sqrt(10.0), obs_sd=1.0, seed=7):
    local_rng = np.random.default_rng(seed)
    x = np.zeros(n)
    y = np.zeros(n)
    x[0] = local_rng.normal(scale=np.sqrt(5.0))
    y[0] = x[0] ** 2 / 20 + local_rng.normal(scale=obs_sd)
    for t in range(1, n):
        x_prev = x[t - 1]
        mean = 0.5 * x_prev + 25 * x_prev / (1 + x_prev**2) + 8 * np.cos(1.2 * t)
        x[t] = mean + local_rng.normal(scale=state_sd)
        y[t] = x[t] ** 2 / 20 + local_rng.normal(scale=obs_sd)
    return x, y

true_state, observations = simulate_nonlinear_state_space()
'''),
        new_markdown_cell(r"""<a id="sequential-importance"></a>
## 2. Sequential Importance Sampling

For particles $x_t^{(i)}$ proposed from the transition density, bootstrap-filter weights are proportional to the observation likelihood:

$$\tilde w_t^{(i)} = w_{t-1}^{(i)}p(y_t\mid x_t^{(i)}),\qquad
w_t^{(i)}=\frac{\tilde w_t^{(i)}}{\sum_j\tilde w_t^{(j)}}.$$

Products of small likelihoods underflow quickly, so we work in log space and normalize with

$$\log\sum_i e^{a_i}=m+\log\sum_i e^{a_i-m},\qquad m=\max_i a_i.$$

The effective sample size

$$ESS_t=\frac{1}{\sum_i(w_t^{(i)})^2}$$

summarizes weight concentration. We resample only when ESS falls below a fraction of the particle count.
"""),
        new_markdown_cell(r"""<a id="systematic-resampling"></a>
## 3. Systematic Resampling

Systematic resampling uses one uniform draw and evenly spaced cumulative-probability cutoffs. It has lower Monte Carlo variance than independent multinomial resampling while remaining simple and $O(N)$.
"""),
        new_code_cell('''def systematic_resample(weights, rng):
    n = len(weights)
    positions = (rng.random() + np.arange(n)) / n
    cumulative = np.cumsum(weights)
    indices = np.searchsorted(cumulative, positions, side="right")
    return np.minimum(indices, n - 1)


def log_normal_pdf(x, mean, sd):
    z = (x - mean) / sd
    return -0.5 * z**2 - np.log(sd) - 0.5 * np.log(2 * np.pi)
'''),
        new_markdown_cell(r"""<a id="bootstrap-filter"></a>
## 4. Bootstrap Particle Filter
"""),
        new_code_cell('''def bootstrap_particle_filter(y, n_particles=4_000, state_sd=np.sqrt(10.0), obs_sd=1.0, ess_fraction=0.5, seed=99):
    pf_rng = np.random.default_rng(seed)
    particles = pf_rng.normal(scale=np.sqrt(5.0), size=n_particles)
    log_weights = np.full(n_particles, -np.log(n_particles))
    filtered = np.empty(len(y))
    ess_path = np.empty(len(y))
    loglik = 0.0

    for t, obs in enumerate(y):
        if t > 0:
            mean = 0.5 * particles + 25 * particles / (1 + particles**2) + 8 * np.cos(1.2 * t)
            particles = mean + pf_rng.normal(scale=state_sd, size=n_particles)

        observation_mean = particles**2 / 20
        log_increment = log_normal_pdf(obs, observation_mean, obs_sd)
        log_unnormalized = log_weights + log_increment
        norm = logsumexp(log_unnormalized)
        log_weights = log_unnormalized - norm
        weights = np.exp(log_weights)
        loglik += norm

        filtered[t] = np.sum(weights * particles)
        ess = 1.0 / np.sum(weights**2)
        ess_path[t] = ess
        if ess < ess_fraction * n_particles:
            indices = systematic_resample(weights, pf_rng)
            particles = particles[indices]
            log_weights.fill(-np.log(n_particles))

    return filtered, ess_path, float(loglik)

filtered_state, ess_path, particle_loglik = bootstrap_particle_filter(observations)
rmse = float(np.sqrt(np.mean((filtered_state - true_state) ** 2)))
naive_proxy = np.sqrt(np.maximum(20 * observations, 0))
naive_rmse = float(np.sqrt(np.mean((naive_proxy - np.abs(true_state)) ** 2)))
print(f"particle-filter state RMSE = {rmse:.3f}")
print(f"naive |state| proxy RMSE = {naive_rmse:.3f}")
print(f"minimum ESS = {ess_path.min():.0f}; log likelihood = {particle_loglik:.2f}")
assert np.all(np.isfinite(filtered_state)) and np.all(ess_path > 0)
'''),
        new_markdown_cell(r"""<a id="diagnostics"></a>
## 5. Diagnostics

The filtered mean can still be a poor summary of a multimodal posterior, so an applied workflow should retain particle quantiles or the full cloud when sign ambiguity matters. ESS reveals degeneracy but not model misspecification; residual or predictive checks are still required.
"""),
        new_code_cell('''fig, axes = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
axes[0].plot(true_state, label="latent state", lw=2)
axes[0].plot(filtered_state, label="particle-filter mean", alpha=0.8)
axes[0].set(ylabel="state", title="Nonlinear filtering")
axes[0].legend()
axes[1].plot(ess_path)
axes[1].axhline(0.5 * 4_000, color="black", ls="--", label="resampling threshold")
axes[1].set(xlabel="time", ylabel="ESS")
axes[1].legend()
plt.show()
'''),
        new_markdown_cell(r"""## Exercises

**1. Degeneracy (Conceptual):** Show that equal weights imply `ESS=N` and a single particle with weight one implies `ESS=1`. Explain why resampling every period can also be harmful.

**2. Particle count (Applied):** Re-run the filter with 250, 1,000, 4,000, and 16,000 particles across 20 seeds. Report RMSE, log-likelihood variability, and runtime; identify diminishing returns.

**3. Economic state-space model (Challenge):** Replace the benchmark transition with a stochastic-volatility or nonlinear DSGE state equation. Write the exact proposal and weight equations before adapting the code.
"""),
        new_markdown_cell(r"""## Summary & Key Takeaways

- Particle filters approximate nonlinear/non-Gaussian filtering distributions with weighted simulated states.
- Log-weight normalization is mandatory numerical hygiene, not an optimization trick.
- Effective sample size identifies degeneracy and supports adaptive resampling.
- Filtering accuracy and model adequacy are distinct questions; both require diagnostics.
"""),
        new_markdown_cell(r"""## References & Further Reading

- Gordon, N. J., Salmond, D. J. & Smith, A. F. M. (1993). Novel approach to nonlinear/non-Gaussian Bayesian state estimation. *IEE Proceedings F*, 140(2), 107–113.
- Doucet, A. & Johansen, A. M. (2011). A tutorial on particle filtering and smoothing. In *The Oxford Handbook of Nonlinear Filtering*.
- Herbst, E. P. & Schorfheide, F. (2015). *Bayesian Estimation of DSGE Models*. Princeton University Press.
"""),
    ]
    return write_notebook("08-Time-Series/07_Nonlinear_Time_Series_and_Particle_Filters.ipynb", cells)


def create_hawkes() -> bool:
    cells = [
        new_markdown_cell(r"""# 08 Hawkes Processes and Market Impact

## The Lens: Modeling Event Clustering Instead of Averaging It Away

High-frequency markets are event streams: orders, trades, cancellations, and quote changes arrive at irregular times. Their arrival intensity is not constant. A trade can trigger more trading, a burst of volatility can invite further activity, and feedback can produce clusters that a Poisson process cannot reproduce. A Hawkes process formalizes this self-excitation by letting every event temporarily raise future intensity.

The economic question is whether observed clustering reflects an endogenous feedback mechanism strong enough to matter for liquidity and execution. The crucial stability quantity is the branching ratio. When the expected number of descendants per event approaches one, activity becomes highly persistent and simulated paths can resemble cascades. We implement Ogata's thinning algorithm for an exponential Hawkes process, verify the stability condition, reconstruct the intensity path, and then connect event-flow risk to a separate empirical regularity: concave, approximately square-root market impact. The two objects should not be conflated—one models arrival dynamics, the other execution cost—but together they form a useful microstructure stress laboratory.

### Learning Objectives
- **Interpret** Hawkes intensity, excitation, decay, and branching ratio.
- **Implement** Ogata thinning for a stable exponential Hawkes process.
- **Reconstruct** event intensity and diagnose clustering.
- **Compare** event-flow feedback with a square-root market-impact benchmark.

### Prerequisites
- `06_High_Frequency_Data.ipynb`: market microstructure data and realized measures.
- `04_Continuous_Time_Finance.ipynb`: continuous-time stochastic processes.
- Point processes, exponential distributions, and Monte Carlo simulation.
"""),
        new_markdown_cell(r"""## Table of Contents

1. [Self-exciting point processes](#hawkes-model)
2. [Stability and branching](#stability)
3. [Ogata thinning](#ogata)
4. [Intensity diagnostics](#intensity-diagnostics)
5. [Square-root market impact](#market-impact)
6. [Exercises](#exercises)
"""),
        common_setup(),
        new_markdown_cell(r"""<a id="hawkes-model"></a>
## 1. Self-Exciting Point Processes

For event times $t_i$, an exponential Hawkes intensity is

$$\lambda(t)=\mu+\sum_{t_i<t}\alpha e^{-\beta(t-t_i)},$$

where $\mu>0$ is baseline activity, $\alpha>0$ is the jump in intensity after an event, and $\beta>0$ controls decay. Conditional on the current history, the chance of an event in a short interval $dt$ is approximately $\lambda(t)dt$.
"""),
        new_markdown_cell(r"""<a id="stability"></a>
## 2. Stability and Branching

The integral of one event's excitation kernel is

$$n=\int_0^\infty \alpha e^{-\beta s}ds=\frac{\alpha}{\beta}.$$

For a stationary univariate Hawkes process we require $n<1$. The long-run mean intensity is

$$E[\lambda(t)]=\frac{\mu}{1-n}.$$

Thus a seemingly small change in $n$ near one can have a large effect on average activity and clustering.
"""),
        new_markdown_cell(r"""<a id="ogata"></a>
## 3. Ogata Thinning

Thinning samples candidate waiting times from an upper bound on the current intensity, advances the clock, recomputes the decayed intensity at the candidate time, and accepts with probability equal to the candidate intensity divided by the bound.
"""),
        new_code_cell('''def simulate_hawkes_exponential(mu=0.4, alpha=0.7, beta=1.2, horizon=200.0, seed=123):
    """Simulate a stable univariate exponential Hawkes process by Ogata thinning."""
    if min(mu, alpha, beta, horizon) <= 0:
        raise ValueError("Parameters and horizon must be positive.")
    if alpha >= beta:
        raise ValueError("Stationarity requires alpha / beta < 1.")
    local_rng = np.random.default_rng(seed)
    events = []
    t = 0.0
    while t < horizon:
        excitation_now = sum(alpha * np.exp(-beta * (t - ti)) for ti in events)
        upper = mu + excitation_now
        t += local_rng.exponential(1.0 / upper)
        if t >= horizon:
            break
        intensity = mu + sum(alpha * np.exp(-beta * (t - ti)) for ti in events)
        if local_rng.random() <= intensity / upper:
            events.append(t)
    return np.asarray(events)

mu, alpha, beta, horizon = 0.4, 0.7, 1.2, 200.0
events = simulate_hawkes_exponential(mu, alpha, beta, horizon)
branching_ratio = alpha / beta
empirical_rate = len(events) / horizon
theoretical_rate = mu / (1 - branching_ratio)
print(f"events={len(events)}, branching ratio={branching_ratio:.3f}")
print(f"empirical rate={empirical_rate:.3f}, stationary mean rate={theoretical_rate:.3f}")
assert branching_ratio < 1
'''),
        new_markdown_cell(r"""<a id="intensity-diagnostics"></a>
## 4. Intensity Diagnostics

A single path is noisy, so agreement with the theoretical stationary rate is only approximate. More informative diagnostics compare inter-arrival distributions, count dispersion across equal time bins, and behavior across many simulated paths. A Poisson process has count variance approximately equal to its mean; self-excitation generally produces over-dispersion.
"""),
        new_code_cell('''grid = np.linspace(0, horizon, 2_000)
intensity = np.full_like(grid, mu)
for ti in events:
    mask = grid > ti
    intensity[mask] += alpha * np.exp(-beta * (grid[mask] - ti))

counts, edges = np.histogram(events, bins=40, range=(0, horizon))
dispersion = counts.var(ddof=1) / counts.mean()
print(f"count variance/mean ratio = {dispersion:.3f}")

fig, axes = plt.subplots(2, 1, figsize=(11, 7), sharex=True)
axes[0].plot(grid, intensity)
axes[0].vlines(events, 0, mu * 0.35, alpha=0.25, lw=0.8)
axes[0].set(ylabel="intensity", title="Self-exciting order-flow intensity")
axes[1].bar(edges[:-1], counts, width=np.diff(edges), align="edge")
axes[1].set(xlabel="time", ylabel="events per bin")
plt.show()
'''),
        new_markdown_cell(r"""<a id="market-impact"></a>
## 5. Square-Root Market Impact

A widely used empirical benchmark for the price impact of executing quantity $Q$ against daily volume $V$ is

$$I(Q)=Y\sigma\sqrt{\frac{Q}{V}},$$

where $\sigma$ is a volatility scale and $Y$ is an order-one coefficient estimated for the relevant market. This is a reduced-form execution-cost relation, not a consequence of the Hawkes model. It is useful here because a burst of self-excited order flow can move an execution into a different participation-rate regime.
"""),
        new_code_cell('''def square_root_impact(quantity, daily_volume, volatility=0.02, y_coefficient=0.8):
    quantity = np.asarray(quantity, dtype=float)
    if np.any(quantity < 0) or daily_volume <= 0 or volatility < 0 or y_coefficient < 0:
        raise ValueError("Impact inputs must be nonnegative and volume positive.")
    return y_coefficient * volatility * np.sqrt(quantity / daily_volume)

participation = np.logspace(-4, -0.3, 100)
impact = square_root_impact(participation, 1.0)
fig, ax = plt.subplots()
ax.loglog(participation, impact)
ax.set(xlabel="Q / V", ylabel="fractional impact", title="Concave square-root market-impact benchmark")
plt.show()
'''),
        new_markdown_cell(r"""## Exercises

**1. Stability (Conceptual):** Derive the stationary mean intensity from the immigrant-offspring interpretation. Why does it diverge as `alpha/beta → 1`?

**2. Clustering (Applied):** Simulate 200 paths for branching ratios 0.1, 0.5, 0.8, and 0.95 while holding the theoretical mean event rate fixed. Compare count dispersion and maximum local intensity.

**3. Bivariate microstructure (Challenge):** Extend the simulator to mutually exciting buy/sell processes with a 2×2 excitation matrix. State the spectral-radius stability condition and examine how cross-excitation changes order-sign autocorrelation.
"""),
        new_markdown_cell(r"""## Summary & Key Takeaways

- Hawkes processes model endogenous event clustering through history-dependent intensity.
- The branching ratio `alpha/beta` is both an interpretable feedback measure and the core univariate stationarity diagnostic.
- Ogata thinning provides an exact simulation route for the exponential-kernel specification.
- Market impact is a distinct reduced-form object; joining it to event-flow dynamics is a stress-analysis exercise, not an identity.
"""),
        new_markdown_cell(r"""## References & Further Reading

- Hawkes, A. G. (1971). Spectra of some self-exciting and mutually exciting point processes. *Biometrika*, 58(1), 83–90.
- Ogata, Y. (1981). On Lewis' simulation method for point processes. *IEEE Transactions on Information Theory*, 27(1), 23–31.
- Bacry, E., Mastromatteo, I. & Muzy, J.-F. (2015). Hawkes processes in finance. *Market Microstructure and Liquidity*, 1(1), 1550005.
"""),
    ]
    return write_notebook("09-Finance/08_Hawkes_Processes_and_Market_Impact.ipynb", cells)


def create_dice() -> bool:
    cells = [
        new_markdown_cell(r"""# 04 Climate-Macro Integrated Assessment: A DICE-Inspired Laboratory

## The Lens: Pricing a Stock Externality Across Centuries

Climate policy is a dynamic control problem with unusually long delays. Emissions today add to an atmospheric stock; the stock changes radiative forcing; temperature responds gradually; damages affect output; and mitigation diverts resources today to reduce future losses. Integrated assessment models (IAMs) make those links explicit so assumptions about growth, discounting, climate persistence, damages, and abatement can be stress-tested in one coherent system.

This notebook builds a deliberately simplified **DICE-inspired** model rather than claiming to reproduce an official DICE release. The simplification is pedagogical: one carbon reservoir and one temperature state replace the multi-box climate module, while output, damages, abatement costs, and discounted utility preserve the feedback structure. We optimize a low-dimensional abatement ramp, compare climate and consumption paths with a no-policy baseline, and compute a local present-value damage increment from an additional unit of emissions. The main lesson is not a single carbon price; it is how the price changes when discounting, damages, carbon persistence, or the policy-control parameterization changes.

### Learning Objectives
- **Map** emissions, carbon stock, temperature, damages, output, and welfare into a dynamic system.
- **Simulate** a transparent DICE-inspired economy-climate model.
- **Optimize** a constrained abatement path and interpret the shadow trade-off.
- **Stress-test** the implied carbon-cost proxy under alternative discounting and damage assumptions.

### Prerequisites
- `../04-Macro-Models/02_Neoclassical_Growth.ipynb`: growth dynamics and intertemporal welfare.
- `../02-Numerical-Methods/05_Optimization.ipynb`: constrained nonlinear optimization.
- `03_Network_Economics.ipynb`: dynamic externalities and propagation intuition.
"""),
        new_markdown_cell(r"""## Table of Contents

1. [A compact economy-climate system](#economy-climate)
2. [Simulation engine](#simulation-engine)
3. [Policy parameterization](#policy-parameterization)
4. [Optimal abatement experiment](#optimal-abatement)
5. [Marginal emissions damage](#marginal-damage)
6. [Sensitivity and exercises](#sensitivity)
"""),
        common_setup("from scipy.optimize import minimize"),
        new_markdown_cell(r"""<a id="economy-climate"></a>
## 1. A Compact Economy-Climate System

Potential output grows exogenously,

$$Y_{t+1}^{pot}=Y_t^{pot}(1+g),$$

baseline industrial emissions are proportional to output, and control $\mu_t\in[0,1]$ abates a fraction:

$$E_t=\sigma_tY_t^{pot}(1-\mu_t).$$

A one-box atmospheric carbon stock follows

$$M_{t+1}=M_{pre}+\phi_M(M_t-M_{pre})+\chi E_t,$$

and temperature evolves toward logarithmic forcing,

$$T_{t+1}=\phi_TT_t+\xi_T\frac{\log(M_t/M_{pre})}{\log 2}.$$

Output losses combine quadratic climate damages $d_2T_t^2$ and convex abatement costs $\theta\mu_t^\psi$. Consumption is positive net output and welfare is the discounted sum of log consumption.
"""),
        new_markdown_cell(r"""<a id="simulation-engine"></a>
## 2. Simulation Engine

Parameter values below are illustrative and internally consistent, not a calibration to any official DICE vintage. That distinction matters: an IAM's numerical carbon price is only as credible as its calibrated climate and economic blocks.
"""),
        new_code_cell('''def simulate_iam(
    control,
    periods=40,
    years_per_period=5,
    growth=0.012,
    emissions_intensity=0.32,
    intensity_decline=0.01,
    carbon_persistence=0.985,
    emissions_to_carbon=0.12,
    temp_persistence=0.88,
    climate_response=0.24,
    damage_quad=0.0025,
    abatement_scale=0.03,
    abatement_power=2.6,
    pure_time_preference=0.015,
    initial_output=100.0,
    initial_carbon=890.0,
    preindustrial_carbon=588.0,
    initial_temp=1.2,
    emissions_pulse=0.0,
):
    """Simulate a transparent one-box DICE-inspired economy-climate model."""
    control = np.clip(np.asarray(control, dtype=float), 0.0, 1.0)
    if control.size != periods:
        raise ValueError("Control path length must equal periods.")
    if min(initial_output, initial_carbon, preindustrial_carbon) <= 0:
        raise ValueError("Output and carbon stocks must be positive.")

    output_potential = np.empty(periods)
    carbon = np.empty(periods)
    temperature = np.empty(periods)
    emissions = np.empty(periods)
    consumption = np.empty(periods)
    damages = np.empty(periods)
    abatement_cost = np.empty(periods)
    output_potential[0], carbon[0], temperature[0] = initial_output, initial_carbon, initial_temp

    for t in range(periods):
        if t > 0:
            output_potential[t] = output_potential[t - 1] * (1 + growth) ** years_per_period
        sigma_t = emissions_intensity * (1 - intensity_decline) ** (t * years_per_period)
        emissions[t] = sigma_t * output_potential[t] * (1 - control[t])
        if t == 0:
            emissions[t] += emissions_pulse

        damage_share = damage_quad * temperature[t] ** 2
        abatement_share = abatement_scale * control[t] ** abatement_power
        damages[t] = output_potential[t] * damage_share
        abatement_cost[t] = output_potential[t] * abatement_share
        consumption[t] = output_potential[t] - damages[t] - abatement_cost[t]
        if consumption[t] <= 0:
            raise ValueError("Calibration produced non-positive consumption.")

        if t + 1 < periods:
            carbon[t + 1] = preindustrial_carbon + carbon_persistence * (carbon[t] - preindustrial_carbon) + emissions_to_carbon * emissions[t]
            forcing = np.log(max(carbon[t], 1e-9) / preindustrial_carbon) / np.log(2)
            temperature[t + 1] = temp_persistence * temperature[t] + climate_response * forcing

    beta = np.exp(-pure_time_preference * years_per_period)
    discount = beta ** np.arange(periods)
    welfare = float(np.sum(discount * np.log(consumption)))
    pv_damages = float(np.sum(discount * damages))
    return pd.DataFrame({
        "output_potential": output_potential,
        "emissions": emissions,
        "carbon": carbon,
        "temperature": temperature,
        "damages": damages,
        "abatement_cost": abatement_cost,
        "consumption": consumption,
        "control": control,
        "discount": discount,
    }), welfare, pv_damages

baseline_control = np.zeros(40)
baseline, baseline_welfare, baseline_pv_damages = simulate_iam(baseline_control)
baseline.tail(3)
'''),
        new_markdown_cell(r"""<a id="policy-parameterization"></a>
## 3. Policy Parameterization

Optimizing one control for every period can hide non-identification behind a high-dimensional optimizer. We start with a two-parameter ramp,

$$\mu_t=\mathrm{clip}(\mu_0+s\,t,0,1),$$

which makes the policy experiment interpretable. A later extension can optimize a spline or direct-control vector once this baseline is verified.
"""),
        new_code_cell('''def ramp_control(params, periods=40):
    mu0, slope = params
    return np.clip(mu0 + slope * np.arange(periods), 0.0, 1.0)


def welfare_objective(params):
    control = ramp_control(params)
    _, welfare, _ = simulate_iam(control)
    return -welfare

opt = minimize(
    welfare_objective,
    x0=np.array([0.05, 0.02]),
    bounds=[(0.0, 1.0), (0.0, 0.10)],
    method="L-BFGS-B",
)
if not opt.success:
    raise RuntimeError(opt.message)
optimal_control = ramp_control(opt.x)
policy, policy_welfare, policy_pv_damages = simulate_iam(optimal_control)
print(f"optimal ramp parameters: mu0={opt.x[0]:.3f}, slope={opt.x[1]:.4f}")
print(f"welfare gain over no-policy baseline: {policy_welfare - baseline_welfare:.5f}")
'''),
        new_markdown_cell(r"""<a id="optimal-abatement"></a>
## 4. Optimal Abatement Experiment

A welfare-improving path trades current abatement cost against lower future climate damages. The optimization should be interpreted comparatively: changing the pure rate of time preference or damage curvature shifts the path because it changes how future losses are valued.
"""),
        new_code_cell('''fig, axes = plt.subplots(2, 2, figsize=(11, 8))
axes = axes.ravel()
axes[0].plot(baseline["temperature"], label="no policy")
axes[0].plot(policy["temperature"], label="optimized ramp")
axes[0].set(title="Temperature", ylabel="°C-equivalent state")
axes[1].plot(baseline["emissions"], label="no policy")
axes[1].plot(policy["emissions"], label="optimized ramp")
axes[1].set(title="Emissions")
axes[2].plot(optimal_control)
axes[2].set(title="Abatement control", ylim=(0, 1.05))
axes[3].plot(baseline["consumption"], label="no policy")
axes[3].plot(policy["consumption"], label="optimized ramp")
axes[3].set(title="Consumption")
for ax in axes: ax.set_xlabel("5-year period")
axes[0].legend(); axes[3].legend()
plt.tight_layout(); plt.show()
'''),
        new_markdown_cell(r"""<a id="marginal-damage"></a>
## 5. Marginal Emissions Damage

A local carbon-cost diagnostic can be formed by perturbing period-0 emissions by a small amount and measuring the change in discounted model damages:

$$MD_0\approx\frac{PV(D\mid E_0+\Delta E)-PV(D\mid E_0)}{\Delta E}.$$

This is **not** a unit-converted official social cost of carbon. It is a marginal-damage proxy in this model's output/emissions units, useful for sensitivity analysis and for checking that the climate block has the expected sign.
"""),
        new_code_cell('''pulse = 0.1
_, _, pv_damage_base = simulate_iam(optimal_control, emissions_pulse=0.0)
_, _, pv_damage_pulse = simulate_iam(optimal_control, emissions_pulse=pulse)
marginal_damage_proxy = (pv_damage_pulse - pv_damage_base) / pulse
print(f"present-value marginal damage proxy = {marginal_damage_proxy:.5f} output units per emissions unit")
assert marginal_damage_proxy > 0
'''),
        new_markdown_cell(r"""<a id="sensitivity"></a>
## 6. Sensitivity and Exercises

**1. Discounting (Conceptual):** Explain why a higher pure rate of time preference generally lowers current abatement in this model. Distinguish the ethical discounting assumption from technological climate persistence.

**2. Damage curvature (Applied):** Re-optimize the ramp for `damage_quad` from 0.001 to 0.008. Plot initial abatement, long-run abatement, peak temperature, and the marginal-damage proxy.

**3. Climate block (Challenge):** Replace the one-box carbon/temperature system with two carbon reservoirs and two thermal boxes. Calibrate only from explicitly cited sources, then compare policy conclusions with the pedagogical one-box model.
"""),
        new_markdown_cell(r"""## Summary & Key Takeaways

- IAMs couple a stock externality to economic dynamics; delays make intertemporal assumptions central to policy results.
- This notebook is DICE-inspired, not a replication of an official DICE codebase or calibration.
- A low-dimensional policy ramp makes the optimization transparent and easier to stress-test before using richer controls.
- Marginal damage, optimal control, and temperature paths should all be reported with sensitivity to discounting, damages, and climate persistence.
"""),
        new_markdown_cell(r"""## References & Further Reading

- Nordhaus, W. D. (2017). Revisiting the social cost of carbon. *Proceedings of the National Academy of Sciences*, 114(7), 1518–1523.
- Nordhaus, W. D. & Sztorc, P. (2013). *DICE 2013R: Introduction and User's Manual*.
- Golosov, M., Hassler, J., Krusell, P. & Tsyvinski, A. (2014). Optimal taxes on fossil fuel in general equilibrium. *Econometrica*, 82(1), 41–88.
"""),
    ]
    return write_notebook("10-Specialized-Models/04_Climate_Macro_Integrated_Assessment_DICE.ipynb", cells)


def append_section(rel: str, marker: str, markdown: str, code: str | None = None) -> bool:
    path = ROOT / rel
    nb = nbformat.read(path, as_version=4)
    if any(marker in (c.source if isinstance(c.source, str) else "".join(c.source)) for c in nb.cells):
        return False
    # Insert before the first summary/exercise/reference cell near the end.
    idx = len(nb.cells)
    for i, cell in enumerate(nb.cells):
        if cell.cell_type != "markdown":
            continue
        src = cell.source if isinstance(cell.source, str) else "".join(cell.source)
        if any(term in src for term in ("# Summary", "## Summary", "# Exercises", "## Exercises", "References & Further Reading")):
            idx = i
            break
    additions = [new_markdown_cell(markdown)]
    if code:
        additions.append(new_code_cell(code))
    nb.cells[idx:idx] = additions
    nbformat.write(nb, path)
    return True


def enrich_existing() -> int:
    changed = 0
    changed += append_section(
        "04-Macro-Models/06_Heterogeneous_Agent_Models.ipynb",
        "Sequence-Space Jacobian Bridge",
        r"""## 5. Sequence-Space Jacobian Bridge: From Aiyagari to HANK

Solving a stationary heterogeneous-agent model is only the first step toward a HANK transition. Sequence-space methods linearize **aggregate sequences** around the stationary equilibrium instead of rebuilding a huge state-space transition system. If an aggregate input path $X=(X_0,X_1,\ldots)$ perturbs an output path $Y$, define the Jacobian

$$J_{t,s}=\frac{\partial Y_t}{\partial X_s}.$$

Around steady state, a small shock sequence obeys

$$dY \approx J\,dX.$$

The computational gain comes from reusing household response objects and exploiting the lower-triangular time structure. General equilibrium then becomes a system of linear equations in sequence space. This does not make heterogeneity disappear: the household Jacobian summarizes how the entire stationary distribution and policy rules respond to prices. The practical diagnostic is to verify that a finite-difference impulse converges to the Jacobian prediction as the shock size shrinks.

The miniature experiment below isolates the aggregation logic using a heterogeneous marginal-propensity-to-consume (MPC) distribution. It is not a full HANK solver; it is a bridge to the Auclert-Bardóczy-Rognlie-Straub algorithm and makes the sequence-space object explicit before introducing implementation complexity.
""",
        '''# Stylized sequence-space consumption Jacobian from heterogeneous MPCs
horizon = 24
mpc_distribution = np.array([0.05, 0.15, 0.30, 0.55, 0.85])
weights = np.array([0.15, 0.25, 0.30, 0.20, 0.10])
persistence = 0.72
aggregate_mpc = float(weights @ mpc_distribution)
J = np.zeros((horizon, horizon))
for s in range(horizon):
    for t in range(s, horizon):
        J[t, s] = aggregate_mpc * persistence ** (t - s)
shock = np.zeros(horizon); shock[0] = 0.01
consumption_response = J @ shock
assert np.allclose(J, np.tril(J))
print(f"aggregate impact MPC = {aggregate_mpc:.3f}; cumulative response = {consumption_response.sum():.4f}")
''',
    )
    changed += append_section(
        "06-Econometrics/08_Difference_in_Differences.ipynb",
        "Honest Parallel-Trends Sensitivity",
        r"""## 4. Honest Parallel-Trends Sensitivity: What If Pre-Trends Are Only Approximately Informative?

Modern staggered-adoption estimators repair contamination from already-treated comparison groups, but they do not make the **parallel-trends assumption** testable after treatment. Rambachan and Roth (2023) therefore ask a different question: how large could post-treatment deviations from the counterfactual trend be before the conclusion changes?

Let $\delta_t$ denote the untreated-potential-outcome trend violation in event time. A sensitivity set constrains post-treatment violations relative to information in the pre-period. One common smoothness idea limits changes in adjacent trend violations,

$$|\delta_{t+1}-\delta_t|\le M\,\bar\Delta_{pre},$$

where $\bar\Delta_{pre}$ summarizes the scale of observed pre-period deviations and $M$ controls how much worse the post-period may be. The output is a **breakdown frontier**: the smallest $M$ at which a confidence set includes zero. This reframes a binary pre-trend test into a quantitative robustness statement.

A disciplined DiD workflow should therefore report (1) an estimator valid for the adoption pattern, (2) event-study diagnostics with honest uncertainty, and (3) a sensitivity analysis tied to economically interpretable trend violations. Failing to reject a pre-trend test is not evidence that violations are zero.

**References:** Rambachan & Roth (2023); Callaway & Sant'Anna (2021); Sun & Abraham (2021).
""",
    )
    changed += append_section(
        "09-Finance/01_Portfolio_Theory.ipynb",
        "Ledoit-Wolf Shrinkage",
        r"""## 4. Ledoit-Wolf Shrinkage: Stabilizing High-Dimensional Covariance Matrices

Mean-variance portfolios are extremely sensitive to covariance estimation. When the number of assets is not small relative to the sample size, the sample covariance matrix is noisy and can become nearly singular. Ledoit-Wolf shrinkage replaces it with a convex combination

$$\hat\Sigma_{LW}=\alpha F+(1-\alpha)S,$$

where $S$ is the sample covariance and $F$ is a structured target. The shrinkage intensity is selected to reduce expected squared estimation error. The relevant portfolio diagnostic is not an in-sample Sharpe ratio; it is out-of-sample stability of weights, realized risk, and turnover.

The code below compares matrix conditioning. A better condition number does not prove a better portfolio, but it removes a major numerical amplification channel and provides a falsifiable reason to test shrinkage out of sample.
""",
        '''from sklearn.covariance import LedoitWolf
# Synthetic correlated returns with P not tiny relative to T.
_local_rng = np.random.default_rng(2026)
n_obs, n_assets = 120, 60
factor = _local_rng.normal(size=(n_obs, 3))
loadings = _local_rng.normal(scale=0.35, size=(3, n_assets))
returns_lw = factor @ loadings + _local_rng.normal(scale=0.7, size=(n_obs, n_assets))
sample_cov = np.cov(returns_lw, rowvar=False)
lw_cov = LedoitWolf().fit(returns_lw).covariance_
print(f"sample condition number: {np.linalg.cond(sample_cov):.2e}")
print(f"Ledoit-Wolf condition number: {np.linalg.cond(lw_cov):.2e}")
assert np.linalg.cond(lw_cov) < np.linalg.cond(sample_cov)
''',
    )
    changed += append_section(
        "09-Finance/03_Option_Pricing.ipynb",
        "Carr-Madan FFT",
        r"""## 9. Carr-Madan FFT: Pricing Many Strikes at Once

Monte Carlo is flexible but expensive when a calibration routine needs prices across a dense strike grid. Carr and Madan (1999) exploit a model's characteristic function and the Fast Fourier Transform (FFT). After damping the call-price function so its Fourier transform is integrable, option prices across log strikes can be recovered from one transformed grid.

For damping parameter $\alpha>0$, define $c_\alpha(k)=e^{\alpha k}C(k)$. Its Fourier transform can be written in terms of the risk-neutral characteristic function $\phi(u)$; numerical quadrature on an evenly spaced frequency grid then becomes an FFT. The method is especially valuable for Heston-style calibration because one expensive characteristic-function evaluation produces a whole strike surface slice.

The implementation burden is not the FFT call itself. Correct work must track transform conventions, damping, grid spacing, interpolation, and the $u=0$ behavior, then validate against a closed-form Black-Scholes price before using a more complex characteristic function. This validation-first workflow is the required exercise here rather than embedding an unverified calibration black box.

**Reference:** Carr, P. & Madan, D. (1999). Option valuation using the fast Fourier transform. *Journal of Computational Finance*, 2(4), 61–73.
""",
    )
    return changed


def main() -> None:
    creators = [create_hjb, create_blp, create_sdid, create_particle_filter, create_hawkes, create_dice]
    created = sum(bool(fn()) for fn in creators)
    enriched = enrich_existing()
    print(f"Created {created} frontier notebooks and enriched {enriched} canonical notebooks.")


if __name__ == "__main__":
    main()
