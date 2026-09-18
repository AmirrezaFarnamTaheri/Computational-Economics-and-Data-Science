# Economic Modeling (DP) Cheat Sheet

> Quick reference for Module 03. Details: [Dynamic Programming](../modules/03-economic-modeling/01-dynamic-programming.md), [Continuous States](../modules/03-economic-modeling/02-continuous-states.md).

## Core objects & dimensions

| Object | Notation | Dimensions |
|---|---|---|
| State grid | $\{s_i\}_{i=1}^{S}$ | $\mathbb{R}^S$ |
| Value function | $V: \mathcal{S} \to \mathbb{R}$ | scalar field on the grid |
| Policy | $a = \pi(s)$ | same space as actions |
| Bellman operator | $T$ | maps functions to functions |
| Discount factor | $\beta$ | $(0, 1)$ |

## Bellman equations

- Stationary: $V(s) = \max_{a \in \Gamma(s)} \big\{ r(s, a) + \beta\, \mathbb{E}\big[V(s') \mid s, a\big] \big\}$
- Contraction: $d(Tx, Ty) \le \beta\, d(x, y)$, so VFI error after $m$ steps satisfies
  $\|V_m - V^*\| \le \frac{\beta^m}{1-\beta}\, d(V_1, V_0)$ — geometric convergence.
- Stopping rule: iterate until $\|V_{m+1} - V_m\|_\infty \le \varepsilon (1-\beta)/\beta$ to bound $\|V_{m+1}-V^*\|_\infty$ by $\varepsilon$. This is a value-function bound, not a bound on policy actions.
- Cake eating with $u(c)=\ln c$ and $w_{t+1}=w_t-c_t$: $c^*(w)=(1-\beta)w$ and $V(w)=\frac{\ln w+\ln(1-\beta)}{1-\beta}+\frac{\beta\ln\beta}{(1-\beta)^2}$ for $w>0$. Check the Bellman equation against this benchmark.

## Algorithms & complexity (discrete state, $S$ states, $A$ actions)

| Algorithm | Cost per step | Notes |
|---|---|---|
| Value function iteration | $O(S^2 A)$ | simple; converge on sup-norm of $V$ **and** $\pi$ |
| Policy function iteration | $O(S^3)$ per policy eval | usually fewer outer iterations |
| Continuous state (collocation) | $O(N^3)$ per solve of coefficients | $N$ basis functions; residual check on off-grid nodes |

## Numerical discipline

- Interpolated policies are valid only **inside** the grid — clamp states to $[s_{min}, s_{max}]$.
- Verify Euler equation residuals on a finer grid than you solved on.
- Monotone policy + concave $V$ are good sanity checks (for convex-once problems).
