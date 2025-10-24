# Code Style Guide

This document outlines the coding standards and best practices for the Computational Economics and Data Science course materials.

## Table of Contents
1. [Naming Conventions](#naming-conventions)
2. [Documentation](#documentation)
3. [Type Hints](#type-hints)
4. [Function Design](#function-design)
5. [Error Handling](#error-handling)
6. [Testing](#testing)
7. [Performance](#performance)
8. [NumPy and Scientific Computing](#numpy-and-scientific-computing)
9. [Jupyter Notebooks](#jupyter-notebooks)
10. [Import Organization](#import-organization)

---

## Naming Conventions

### General Rules
- **Classes**: PascalCase (`EconomicAgent`, `MarketSimulator`, `DSGEModel`)
- **Functions/Methods**: snake_case (`solve_bellman`, `compute_equilibrium`, `calculate_pv`)
- **Variables**: snake_case (`discount_factor`, `price_level`, `value_function`)
- **Constants**: UPPER_SNAKE_CASE (`MAX_ITER`, `TOLERANCE`, `DEFAULT_PARAMS`)
- **Private attributes/methods**: _leading_underscore (`_internal_helper`, `_cache`)
- **"Magic" methods**: Double underscore (`__init__`, `__repr__`)

### Economics-Specific Conventions
```python
# Good: Clear, domain-specific names
beta = 0.96              # Discount factor
gamma = 2.0              # CRRA coefficient
capital_stock = 100.0    # Current capital
value_function = np.zeros(n)

# Bad: Vague or confusing names
b = 0.96
g = 2.0
k = 100.0
v = np.zeros(n)
```

### Abbreviations
Use standard economics abbreviations, but define them:
```python
# Standard abbreviations (acceptable)
gdp = compute_gdp()       # Gross Domestic Product
cpi = get_inflation()     # Consumer Price Index
var_model = VAR(data)     # Vector Autoregression

# Define less common abbreviations in docstrings
def compute_efp(params):
    """Compute External Finance Premium (EFP)."""
    pass
```

---

## Documentation

### Docstring Style
**Always use NumPy-style docstrings** for consistency with scientific Python ecosystem.

#### Function Documentation
```python
def solve_dp_problem(V_init, params, tol=1e-6, max_iter=1000):
    """
    Solve dynamic programming problem via value function iteration.

    This function implements the standard value function iteration algorithm
    for discrete-state dynamic programming problems. It iterates until
    convergence or maximum iterations are reached.

    Parameters
    ----------
    V_init : np.ndarray
        Initial value function guess, shape (n_states,)
    params : dict
        Model parameters containing:
        - 'beta' : float, discount factor
        - 'gamma' : float, risk aversion coefficient
        - Additional model-specific parameters
    tol : float, default=1e-6
        Convergence tolerance for sup norm
    max_iter : int, default=1000
        Maximum number of iterations

    Returns
    -------
    V : np.ndarray
        Converged value function, shape (n_states,)
    policy : np.ndarray
        Optimal policy function (indices), shape (n_states,)
    converged : bool
        Whether algorithm converged

    Raises
    ------
    ValueError
        If V_init has wrong shape or params missing required keys
    RuntimeError
        If algorithm fails to converge within max_iter

    Notes
    -----
    The algorithm implements the Bellman operator:
    .. math::
        T(V)(s) = \max_{a} u(s, a) + \beta \sum_{s'} P(s'|s, a) V(s')

    References
    ----------
    .. [1] Stokey, Lucas, and Prescott (1989), "Recursive Methods in
           Economic Dynamics"

    Examples
    --------
    >>> params = {'beta': 0.96, 'gamma': 2.0}
    >>> V0 = np.zeros(100)
    >>> V, policy, converged = solve_dp_problem(V0, params)
    >>> print(f"Converged: {converged}")
    Converged: True
    """
    pass
```

#### Class Documentation
```python
class DSGEModel:
    """
    Dynamic Stochastic General Equilibrium model solver.

    This class provides methods for solving and simulating linear
    DSGE models using the Klein (2000) solution method.

    Parameters
    ----------
    equations : list of str
        Model equations in string format
    parameters : dict
        Calibrated parameter values
    shock_std : dict, optional
        Standard deviations of shocks

    Attributes
    ----------
    n_vars : int
        Number of endogenous variables
    solution : dict
        Solved policy and transition matrices
    is_solved : bool
        Whether model has been solved

    Methods
    -------
    solve()
        Solve the model using Klein method
    impulse_response(shock_name, periods=40)
        Generate impulse response functions
    simulate(T=1000, burn=100)
        Simulate model time series

    Examples
    --------
    >>> model = DSGEModel(equations, params)
    >>> model.solve()
    >>> irfs = model.impulse_response('technology', periods=50)

    References
    ----------
    .. [1] Klein, P. (2000). "Using the generalized Schur form to solve
           a multivariate linear rational expectations model." Journal of
           Economic Dynamics and Control, 24(10), 1405-1423.
    """
    pass
```

### Inline Comments
```python
# Good: Explain WHY, not WHAT
# Use Euler equation approximation to avoid solving implicit equation
consumption = income - savings  # Budget constraint

# Bad: Obvious comment
# Set x to 5
x = 5
```

---

## Type Hints

Use type hints for function signatures to improve code clarity and enable static analysis.

### Basic Type Hints
```python
from typing import Optional, Union, List, Dict, Tuple, Callable
import numpy as np
import pandas as pd
from numpy.typing import NDArray

def calculate_pv(
    fv: float,
    r: float,
    n: int
) -> float:
    """Calculate present value."""
    return fv / (1 + r) ** n

def solve_model(
    params: Dict[str, float],
    grid_size: int = 100,
    tol: float = 1e-6
) -> Tuple[NDArray[np.float64], NDArray[np.float64]]:
    """
    Solve economic model.

    Returns
    -------
    value_function : NDArray[np.float64]
        Value function on grid
    policy_function : NDArray[np.float64]
        Policy function on grid
    """
    pass
```

### Advanced Type Hints
```python
from typing import Protocol, TypeVar, Generic

# Protocol for callables
class UtilityFunction(Protocol):
    def __call__(self, consumption: float, labor: float) -> float: ...

# Generic types
T = TypeVar('T', bound=np.ndarray)

def normalize(data: T) -> T:
    """Normalize data preserving type."""
    return data / data.sum()
```

---

## Function Design

### Parameter Dictionaries
For functions with many parameters (>5), use parameter dictionaries:

```python
# Good: Parameter dictionary
def rbc_model(params: Dict[str, float]) -> Dict[str, NDArray]:
    """
    Solve RBC model.

    Parameters
    ----------
    params : dict
        Model parameters:
        - 'beta' : float, discount factor (0 < beta < 1)
        - 'alpha' : float, capital share (0 < alpha < 1)
        - 'delta' : float, depreciation rate (0 < delta < 1)
        - 'sigma' : float, risk aversion (sigma > 0)
        - 'rho' : float, TFP persistence (0 < rho < 1)
        - 'sigma_eps' : float, TFP shock std dev (sigma_eps > 0)
    """
    beta = params['beta']
    alpha = params['alpha']
    # ... model solution ...
    return {'capital': k_grid, 'consumption': c_grid}

# Bad: Too many positional arguments
def rbc_model(beta, alpha, delta, sigma, rho, sigma_eps, gamma, phi, psi):
    pass
```

### Default Parameters
```python
# Good: Sensible defaults in signature
def value_iteration(
    bellman_operator: Callable,
    V_init: NDArray,
    tol: float = 1e-6,
    max_iter: int = 1000,
    verbose: bool = False
) -> Tuple[NDArray, bool]:
    """Value function iteration with clear defaults."""
    pass

# Bad: Mutable default arguments
def bad_function(data, cache={}):  # DON'T DO THIS!
    pass

# Good: Use None and create in function
def good_function(data, cache=None):
    if cache is None:
        cache = {}
    pass
```

### Return Values
```python
# Good: Return dictionary for multiple values with clear names
def estimate_model(data):
    results = {
        'coefficients': beta_hat,
        'std_errors': se,
        'r_squared': r2,
        'residuals': resid
    }
    return results

# Also good: Named tuple
from collections import namedtuple
RegressionResults = namedtuple('RegressionResults',
                               ['coefficients', 'std_errors', 'r_squared'])

def estimate_model(data):
    return RegressionResults(beta_hat, se, r2)
```

---

## Error Handling

### Validation
Always validate inputs for economic models:

```python
def utility(c: float, gamma: float) -> float:
    """
    CRRA utility function.

    Parameters
    ----------
    c : float
        Consumption (must be positive)
    gamma : float
        Risk aversion coefficient (must be positive)

    Raises
    ------
    ValueError
        If c <= 0 or gamma <= 0
    """
    if c <= 0:
        raise ValueError(f"Consumption must be positive, got {c}")
    if gamma <= 0:
        raise ValueError(f"Risk aversion must be positive, got {gamma}")

    if gamma == 1:
        return np.log(c)
    else:
        return (c ** (1 - gamma) - 1) / (1 - gamma)
```

### Exception Handling
```python
# Good: Specific exceptions
try:
    data = pd.read_csv(filename)
except FileNotFoundError:
    print(f"Data file {filename} not found")
    raise
except pd.errors.ParserError:
    print(f"Could not parse {filename}")
    raise

# Bad: Bare except
try:
    data = pd.read_csv(filename)
except:  # DON'T DO THIS
    pass
```

### Custom Exceptions
```python
class ConvergenceError(Exception):
    """Raised when numerical algorithm fails to converge."""
    pass

class ModelSpecificationError(Exception):
    """Raised when model is incorrectly specified."""
    pass

def solve_model(params):
    for iteration in range(max_iter):
        # ... solution code ...
        if converged:
            return solution

    raise ConvergenceError(
        f"Algorithm did not converge after {max_iter} iterations. "
        f"Final error: {error:.2e}"
    )
```

---

## Testing

### Test Organization
```python
# test_module.py
import pytest
import numpy as np
from module import function_to_test


class TestFunctionName:
    """Tests for function_name."""

    def test_standard_case(self):
        """Test with standard inputs."""
        result = function_to_test(10, 0.05)
        assert result == pytest.approx(9.5238, rel=1e-4)

    def test_edge_case_zero(self):
        """Test with zero input."""
        result = function_to_test(0, 0.05)
        assert result == 0

    def test_raises_on_negative(self):
        """Test that negative input raises ValueError."""
        with pytest.raises(ValueError):
            function_to_test(-1, 0.05)

    @pytest.mark.parametrize("input,expected", [
        (10, 9.52),
        (100, 95.24),
        (1000, 952.38),
    ])
    def test_parametrized(self, input, expected):
        """Parametrized tests."""
        result = function_to_test(input, 0.05)
        assert result == pytest.approx(expected, rel=1e-2)
```

---

## Performance

### NumPy Vectorization
```python
# Good: Vectorized operations
def crra_utility(c: NDArray, gamma: float) -> NDArray:
    """Vectorized CRRA utility."""
    if gamma == 1:
        return np.log(c)
    else:
        return (c ** (1 - gamma) - 1) / (1 - gamma)

# Bad: Loops over arrays
def crra_utility_slow(c: NDArray, gamma: float) -> NDArray:
    u = np.zeros_like(c)
    for i in range(len(c)):  # SLOW!
        if gamma == 1:
            u[i] = np.log(c[i])
        else:
            u[i] = (c[i] ** (1 - gamma) - 1) / (1 - gamma)
    return u
```

### Numba for Loops
```python
from numba import jit, njit

@njit
def value_iteration_step(V, states, actions, params):
    """
    JIT-compiled value iteration step.

    Note: Only use @njit for functions that don't call
    unsupported libraries (e.g., scipy.stats).
    """
    V_new = np.zeros_like(V)
    for i in range(len(states)):
        max_val = -np.inf
        for a in actions:
            val = utility(states[i], a) + params['beta'] * V[i]
            if val > max_val:
                max_val = val
        V_new[i] = max_val
    return V_new
```

---

## NumPy and Scientific Computing

### Array Creation
```python
# Good: Specify dtype for clarity
grid = np.linspace(0, 10, 100, dtype=np.float64)
indices = np.arange(10, dtype=np.int32)

# Preallocate arrays
results = np.empty((1000, 50), dtype=np.float64)

# Use zeros/ones with explicit shapes
value_function = np.zeros((n_states, n_actions))
```

### Broadcasting
```python
# Leverage broadcasting for cleaner code
prices = np.array([[10], [20], [30]])  # shape (3, 1)
quantities = np.array([1, 2, 3, 4])    # shape (4,)

# Automatic broadcasting: (3, 1) × (4,) → (3, 4)
revenues = prices * quantities
```

### Numerical Stability
```python
# Good: Log-sum-exp trick
def log_sum_exp(x):
    """Numerically stable log-sum-exp."""
    c = x.max()
    return c + np.log(np.sum(np.exp(x - c)))

# Good: Avoid dividing by potentially small numbers
def safe_divide(a, b, fill=0.0):
    """Division with fallback for division by zero."""
    return np.divide(a, b, out=np.full_like(a, fill), where=b != 0)
```

---

## Jupyter Notebooks

### Cell Organization
1. **Imports cell** - All imports at the top
2. **Configuration cell** - Plotting settings, random seeds
3. **Functions/classes** - Reusable code
4. **Analysis cells** - One concept per cell
5. **Visualization cells** - Separate plotting from computation

### Notebook Structure
```python
# Cell 1: Imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import optimize

# Cell 2: Configuration
%matplotlib inline
plt.style.use('seaborn-v0_8-darkgrid')
np.random.seed(42)
pd.options.display.max_rows = 100

# Cell 3: Functions
def compute_equilibrium(params):
    """Compute market equilibrium."""
    pass

# Cell 4: Analysis
params = {'alpha': 0.3, 'beta': 0.96}
result = compute_equilibrium(params)

# Cell 5: Visualization
fig, ax = plt.subplots()
ax.plot(result['prices'])
ax.set_title('Equilibrium Prices')
plt.show()
```

### Markdown Cells
- Use headers to structure content
- Include mathematical notation in LaTeX: `$\beta$` or `$$E[x]$$`
- Add explanations before code cells
- Include references and citations

---

## Import Organization

### Import Order (PEP 8)
```python
# 1. Standard library imports
import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple

# 2. Third-party imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import optimize, stats

# 3. Local application imports
from models.dsge import DSGEModel
from utils.plotting import plot_irf
```

### Avoid Wildcard Imports
```python
# Bad
from numpy import *
from scipy.stats import *

# Good
import numpy as np
from scipy.stats import norm, t
```

---

## Additional Best Practices

### Magic Numbers
```python
# Bad
result = value * 0.05

# Good
DISCOUNT_RATE = 0.05
result = value * DISCOUNT_RATE
```

### List/Dict Comprehensions
```python
# Good: Readable comprehensions
squared = [x**2 for x in range(10)]
params = {k: v * 1.1 for k, v in old_params.items() if v > 0}

# Bad: Overly complex comprehensions (use regular loops instead)
result = [f(g(h(x))) for x in data if condition1(x) and condition2(x)]
```

### F-strings for Formatting
```python
# Good: F-strings (Python 3.6+)
name = "GDP"
value = 1234.56
print(f"{name}: ${value:,.2f}")

# Also good for expressions
print(f"Mean: {np.mean(data):.3f}")
```

---

## Summary Checklist

- [ ] Use descriptive, domain-appropriate variable names
- [ ] Include NumPy-style docstrings for all public functions
- [ ] Add type hints to function signatures
- [ ] Validate inputs and handle errors explicitly
- [ ] Write tests for edge cases and standard cases
- [ ] Vectorize operations instead of using loops
- [ ] Document parameter dictionaries thoroughly
- [ ] Organize imports following PEP 8
- [ ] Use f-strings for string formatting
- [ ] Follow PEP 8 style guidelines
