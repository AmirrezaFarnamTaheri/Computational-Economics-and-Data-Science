# Specialized Models Cheat Sheet

> Quick reference for Module 10. Details: [Agent-Based Models](../modules/10-specialized/01-abm.md), [Network Economics](../modules/10-specialized/03-networks.md).

## Agent-based models

| Ingredient | Typical form | Dimensions |
|---|---|---|
| Agents | heterogeneous state $(x_i, s_i)$ | $N$ agents |
| Update rule | threshold / utility-based | per-agent scalar |
| Environment | lattice or network | $N \times N$ adjacency |
| Output | aggregate time series | scalar per step |

- Schelling: mild preferences ($\ge 1/3$ same-type neighbors) → extreme segregation; emergence, not design.
- Discipline: run **ensembles across seeds**, report distributions; verification (code matches model) ≠ validation (model matches reality); many micro-rules can mimic the same stylized fact (equifinality).
- Complexity: $O(N \cdot \text{steps})$ per run; parameter sweeps multiply this — design grids sparingly.

## Network economics

| Concept | Formula | Complexity |
|---|---|---|
| Degree centrality | $d_i / (N-1)$ | $O(N + E)$ |
| Eigenvector centrality | $x = \frac{1}{\lambda} A x$ | power iteration $O(E)$ per step |
| PageRank | $r = d\,\mathbf{1} + \alpha A' D^{-1} r$ (normalized) | $O(E)$ per iteration |
| Betweenness | # shortest paths through $i$ | $O(NE)$ (Brandes) |
| Clustering coefficient | $\frac{2 e_i}{d_i(d_i-1)}$ | $O(d_i^2)$ |

## Integrated assessment (DICE)

- Ramsey block: $\max \int_0^\infty e^{-\rho t} \frac{C_t^{1-\theta}}{1-\theta} L_t\, dt$ subject to capital accumulation and the carbon cycle.
- Social cost of carbon: $SCC = -\frac{\partial W / \partial E_t}{\partial W / \partial C_t}$ — marginal damage in consumption units (scalar).
- Policy runs are deterministic optimizations; uncertainty enters via scenario ensembles.

## Heterogeneous-agent GE

Cross-sectional distribution $g(a, z)$ evolves by $\tilde{A}' g$ (transition matrix); equilibrium = fixed point in prices **and** distribution — iterate both.
