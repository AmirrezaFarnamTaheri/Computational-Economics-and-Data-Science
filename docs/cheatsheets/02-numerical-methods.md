# Numerical Methods Cheat Sheet

> Quick reference for Module 02. Details: [Linear Algebra](../modules/02-numerical-methods/01-linear-algebra.md), [Root Finding](../modules/02-numerical-methods/04-root-finding.md), [Optimization](../modules/02-numerical-methods/05-optimization.md), [Integration](../modules/02-numerical-methods/07-integration.md).

## Core objects & dimensions

| Object | Notation | Dimensions |
|---|---|---|
| System matrix | $A$ | $\mathbb{R}^{n \times n}$ |
| Solution / rhs | $\mathbf{x}, \mathbf{b}$ | $\mathbb{R}^n$ |
| Jacobian | $J$ | $\mathbb{R}^{n \times n}$ for $F: \mathbb{R}^n \to \mathbb{R}^n$ |
| Root / iterate | $x_n$ | $\mathbb{R}$ (scalar methods) |

## Linear algebra

- Solve $A\mathbf{x} = \mathbf{b}$ with `solve`, **never** `inv(A) @ b`: Gaussian elimination costs $O(n^3)$ once; explicit inverses lose accuracy when $\kappa(A) = \|A\|\,\|A^{-1}\| \geq 1$ is large (rule of thumb: lose $\approx \log_{10}\kappa$ digits).
- Least squares: `lstsq` (SVD-based) is robust to rank deficiency; normal equations square the condition number.
- Eigenvalues: $O(n^3)$; check stability of $x_{t+1} = A x_t$ via $|\lambda_i|$ vs 1.

## Root finding

| Method | Order | Cost/iter | Needs |
|---|---|---|---|
| Bisection | 1 (halving) | 1 eval | bracket $f(a)f(b)<0$; error $\le (b-a)/2^{n+1}$, so $n \ge \log_2\frac{b-a}{\varepsilon} - 1$ |
| Newton | 2 | 2 evals ($f, f'$) | good guess, $f' \neq 0$ |
| Secant | $\approx 1.618$ | 1 eval | two starts |
| Brent (`brentq`) | superlinear | adaptive | bracket — **the default** |

## Optimization & approximation

- Convex problems: local = global; use CVXPY. Non-convex: multi-start, and always check `result.success` + gradient norm.
- Interpolation: equispaced high-degree polynomials oscillate (Runge); use Chebyshev nodes or splines. Barycentric evaluation $O(n)$ per point.
- Quadrature: trapezoid error $O(h^2)$, Simpson $O(h^4)$; $n$-point Gauss rules integrate polynomials up to degree $2n-1$ exactly (Gauss-Hermite for $\int e^{-x^2}g(x)dx$).
- ODEs: explicit Euler global error $O(h)$, RK4 $O(h^4)$; stiff systems (fast + slow eigenvalues) need implicit `BDF`/`Radau`.

## Dimension discipline

Every estimate is a scalar or vector with known shape: derivatives of $f:\mathbb{R}\to\mathbb{R}$ are scalars; $\nabla f:\mathbb{R}^n\to\mathbb{R}^n$; Hessian $\mathbb{R}^{n\times n}$. Annotate before you code.
