# Module 2: Numerical Methods

Master the computational techniques essential for solving economic models.

---

## Overview

This module provides comprehensive coverage of numerical methods used in computational economics. You'll learn the mathematical foundations and practical implementations of algorithms for solving systems of equations, optimization problems, and differential equations.

**Duration:** 4-5 weeks
**Difficulty:** Intermediate
**Prerequisites:** Module 1 (Foundations), Calculus, Linear Algebra

---

## Learning Objectives

By the end of this module, you will be able to:

- ✓ Solve linear systems using direct and iterative methods
- ✓ Apply root-finding algorithms to nonlinear equations
- ✓ Implement numerical differentiation and integration
- ✓ Solve unconstrained and constrained optimization problems
- ✓ Use interpolation and approximation methods
- ✓ Solve ordinary and partial differential equations numerically

---

## Topics Covered

### 1. Linear Algebra
**Notebook:** `01_Linear_Algebra.ipynb`

- Direct methods: LU decomposition, Cholesky factorization
- Iterative methods: Jacobi, Gauss-Seidel, conjugate gradient
- Eigenvalue problems and spectral decomposition
- Sparse matrix techniques
- Applications to economic models

**Key Applications:**
- Input-output analysis
- Markov chains and transition matrices
- Solving large-scale equilibrium models

---

### 2. Numerical Preliminaries
**Notebook:** `02_Numerical_Preliminaries.ipynb`

- Floating-point arithmetic and numerical precision
- Conditioning and stability
- Error analysis
- Algorithm complexity
- Best practices for numerical computing

---

### 3. Numerical Differentiation
**Notebook:** `03_Numerical_Differentiation.ipynb`

- Finite difference methods (forward, backward, central)
- Richardson extrapolation
- Automatic differentiation
- Computing Jacobians and Hessians
- Applications to economic optimization

---

### 4. Root Finding
**Notebook:** `04_Root_Finding.ipynb`

- Bisection and bracketing methods
- Newton-Raphson and quasi-Newton methods
- Secant method and Brent's method
- Systems of nonlinear equations
- Fixed-point iteration

**Economic Applications:**
- Finding equilibrium prices
- Solving Euler equations
- Computing steady states

---

### 5. Optimization
**Notebook:** `05_Optimization.ipynb`

- Unconstrained optimization: gradient descent, Newton's method
- Constrained optimization: penalty methods, Lagrange multipliers
- Linear programming and the simplex algorithm
- Nonlinear programming: BFGS, conjugate gradient
- Global optimization methods

**Economic Applications:**
- Utility maximization
- Cost minimization
- Optimal control problems
- Portfolio optimization

---

### 6. Interpolation and Approximation
**Notebook:** `06_Interpolation_and_Approximation.ipynb`

- Polynomial interpolation (Lagrange, Newton)
- Spline interpolation (linear, cubic, B-splines)
- Chebyshev polynomials
- Function approximation methods
- Curse of dimensionality

**Applications:**
- Value function approximation
- Policy function representation
- Solving dynamic programming problems

---

### 7. Numerical Integration
**Notebook:** `07_Numerical_Integration.ipynb`

- Riemann sums and trapezoidal rule
- Simpson's rule and adaptive quadrature
- Gaussian quadrature
- Monte Carlo integration
- Quasi-Monte Carlo methods

**Economic Applications:**
- Computing expected values
- Welfare calculations
- Numerical computation of integrals in continuous-state models

---

### 8. Differential Equations
**Notebook:** `08_Differential_Equations.ipynb`

- Initial value problems: Euler, Runge-Kutta methods
- Boundary value problems: shooting and finite difference
- Stiff equations and adaptive step sizes
- Partial differential equations (PDEs)
- Finite element methods

**Applications:**
- Dynamic economic models
- Asset pricing (Black-Scholes PDE)
- Growth models with differential equations
- Spatial economics models

---

## Prerequisites

### Required Knowledge

**Mathematics:**
- Single and multivariable calculus
- Linear algebra (matrices, eigenvalues)
- Basic real analysis

**Programming:**
- Python fundamentals (Module 1)
- NumPy and array operations
- Basic algorithm implementation

---

## Key Libraries

This module uses:

- **NumPy**: Core numerical operations
- **SciPy**: Scientific computing algorithms
- **Matplotlib**: Visualization
- **QuantEcon**: Economic-specific numerical tools

---

## Learning Path

### Week 1: Linear Systems and Preliminaries
- Complete notebooks 01-02
- Implement basic linear solvers
- Understand numerical precision

### Week 2: Differentiation and Root Finding
- Complete notebooks 03-04
- Practice Newton's method
- Apply to economic equilibrium problems

### Week 3: Optimization
- Complete notebook 05
- Implement optimization algorithms
- Solve constrained problems

### Week 4: Approximation and Integration
- Complete notebooks 06-07
- Master interpolation techniques
- Compute integrals numerically

### Week 5: Differential Equations
- Complete notebook 08
- Solve ODEs and PDEs
- Apply to economic dynamics

---

## Practice Exercises

Throughout the notebooks, you'll find exercises such as:

1. **Linear Systems**: Solve large sparse systems from economic input-output tables
2. **Root Finding**: Find equilibrium in a simple exchange economy
3. **Optimization**: Solve a consumer's utility maximization problem
4. **Interpolation**: Approximate value functions in dynamic programming
5. **Integration**: Compute expected utility with numerical integration
6. **Differential Equations**: Solve the Solow growth model

---

## Common Challenges

### Challenge: Numerical Instability
**Solution:**
- Use stable algorithms (e.g., QR instead of normal equations)
- Check condition numbers
- Rescale variables

### Challenge: Slow Convergence
**Solution:**
- Choose better initial guesses
- Use acceleration techniques
- Consider alternative algorithms

### Challenge: High Dimensionality
**Solution:**
- Exploit problem structure
- Use sparse methods
- Consider dimension reduction

---

## Resources

### Essential Reading
- Judd, K. (1998). *Numerical Methods in Economics*. MIT Press
- Press, W. et al. (2007). *Numerical Recipes*. Cambridge
- Miranda, M. & Fackler, P. (2002). *Applied Computational Economics*. MIT Press

### Documentation
- [NumPy Documentation](https://numpy.org/doc/)
- [SciPy Optimization](https://docs.scipy.org/doc/scipy/reference/optimize.html)
- [QuantEcon Lectures](https://quantecon.org/)

### Online Resources
- MIT OpenCourseWare: Numerical Analysis
- Stanford CME 292: Advanced MATLAB for Scientific Computing
- Numerical Tours: [www.numerical-tours.com](http://www.numerical-tours.com)

---

## Assessment

Master the following to complete this module:

- [ ] Implement basic numerical algorithms from scratch
- [ ] Use SciPy effectively for numerical problems
- [ ] Choose appropriate methods for different problem types
- [ ] Understand stability and convergence issues
- [ ] Apply methods to economic problems
- [ ] Interpret numerical results correctly

---

## Next Steps

After completing this module:

1. **Module 3: Economic Modeling** - Apply these methods to dynamic programming
2. **Module 4: Macro Models** - Use numerical methods for RBC and DSGE models
3. **Module 6: Econometrics** - Apply optimization to estimation problems

---

## Need Help?

- Review [Mathematical Appendices](../../appendices/mathematics.md)
- Check [FAQ](../../resources/faq.md) for common issues
- Ask questions in [Discussions](https://github.com/AmirrezaFarnamTaheri/Computational-Economics-and-Data-Science/discussions)

---

**Ready to dive in?** Start with notebook 01_Linear_Algebra.ipynb!
