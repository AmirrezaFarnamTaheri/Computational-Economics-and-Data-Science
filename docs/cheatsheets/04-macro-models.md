# Macro Models Cheat Sheet

> Quick reference for Module 04. Details: [Module 4 index](../modules/04-macro-models/index.md).

## Core objects & dimensions

| Object | Notation | Dimensions |
|---|---|---|
| Capital per effective worker | $k = K/(AL)$ | $\mathbb{R}_+$ scalar |
| Consumption / output | $c, y = f(k)$ | scalars |
| Log-deviation variables | $\hat{x}_t = \ln x_t - \ln x$ | scalars (percent) |
| Linearized system | $E_t z_{t+1} = A z_t + B \varepsilon_{t+1}$ | $z \in \mathbb{R}^n$, $A \in \mathbb{R}^{n \times n}$ |
| Sequence-space Jacobian | $J_{t,s} = \partial Y_t / \partial X_s$ | $\mathbb{R}^{T \times T}$ |

## Workhorse equations

- **Solow**: $\dot{k} = s f(k) - (n+g+\delta)k$; Cobb-Douglas steady state $k^* = \left(\tfrac{s}{n+g+\delta}\right)^{1/(1-\alpha)}$.
- **RBC (FOCs)**: $\psi C_t^{\sigma} L_t^{\phi} = w_t$ and $C_t^{-\sigma} = \beta E_t[C_{t+1}^{-\sigma}(1 + r_{t+1} - \delta)]$.
- **Blanchard-Kahn**: # unstable eigenvalues of $A$ must equal # forward-looking variables, else explosive or indeterminate.
- **NK 3-equation**:
  $x_t = E_t x_{t+1} - \sigma^{-1}(\hat{i}_t - E_t \pi_{t+1} - r_t^n)$;
  $\pi_t = \beta E_t \pi_{t+1} + \kappa x_t$;
  $\hat{i}_t = \phi_\pi \pi_t + \phi_y x_t + v_t$; determinacy iff $\phi_\pi > 1 - \tfrac{1-\beta}{\kappa}\phi_y$ (Taylor principle).
- **Heterogeneous agents**: solve policy $c(a; z)$ on grid with borrowing limit $a_{min}$; iterate prices $\leftrightarrow$ stationary distribution to fixed point.

## Solution methods & complexity

| Method | Setup | Per-step cost | Watch for |
|---|---|---|---|
| Log-linearization + Blanchard-Kahn | analytic Jacobian | eigen-decomposition $O(n^3)$ | eigenvalue counts |
| Value/ policy iteration on $(a, z)$ grid | — | $O(N_a^2 N_z)$ | borrowing-constraint edge |
| Sequence-space Jacobian (HANK) | household Jacobian once | $O(T^2)$ applies | truncation horizon $T$ |
| Calibration moments | — | — | filter model **and** data identically |

## Sanity checks

Transversality holds; steady state exists ($\beta$ vs $\delta$, $\rho$); impulse responses die out; moments compared on identical transformations.
