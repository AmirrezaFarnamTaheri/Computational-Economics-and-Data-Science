# Autograding with Otter-Grader

Learn to create auto-graded assignments for computational economics courses.

---

## Overview

This appendix teaches you how to use Otter-Grader, an open-source autograding tool for Jupyter notebooks, to create and grade programming assignments. This is invaluable for instructors teaching computational economics and students wanting to self-assess their understanding.

**Notebook:** `Appendix/02_Autograding_with_Otter.ipynb`

---

## What is Otter-Grader?

Otter-Grader is an autograding tool developed at UC Berkeley for Jupyter notebook assignments. It enables:

- **Automated Testing**: Check student code against test cases
- **Instant Feedback**: Students see test results immediately
- **Gradescope Integration**: Upload to Gradescope for grading
- **Local Grading**: Command-line grading without cloud services
- **Partial Credit**: Flexible scoring for complex problems
- **Hidden Tests**: Prevent hardcoding solutions

### Why Use Autograding in Economics?

1. **Scalability**: Grade hundreds of submissions automatically
2. **Consistency**: Same standards applied to all students
3. **Instant Feedback**: Students learn from mistakes immediately
4. **Time Savings**: Instructors focus on conceptual help, not syntax errors
5. **Academic Integrity**: Harder to share solutions (hidden tests)

---

## Installation

```bash
# Install Otter-Grader
pip install otter-grader

# Verify installation
otter --version

# Optional: Gradescope integration
pip install otter-grader[gradescope]
```

---

## Workflow Overview

### Instructor Workflow

1. **Create Master Notebook**: Write problems with solutions
2. **Add Tests**: Write test cases for each question
3. **Generate Assignment**: Use Otter to create student version
4. **Distribute**: Share student notebook (tests included)
5. **Collect Submissions**: Via LMS or file upload
6. **Grade**: Run Otter on submissions
7. **Return**: Share results with students

### Student Workflow

1. **Receive Assignment**: Download notebook
2. **Complete Problems**: Write code in designated cells
3. **Run Tests**: Execute test cells to check work
4. **Submit**: Upload completed notebook
5. **Receive Feedback**: View autograder results

---

## Creating Assignments

### Basic Structure

```python
# Master notebook: assignment.ipynb

## Question 1: OLS Estimation

Implement ordinary least squares regression.

# BEGIN SOLUTION
import numpy as np

def ols(X, y):
    """
    Compute OLS estimator.

    Parameters
    ----------
    X : np.ndarray
        Design matrix (n x k)
    y : np.ndarray
        Dependent variable (n x 1)

    Returns
    -------
    beta_hat : np.ndarray
        OLS estimates (k x 1)
    """
    return np.linalg.inv(X.T @ X) @ X.T @ y
# END SOLUTION

# BEGIN TESTS
import numpy as np
from numpy.testing import assert_array_almost_equal

# Test 1: Simple case
X_test = np.array([[1, 1], [1, 2], [1, 3]])
y_test = np.array([[1], [2], [3]])
beta_expected = np.array([[0], [1]])
assert_array_almost_equal(ols(X_test, y_test), beta_expected, decimal=6)

# Test 2: Different data
X_test2 = np.array([[1, 2], [1, 4], [1, 6]])
y_test2 = np.array([[3], [5], [7]])
beta_expected2 = np.array([[1], [1]])
assert_array_almost_equal(ols(X_test2, y_test2), beta_expected2, decimal=6)
# END TESTS
```

### Generate Student Version

```bash
# Generate student notebook (removes solutions)
otter assign assignment.ipynb output_dir/

# This creates:
# - autograder.zip (for Gradescope)
# - student/ (student notebooks)
# - .otter (grading config)
```

The student version will have:

```python
## Question 1: OLS Estimation

Implement ordinary least squares regression.

def ols(X, y):
    """
    Compute OLS estimator.

    Parameters
    ----------
    X : np.ndarray
        Design matrix (n x k)
    y : np.ndarray
        Dependent variable (n x 1)

    Returns
    -------
    beta_hat : np.ndarray
        OLS estimates (k x 1)
    """
    # YOUR CODE HERE
    raise NotImplementedError()
```

