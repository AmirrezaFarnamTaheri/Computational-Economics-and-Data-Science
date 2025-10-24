# Module 3: Economic Modeling

Learn to solve dynamic economic models using computational methods.

---

## Overview

This module teaches you how to formulate and solve economic models computationally, with a focus on dynamic programming (DP) and optimal control. You'll master the tools needed to analyze intertemporal decision-making, optimal policies, and structural estimation.

**Duration:** 5-6 weeks
**Difficulty:** Advanced
**Prerequisites:** Modules 1-2, Dynamic optimization theory

---

## Learning Objectives

By the end of this module, you will be able to:

- ✓ Formulate economic problems as dynamic programs
- ✓ Solve discrete and continuous-state DP problems
- ✓ Implement value function iteration and policy iteration
- ✓ Handle infinite-horizon and finite-horizon problems
- ✓ Apply optimal stopping techniques
- ✓ Use robust control methods
- ✓ Perform structural estimation of economic models

---

## Topics Covered

### 1. Dynamic Programming
**Notebook:** `01_Dynamic_Programming.ipynb`

- Bellman equations and optimality principles
- Value function iteration (VFI)
- Policy function iteration (PFI)
- Modified policy iteration
- Convergence theory and error bounds
- Howard improvement algorithm

**Key Concepts:**
- Contraction mapping theorem
- Successive approximations
- Speedup techniques

**Applications:**
- Optimal savings problems
- Inventory management
- Resource extraction

---

### 2. DP with Continuous States
**Notebook:** `02_DP_with_Continuous_States.ipynb`

- Discretization methods
- Function approximation techniques
- Interpolation in DP
- Endogenous grid method (EGM)
- Time iteration vs. value iteration
- Envelope condition method

**Techniques:**
- Grid-based methods
- Collocation
- Projection methods

**Applications:**
- Consumption-savings problems
- Income fluctuation problems
- Asset accumulation models

---

### 3. Discrete-Continuous DP
**Notebook:** `03_Discrete_Continuous_DP.ipynb`

- Mixed discrete-continuous choice problems
- Logit smoothing and discrete choice
- Nested fixed point algorithm
- MPEC (Mathematical Programming with Equilibrium Constraints)
- Hotz-Miller conditional choice probabilities

**Applications:**
- Labor supply with discrete hours
- Discrete investment decisions
- Entry/exit problems
- Durable goods purchases

---

### 4. Estimation and Calibration
**Notebook:** `04_Estimation_and_Calibration.ipynb`

- Calibration vs. estimation
- Method of moments
- Simulated method of moments (SMM)
- Indirect inference
- Model validation and testing
- Sensitivity analysis

**Workflow:**
1. Specify economic model
2. Choose parameters to calibrate/estimate
3. Define moment conditions or objectives
4. Optimize to match data
5. Validate and test

**Applications:**
- Calibrating macro models
- Estimating discount factors
- Matching wealth distributions

---

### 5. Optimal Stopping Problems
**Notebook:** `05_Optimal_Stopping_Problems.ipynb`

- Theory of optimal stopping
- Reservation values and stopping rules
- Sequential decision problems
- American option pricing framework
- Search models

**Solution Methods:**
- Backward induction
- Value function approach
- Smooth pasting conditions

**Applications:**
- Job search models
- Real options
- Marriage/divorce decisions
- Technology adoption timing

---

### 6. Robust Control
**Notebook:** `06_Robust_Control.ipynb`

- Model uncertainty and robustness
- Risk-sensitivity and entropy
- Robust dynamic programming
- Worst-case analysis
- Robustness-performance tradeoffs
- Connection to risk aversion

**Mathematical Tools:**
- Multiplier preferences
- Constraint preferences
- Detection error probabilities

**Applications:**
- Robust monetary policy
- Robust portfolio choice
- Precautionary behavior
- Model diagnostics

---

### 7. Structural Estimation
**Notebook:** `07_Structural_Estimation.ipynb`

- Maximum likelihood estimation of DP models
- Nested fixed point (NFXP) algorithm
- Two-step estimation procedures
- Computational challenges
- Identification issues
- Standard errors and inference

**Advanced Topics:**
- Rust's bus engine replacement problem
- Dynamic discrete choice estimation
- Parallel computing for structural models
- Importance sampling

**Applications:**
- Estimating dynamic labor supply
- Consumer durable goods demand
- Firm dynamics and entry/exit

---

## Prerequisites

### Required Knowledge

**Economics:**
- Intermediate micro and macro
- Dynamic optimization
- Basic game theory concepts

**Mathematics:**
- Real analysis and metric spaces
- Probability theory
- Optimization theory

**Programming:**
- Modules 1-2 completed
- Comfortable with NumPy and numerical methods
- Experience with optimization algorithms

---

## Key Libraries

- **NumPy**: Array operations
- **SciPy**: Optimization and interpolation
- **QuantEcon**: Dynamic programming tools
- **Numba**: JIT compilation for speed
- **Matplotlib**: Visualization

---

## Learning Path

### Week 1: DP Foundations
- Complete notebook 01
- Master VFI and PFI
- Understand Bellman equations

