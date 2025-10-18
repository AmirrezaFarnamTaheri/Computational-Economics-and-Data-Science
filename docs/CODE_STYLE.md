# Code Style Guide

## Naming Conventions
- **Classes**: PascalCase (`EconomicAgent`, `MarketSimulator`)
- **Functions**: snake_case (`solve_bellman`, `compute_equilibrium`)
- **Constants**: UPPER_SNAKE_CASE (`MAX_ITER`, `TOLERANCE`)
- **Private**: _leading_underscore (`_internal_helper`)

## Function Documentation
Use NumPy style docstrings:

```python
def solve_dp_problem(V_init, params, tol=1e-6):
    """
    Solve dynamic programming problem via value function iteration.

    Parameters
    ----------
    V_init : np.ndarray
        Initial value function guess
    params : dict
        Model parameters (beta, gamma, etc.)
    tol : float, default=1e-6
        Convergence tolerance

    Returns
    -------
    V : np.ndarray
        Converged value function
    policy : np.ndarray
        Optimal policy function

    Examples
    --------
    >>> V, policy = solve_dp_problem(V0, {'beta': 0.96})
    """
```

## Parameter Dictionaries
Always use explicit parameter dictionaries:

```python
# Good
params = {
    'beta': 0.96,      # Discount factor
    'gamma': 2.0,      # Risk aversion
    'r': 0.04          # Interest rate
}

# Bad
def solve(beta, gamma, r, delta, rho, sigma, ...):  # Too many args
```