# Module 4: Macroeconomic Models

Apply computational methods to modern macroeconomic theory and policy analysis.

---

## Overview

This module covers the core models of modern macroeconomics, from growth theory to business cycle models. You'll learn to solve, simulate, and estimate canonical macroeconomic models using the computational techniques from previous modules.

**Duration:** 6-7 weeks
**Difficulty:** Advanced
**Prerequisites:** Modules 1-3, Intermediate Macroeconomics

---

## Learning Objectives

By the end of this module, you will be able to:

- ✓ Solve and simulate growth models computationally
- ✓ Build and analyze Real Business Cycle (RBC) models
- ✓ Implement overlapping generations (OLG) models
- ✓ Solve New Keynesian DSGE models
- ✓ Work with heterogeneous agent macroeconomic models
- ✓ Analyze endogenous growth mechanisms
- ✓ Apply models to policy questions

---

## Topics Covered

### 1. Job Search Models
**Notebook:** `01_Job_Search.ipynb`

- McCall search model
- Sequential search with learning
- On-the-job search
- Wage posting and bargaining
- Unemployment duration analysis
- Reservation wage dynamics

**Policy Applications:**
- Unemployment insurance design
- Active labor market policies
- Minimum wage effects

**Computational Methods:**
- Dynamic programming with continuous wages
- Stationary distributions
- Monte Carlo simulation

---

### 2. Neoclassical Growth Models
**Notebook:** `02_Neoclassical_Growth.ipynb`

- Solow-Swan growth model
- Ramsey-Cass-Koopmans model
- Optimal growth with uncertainty
- Stochastic growth models
- Convergence dynamics
- Transitional dynamics

**Key Concepts:**
- Steady state analysis
- Golden rule of capital accumulation
- Saddle-path stability
- Policy functions

**Applications:**
- Long-run growth determinants
- Capital accumulation paths
- Convergence predictions

---

### 3. Real Business Cycle (RBC) Models
**Notebook:** `03_RBC_Models.ipynb`

- Basic RBC framework
- Technology shocks and business cycles
- Log-linearization methods
- Impulse response functions
- Moment matching
- Model calibration

**Solution Methods:**
- Perturbation methods
- Value function iteration
- Linear-quadratic approximation

**Empirical Analysis:**
- Business cycle statistics
- Volatilities and correlations
- Model vs. data comparison

---

### 4. Overlapping Generations (OLG) Models
**Notebook:** `04_OLG_Models.ipynb`

- Diamond OLG model
- Lifecycle consumption and saving
- Social Security systems
- Dynamic inefficiency
- Pay-as-you-go vs. funded pensions
- Intergenerational redistribution

**Computational Challenges:**
- Solving for equilibrium
- Multiple steady states
- Transitional dynamics with many cohorts

**Policy Questions:**
- Pension reform effects
- Demographic transitions
- Government debt sustainability

---

### 5. New Keynesian Models
**Notebook:** `05_New_Keynesian_Models.ipynb`

- Sticky prices and nominal rigidities
- New Keynesian Phillips Curve
- Monetary policy rules (Taylor rule)
- Zero lower bound on interest rates
- Forward guidance
- Fiscal policy multipliers

**Solution Techniques:**
- Log-linearization around steady state
- Blanchard-Kahn conditions
- Solving linear rational expectations models

**Applications:**
- Optimal monetary policy
- Effects of interest rate changes
- Inflation dynamics

---

### 6. Heterogeneous Agent Models (HANK)
**Notebook:** `06_Heterogeneous_Agent_Models.ipynb`

- Aiyagari model
- Income and wealth inequality
- Incomplete markets and idiosyncratic risk
- Precautionary savings
- General equilibrium with heterogeneity
- Distribution dynamics

**Advanced Topics:**
- Aggregate shocks in HA models
- Transition paths
- Computational methods for HA models
- Sequence-space Jacobians

**Policy Analysis:**
- Fiscal stimulus effectiveness
- Redistribution policies
- Financial regulation

---

### 7. Endogenous Growth Models
**Notebook:** `08_Endogenous_Growth.ipynb`

- AK models
- Romer's product variety model
- Schumpeterian growth (creative destruction)
- Human capital accumulation
- R&D and innovation
- Knowledge spillovers

**Computational Techniques:**
- Balanced growth paths
- Transitional dynamics
- Calibration to growth facts

**Applications:**
- Innovation policy
- Education investment
- Patent protection
- Technology diffusion

---

## Prerequisites

### Required Knowledge

**Economics:**
- **Essential**: Intermediate macro (IS-LM, AS-AD, Solow model)
- **Helpful**: Graduate macro (dynamic optimization, rational expectations)

**Mathematics:**
- Dynamic optimization and optimal control
- Stochastic processes
- Linear algebra

**Programming:**
- Modules 1-3 completed
- Dynamic programming proficiency
- Numerical methods mastery

---

## Key Libraries

- **QuantEcon**: Macroeconomic models and tools
- **NumPy/SciPy**: Numerical computations
- **Numba**: Performance optimization
- **Matplotlib/Seaborn**: Visualization
- **Statsmodels**: Time series analysis

---

## Learning Path

