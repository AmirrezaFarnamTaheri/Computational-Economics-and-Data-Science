# Micro Models Cheat Sheet

> Quick reference for Module 05. Details: [Game Theory](../modules/05-micro-models/03-game-theory.md), [Discrete Choice](../modules/05-micro-models/04-discrete-choice.md).

## Consumer theory

| Object | Formula | Dimensions |
|---|---|---|
| Marshallian demand | $\mathbf{x}^*(\mathbf{p}, I)$ | $\mathbb{R}^n_+$ |
| Indirect utility | $v(\mathbf{p}, I)$ | scalar |
| Expenditure function | $e(\mathbf{p}, u)$ | scalar |
| Cobb-Douglas demands | $x_i^* = \frac{\alpha_i I}{p_i}$, $\sum\alpha_i = 1$ | scalars |
| Optimality | $MRS_{xy} = \frac{MU_x}{MU_y} = \frac{p_x}{p_y}$ (interior) | scalar ratio |
| Shephard's lemma | $h_i(\mathbf{p}, u) = \frac{\partial e}{\partial p_i}$ | scalar |

Corner solutions: FOCs with equality **fail** at $x_i = 0$; use KKT complementary slackness.

## Game theory & auctions

- Nash equilibrium: $a^*$ such that $u_i(a_i^*, a_{-i}^*) \ge u_i(a_i, a_{-i}^*)\ \forall a_i, \forall i$. Finite games always have one in mixed strategies (Nash 1950).
- Computing NE is **PPAD-hard** in general — `nashpy` uses Lemke-Howson / support enumeration; expect multiple equilibria and report all.
- VCG: charge each bidder the externality they impose — truthful bidding is dominant.
- Revenue equivalence (benchmark auctions, risk-neutral, private values): expected revenue identical.

## Discrete choice

| Object | Formula | Notes |
|---|---|---|
| Logit probability | $P(i) = \dfrac{e^{V_i}}{\sum_j e^{V_j}}$ | $V_i$ scalar payoff |
| IIA | $P(i)/P(j)$ independent of other options | red-bus/blue-bus limitation |
| Consumer surplus (logit) | $CS = \frac{1}{\lambda} \ln \sum_j e^{V_j} + C$ | $\lambda$ = scale |
| BLP random coefficients | $s_{jt} = \int s_{jt}(\nu)\, dF(\nu)$ | integration over $\nu \in \mathbb{R}^d$ |

## Principal-agent (moral hazard)

FOC of the agent: $c'(a) = \sum_i \lambda_i \partial q_i / \partial a$; the likelihood ratio $\partial q_i/\partial a$ is what the contract should reward.
