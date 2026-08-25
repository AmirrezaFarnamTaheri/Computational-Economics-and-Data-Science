# Numerical Methods — Bibliography

> Pathway in one line: trust algorithms because you understand their error, not because they ran.

## Reading pathway

1. Trefethen & Bau — the clearest entry to numerical linear algebra.
2. Nocedal & Wright — optimization as this curriculum implements it.
3. Golub & Van Loan — the reference you graduate to.
4. Boyd & Vandenberghe — convexity as a superpower (CVXPY's worldview).
5. Higham — why accuracy claims need backward error.

## Seminal

- **Wilkinson (1965).** *The Algebraic Eigenvalue Problem.* Clarendon Press. —
  Backward error analysis: why floating-point linear algebra deserves trust.
- **Isaacson & Keller (1966).** *Analysis of Numerical Methods.* Wiley. —
  Classical convergence and stability treatment of the methods in Module 02.

## Modern

- **Trefethen & Bau (1997).** *Numerical Linear Algebra.* SIAM. — Forty short
  lectures; the best first pass over SVD, QR, and conditioning.
- **Nocedal & Wright (2006).** *Numerical Optimization*, 2nd ed. Springer. —
  Line search, trust regions, and the SQP machinery behind `scipy.optimize`.
- **Boyd & Vandenberghe (2004).** *Convex Optimization.* Cambridge University
  Press. — The theory making CVXPY's guarantees possible; duality and KKT done
  properly.
- **Higham (2002).** *Accuracy and Stability of Numerical Algorithms*, 2nd ed.
  SIAM. — The encyclopedia of rounding-error behavior; consult when results
  look "off by digits".

## Theoretical

- **Golub & Van Loan (2013).** *Matrix Computations*, 4th ed. Johns Hopkins
  University Press. — The standard reference for every factorization used in
  `numpy.linalg` and `scipy.sparse.linalg`.