### Week 2: Continuous States
- Complete notebook 02
- Implement interpolation methods
- Apply EGM

### Week 3: Mixed Problems
- Complete notebook 03
- Solve discrete-continuous problems
- Learn NFXP and MPEC

### Week 4: Calibration and Estimation
- Complete notebook 04
- Match model moments to data
- Perform sensitivity analysis

### Week 5: Optimal Stopping
- Complete notebook 05
- Solve search models
- Compute reservation values

### Week 6: Robustness and Structural Estimation
- Complete notebooks 06-07
- Implement robust control
- Estimate structural parameters

---

## Practice Exercises

Key exercises throughout the module:

1. **Cake Eating Problem**: Solve the classic optimal consumption problem
2. **Income Fluctuation**: Model precautionary savings with income risk
3. **Job Search**: Implement McCall search model with reservation wages
4. **Rust's Bus Problem**: Replicate Rust (1987) bus engine replacement
5. **Robust Policy**: Design robust policy under model misspecification
6. **Structural Estimation**: Estimate dynamic discrete choice model

---

## Computational Strategies

### Speed Optimization

**Problem**: DP problems can be computationally intensive

**Solutions:**
- Use vectorization (avoid Python loops)
- Apply Numba JIT compilation
- Exploit monotonicity and concavity
- Use coarser grids initially
- Implement smart initialization

### Numerical Stability

**Problem**: Value function iteration may diverge or be unstable

**Solutions:**
- Check contraction mapping conditions
- Use smaller step sizes
- Apply relaxation: $V_{n+1} = \lambda \tilde{V}_{n+1} + (1-\lambda) V_n$
- Monitor convergence metrics

### Curse of Dimensionality

**Problem**: State space grows exponentially with dimensions

**Solutions:**
- Reduce state space when possible
- Use sparse grids
- Apply approximation methods
- Consider simulation-based approaches

---

## Common Challenges

### Challenge: Slow Convergence in VFI
**Solutions:**
- Use policy iteration instead
- Implement acceleration techniques (Anderson mixing)
- Better initial guess from simpler model

### Challenge: Non-Smooth Value Functions
**Solutions:**
- Use finer grids near kinks
- Apply smoothing techniques
- Consider adaptive grids

### Challenge: High-Dimensional State Space
**Solutions:**
- Use endogenous grid method
- Apply simulation-based approaches
- Reduce dimensions through aggregation

---

## Resources

### Essential Reading

**Books:**
- Ljungqvist, L. & Sargent, T. (2018). *Recursive Macroeconomic Theory*, 4th ed.
- Stokey, N., Lucas, R., & Prescott, E. (1989). *Recursive Methods in Economic Dynamics*
- Adda, J. & Cooper, R. (2003). *Dynamic Economics*

**Papers:**
- Rust, J. (1987). "Optimal Replacement of GMC Bus Engines"
- Hotz, V. J. & Miller, R. A. (1993). "Conditional Choice Probabilities"
- Carroll, C. (2006). "The Method of Endogenous Gridpoints"

### Documentation
- [QuantEcon Lectures: Dynamic Programming](https://python.quantecon.org/intro.html)
- [SciPy Optimization Guide](https://docs.scipy.org/doc/scipy/reference/optimize.html)
- [Numba Documentation](https://numba.pydata.org/)

---

## Real-World Applications

This module's methods are used in:

**Academic Research:**
- Labor economics (lifecycle models)
- Macroeconomics (heterogeneous agent models)
- Industrial organization (firm dynamics)
- Public finance (tax policy analysis)

**Policy Analysis:**
- Social Security reform
- Education policy
- Healthcare decisions
- Environmental regulation

**Industry:**
- Dynamic pricing
- Inventory management
- Capacity planning
- Investment timing

---

## Assessment

To master this module, you should be able to:

- [ ] Formulate economic problems as Bellman equations
- [ ] Implement VFI and PFI efficiently
- [ ] Solve models with continuous state spaces
- [ ] Handle discrete-continuous choice problems
- [ ] Calibrate models to match data
- [ ] Apply optimal stopping techniques
- [ ] Implement robust control methods
- [ ] Estimate structural parameters

---

## Next Steps

After completing this module:

1. **Module 4: Macro Models** - Apply DP to growth and business cycle models
2. **Module 5: Micro Models** - Extend to game theory and equilibrium
3. **Module 6: Econometrics** - Advanced estimation techniques

---

## Tips for Success

1. **Start Simple**: Master deterministic problems before adding uncertainty
2. **Visualize**: Plot value and policy functions to build intuition
3. **Test**: Verify solutions with analytical benchmarks when available
4. **Optimize**: Use profiling to find bottlenecks before optimizing
5. **Document**: Keep detailed notes on algorithm convergence

---

## Need Help?

- Review [Mathematical Appendices](../../appendices/mathematics.md)
- Check [FAQ](../../resources/faq.md)
- Join [GitHub Discussions](https://github.com/AmirrezaFarnamTaheri/Computational-Economics-and-Data-Science/discussions)
- See [References](../../resources/references.md) for additional reading

---

**Ready to start?** Begin with `01_Dynamic_Programming.ipynb`!