### Week 1: Search and Growth Foundations
- Complete notebooks 01-02
- Understand baseline models
- Master steady-state computation

### Week 2: RBC Models
- Complete notebook 03
- Learn linearization techniques
- Match business cycle moments

### Week 3: OLG Models
- Complete notebook 04
- Solve for equilibrium
- Analyze policy changes

### Week 4: New Keynesian Framework
- Complete notebook 05
- Implement monetary policy rules
- Compute impulse responses

### Week 5-6: Heterogeneous Agents
- Complete notebook 06
- Solve Aiyagari model
- Compute stationary distributions

### Week 7: Endogenous Growth
- Complete notebook 08
- Model innovation
- Analyze growth policies

---

## Practice Exercises

Key exercises in this module:

1. **Calibrate RBC Model**: Match US business cycle statistics
2. **Social Security Reform**: Analyze welfare effects in OLG model
3. **Monetary Policy**: Design optimal Taylor rule in NK model
4. **Wealth Inequality**: Compute Gini coefficients in Aiyagari model
5. **Innovation Policy**: Evaluate R&D subsidies in endogenous growth
6. **Fiscal Multipliers**: Compare multipliers across different models

---

## Computational Challenges

### Challenge: High-Dimensional State Space (HANK)
**Solutions:**
- Use histogram methods
- Apply spline interpolation
- Exploit parallel computing
- Consider approximation methods

### Challenge: Solving Rational Expectations
**Solutions:**
- Master Blanchard-Kahn conditions
- Use Klein's method
- Apply Sims' gensys algorithm
- Check eigenvalues carefully

### Challenge: Transitional Dynamics
**Solutions:**
- Shooting algorithms
- Relaxation methods
- Sequence-space approach
- Good initial guesses

---

## Real-World Applications

These models are actively used by:

**Central Banks:**
- Federal Reserve (FRB/US model)
- European Central Bank (NAWM)
- Bank of England
- Policy scenario analysis

**Government Agencies:**
- Congressional Budget Office
- Treasury departments
- Fiscal policy analysis

**International Organizations:**
- IMF and World Bank
- OECD economic projections

**Academia:**
- Business cycle research
- Growth empirics
- Policy evaluation

---

## Key Debates

Modern macro involves active debates:

1. **Micro-founded vs. Reduced-form**: Structural models vs. VARs
2. **Representative agent vs. Heterogeneity**: When does aggregation fail?
3. **RBC vs. NK**: Technology vs. demand shocks
4. **Calibration vs. Estimation**: What's the right approach?

Understanding these debates helps you:
- Choose appropriate models
- Interpret results correctly
- Communicate findings effectively

---

## Resources

### Essential Reading

**Textbooks:**
- Ljungqvist, L. & Sargent, T. (2018). *Recursive Macroeconomic Theory*, 4th ed.
- Galí, J. (2015). *Monetary Policy, Inflation, and the Business Cycle*, 2nd ed.
- Acemoglu, D. (2008). *Introduction to Modern Economic Growth*

**Classic Papers:**
- Kydland, F. & Prescott, E. (1982). "Time to Build and Aggregate Fluctuations"
- Aiyagari, S. R. (1994). "Uninsured Idiosyncratic Risk and Aggregate Saving"
- Clarida, R., Galí, J., & Gertler, M. (1999). "The Science of Monetary Policy"

### Online Resources
- [QuantEcon Lectures](https://quantecon.org/)
- [Dynare Software](https://www.dynare.org/) - DSGE modeling toolkit
- [Federal Reserve Economic Data (FRED)](https://fred.stlouisfed.org/)

---

## Policy Applications

Learn to answer questions like:

- What are the effects of monetary policy tightening?
- How do fiscal stimulus packages affect output?
- What's the optimal unemployment insurance generosity?
- How does inequality affect macroeconomic dynamics?
- What policies promote long-run growth?

---

## Assessment

Master these skills:

- [ ] Solve growth models analytically and numerically
- [ ] Calibrate models to match data moments
- [ ] Log-linearize DSGE models
- [ ] Compute impulse response functions
- [ ] Solve for stationary distributions in HA models
- [ ] Analyze policy counterfactuals
- [ ] Interpret model results for policy

---

## Next Steps

After this module:

1. **Module 6: Econometrics** - Estimate macro models
2. **Module 8: Time Series** - Analyze macro data
3. **Module 9: Finance** - Asset pricing in macro models

---

## Tips for Success

1. **Master the Basics**: Understand the economic intuition before coding
2. **Start Simple**: Solve deterministic versions first
3. **Verify**: Compare numerical solutions to analytical results when possible
4. **Visualize**: Plot policy functions and impulse responses
5. **Calibrate Carefully**: Use empirically realistic parameter values

---

## Need Help?

- Review [Economic Modeling](../03-economic-modeling/index.md) for DP refresher
- Check [Numerical Methods](../02-numerical-methods/index.md) for solution techniques
- See [FAQ](../../resources/faq.md) for common issues
- Join [Discussions](https://github.com/AmirrezaFarnamTaheri/Computational-Economics-and-Data-Science/discussions)

---

**Ready to explore macro models?** Start with `01_Job_Search.ipynb`!
