import nbformat
import os

# Dictionary containing the "Gold Standard" content for each notebook
CONTENT_MAP = {
    '02_Numerical_Preliminaries.ipynb': {
        'lens': """# The Lens: The Illusion of Continuity

**What problem are we solving?**
Economic theory deals with continuous variables: prices, quantities, probabilities. We write models using real numbers ($\mathbb{R}$). But computers are discrete machines. They cannot represent the continuum. They approximate real numbers using **floating-point arithmetic**, which introduces small but cumulative errors.

**Why this method?**
Understanding the limitations of the machine is the first step in computational economics.
*   **Machine Epsilon:** The smallest difference the computer can distinguish.
*   **Round-off Error:** The error introduced by finite precision.
*   **Truncation Error:** The error introduced by approximating an infinite process (like a limit) with a finite one.

This notebook is about "knowing your tools." Before we solve complex models, we must understand how the computer counts.""",
        'summary': """# Summary

Numerical computing is the art of managing error.

**Key Takeaways:**
*   **Floats are approximations:** $0.1 + 0.2 \\neq 0.3$ in standard floating point arithmetic. Always use a tolerance (`np.isclose`) when comparing floats.
*   **Errors Accumulate:** In large iterative models (like VFI), small round-off errors can compound.
*   **Conditioning Matters:** Some mathematical formulations are numerically stable; others are not. Always prefer the stable form (e.g., `log-sum-exp` trick)."""
    },
    '03_Numerical_Differentiation.ipynb': {
        'lens': """# The Lens: The Calculus of the Discrete

**What problem are we solving?**
In economics, we constantly need derivatives. Marginal utility is a derivative ($u'(c)$). Marginal cost is a derivative ($C'(q)$). The first-order condition for optimality sets a derivative to zero. But computers don't know calculus rules; they only know arithmetic. How do we compute a derivative without an analytical formula?

**Why this method?**
**Finite Difference** methods allow us to approximate derivatives using only function evaluations.
*   **Forward Difference:** Simple but less accurate.
*   **Central Difference:** More accurate ($O(h^2)$ error) but requires two evaluations.
*   **Complex Step:** A "magic" trick that gives exact derivatives for holomorphic functions.

This notebook bridges the gap between the continuous theory of optimization and the discrete reality of the computer.""",
        'summary': """# Summary

Numerical differentiation allows us to optimize black-box functions.

**Key Takeaways:**
*   **The Step Size Dilemma:** Choosing the step size $h$ is a trade-off. Too large, and truncation error dominates. Too small, and round-off error dominates.
*   **Central Difference is Best:** For most standard applications, the central difference method offers the best balance of accuracy and cost.
*   **Automatic Differentiation:** In modern ML-driven economics (using JAX or PyTorch), we use "autodiff" to get exact derivatives efficiently, bypassing finite differences entirely."""
    },
    '04_Root_Finding.ipynb': {
        'lens': """# The Lens: Equilibrium is a Zero

**What problem are we solving?**
In economics, equilibrium is everything. A market clears when supply equals demand ($S(p) - D(p) = 0$). A firm maximizes profit where marginal revenue equals marginal cost ($MR(q) - MC(q) = 0$). A macroeconomy is in steady state when capital accumulation ceases ($s f(k) - \delta k = 0$). All of these are **root-finding problems**. We are looking for the value of a variable $x$ that makes a function $f(x)$ equal to zero.

**Why this method?**
Analytical solutions are rare. For most realistic economic models, we must find the root numerically.
*   **Bisection:** Guaranteed convergence but slow.
*   **Newton-Raphson:** Quadratic convergence (fast) but can be unstable.
*   **Brent's Method:** The industrial standard that combines the best of both.

This notebook gives you the tools to solve the fundamental equation of economics: $f(x) = 0$.""",
        'summary': """# Summary

Root finding is the computational engine of equilibrium analysis.

**Key Takeaways:**
*   **Use Brent's Method:** For scalar problems, `scipy.optimize.brentq` is the gold standard. It is robust and fast.
*   **Provide Bounds:** Algorithms work best when you can bracket the solution (e.g., knowing the price must be between 0 and 100).
*   **Newton requires Derivatives:** If you have the derivative, Newton's method is lightning fast. If not, use Secant or Brent."""
    },
    '05_Optimization.ipynb': {
        'lens': """# The Lens: The Rational Agent's Toolkit

**What problem are we solving?**
The central behavioral assumption in economics is **optimization**.
*   Households maximize utility.
*   Firms maximize profit.
*   Governments maximize social welfare.
Mathematically, this means finding the vector $x$ that maximizes (or minimizes) an objective function $f(x)$.

**Why this method?**
Optimization algorithms are the "search parties" of the mathematical landscape.
*   **Local Search (BFGS, Nelder-Mead):** Like climbing a hill in the fog. Efficient if the hill is smooth and single-peaked (convex).
*   **Global Search (Differential Evolution):** Like parachuting into a mountain range. Necessary if the landscape has many false peaks (non-convex).

This notebook explores the algorithms that allow us to model rational choice.""",
        'summary': """# Summary

Optimization is the computational implementation of rationality.

**Key Takeaways:**
*   **Convexity is King:** If your problem is convex, any local minimum is the global minimum. Standard gradient-based solvers (BFGS) work perfectly.
*   **Gradient-Free vs. Gradient-Based:** If you can compute gradients (analytically or via autodiff), always use gradient-based methods. They are orders of magnitude faster.
*   **Constraints:** Real economic problems have constraints (budget sets). Use `scipy.optimize.minimize(method='SLSQP')` or `method='trust-constr'` to handle them."""
    },
    '06_Interpolation_and_Approximation.ipynb': {
        'lens': """# The Lens: Connecting the Dots

**What problem are we solving?**
In computational economics, we often know the value of a function only at a few specific points (grid points).
*   We know the Value Function $V(k)$ at $k=10, 20, 30$.
*   But what is $V(25)$?
To evaluate the function between the grid points, we need **interpolation**.

**Why this method?**
We need to construct a continuous function from discrete data.
*   **Linear Interpolation:** Safe, shape-preserving, but not smooth.
*   **Cubic Splines:** Smooth (differentiable), but can oscillate.
*   **Chebyshev Polynomials:** The "gold standard" for smooth function approximation in macroeconomics.

This notebook teaches you how to fill in the blanks.""",
        'summary': """# Summary

Interpolation allows us to treat discrete data as continuous functions.

**Key Takeaways:**
*   **Linear is Robust:** For Value Function Iteration, linear interpolation is often preferred because it preserves monotonicity and concavity (shape-preserving).
*   **Chebyshev for Smoothness:** If you need high accuracy for a smooth function (like a policy function in a growth model), Chebyshev polynomials are incredibly efficient (spectral convergence).
*   **The Curse of Dimensionality:** Standard grids grow exponentially with dimension. For high-dimensional problems, we need sparse grids or neural networks."""
    },
    '07_Numerical_Integration.ipynb': {
        'lens': """# The Lens: Expectations as Integrals

**What problem are we solving?**
Economics is full of uncertainty. Agents make decisions based on **expectations** of the future.
*   $E[V(k')] = \int V(k') f(k') dk'$
Mathematically, an expectation is an **integral**. To solve dynamic models with risk, we must compute these integrals numerically.

**Why this method?**
We cannot sum over a continuum. We must approximate the integral as a weighted sum.
*   **Newton-Cotes (Trapezoidal):** Simple, good for smooth functions.
*   **Gaussian Quadrature:** The most efficient method for smooth functions (e.g., normal shocks).
*   **Monte Carlo:** The only feasible method for high-dimensional integrals, but convergence is slow ($1/\sqrt{N}$).

This notebook shows how to quantify the average future.""",
        'summary': """# Summary

Numerical integration bridges the gap between uncertainty and decision making.

**Key Takeaways:**
*   **Gauss-Hermite Quadrature:** The standard tool for integrating over Normally distributed shocks in macro models. It is far more efficient than Monte Carlo for low dimensions.
*   **Monte Carlo:** The "method of last resort." Use it when the dimensionality is high (> 4-5) or the domain is irregular.
*   **Discretization:** Methods like Tauchen or Rouwenhorst turn an integral into a matrix sum, simplifying dynamic programming."""
    },
    '08_Differential_Equations.ipynb': {
        'lens': """# The Lens: The Law of Motion

**What problem are we solving?**
Economic systems evolve over time.
*   Capital accumulates: $\dot{k}(t) = i(t) - \delta k(t)$
*   Populations grow: $\dot{N}(t) = n N(t)$
*   Assets price changes: $dP/P = \mu dt + \sigma dZ$
These are **Differential Equations**. They describe the *instantaneous* change of a system. To simulate the economy, we must solve for the path of the variables over time.

**Why this method?**
We need to "integrate" these equations forward in time.
*   **Euler Method:** The simplest approach. Step forward by slope $\\times$ step size.
*   **Runge-Kutta (RK4):** The industry standard. It samples the slope at multiple points to get a much more accurate step.

This notebook teaches you how to simulate the trajectory of a dynamic economy.""",
        'summary': """# Summary

Differential equations describe the mechanics of change.

**Key Takeaways:**
*   **ODE vs. SDE:** Ordinary Differential Equations (ODEs) are deterministic. Stochastic Differential Equations (SDEs) include random noise (diffusion) and require special methods (Euler-Maruyama).
*   **Stability:** Some methods (like Forward Euler) can explode if the step size is too large. Implicit methods are more stable but harder to solve.
*   **RK4 is the Workhorse:** For most deterministic economic simulations, the 4th-order Runge-Kutta method provides the best balance of accuracy and efficiency."""
    }
}