---

## Test Design

### Test Cell Format

```python
# HIDDEN
# This test is hidden from students
import numpy as np
from numpy.testing import assert_allclose

X = np.random.randn(100, 5)
beta_true = np.array([1, 2, 3, 4, 5])
y = X @ beta_true + np.random.randn(100) * 0.1

beta_hat = ols(X, y)
assert_allclose(beta_hat, beta_true, atol=0.5)
```

Test types:

- **Public Tests**: Visible to students (basic checks)
- **Hidden Tests**: Run during grading only (prevent hardcoding)
- **Edge Cases**: Empty arrays, singular matrices, etc.

### Best Practices

1. **Test Incrementally**: Start with simple cases, then complex
2. **Use Multiple Tests**: Different data, edge cases
3. **Informative Errors**: Help students debug
4. **Hidden Tests**: At least 50% should be hidden
5. **Partial Credit**: Use `@points()` decorator

---

## Otter Configuration

Create `.otter` file:

```yaml
name: "Computational Economics Problem Set 1"
solutions_pdf: false
export_cell: true
seed: 42
generate: true
save_environment: false
variables:
  tolerance: 0.01

tests:
  q1:
    name: "OLS Estimation"
    points: 10
  q2:
    name: "GMM Estimation"
    points: 15
  q3:
    name: "Bootstrap Inference"
    points: 20
```

---

## Advanced Features

### Partial Credit

```python
# BEGIN SOLUTION
def gmm_estimation(X, y, W):
    """GMM estimator implementation"""
    # Step 1: Compute moments (5 points)
    moments = compute_moments(X, y)

    # Step 2: Optimize (5 points)
    theta_hat = minimize_objective(moments, W)

    return theta_hat
# END SOLUTION

# BEGIN TESTS
# @points(5)
# Test moments computation
assert moments.shape == (10, 1)

# @points(5)
# Test optimization
assert np.linalg.norm(gradient(theta_hat)) < 1e-6
# END TESTS
```

### Custom Test Functions

```python
# In otter_config.py
def check_convergence(result, tol=1e-6):
    """Custom test for convergence"""
    return result['converged'] and result['fun'] < tol

def check_economic_interpretation(beta, X):
    """Check if estimates make economic sense"""
    # Marginal effects should be reasonable
    return all(beta > 0) and all(beta < 100)
```

### Hidden Tests

```python
# HIDDEN TEST
# This test is not visible in student notebook
import numpy as np

# Use different random seed
np.random.seed(9999)
X_hidden = np.random.randn(200, 10)
y_hidden = X_hidden @ np.ones(10) + np.random.randn(200)

beta_student = ols(X_hidden, y_hidden)
assert beta_student.shape == (10, 1)
assert np.allclose(beta_student, np.ones((10, 1)), atol=0.5)
```

---

## Grading Submissions

### Local Grading

```bash
# Grade all submissions in a directory
otter grade -p submissions/ -a autograder.zip -o results/

# Grade single submission
otter grade -p student_submission.ipynb -a autograder.zip

# Export grades to CSV
otter export results/ --csv grades.csv
```

### Gradescope Integration

1. **Upload Autograder**: Upload `autograder.zip` to Gradescope
2. **Configure**: Set language to Python, timeout, etc.
3. **Students Submit**: Upload `.ipynb` files
4. **Automatic Grading**: Gradescope runs tests
5. **Manual Grading**: Review and adjust as needed

---

## Example Economics Problems

### Problem 1: Optimization

```python
## Question: Utility Maximization

# Implement utility maximization subject to budget constraint
# U(x, y) = x^α * y^(1-α)
# Subject to: p_x * x + p_y * y = I

# BEGIN SOLUTION
from scipy.optimize import minimize

def utility_max(alpha, p_x, p_y, I):
    """
    Find optimal consumption bundle.

    Returns (x*, y*)
    """
    # Analytical solution (Cobb-Douglas)
    x_star = alpha * I / p_x
    y_star = (1 - alpha) * I / p_y
    return x_star, y_star
# END SOLUTION

# BEGIN TESTS
x, y = utility_max(0.5, 2, 3, 100)
assert abs(x - 25) < 0.01
assert abs(y - 16.67) < 0.01

# Check budget constraint
assert abs(2*x + 3*y - 100) < 0.01
# END TESTS
```

