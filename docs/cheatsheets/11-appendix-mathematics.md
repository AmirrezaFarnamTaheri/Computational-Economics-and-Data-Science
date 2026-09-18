# Mathematics Appendix Cheat Sheet

> Quick reference for the Appendix. Details: [Mathematics Review](../appendices/mathematics.md).

## Real analysis & fixed points

| Object | Statement | Dimensions |
|---|---|---|
| Contraction | $d(Tx, Ty) \le \beta\, d(x, y)$, $\beta \in [0,1)$ | $(X, d)$ metric space |
| Banach theorem | unique $x^*$ with $Tx^* = x^*$; $x_m \to x^*$ | $x^* \in X$ |
| Error bound | $\|x_m - x^*\| \le \frac{\beta^m}{1-\beta} d(x_0, x_1)$ | scalar |
| Blackwell (discounted) | Monotonicity plus $T(v + a) \le Tv + \beta a$ imply a $\beta$-contraction in the sup norm on bounded functions | $a \ge 0$ scalar |
| Separating hyperplane | disjoint convex sets ⇒ $\exists p \ne 0, c$: $p'A \le c \le p'B$ | $p \in \mathbb{R}^n$ |

## Multivariate calculus

- Gradient: $\nabla f(x) \in \mathbb{R}^n$; Hessian $D^2f(x) \in \mathbb{R}^{n \times n}$ (symmetric if $f \in C^2$).
- Taylor: $f(x + h) = f(x) + \nabla f' h + \tfrac{1}{2} h' D^2 f(\xi) h$.
- Envelope: $\frac{dV}{d\theta} = \frac{\partial f(x^*(\theta), \theta)}{\partial \theta}$ — the indirect effect vanishes at the optimum.
- Implicit function theorem: $F(x, \theta) = 0$ ⇒ $dx^*/d\theta = -F_x^{-1} F_\theta$ ($F_x \in \mathbb{R}^{n \times n}$ nonsingular).

## Probability

- Bayes: $P(A \mid B) = \frac{P(B \mid A) P(A)}{P(B)}$ — probabilities in $[0, 1]$; do not swap conditional directions.
- LIE: $E[X] = E[E[X \mid G]]$; conditional expectation $Z = E[X \mid \mathcal{G}]$ is $\mathcal{G}$-measurable with $\int_A Z dP = \int_A X dP$ for $A \in \mathcal{G}$.
- LLN/CLT: $\bar{X}_n \to \mu$; $\sqrt{n}(\bar{X}_n - \mu) \Rightarrow N(0, \sigma^2)$.
- Disjoint ≠ independent (except degenerate zero-probability cases).

## Linear algebra

- Eigenpair: $Av = \lambda v$, $v \in \mathbb{R}^n \setminus \{0\}$, $\lambda \in \mathbb{C}$; Rayleigh quotient $v'Av / v'v$ scalar.
- Perron-Frobenius: positive matrices have a dominant positive eigenvalue/eigenvector (growth, Leontief, PageRank).
- Diagonalization: $A = V\Lambda V^{-1}$ ⇒ $A^t = V\Lambda^t V^{-1}$; stability from $|\lambda_i|$.
