# Code Style Guide

Follow these guidelines for writing clean, maintainable code in the course.

---

## Full Guide

The complete code style guide is available in the repository:

**[:material-file-document: View Full Code Style Guide](https://github.com/AmirrezaFarnamTaheri/Computational-Economics-and-Data-Science/blob/main/docs/CODE_STYLE.md){ .md-button .md-button--primary }**

---

## Quick Reference

### Naming Conventions

```python
# Classes: PascalCase
class EconomicAgent:
    pass

# Functions: snake_case
def solve_bellman_equation():
    pass

# Constants: UPPER_SNAKE_CASE
MAX_ITERATIONS = 1000

# Private: _leading_underscore
def _internal_helper():
    pass
```

### Documentation

**Use NumPy-style docstrings:**

```python
def present_value(fv, r, n):
    """
    Calculate present value.

    Parameters
    ----------
    fv : float
        Future value
    r : float
        Discount rate
    n : int
        Number of periods

    Returns
    -------
    float
        Present value
    """
    return fv / (1 + r) ** n
```

### Type Hints

```python
from typing import Dict, List, Tuple
import numpy as np
from numpy.typing import NDArray

def solve_model(
    params: Dict[str, float],
    grid_size: int = 100
) -> Tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Solve economic model."""
    pass
```

### Error Handling

```python
# Validate inputs
if consumption <= 0:
    raise ValueError(f"Consumption must be positive, got {consumption}")

# Specific exceptions
try:
    data = pd.read_csv(filename)
except FileNotFoundError:
    print(f"File {filename} not found")
    raise
```

### Best Practices

- ✓ Use descriptive variable names
- ✓ Keep functions small and focused
- ✓ Write tests for your code
- ✓ Add comments explaining WHY, not WHAT
- ✓ Use vectorization instead of loops
- ✓ Follow PEP 8

---

## Additional Resources

- [PEP 8](https://pep8.org/) - Python Style Guide
- [NumPy Docstring Guide](https://numpydoc.readthedocs.io/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)

---

[:material-arrow-left: Back to Resources](index.md){ .md-button }