### Problem 2: Dynamic Programming

```python
## Question: Value Function Iteration

# Implement VFI for consumption-savings problem

# BEGIN SOLUTION
def value_function_iteration(beta, grid, u, tol=1e-6):
    """
    Solve consumption-savings problem via VFI.

    Parameters
    ----------
    beta : float
        Discount factor
    grid : np.ndarray
        State space grid
    u : callable
        Utility function

    Returns
    -------
    V : np.ndarray
        Value function
    policy : np.ndarray
        Policy function
    """
    n = len(grid)
    V = np.zeros(n)
    V_new = np.zeros(n)
    policy = np.zeros(n, dtype=int)

    while True:
        for i in range(n):
            candidates = np.array([
                u(grid[i] - grid[j]) + beta * V[j]
                for j in range(i+1)  # Feasible choices
            ])
            V_new[i] = np.max(candidates)
            policy[i] = np.argmax(candidates)

        if np.max(np.abs(V_new - V)) < tol:
            break
        V = V_new.copy()

    return V, policy
# END SOLUTION

# BEGIN TESTS
# Test convergence
beta = 0.95
grid = np.linspace(0, 10, 50)
u = lambda c: np.log(c + 1e-10)

V, policy = value_function_iteration(beta, grid, u)

# V should be increasing
assert all(np.diff(V) > 0)

# Policy should be weakly increasing
assert all(np.diff(policy) >= 0)

# Check Bellman equation approximately holds
# END TESTS
```

### Problem 3: Econometrics

```python
## Question: Difference-in-Differences

# Implement DiD estimator

# BEGIN SOLUTION
import pandas as pd

def did_estimator(data):
    """
    Compute 2x2 DiD estimator.

    Parameters
    ----------
    data : pd.DataFrame
        Must have columns: outcome, treated, post

    Returns
    -------
    float
        DiD estimate
    """
    # Average outcomes by group and time
    y_treated_post = data[(data['treated']==1) & (data['post']==1)]['outcome'].mean()
    y_treated_pre = data[(data['treated']==1) & (data['post']==0)]['outcome'].mean()
    y_control_post = data[(data['treated']==0) & (data['post']==1)]['outcome'].mean()
    y_control_pre = data[(data['treated']==0) & (data['post']==0)]['outcome'].mean()

    did = (y_treated_post - y_treated_pre) - (y_control_post - y_control_pre)
    return did
# END SOLUTION

# BEGIN TESTS
# Create test data
np.random.seed(42)
n = 1000
test_data = pd.DataFrame({
    'treated': np.repeat([0, 1], n//2),
    'post': np.tile([0, 1], n//2),
    'outcome': np.random.randn(n)
})
# Add treatment effect
test_data.loc[(test_data['treated']==1) & (test_data['post']==1), 'outcome'] += 5

estimate = did_estimator(test_data)
assert 4 < estimate < 6  # True effect is 5
# END TESTS
```

---

## Tips for Effective Autograding

### For Instructors

1. **Clear Instructions**: Specify function signatures, return types
2. **Multiple Tests**: Cover normal cases and edge cases
3. **Informative Messages**: Help students debug
4. **Hidden Tests**: Prevent solution sharing
5. **Partial Credit**: Reward correct partial solutions
6. **Time Limits**: Prevent infinite loops
7. **Documentation**: Require docstrings

### For Students

1. **Read Instructions**: Understand what's expected
2. **Test Locally**: Run test cells before submitting
3. **Start Simple**: Get basic version working first
4. **Check Types**: Ensure correct return types
5. **Handle Edge Cases**: Empty inputs, zeros, etc.
6. **Don't Hardcode**: Tests use different data
7. **Document**: Write clear code and comments

---

## Common Pitfalls

### Pitfall: Hardcoding Solutions
**Student tries**: `return np.array([0, 1])` to pass specific test