def refactor_notebook(filename, content):
    filepath = os.path.join('02-Numerical-Methods', filename)
    if not os.path.exists(filepath):
        print(f"Skipping {filename}: File not found.")
        return

    print(f"Processing {filename}...")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=4)
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        return

    # 1. Update TOC (Generic clean up)
    # We will look for the TOC cell and ensure it uses the new H1 headers if possible,
    # but since links are hard to guess, we'll focus on just ensuring the cell exists and maybe cleaning headers in it.
    # Actually, let's leave the TOC links alone but ensure the header is "### Table of Contents" or similar standard.

    # 2. Inject Lens
    # Strategy: Find existing Lens or Introduction and REPLACE it.
    lens_injected = False
    for cell in nb.cells:
        if cell.cell_type == 'markdown':
            # Check for existing Lens/Intro
            if any(x in cell.source for x in ["# The Lens", "# Introduction", "### The Lens", "### Introduction"]):
                # Verify it's not the TOC
                if "Table of Contents" not in cell.source:
                    cell.source = content['lens']
                    lens_injected = True
                    break

    if not lens_injected:
        # Insert after the first few cells (likely Imports/Setup)
        # We'll insert at index 2 or 3.
        insert_idx = 2
        # Check if index 2 is code (setup)
        if insert_idx < len(nb.cells) and nb.cells[insert_idx].cell_type == 'code':
            insert_idx += 1
        nb.cells.insert(insert_idx, nbformat.v4.new_markdown_cell(content['lens']))

    # 3. Inject Summary
    # Strategy: Find existing Summary and REPLACE it.
    summary_injected = False
    for cell in nb.cells:
        if cell.cell_type == 'markdown':
            if any(x in cell.source for x in ["# Summary", "### Summary", "## Summary", "### Conclusion"]):
                 # Avoid TOC lines
                 if "[" not in cell.source:
                     cell.source = content['summary']
                     summary_injected = True
                     break

    if not summary_injected:
        nb.cells.append(nbformat.v4.new_markdown_cell(content['summary']))

    # 4. Standardize Headers (Promote H3 to H1 for main sections if needed)
    # This is a bit risky for general sections, but we specifically want to fix "The Lens" and "Summary" which we just did via replacement.
    # Let's clean up any lingering "### The Lens" if we missed it.

    # 5. Fix Exercises Header
    for cell in nb.cells:
        if cell.cell_type == 'markdown' and "Exercises" in cell.source:
             if cell.source.strip().startswith("###"):
                 cell.source = cell.source.replace("###", "#", 1)

    # Save
    with open(filepath, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)
    print(f"  -> Success.")

def main():
    for filename, content in CONTENT_MAP.items():
        refactor_notebook(filename, content)

if __name__ == "__main__":
    main()