**Prevention**: Use hidden tests with different data

### Pitfall: Type Mismatches
**Student returns**: List instead of NumPy array

**Prevention**: Specify exact return types, test with `isinstance()`

### Pitfall: Floating Point Errors
**Student fails**: `assert x == 0.3` fails due to rounding

**Prevention**: Use `np.allclose()` or `assert_almost_equal()`

### Pitfall: Random Seed Issues
**Inconsistent results** across runs

**Prevention**: Set `np.random.seed()` in tests

---

## Integration with Course

### Weekly Problem Sets

```
ps1/
├── ps1.ipynb              # Master with solutions
├── ps1_student.ipynb      # Generated for students
├── tests/                 # Test files
│   ├── q1.py
│   ├── q2.py
│   └── q3.py
├── data/                  # Data files
│   └── dataset.csv
└── autograder.zip        # For Gradescope
```

### Gradebook Management

```python
# Merge Otter results with LMS gradebook
import pandas as pd

otter_results = pd.read_csv('otter_results.csv')
gradebook = pd.read_csv('lms_export.csv')

merged = gradebook.merge(otter_results, on='student_id')
merged.to_csv('updated_gradebook.csv', index=False)
```

---

## Resources

### Documentation
- [Otter-Grader Docs](https://otter-grader.readthedocs.io/)
- [Gradescope Integration Guide](https://otter-grader.readthedocs.io/en/latest/gradescope.html)

### Examples
- [Data 8 Assignments](https://github.com/data-8/materials-sp22) - UC Berkeley
- [Data 100 Assignments](https://github.com/DS-100/sp22) - UC Berkeley

### Community
- [Otter-Grader GitHub](https://github.com/ucbds-infra/otter-grader)
- [Discussions](https://github.com/ucbds-infra/otter-grader/discussions)

---

## Alternatives

### Other Autograding Tools

- **nbgrader**: Full-featured but more complex
- **OK**: Another Berkeley tool, older
- **Papermill**: Notebook parameterization and execution
- **Custom Scripts**: Roll your own with unittest

### When to Use Otter

✅ **Use Otter when**:
- Teaching large classes
- Want Gradescope integration
- Need hidden tests
- Prefer simple setup

❌ **Consider alternatives when**:
- Very small class (manual grading okay)
- Need complex rubrics
- Want more customization
- Using JupyterHub with nbgrader

---

## Assessment

After this appendix, you should be able to:

- [ ] Install and configure Otter-Grader
- [ ] Create master notebooks with solutions and tests
- [ ] Generate student versions of assignments
- [ ] Write effective test cases (public and hidden)
- [ ] Grade submissions locally
- [ ] Integrate with Gradescope
- [ ] Provide meaningful feedback to students
- [ ] Design problems suitable for autograding

---

## Practice Exercises

1. **Simple Assignment**: Create 3-question assignment on Python basics
2. **Economics Problem**: Auto-graded OLS implementation
3. **Hidden Tests**: Add hidden tests to prevent hardcoding
4. **Gradescope**: Upload and test autograder.zip
5. **Grade Local**: Practice grading sample submissions
6. **Full Problem Set**: Create complete problem set for your course

---

## Ethical Considerations

### Academic Integrity

- **Don't Over-Rely**: Autograding complements, doesn't replace, human judgment
- **Partial Credit**: Recognize partial understanding
- **Second Chances**: Allow resubmissions for learning
- **Accessibility**: Ensure tests work for all students

### Transparency

- **Share Rubrics**: Students should know how they're graded
- **Explain Tests**: Demystify the grading process
- **Provide Examples**: Show what good solutions look like

---

## Need Help?

- Work through `Appendix/02_Autograding_with_Otter.ipynb`
- Check [Otter Documentation](https://otter-grader.readthedocs.io/)
- Ask on [GitHub Discussions](https://github.com/ucbds-infra/otter-grader/discussions)
- Post in [Course Discussions](https://github.com/AmirrezaFarnamTaheri/Computational-Economics-and-Data-Science/discussions)

---

**Automate grading to focus on teaching economics, not debugging syntax!**
